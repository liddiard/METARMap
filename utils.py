import math

from constants import Category


def get_ceiling(clouds):
    """Ceiling is the lowest layer of broken or overcast clouds. Returns 
    `math.inf` if there is no ceiling
    """
    ceiling = math.inf
    for layer in clouds:
        sky_cover = layer["cover"]
        if sky_cover in ("BKN", "OVC"):
            ceiling = layer["base"]
            break
    return ceiling


def get_flight_category(metar):
    """Determine flight category from metar
    """
    visibility = metar["visib"]
    if visibility == "10+":
        visibility = math.inf
    else:
        visibility = int(visibility)

    ceiling = get_ceiling(metar["clouds"])
    if ceiling < 500 or visibility < 1:
        return Category.LIFR
    elif ceiling < 1000 or visibility < 3:
        return Category.IFR
    elif ceiling <= 3000 or visibility <= 5:
        return Category.MVFR
    elif ceiling <= 5000 or visibility <= 10:
        return Category.VFR_BELOW_MINIMUMS
    else:
        return Category.VFR



