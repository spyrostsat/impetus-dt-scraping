from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
import json
import os


class MeteoScraper(webdriver.Chrome):

    ids = ["28", "231", "12", "308", "255", "88", "86", "231", "89", "261", "157", "155", "284",
           "27", "310", "213", "156", "87", "29", "30", "238", "61", "128", "60", "191"]  # len(ids) = 25

    # ids = ["28"]

    url_first_part = "https://meteo.gr/cf.cfm?city_id="

    def __init__(self):
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

            except Exception:
                continue


    def save_data_to_json(self, count, city_name, current_time, temperature, wind_speed, beaufort, humidity, pressure, highest_daily_temperature,
                          lowest_daily_temperature, daily_rain, highest_daily_gust):
        items_to_return = {
            'city_name': city_name,
            'current_time': current_time,
            'temperature': temperature,
            'wind_speed': wind_speed,
            'beaufort': beaufort,
            'humidity': humidity,
            'pressure': pressure,
            'highest_daily_temperature': highest_daily_temperature,
            'lowest_daily_temperature': lowest_daily_temperature,
            'daily_rain': daily_rain,
            'highest_daily_gust': highest_daily_gust
        }

        items_to_return = json.dumps(items_to_return, indent=4)

        current_directory = os.getcwd()
        new_directory = os.path.join(current_directory, "output")

        if not os.path.exists(new_directory):
            os.makedirs(new_directory)

        file_path = os.path.join(new_directory, f"output_{str(count)}.json")

        with open(file_path, "w") as f:
            f.write(items_to_return)
            f.write("\n")
