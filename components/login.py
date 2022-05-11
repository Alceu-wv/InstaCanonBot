import time
from loguru import logger
from components.faker import bit



class Login():
    def __init__(self, browser):
        self.browser = browser
        self.email = "ceuitalian"
        self.password = "Italy2023"
        
    def login(self):
        self.browser.find_element_by_xpath('//*[@id="loginForm"]/div/div[1]/div/label/input').send_keys(self.email)
        time.sleep(bit())
        self.browser.find_element_by_xpath('//*[@id="loginForm"]/div/div[2]/div/label/input').send_keys(self.password)
        time.sleep(bit())
        self.browser.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]/button/div').click()
        time.sleep(bit())
        logger.info(f"Login for {self.email}")