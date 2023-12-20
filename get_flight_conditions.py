from urllib import request
import json

from utils import get_flight_category


def parse_weather(metars):
    """given a list of metars, return a dict keyed by ICAO airport code,
    containing the fields we care about for the map
    """
    weather = {}
    # retrieve flying conditions from the service response and store in a
    # dictionary for each airport
    for metar in metars:
        airport = metar["icaoId"]
        weather[airport] = {
            "flight_category": get_flight_category(metar),
            "wind_speed": int(metar.get("wspd") or 0),
            "wind_gust": int(metar.get("wgst") or 0)
        }
    return weather

def get_weather(airports, hours_before_now=2):
    """given a list of airports, make a request to the aviation weather
    server, parse the response, and return a list of METARs
    """
    # https://aviationweather.gov/data/api/#/Data/dataMetars
    url = f"https://aviationweather.gov/cgi-bin/data/metar.php?format=json&taf=false&hours={hours_before_now}&ids=" + ",".join([item for item in airports if item != "NULL"])
    content = request.urlopen(url, timeout=30).read()
    return parse_weather(json.loads(content))


