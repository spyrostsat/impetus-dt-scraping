from pprint import pprint
from mongo_read_for_contour_maps.constants import *
from copy import deepcopy
import requests
import pymongo


class OrionDataManipulation:
    def __init__(self):
        self.url = 'http://localhost:1026/ngsi-ld/v1/entities/'

        self.all_attrs_names = deepcopy(all_attrs_names)

        self.useful_attrs_names = deepcopy(useful_attrs_names)

        self.short_useful_attrs_names = deepcopy(short_useful_attrs_names)

        self.my_client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.my_db = self.my_client["impetus-dev"]
        self.my_col = self.my_db["featurecollections"]

        # Christodoulos commented one line and added the following delete_many
        # self.my_col.delete_many({}) # first we clear the whole meteo collection from old data and then we re-occupy it with the new data from all the stations
        result = self.my_col.delete_many({'id': {'$in': ['temperature', 'windSpeed', 'beaufort', 'humidity', 'atmosphericPressure', 'highestDailyTemperature', 'lowestDailyTemperature', 'precipitation', 'highestDailyGust']}})

    def create_json_from_orion_data(self):
        for i in range(0, len(self.useful_attrs_names), 2):
            params = {
                'type': 'https://smartdatamodels.org/dataModel.Weather/WeatherObserved',
                'attrs': f'{self.useful_attrs_names[i]},{self.useful_attrs_names[i+1]},{self.all_attrs_names[3]},{self.all_attrs_names[4]},{self.all_attrs_names[5]}',
                'limit': 100
            }

            response = requests.get(self.url, params=params)
            response_json = response.json()

            all_stations_json = []

            for resp in response_json:
                if "https://smartdatamodels.org/dataModel.Weather" in self.useful_attrs_names[i]:
                    measurement_value = resp[self.useful_attrs_names[i]]["value"]
                else:
                    measurement_value = resp[self.short_useful_attrs_names[i]]["value"]

                new_station_json = {
                    "type": "Feature",
                    "properties": {
                        self.short_useful_attrs_names[i]: measurement_value,
                        "stationName": resp["stationName"]["value"]
                    },
                    "geometry": {
                        "type": "Point",
                        "coordinates": resp["location"]["value"]["coordinates"]
                    }
                }

                all_stations_json.append(new_station_json)

            json_common = {
                "type": "FeatureCollection",
                "features": all_stations_json,
                "properties": {
                    "FeatureName": self.short_useful_attrs_names[i],
                    "FeatureUnit": response_json[0][self.short_useful_attrs_names[i+1]]["value"],
                    "TimeOfObservation": response_json[0][self.all_attrs_names[5]]["value"]["@value"]
                },
            }

			# This json is created to maintain the old database structure (featurecollections)
            final_json = deepcopy(json_common)
            final_json["id"] = self.short_useful_attrs_names[i]
            self.my_col.insert_one(final_json)
            
            # This json will make a post request to handle the database storage in the backend
            json_post = deepcopy(json_common)
            json_post["name"] = self.short_useful_attrs_names[i]
            
            requests.post('http://localhost:5000/heatmaps', json=json_post)
            