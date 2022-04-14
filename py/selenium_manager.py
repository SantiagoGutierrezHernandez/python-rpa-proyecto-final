from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from py.utils.logger import Logger

class SeleniumManager:
    def __init__(self, driver_path, wait_time = 5):
        self.driver_path = driver_path
        self.driver = webdriver.Chrome(driver_path)
        self.wait = wait_time

    def start(self):
        pass

    def goto(self, url):
        self.driver.get(url)

    def class_all(self, classname, close_on_fail=False):
        try:
            return WebDriverWait(self.driver, self.wait).until(
                EC.presence_of_element_located((By.CLASS_NAME, classname))
            )
        except TimeoutError as e:
            Logger.error(f"No se pudo encontrar el elemento. {e}")
            if close_on_fail: self.end()

    def xpath_clickable(self,xpath, close_on_fail=False):
        try:
            return WebDriverWait(self.driver, self.wait).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
        except TimeoutError as e:
            Logger.error(f"No se pudo encontrar el elemento. {e}")
            if close_on_fail: self.end()

    def xpath(self, xpath, close_on_fail= False):
        try:
            return WebDriverWait(self.driver, self.wait).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
        except TimeoutError as e:
            Logger.error(f"No se pudo encontrar el elemento. {e}")
            if close_on_fail: self.end()

    def end(self):
        self.driver.quit()