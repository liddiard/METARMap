#!/usr/bin/env python3

import time
import neopixel
import constants
from get_flight_conditions import get_metars, get_tafs

# Initialize the LED strip
pixels = neopixel.NeoPixel(
    constants.LED_PIN,
    constants.LED_COUNT,
    pixel_order=constants.LED_ORDER,
    brightness=constants.LED_BRIGHTNESS,
    auto_write=False
)

# Read the airports file to retrieve list of airports and use as order for LEDs
with open("/home/pi/airports") as f:
    airports = f.readlines()
airports = [x.strip() for x in airports]

def get_taf_animation_state(tafs, time_elapsed):
    """Given a list of TAFs and a time elapsed, return a dict mapping airport
    codes to RGB color tuples"""
    return False # called in a loop, return True/False when done

def animate_taf(tafs):
    tafs = get_tafs(airports)
    animation_state = get_taf_animation_state(tafs, 0)
    time_start = time.time()
    while animation_state:
        for i, airport in enumerate(airports):
            # Skip empty entries
            if not airport:
                continue
            color = animation_state.get(airport, constants.COLOR_OFF)
            pixels[i] = color
        animation_state = get_taf_animation_state(tafs, time.time() - time_start)

def animate_winds(tafs):
    pass # define a long looped animation curve?


def update_metar_map():
    metars = get_metars(airports)

    # Setting LED colors based on weather conditions
    for i, airport in enumerate(airports):
        # Skip empty entries
        if not airport:
            continue
        
        flight_category = metars.get(airport, {}).get("flight_category")
        color = constants.FLIGHT_CATEGORY_TO_COLOR_MAP.get(flight_category, constants.COLOR_OFF)
        
        if (flight_category):
            print("Setting LED " + str(i) + " for " + airport + " to " + flight_category + " " + str(color))
        pixels[i] = color

    # Update actual LEDs all at once
    pixels.show()
    return metars


last_update_time = 0

while True:
    if time.time() > last_update_time + constants.UPDATE_FREQUENCY * 60:
        metars = update_metar_map()
        last_update_time = time.time()
    animate_winds(metars)
