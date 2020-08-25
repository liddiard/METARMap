import board
import neopixel


MAX_COLOR_VALUE = 255

def tint(color, _tint=(60,40,20)):
    new_color = tuple()
    for (color_channel, tint_channel) in zip(color, _tint):
        new_color += (min(color_channel + tint_channel, MAX_COLOR_VALUE),)
    return new_color

# application settings

# How often to update the METAR map in minutes
UPDATE_FREQUENCY = 5
# A markov chain-like value that is the probability the wind animation in a
# non-gusting state will transition to a gusting state or vice versa. A lower
# value makes the animation more likely to stay in the existing state. Value 
# should be below 0.5, where 0.5 is equally likely to stay in the current 
# state or transition to the other state.
GUSTING_STICKINESS = 0.15
# The minimum wind speed in knots at which point MIN_FLICKER_BRIGHTNESS can be
# reached. This value defines how quickly brightness will drop off as wind 
# speed increases. A lower value corresponds to a quicker dropoff.
MAX_WIND_AMPLITUDE = 40
# The minimum period (frequency) at which the brightness of an LED can flicker
MIN_WIND_PERIOD = 4
# How much the flicker frequency can increase from its minimum frequency
WIND_PERIOD_VARIANCE = 2


# NeoPixel LED configuration
LED_COUNT = 50 # Number of LED pixels.
LED_PIN = board.D18 # GPIO pin connected to the pixels (18 is PCM)
LED_ORDER = neopixel.RGB # Strip type and colour ordering
LED_INITIAL_BRIGHTNESS = 0.25 # Float from 0.0 (min) to 1.0 (max)
LED_MIN_BRIGHTNESS = 0.05 # Never drop below this brightness while on


# photoresistor configuration
PHOTORESISTOR_PIN = 4
# The minimum amount of light for the photoresistor to measure
# We set this number so the light sensor rc_time function doesn't get stuck in
# its `while` loop in near complete darkness
# Counterintuitively, a higher number corresponds to lower brightness
MIN_AMBIENT_LIGHT = 1000000
# Ambient light reading above which the map will turn on
AMBIENT_LIGHT_ACTIVATION_THRESHOLD = 500000


# flight categories
VFR = "VFR"
VFR_BELOW_MINIMUMS = "VFR_BELOW_MINIMUMS" # custom category, not official
MVFR = "MVFR"
IFR = "IFR"
LIFR = "LIFR"


# flight category colors
COLOR_VFR = tint((0, 170, 0)) # green
COLOR_VFR_BELOW_MINIMUMS = tint((0, 120, 120)) # teal
COLOR_MVFR = tint((0, 0, 255), (15, 75, 0)) # blue
COLOR_IFR = tint((120, 0, 0), (80, 50, 15)) # red
COLOR_LIFR = tint((120, 0, 120), (80, 20, 20)) # magenta
COLOR_OFF = (0, 0, 0)

FLIGHT_CATEGORY_TO_COLOR_MAP = {
    VFR: COLOR_VFR,
    MVFR: COLOR_MVFR,
    IFR: COLOR_IFR,
    LIFR: COLOR_LIFR,
    VFR_BELOW_MINIMUMS: COLOR_VFR_BELOW_MINIMUMS
}
