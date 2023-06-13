import requests
from pprint import pprint

url = 'http://localhost:1026/ngsi-ld/v1/entities/'
params = {
    'type': 'https://smartdatamodels.org/dataModel.Weather/WeatherObserved',
    'attrs': 'https://smartdatamodels.org/dataModel.Weather/temperature,location'
}

response = requests.get(url, params=params)

# pprint(response.json()[0])
pprint(response.json()[0]["https://smartdatamodels.org/dataModel.Weather/temperature"]["value"])
pprint(response.json()[0]["location"]["value"]["coordinates"])
