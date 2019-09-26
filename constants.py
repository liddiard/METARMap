import board
import neopixel

# NeoPixel LED Configuration
LED_COUNT		= 50					# Number of LED pixels.
LED_PIN			= board.D18				# GPIO pin connected to the pixels (18 is PCM).
LED_BRIGHTNESS	= 0.5					# Float from 0.0 (min) to 1.0 (max)
LED_ORDER		= neopixel.RGB			# Strip type and colour ordering

COLOR_VFR		= (0,255,0)				# Green
COLOR_MVFR		= (0,0,255)				# Blue
COLOR_IFR		= (255,0,0)				# Red
COLOR_LIFR		= (125,0,125)			# Magenta
COLOR_OFF		= (0,0,0)				# Off

FLIGHT_CATEGORY_TO_COLOR_MAP = {
    "VFR": COLOR_VFR,
    "MVFR": COLOR_MVFR,
    "IFR": COLOR_IFR,
    "LIFR": COLOR_LIFR
}
