#!/usr/bin/env python3

import time
import neopixel
import constants
from get_flight_conditions import get_metars

# Initialize the LED strip
pixels = neopixel.NeoPixel(
    constants.LED_PIN,
    constants.LED_COUNT,
    pixel_order=constants.LED_ORDER,
    brightness=constants.LED_BRIGHTNESS,
    auto_write=False
)


def set_taf_animation_state(tafs, ms_elapsed):
    pass # called in a loop, return True/False when done

def animate_taf(tafs):
    pass # calls function above in a loop

def animate_winds(tafs):
    pass # define a long looped animation curve?


def update_metar_map():
    # Read the airports file to retrieve list of airports and use as order for LEDs
    with open("/home/pi/airports") as f:
        airports = f.readlines()
    airports = [x.strip() for x in airports]

    airport_conditions = get_metars(airports)

    # Setting LED colors based on weather conditions
    for i, airport in enumerate(airports):
        # Skip empty entries
        if not airport:
            continue
        
        flight_category = airport_conditions.get(airport, {}).get("flight_category")
        color = constants.FLIGHT_CATEGORY_TO_COLOR_MAP.get(flight_category, constants.COLOR_OFF)
        
        print()
        if (flight_category):
            print("Setting LED " + str(i) + " for " + airport + " to " + flight_category + " " + str(color))
        pixels[i] = color

    # Update actual LEDs all at once
    pixels.show()

    print()
    print("Done")


last_update_time = 0

while True:
    if time.time() > last_update_time + constants.UPDATE_FREQUENCY * 60:
        update_metar_map()
        last_update_time = time.time()
