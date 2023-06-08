from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime
import json
import os


class MeteoScraper(webdriver.Chrome):

    ids = ["28", "231", "12", "308", "255", "88", "86", "231", "89", "261", "157", "155", "284",
           "27", "310", "213", "156", "87", "29", "30", "238", "61", "128", "60", "191"]  # len(ids) = 25

    # ids = ["28"]

    total_ids = len(ids)

    stations_locations = [
        [23.72238872883628, 37.891532268518801],
        [23.85926241126208, 38.142993324527026],
        [23.734946186509262, 37.97542982908729],
        [23.931370861085497, 37.73586981067058],
        [23.589236161971428, 38.05860969744705],
        [23.833675367859627, 38.05749118698577],
        [23.803391552253487, 38.09769261031022],
        [23.876904285954993, 38.13086798933955],
        [23.74512581914925, 37.893796901977936],
        [23.534845504826137, 38.04763426871179],
        [23.324141442788175, 38.21737333919907],
        [23.796193615420606, 38.23910991564784],
        [23.500325481062106, 38.07319920659407],
        [23.961350968451853, 38.15687413078601],
        [23.932273726794193, 37.88280650362145],
        [23.34292454848344, 37.994881264823890],
        [23.418808398957765, 38.00283072694239],
        [23.99175827837084, 37.733513852438335],
        [23.78737950000078, 38.036245301040370],
        [23.799770068617107, 38.08127325317486],
        [23.720060644052666, 38.14648511057399],
        [23.647197470075014, 37.94347523560283],
        [23.593009744470322, 37.96574027277751],
        [23.494194747455026, 37.96671997227759],
        [23.916228454216906, 37.96367237254712],
    ]

    url_first_part = "https://meteo.gr/cf.cfm?city_id="

    def __init__(self):
        self.current_datetime = datetime.now().strftime("%Y-%m-%dT")
        # service = Service(ChromeDriverManager().install())
        options = Options()
        options.add_experimental_option("detach", True)  # this leaves the browser open even after the python script is finished

        # these arguments make the browser run on the background
        options.add_argument("--headless")  # Enable headless mode
        # options.add_argument("--disable-gpu")  # Disable GPU acceleration
        options.add_argument("--no-sandbox")  # Disable sandbox mode (Linux only)

        super(MeteoScraper, self).__init__(options=options)
        self.implicitly_wait(3)


    def scrap_attica(self):
        for count, city_id in enumerate(MeteoScraper.ids):
            try:
                url_to_scrap = MeteoScraper.url_first_part + city_id
                self.get(url_to_scrap)
                self.maximize_window()
                if count == 0:
                    try:
                        accept_cookies_element = self.find_element("xpath", "//div[@class='qc-cmp2-summary-buttons']/button[contains(@class, 'css-k8o10q')]/span[text()[contains(., 'ΣΥΜΦΩΝΩ')]]")
                        accept_cookies_element.click()
                    except NoSuchElementException as e:
                        pass

                city_name_element = self.find_element("xpath", "//h1[contains(@class, 'cityname fl')]")
                city_name = city_name_element.get_attribute("innerHTML").strip()

                current_time_element = self.find_element("xpath", "//div[contains(@class, 'headernew')]//span[contains(@class, 'livetime')]")
                current_time = current_time_element.get_attribute("innerHTML").strip()

                temperature_element = self.find_element("xpath", "//div[contains(@class, 'livepanel')]//div[contains(@class, 'newtemp')]")
                temperature_unit_element = self.find_element("xpath", "//div[contains(@class, 'livepanel')]//div[contains(@class, 'newtemp')]/span[contains(@class, 'newcelc')]")
                temperature_unit = temperature_unit_element.get_attribute("innerHTML")
                temperature = temperature_element.get_attribute("innerHTML").split("<")[0]
                temperature =  (temperature + " " + temperature_unit).strip()

                wind_speed_element = self.find_elements("xpath", "//div[contains(@class, 'livepanel')]//div[contains(@class, 'windnr')]")[0]
                wind_speed_unit_element = self.find_element("xpath", "//div[contains(@class, 'livepanel')]//div[contains(@class, 'windnr')]/span")
                wind_speed = wind_speed_element.get_attribute("innerHTML").split("<")[0].strip() + " " + wind_speed_unit_element.get_attribute("innerHTML").strip()

                beaufort_element = self.find_elements("xpath", "//div[contains(@class, 'livepanel')]//div[contains(@class, 'windnr')]")[1]
                beaufort = beaufort_element.get_attribute("innerHTML").strip()

                humidity_element = self.find_element("xpath", "//div[contains(@class, 'livepanel')]//div[contains(@class, 'ygrasia')]")
                humidity = humidity_element.get_attribute("innerHTML").split(":")[-1].strip()

                pressure_element = self.find_element("xpath", "//div[contains(@class, 'livepanel')]//div[contains(@class, 'piesi')]")
                pressure_unit_element = self.find_element("xpath", "//div[contains(@class, 'livepanel')]//div[contains(@class, 'piesi')]/span")
                pressure = pressure_element.get_attribute("innerHTML").split("<")[0].strip().split(":")[-1].strip() + " " + pressure_unit_element.get_attribute("innerHTML").split(";")[-1]

                highest_daily_temperature_element = self.find_elements("xpath", "//div[contains(@class, 'dailydata')]")[0]
                highest_daily_temperature = highest_daily_temperature_element.get_attribute("innerHTML").split(" ")[-1].split(">")[-2].split("<")[0].strip()

                lowest_daily_temperature_element = self.find_elements("xpath", "//div[contains(@class, 'dailydata')]")[1]
                lowest_daily_temperature = lowest_daily_temperature_element.get_attribute("innerHTML").split(" ")[-1].split(">")[-2].split("<")[0].strip()

                daily_rain_element = self.find_elements("xpath", "//div[contains(@class, 'dailydata')]")[2]
                daily_rain = daily_rain_element.get_attribute("innerHTML").split("<")[0].split("\n")[-1].strip() + " mm"

                highest_daily_gust_element = self.find_elements("xpath", "//div[contains(@class, 'dailydata')]")[3]
                highest_daily_gust = highest_daily_gust_element.get_attribute("innerHTML").split("<span")[1].split("\n")[-1].strip() + " km/h"

                self.save_data_to_json(count, city_name, current_time, temperature, wind_speed, beaufort, humidity, pressure, highest_daily_temperature,
                                       lowest_daily_temperature, daily_rain, highest_daily_gust)

                print(f"Completed: {count+1} / {MeteoScraper.total_ids}") # info

            except Exception:
                continue


    def save_data_to_json(self, count, city_name, current_time, temperature, wind_speed, beaufort, humidity, pressure, highest_daily_temperature,
                          lowest_daily_temperature, daily_rain, highest_daily_gust):

        actual_time = self.current_datetime + current_time + ":00"

        jsonData = {
            "id": f"urn:ngsi-ld:WeatherObserved:Greece-Attica-WeatherObserved-{city_name}-{actual_time}",
            "type": "WeatherObserved",
            "address": {
                "addressLocality": f"{city_name}",
                "addressCountry": "GR"
            },
            "dataProvider": "METEO",
            "source": "https://meteo.gr/",
            "stationName": city_name,
            "location": {
                "type": "Point",
                "coordinates": MeteoScraper.stations_locations[count]
            },
            "dateObserved": actual_time,
            "temperature": temperature,
            "windSpeed": wind_speed,
            "beaufort": beaufort,
            "humidity": humidity,
            "atmosphericPressure": pressure,
            "highest_daily_temperature": highest_daily_temperature,
            "lowest_daily_temperature": lowest_daily_temperature,
            "precipitation": daily_rain,
            "highest_daily_gust": highest_daily_gust
        }


        jsonData = json.dumps(jsonData, indent=4)

        current_directory = os.getcwd()
        new_directory = os.path.join(current_directory, "output")

        if not os.path.exists(new_directory):
            os.makedirs(new_directory)

        file_path = os.path.join(new_directory, f"output_{str(count)}.json")

        with open(file_path, "w") as f:
            f.write(jsonData)
            f.write("\n")
