from pprint import pprint
from mongo_read_for_contour_maps.constants import *
from copy import deepcopy
import requests


class OrionDataManipulation:
    def __init__(self):
        self.url = 'http://localhost:1026/ngsi-ld/v1/entities/'

        self.all_attrs_names = deepcopy(all_attrs_names)

        self.useful_attrs_names = deepcopy(useful_attrs_names)

        self.short_useful_attrs_names = deepcopy(short_useful_attrs_names)


    def create_json_from_orion_data(self):
        for i in range(3, len(self.useful_attrs_names)):
            params = {
                'type': 'https://smartdatamodels.org/dataModel.Weather/WeatherObserved',
                'attrs': f'{self.useful_attrs_names[i]},location'
            }

            response = requests.get(self.url, params=params)
            response_json = response.json()

            if "https://smartdatamodels.org/dataModel.Weather" in self.useful_attrs_names[i]:
                for resp in response_json:
                    new_json = {
                                  "type": "FeatureCollection",
                                  "features": [
                                    {
                                      "type": "Feature",
                                      "properties": {
                                        self.short_useful_attrs_names[i]: resp[self.useful_attrs_names[i]]["value"]
                                      },
                                      "geometry": {
                                        "type": "Point",
                                        "coordinates": resp["location"]["value"]["coordinates"]
                                      }
                                    }
                                  ]
                                }
                    pprint(new_json)
                    print("\n")

            else:
                for resp in response_json:
                    new_json = {
                                  "type": "FeatureCollection",
                                  "features": [
                                    {
                                      "type": "Feature",
                                      "properties": {
                                        self.short_useful_attrs_names[i]: resp[self.short_useful_attrs_names[i]]["value"]
                                      },
                                      "geometry": {
                                        "type": "Point",
                                        "coordinates": resp["location"]["value"]["coordinates"]
                                      }
                                    }
                                  ]
                                }
                    pprint(new_json)
                    print("\n")
