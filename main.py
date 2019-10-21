import time
import random
import math
import urllib
from datetime import datetime

import neopixel

import constants
from get_flight_conditions import get_metars


# initialize the LEDs
pixels = neopixel.NeoPixel(
    constants.LED_PIN,
    constants.LED_COUNT,
    pixel_order=constants.LED_ORDER,
    brightness=constants.LED_BRIGHTNESS,
    auto_write=False
)

# startup test of all pixels
pixels.fill((255,255,255))
pixels.show()
time.sleep(1)
pixels.fill(constants.COLOR_OFF)

# read the airports file to retrieve list of airports and use as order for LEDs
with open("/home/pi/airports") as f:
    airports = f.readlines()
airports = [x.strip() for x in airports]


def get_brightness(animation_state, metar):
    """given an animation state and a single metar, update the animation state
    based on the winds, amplitude, period, and elapsed time, and return the
    brightness to which that the LED should be set
    """
    wind_speed = metar.get("wind_speed", 0)
    wind_gust = metar.get("wind_gust")
    period = animation_state.get("period")
    gusting = animation_state.get("gusting", False)
    time_elapsed = time.time() - animation_state.get("time_at_start", math.inf)
    # if there is no existing animation or we're past the end of one 
    # oscillation (2π / period), start a new animation
    if period is None or time_elapsed > ((2 * math.pi) / period):
        intensity = wind_speed
        # if there's a wind gust factor…
        if wind_gust is not None:
            if gusting:
                # if we're gusting, we're more likely to remain in the gusting
                # state according to GUSTING_STICKINESS
                if random.random() > constants.GUSTING_STICKINESS:
                    intensity = wind_gust
                else:
                    intensity = wind_speed
                    # we're transitioning states; update the animation state
                    animation_state["gusting"] = False
            else:
                # if we're NOT gusting, we're more likely to remain in the NOT
                # gusting state according to GUSTING_STICKINESS
                if random.random() < constants.GUSTING_STICKINESS:
                    intensity = wind_gust
                    # we're transitioning states; update the animation state
                    animation_state["gusting"] = True
                else:
                    intensity = wind_speed
        animation_state["amplitude"] = random.uniform(
            0.0,
            # an amplitude above 0.5 would cause the animation curve to drop
            # below zero, so it's a hard ceiling
            min(intensity / (constants.MAX_WIND_AMPLITUDE * 2), 0.5)
        )
        animation_state["period"] = random.uniform(
            max(intensity / constants.WIND_PERIOD_VARIANCE, constants.MIN_WIND_PERIOD),
            max(intensity * constants.WIND_PERIOD_VARIANCE, constants.MIN_WIND_PERIOD)
        )
        animation_state["time_at_start"] = time.time()
        time_elapsed = 0
    # function is: amplitude * cos(time_elapsed * period) + (1 - amplitude)
    # "1 - amplitude" displaces the animation curve downward from 1 (max
    # brightness)
    return animation_state["amplitude"] * \
        math.cos(animation_state["period"]* time_elapsed) + \
        (1 - animation_state["amplitude"])
        

def animate_winds(animation_state, metars):
    """given an animation state and a list of METARs, animate the next "frame"
    for all LEDs
    """
    for i, airport in enumerate(airports):
        metar = metars.get(airport)
        # skip LEDs without an airport or missing a METAR
        if not airport or metar is None:
            continue

        flight_category = metar.get("flight_category")
        color = constants.FLIGHT_CATEGORY_TO_COLOR_MAP.get(flight_category, constants.COLOR_OFF)
        brightness = get_brightness(animation_state[airport], metar)
        # multiply each color value by the current brightness (between 0 and 1)
        pixels[i] = tuple(map(lambda x: int(brightness * x), color))
    pixels.show()


def update_metar_map(airports):
    """given a list of airports, fetch METARs for them, update the LEDs 
    accordingly, and return a dictionary of the METAR data
    """
    print("\nFetching METARs at: {}".format(datetime.now()))
    try:
        metars = get_metars(airports)
    # if we encounter an fetching METARs, don't crash the script, just log the
    # error
    except urllib.error.URLError as e:
        print("Error fetching METARs: {}".format(e))
        return

    # Setting LED colors based on weather conditions
    for i, airport in enumerate(airports):
        # Skip empty entries
        if not airport:
            continue
        
        metar = metars.get(airport)

        if not metar:
            print("No METAR for {}; skipping".format(airport))
            pixels[i] = constants.COLOR_OFF
            continue

        flight_category = metar.get("flight_category")
        color = constants.FLIGHT_CATEGORY_TO_COLOR_MAP.get(flight_category, constants.COLOR_OFF)
        
        if flight_category is not None:
            print("Setting LED {index} for {airport} to {flight_category} {color}"\
                .format(index=i, airport=airport, flight_category=flight_category, color=color))
        else:
            print("Missing flight category for {}; setting to off".format(airport))
        pixels[i] = color

    pixels.show()
    return metars


# holds the current RGB values of the LEDs for wind animation
# format: 
# { 
#   "airport_code": {
#       "period": [float],
#       "amplitude": [float],
#       "time_at_start": [float],
#       "gusting": [boolean]
#   }
# }
animation_state = {}
# initialize the animation state with empty dicts for each airport code
for airport in airports:
    if airport:
        animation_state[airport] = {}

# time in seconds since the METAR data was last updated
last_update_time = 0

# main loop
while True:
    if time.time() > last_update_time + constants.UPDATE_FREQUENCY * 60:
        metars = update_metar_map(airports)
        last_update_time = time.time()
    animate_winds(animation_state, metars)
