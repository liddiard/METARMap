import board
import neopixel

UPDATE_FREQUENCY = 5 # how often to update the METAR map in minutes
TAF_ANIMATION_DURATION = 15 # forecast animation duration in seconds

# NeoPixel LED Configuration
LED_COUNT		= 50					# Number of LED pixels.
LED_PIN			= board.D18				# GPIO pin connected to the pixels (18 is PCM).
LED_BRIGHTNESS	= 0.25					# Float from 0.0 (min) to 1.0 (max)
LED_ORDER		= neopixel.RGB			# Strip type and colour ordering

VFR_BELOW_MINIMUMS = "VFR_BELOW_MINIMUMS"

COLOR_VFR		= (0,170,0)				# Green
COLOR_VFR_BELOW_MINIMUMS = (0, 125, 125)                        # Teal
COLOR_MVFR		= (0,0,255)				# Blue
COLOR_IFR		= (255,0,0)				# Red
COLOR_LIFR		= (125,0,125)			# Magenta
COLOR_OFF		= (0,0,0)				# Off

FLIGHT_CATEGORY_TO_COLOR_MAP = {
    "VFR": COLOR_VFR,
    "MVFR": COLOR_MVFR,
    "IFR": COLOR_IFR,
    "LIFR": COLOR_LIFR,
    VFR_BELOW_MINIMUMS: COLOR_VFR_BELOW_MINIMUMS
}
