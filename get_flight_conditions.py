from urllib import request
import xml.etree.ElementTree as ET

import constants
from utils import is_vfr_below_minimums


def get_weather(airports, type, hours_before_now=2):
    """given a list of airports and a type of weather ("metars" or "tafs"),
    make a request to the aviation weather server, parse the response, and
    return an XML element tree object
    """
    # https://www.aviationweather.gov/dataserver/example?datatype=metar
    url = f"https://www.aviationweather.gov/adds/dataserver_current/httpparam?dataSource={type}&requestType=retrieve&format=xml&hoursBeforeNow={hours_before_now}&mostRecentForEachStation=true&stationString=" + ",".join([item for item in airports if item != "NULL"])
    content = request.urlopen(url, timeout=30).read()
    return ET.fromstring(content)


def get_metars(airports):
    """given a list of airports, make a request to get the METARs for them
    and return the information we care about from each METAR in a dict keyed
    by airport
    """
    metars = {}
    weather = get_weather(airports, "metars")
    # retrieve flying conditions from the service response and store in a
    # dictionary for each airport
    for metar in weather.iter("METAR"):
        airport = metar.find("station_id").text
        metars[airport] = {}
        flight_category = metar.find("flight_category")
        if flight_category is not None:
            metars[airport]["flight_category"] = flight_category.text
        if is_vfr_below_minimums(metar):
            metars[airport]["flight_category"] = constants.VFR_BELOW_MINIMUMS
        wind_speed = metar.find("wind_speed_kt")
        if wind_speed is not None:
            metars[airport]["wind_speed"] = int(wind_speed.text)
        wind_gust = metar.find("wind_gust_kt")
        if wind_gust is not None:
            metars[airport]["wind_gust"] = int(wind_gust.text)
    return metars
