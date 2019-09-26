#!/usr/bin/env python3

import neopixel
import constants
from get_flight_conditions import get_metars

# Initialize the LED strip
pixels = neopixel.NeoPixel(
    constants.LED_PIN,
    constants.LED_COUNT,
    pixel_order=constants.LED_ORDER,
    auto_write=False
)

# Read the airports file to retrieve list of airports and use as order for LEDs
with open("/home/pi/airports") as f:
    airports = f.readlines()
airports = [x.strip() for x in airports]

airport_conditions = get_metars(airports)

# Setting LED colors based on weather conditions
for i, airport in enumerate(airports):
    # Skip NULL entries
    if airport == "NULL":
        continue
    
    flight_category = airport_conditions.get(airport)["flight_category"]
    color = constants.FLIGHT_CATEGORY_TO_COLOR_MAP.get(flight_category, constants.COLOR_OFF)
    
    print()
    print("Setting LED " + str(i) + " for " + airport + " to " + flight_category + " " + str(color))
    pixels[i] = color

# Update actual LEDs all at once
pixels.show()

print()
print("Done")
