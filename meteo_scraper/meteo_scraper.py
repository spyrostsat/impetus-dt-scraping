from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


class MeteoScraper(webdriver.Chrome):
    def __init__(self):
        service = Service(ChromeDriverManager().install())
        options = Options()
        options.add_experimental_option("detach", True)  # this leaves the browser open even after the python script is finished
        super(MeteoScraper, self).__init__(service=service, options=options)

    def land_first_page(self):
        self.get("https://meteo.gr/")
        self.maximize_window()
        accept_cookies_element = self.find_element("xpath", "//div[@class='qc-cmp2-summary-buttons']/button[contains(@class, 'css-k8o10q')]/span[text()[contains(., 'ΣΥΜΦΩΝΩ')]]")
        accept_cookies_element.click()
