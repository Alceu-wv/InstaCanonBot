import time
from loguru import logger
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from components.faker import bit



class Login():
    def __init__(self, browser, user):
        self.browser = browser
        self.user = user
        
    def login(self):
        username_field = WebDriverWait(self.browser, 5+bit()).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="loginForm"]/div/div[1]/div/label/input')))
        username_field.send_keys(self.user.email or self.user.url_name)
        time.sleep(bit())
        
        password_field = WebDriverWait(self.browser, 5+bit()).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="loginForm"]/div/div[2]/div/label/input')))
        password_field.send_keys(self.user.password)
        time.sleep(bit())
        
        self.browser.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[3]/button/div').click()
        time.sleep(bit())
        logger.info(f"Login in for {self.user}")