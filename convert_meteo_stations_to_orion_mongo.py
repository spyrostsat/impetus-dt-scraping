import pymongo
import requests
import os
from unidecode import unidecode
import json


def kmh_to_beaufort(wind_speed_kmh):
    if wind_speed_kmh < 0:
        raise ValueError("Wind speed cannot be negative.")

    if wind_speed_kmh < 1:
        return 0
    elif wind_speed_kmh < 6:
        return 1
    elif wind_speed_kmh < 12:
        return 2
    elif wind_speed_kmh < 20:
        return 3
    elif wind_speed_kmh < 29:
        return 4
    elif wind_speed_kmh < 39:
        return 5
    elif wind_speed_kmh < 50:
        return 6
    elif wind_speed_kmh < 62:
        return 7
    elif wind_speed_kmh < 75:
        return 8
    elif wind_speed_kmh < 89:
        return 9
    elif wind_speed_kmh < 103:
        return 10
    elif wind_speed_kmh < 118:
        return 11
    else:
        return 12


client = pymongo.MongoClient("mongodb://localhost:27027/")
db = client["impetus-dev"]
mete_stations_col = db["meteo-stations"]

all_docs = mete_stations_col.find({})

for doc in all_docs:
    city_name = doc['text']
    city_name = unidecode(city_name).strip().replace(" ", "-")

    actual_time = doc['timestamp'].strftime('%Y-%m-%dT%H:%M:%S')
    try:
        coordinates = doc['geometry']['coordinates']
    except KeyError as e:
        continue

    try:
        temperature = doc['temperature']['value']
        temperature_unit = doc['temperature']['unit']
    except KeyError as e:
        continue

    wind_speed = doc['wind']['value']
    wind_speed_unit = doc['wind']['unit']

    beaufort = kmh_to_beaufort(float(wind_speed))
    beaufort_unit = "Beaufort"

    humidity = doc['humidity']['value']
    humidity_unit = doc['humidity']['unit']

    pressure = doc['barometer']['value']
    pressure_unit = doc['barometer']['unit']

    highest_daily_temperature = "-"
    highest_daily_temperature_unit = "C"

    lowest_daily_temperature = "-"
    lowest_daily_temperature_unit = "C"

    daily_rain = doc['today_s_rain']['value']
    daily_rain_unit = doc['today_s_rain']['unit']

    highest_daily_gust = "Not scraped yet"
    highest_daily_gust_unit = "km/h"

    jsonData = {
        "id": f"urn:ngsi-ld:WeatherObserved:Greece-Attica-WeatherObserved-{city_name}",
        "type": "WeatherObserved",
        "address": {
            "type": "Property",
            "value": {
                "addressLocality": f"{city_name}",
                "addressCountry": "GR",
                "type": "PostalAddress"
            }
        },
        "dataProvider": {
            "type": "Property",
            "value": "METEO"
        },
        "source": {
            "type": "Property",
            "value": "https://meteo.gr/"
        },
        "stationName": {
            "type": "Property",
            "value": city_name
        },
        "location": {
            "type": "GeoProperty",
            "value": {
                "type": "Point",
                "coordinates": coordinates
            }
        },
        "dateObserved": {
            "type": "Property",
            "value": {
                "@type": "DateTime",
                "@value": actual_time
            }
        },
        "temperature": {
            "type": "Property",
            "value": temperature
        },
        "temperatureUnit": {
            "type": "Property",
            "value": temperature_unit
        },
        "windSpeed": {
            "type": "Property",
            "value": wind_speed
        },
        "windSpeedUnit": {
            "type": "Property",
            "value": wind_speed_unit
        },
        "beaufort": {
            "type": "Property",
            "value": beaufort
        },
        "beaufortUnit": {
            "type": "Property",
            "value": beaufort_unit
        },
        "humidity": {
            "type": "Property",
            "value": humidity
        },
        "humidityUnit": {
            "type": "Property",
            "value": humidity_unit
        },
        "atmosphericPressure": {
            "type": "Property",
            "value": pressure
        },
        "atmosphericPressureUnit": {
            "type": "Property",
            "value": pressure_unit
        },
        "highestDailyTemperature": {
            "type": "Property",
            "value": highest_daily_temperature
        },
        "highestDailyTemperatureUnit": {
            "type": "Property",
            "value": highest_daily_temperature_unit
        },
        "lowestDailyTemperature": {
            "type": "Property",
            "value": lowest_daily_temperature
        },
        "lowestDailyTemperatureUnit": {
            "type": "Property",
            "value": lowest_daily_temperature_unit
        },
        "precipitation": {
            "type": "Property",
            "value": daily_rain
        },
        "precipitationUnit": {
            "type": "Property",
            "value": daily_rain_unit
        },
        "highestDailyGust": {
            "type": "Property",
            "value": highest_daily_gust
        },
        "highestDailyGustUnit": {
            "type": "Property",
            "value": highest_daily_gust_unit
        },
        "@context": [
            "https://smart-data-models.github.io/dataModel.Weather/context.jsonld",
            "https://raw.githubusercontent.com/smart-data-models/dataModel.Weather/master/context.jsonld"
        ]
    }

    print(jsonData)

    payload = json.dumps(jsonData, indent=4)

    current_directory = os.getcwd()
    new_directory = os.path.join(current_directory, "output")

    if not os.path.exists(new_directory):
        os.makedirs(new_directory)

    file_path = os.path.join(new_directory, f"output_city_name_{city_name}.json")

    with open(file_path, "w") as f:
        f.write(payload)
        f.write("\n")

    response = requests.post(url="http://localhost:1026/ngsi-ld/v1/entities", headers={
        "content-type": "application/ld+json"}, data=payload)

    if str(response.status_code) == "409":
        response = requests.delete(url=f"http://localhost:1026/ngsi-ld/v1/entities/{jsonData['id']}")
        print("DELETE")

        response = requests.post(url="http://localhost:1026/ngsi-ld/v1/entities", headers={
            "content-type": "application/ld+json"}, data=payload)
