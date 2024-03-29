import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from loguru import logger
from components.faker import bit

XPATH_DISMISS_ACTIVE_NOTIFICATIONS1 = '/html/body/div[5]/div/div/div/div[3]/button[2]'
XPATH_DISMISS_ACTIVE_NOTIFICATIONS2 = '/html/body/div[6]/div/div/div/div[3]/button[2]'

class Dismiss:
    def __init__(self, browser):
        self.browser = browser
        
    def dismiss_active_notifications(self):        
        try:
            pop_up_button = WebDriverWait(self.browser, 3+bit()).until(
                EC.presence_of_element_located((By.XPATH, XPATH_DISMISS_ACTIVE_NOTIFICATIONS2))
            )
        except TimeoutException:
            logger.error(f"Could not find pop_up_button from XPATH 2 {XPATH_DISMISS_ACTIVE_NOTIFICATIONS2}")

        try:
            pop_up_button = WebDriverWait(self.browser, bit()).until(
                EC.presence_of_element_located((By.XPATH, XPATH_DISMISS_ACTIVE_NOTIFICATIONS1))
            )
        except TimeoutException:
            logger.error(f"Could not find pop_up_button from XPATH 1 {XPATH_DISMISS_ACTIVE_NOTIFICATIONS1}")
        
        time.sleep(bit())
        pop_up_button.click()
        logger.info("Dismiss active notifications")
        
    def dismiss_save_login(self):
        pop_up_button = WebDriverWait(self.browser, 5+bit()).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="react-root"]/section/main/div/div/div/div/button'))
        )
        time.sleep(bit())
        pop_up_button.click()
        logger.info("Dismiss save login")
        
        