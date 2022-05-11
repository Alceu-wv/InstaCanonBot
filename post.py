import time
import pyautogui
from loguru import logger
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from file_manager import FileManager


class TimelinePost:
    def __init__(self, browser, sleep_time=1):
        self.browser = browser
        self.sleep_time = sleep_time
        self.file_manager = FileManager()
        
    def _checkout(self):
        confirmation_text = WebDriverWait(self.browser, 5).until(
                EC.presence_of_all_elements_located((By.XPATH, "//*[contains(text(),'" + "Sua publicação foi compartilhada" + "')]"))
            )
        if confirmation_text:
            self.file_manager.rename_posted_photo()
            logger.warning("Post successfuly uploaded to timeline!!!")
        else:
            logger.error("Could not confirm post upload to timeline")
        
    def _next(self):
        next_button = WebDriverWait(self.browser, 5).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div[6]/div[2]/div/div/div/div[1]/div/div/div[3]/div/button"))
            )
        next_button.click()
        
    def _select_photo(self):
        self.browser.find_elements_by_tag_name("button")[-1].click()
        logger.warning("WRITING")
        time.sleep(3)
        pyautogui.write(self.file_manager.get_photo_path())
        logger.warning("PRESSING ENTER")
        time.sleep(3)
        pyautogui.press('enter')
        
    def _write_post_text(self):
        textarea = WebDriverWait(self.browser, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "textarea[aria-label='Escreva uma legenda...']"))
            )
        textarea.click()
        pyautogui.write(self.file_manager.get_post_text())
    
    def post(self):
        self.browser.find_element_by_css_selector('[aria-label="Nova publicação"]').click()
        self._select_photo()
        self._next()
        self._next()
        self._write_post_text()
        self._next()
        self._checkout()
