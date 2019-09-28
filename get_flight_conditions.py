import math
from urllib import request
import xml.etree.ElementTree as ET
import dateutil.parser

def determine_flight_category(forecast):
    # https://www.aviationweather.gov/taf/help?page=plot
    visibility = forecast["visibility"]
    sky_conditions = forecast["sky_conditions"]
    ceiling = math.inf
    for layer in sky_conditions:
        sky_cover = layer["sky_cover"]
        if sky_cover == "BKN" or sky_cover == "OVC":
            ceiling = layer["cloud_base"]
            break
    if ceiling < 500 or visibility < 1:
        return "LIFR"
    elif ceiling < 1000 or visibility < 3:
        return "IFR"
    elif ceiling <= 3000 or visibility <= 5:
        return "MVFR"
    else:
        return "VFR"

def get_weather(airports, type):
    # Details about parameters can be found here: https://www.aviationweather.gov/dataserver/example?datatype=metar
    url = f"https://www.aviationweather.gov/adds/dataserver_current/httpparam?dataSource={type}&requestType=retrieve&format=xml&hoursBeforeNow=5&mostRecentForEachStation=true&stationString=" + ",".join([item for item in airports if item != "NULL"])
    content = request.urlopen(url).read()
    return ET.fromstring(content)

def get_metars(airports):
    metars = {}
    weather = get_weather(airports, "metars")
    # Retrieve flying conditions from the service response and store in a dictionary for each airport
    for metar in weather.iter("METAR"):
        airport = metar.find("station_id").text
        if metar.find("flight_category") is None:
            print("Missing flight condition for %s, skipping." % airport)
            continue
        metars[airport] = {
            "flight_category": metar.find("flight_category").text,
            "wind_speed": int(metar.find("wind_speed_kt").text)
        }
        wind_gust = metar.find("wind_gust_kt")
        if wind_gust is not None:
            metars[airport]["wind_gust"] = int(wind_gust.text)
    return metars

def get_tafs(airports):
    tafs = {}
    weather = get_weather(airports, "tafs")

    for taf in weather.iter("TAF"):
        airport = taf.find("station_id").text
        tafs[airport] = []

        for forecast in taf.iter("forecast"):
            forecast_obj = {
                "from": dateutil.parser.parse(forecast.find("fcst_time_from").text),
                "to": dateutil.parser.parse(forecast.find("fcst_time_to").text),
            }

            wind_speed = forecast.find("wind_speed_kt")
            if wind_speed is None:
                forecast_obj["wind_speed"] = tafs[airport][-1]["wind_speed"]
            else:
                forecast_obj["wind_speed"] = int(wind_speed.text)

            wind_gust = forecast.find("wind_gust_kt")
            if wind_gust is not None:
                forecast_obj["wind_gust"] = int(wind_gust.text)

            sky_conditions = forecast.findall("sky_condition")
            if sky_conditions:
                sky_conditions_list = []
                for layer in sky_conditions:
                    layer_obj = {
                        "sky_cover": layer.attrib.get("sky_cover"),
                        "cloud_base": int(layer.attrib.get("cloud_base_ft_agl", "12000"))
                    }
                    sky_conditions_list.append(layer_obj)
                forecast_obj["sky_conditions"] = sky_conditions_list
            else:
                forecast_obj["sky_conditions"] = tafs[airport][-1]["sky_conditions"]
            
            visibility = forecast.find("visibility_statute_mi")
            if visibility is None:
                forecast_obj["visibility"] = tafs[airport][-1]["visibility"]
            else:
                forecast_obj["visibility"] = float(visibility.text)

            change_indicator = forecast.find("change_indicator")
            if change_indicator is not None:
                forecast_obj["change_indicator"] = change_indicator.text
            
            forecast_obj["flight_category"] = determine_flight_category(forecast_obj)
            tafs[airport].append(forecast_obj)
    
    return tafs
    
