import dateutil.parser


TAF_ANIMATION_DURATION = 15 # forecast animation duration in seconds


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


def get_taf_animation_state(tafs, time_elapsed):
    """Given a list of TAFs and a time elapsed, return a dict mapping airport
    codes to RGB color tuples"""
    return False # called in a loop, return True/False when done


def animate_taf(tafs):
    tafs = get_tafs(airports)
    animation_state = get_taf_animation_state(tafs, 0)
    time_start = time.time()
    while animation_state:
        for i, airport in enumerate(airports):
            # Skip empty entries
            if not airport:
                continue
            color = animation_state.get(airport, constants.COLOR_OFF)
            pixels[i] = color
        animation_state = get_taf_animation_state(tafs, time.time() - time_start)
