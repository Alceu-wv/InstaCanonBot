
import time
from components.faker import bit
from selenium.webdriver.common.by import By
class Search:
    def __init__(self, browser):
        self.browser = browser
        
    def search_profile(self, profile):
        self.browser.find_element(By.XPATH, '//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/div[1]/div').click()
        time.sleep(bit())
        self.browser.find_element(By.XPATH, '//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/input').send_keys(profile)
        time.sleep(bit()*2)
        self.browser.find_element(By.XPATH, '//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/div[3]/div/div[2]/div/div[1]/a/div').click()
        time.sleep(bit()*2)
    