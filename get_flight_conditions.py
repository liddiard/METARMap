
from urllib import request
import xml.etree.ElementTree as ET

def determine_flight_category(forecast):
    # https://www.aviationweather.gov/taf/help?page=plot
    visibility = forecast.get("visibility_statute_mi")
    sky_condition = forecast.find("sky_condition")
    if not visibility or not sky_condition:
        raise ValueError("Forecast missing visibility or sky condition")
    # ceiling = 

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
            "wind_speed": metar.find("wind_speed_kt").text
        }
        wind_gust = metar.find("wind_gust_kt")
        if wind_gust:
            metars[airport]["wind_gust"] = wind_gust
    return metars

def get_tafs(airports):
    tafs = {}
    weather = get_weather(airports, "tafs")
    for taf in weather.iter("TAF"):
        airport = taf.find("station_id").text
        for forecast in taf.iter("forecast"):
            print(forecast.find("sky_condition").attrib["sky_cover"])
        tafs[airport] = {}
    pass

