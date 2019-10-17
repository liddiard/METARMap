import board
import neopixel

# application settings

# How often to update the METAR map in minutes
UPDATE_FREQUENCY = 5
# A markov chain-like value that is the probability the wind animation in a
# non-gusting state will transition to a gusting state or vice versa. A lower
# value makes the animation more likely to stay in the existing state. Value 
# should be below 0.5, where 0.5 is equally likely to stay in the current 
# state or transition to the other state.
GUSTING_STICKINESS = 0.2
# Even in the highest wind conditions, don't dip brightness below this value
MIN_FLICKER_BRIGHTNESS = 0.2
# The minimum wind speed in knots at which point MIN_FLICKER_BRIGHTNESS can be
# reached. This value defines how quickly brightness will drop off as wind 
# speed increases. A lower value corresponds to a quicker dropoff.
MAX_WIND_AMPLITUDE = 60
# The minimum period (frequency) at which the brightness of an LED can flicker
MIN_WIND_PERIOD = 4
# How much the flicker frequency can increase from its minimum frequency
WIND_PERIOD_MULTIPLIER = 2


# NeoPixel LED Configuration
LED_COUNT = 50 # Number of LED pixels.
LED_PIN = board.D18 # GPIO pin connected to the pixels (18 is PCM)
LED_BRIGHTNESS = 0.25 # Float from 0.0 (min) to 1.0 (max)
LED_ORDER = neopixel.RGB # Strip type and colour ordering


# flight categories
VFR = "VFR"
VFR_BELOW_MINIMUMS = "VFR_BELOW_MINIMUMS" # custom category, not official
MVFR = "MVFR"
IFR = "IFR"
LIFR = "LIFR"


# flight category colors
COLOR_VFR = (0, 170, 0) # green
COLOR_VFR_BELOW_MINIMUMS = (0, 120, 120) # teal
COLOR_MVFR = (0, 0, 255) # blue
COLOR_IFR = (170, 0, 0) # red
COLOR_LIFR = (120, 0, 120) # magenta
COLOR_OFF = (0, 0, 0)

FLIGHT_CATEGORY_TO_COLOR_MAP = {
    VFR: COLOR_VFR,
    MVFR: COLOR_MVFR,
    IFR: COLOR_IFR,
    LIFR: COLOR_LIFR,
    VFR_BELOW_MINIMUMS: COLOR_VFR_BELOW_MINIMUMS
}
