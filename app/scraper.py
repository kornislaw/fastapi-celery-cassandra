import time
from dataclasses import dataclass

from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver


def get_user_agent():
    return UserAgent(verify_ssl=False).data_randomize


@dataclass
class Scraper:
    url: str
    endless_scroll: bool = False
    endless_scroll_time: int = 5
    driver: WebDriver = None

    def get_driver(self):
        if self.driver is None:
            options = Options()
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            driver = webdriver.Chrome(options=options)
            self.driver = driver
        return self.driver

    def get(self):
        driver = self.get_driver()
        driver.get(self.url)
        self.perform_scroll(driver)
        return driver.page_source

    def perform_scroll(self, driver=None):
        if driver is None:
            return
        if self.endless_scroll:
            """
            Interesting: you can do it by executing JS this way:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            """
            current_height: int = driver.execute_script("return document.body.scrollHeight")
            while True:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
                iter_height: int = driver.execute_script("return document.body.scrollHeight")
                if current_height == iter_height:
                    break
                else:
                    current_height = iter_height
                    time.sleep(self.endless_scroll_time)
