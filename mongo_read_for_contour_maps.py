import requests
from pprint import pprint


class OrionDataManipulation:
    def __init__(self):
        self.url = 'http://localhost:1026/ngsi-ld/v1/entities/'

        self.all_attrs_names = [
            "https://smartdatamodels.org/address",
            "https://smartdatamodels.org/dataProvider",
            "https://smartdatamodels.org/source",
            "https://uri.etsi.org/ngsi-ld/default-context/stationName",
            "location",
            "https://smartdatamodels.org/dateObserved",
            "https://smartdatamodels.org/dataModel.Weather/temperature",
            "https://uri.etsi.org/ngsi-ld/default-context/temperatureUnit",
            "https://smartdatamodels.org/dataModel.Weather/windSpeed",
            "https://uri.etsi.org/ngsi-ld/default-context/windSpeedUnit",
            "https://uri.etsi.org/ngsi-ld/default-context/beaufort",
            "https://uri.etsi.org/ngsi-ld/default-context/beaufortUnit",
            "https://uri.etsi.org/ngsi-ld/default-context/humidity",
            "https://uri.etsi.org/ngsi-ld/default-context/humidityUnit",
            "https://smartdatamodels.org/dataModel.Weather/atmosphericPressure",
            "https://uri.etsi.org/ngsi-ld/default-context/atmosphericPressureUnit",
            "https://uri.etsi.org/ngsi-ld/default-context/highestDailyTemperature",
            "https://uri.etsi.org/ngsi-ld/default-context/highestDailyTemperatureUnit",
            "https://uri.etsi.org/ngsi-ld/default-context/lowestDailyTemperature",
            "https://uri.etsi.org/ngsi-ld/default-context/lowestDailyTemperatureUnit",
            "https://smartdatamodels.org/dataModel.Weather/precipitation",
            "https://uri.etsi.org/ngsi-ld/default-context/precipitationUnit",
            "https://uri.etsi.org/ngsi-ld/default-context/highestDailyGust",
            "https://uri.etsi.org/ngsi-ld/default-context/highestDailyGustUnit"
        ]

        self.useful_attrs_names = [
            # "https://smartdatamodels.org/address",
            # "https://smartdatamodels.org/dataProvider",
            # "https://smartdatamodels.org/source",
            "https://uri.etsi.org/ngsi-ld/default-context/stationName",
            "location",
            "https://smartdatamodels.org/dateObserved",
            "https://smartdatamodels.org/dataModel.Weather/temperature",
            # "https://uri.etsi.org/ngsi-ld/default-context/temperatureUnit",
            "https://smartdatamodels.org/dataModel.Weather/windSpeed",
            # "https://uri.etsi.org/ngsi-ld/default-context/windSpeedUnit",
            "https://uri.etsi.org/ngsi-ld/default-context/beaufort",
            # "https://uri.etsi.org/ngsi-ld/default-context/beaufortUnit",
            "https://uri.etsi.org/ngsi-ld/default-context/humidity",
            # "https://uri.etsi.org/ngsi-ld/default-context/humidityUnit",
            "https://smartdatamodels.org/dataModel.Weather/atmosphericPressure",
            # "https://uri.etsi.org/ngsi-ld/default-context/atmosphericPressureUnit",
            "https://uri.etsi.org/ngsi-ld/default-context/highestDailyTemperature",
            # "https://uri.etsi.org/ngsi-ld/default-context/highestDailyTemperatureUnit",
            "https://uri.etsi.org/ngsi-ld/default-context/lowestDailyTemperature",
            # "https://uri.etsi.org/ngsi-ld/default-context/lowestDailyTemperatureUnit",
            "https://smartdatamodels.org/dataModel.Weather/precipitation",
            # "https://uri.etsi.org/ngsi-ld/default-context/precipitationUnit",
            "https://uri.etsi.org/ngsi-ld/default-context/highestDailyGust",
            # "https://uri.etsi.org/ngsi-ld/default-context/highestDailyGustUnit"
        ]

        self.short_useful_attrs_names = [
            # "address",
            # "dataProvider",
            # "source",
            "stationName",
            "location",
            "dateObserved",
            "temperature",
            # "temperatureUnit",
            "windSpeed",
            # "windSpeedUnit",
            "beaufort",
            # "beaufortUnit",
            "humidity",
            # "humidityUnit",
            "atmosphericPressure",
            # "atmosphericPressureUnit",
            "highestDailyTemperature",
            # "highestDailyTemperatureUnit",
            "lowestDailyTemperature",
            # "lowestDailyTemperatureUnit",
            "precipitation",
            # "precipitationUnit",
            "highestDailyGust",
            # "highestDailyGustUnit"
    ]

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

            else:
                print("===============================")
                print(response_json[0])
                print("===============================")


orionDataManipulation = OrionDataManipulation()
orionDataManipulation.create_json_from_orion_data()
