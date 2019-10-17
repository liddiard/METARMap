import math

import constants


def determine_ceiling(sky_conditions):
    """Ceiling is the lowest layer of broken or overcast clouds. Returns 
    `math.inf` if there is no ceiling
    """
    ceiling = math.inf
    for layer in sky_conditions:
        sky_cover = layer["sky_cover"]
        if sky_cover == "BKN" or sky_cover == "OVC":
            ceiling = layer["cloud_base"]
            break
    return ceiling


def determine_flight_category(forecast):
    """Determine flight category from a TAF using the rules at:
    https://www.aviationweather.gov/taf/help?page=plot
    """
    visibility = forecast["visibility"]
    ceiling = determine_ceiling(forecast["sky_conditions"])
    if ceiling < 500 or visibility < 1:
        return "LIFR"
    elif ceiling < 1000 or visibility < 3:
        return "IFR"
    elif ceiling <= 3000 or visibility <= 5:
        return "MVFR"
    else:
        return "VFR"


def is_vfr_below_minimums(metar):
    """VFR below minimums is below 10 statute miles visibility or a cloud 
    ceiling at or below 5000' AGL
    """
    return (metar.find("flight_category") is not None and \
        metar.find("flight_category").text == constants.VFR) and \
        (metar.find("visibility_statute_mi") is not None and \
        float(metar.find("visibility_statute_mi").text) < 10) or \
        (metar.find("sky_condition") and \
        determine_ceiling(int(metar.find("sky_condition").text)) <= 5000)
