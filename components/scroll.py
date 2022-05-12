import time
from loguru import logger
from components.faker import bit
from selenium.webdriver.common.by import By

class ShowProfileList():
    def __init__(self, browser, insistence=10):
        self.browser = browser
        self.insistence = insistence
        
    def _scroll_profiles(self):
        repeated = 0
        while repeated != self.insistence:
            inicial_len = self._profiles_len()
            self.browser.execute_script("document.getElementsByClassName('isgrP')[0].scrollTop=document.getElementsByClassName('isgrP')[0].scrollTop+document.getElementsByClassName('isgrP')[0].scrollHeight")
            time.sleep(0.3 + bit())
            final_len = self._profiles_len()
            if final_len == inicial_len:
                repeated+=1
            logger.info(final_len)
                
        logger.info(f"{self.__class__.__name__} >> _scroll_profiles >> Discovered users == {final_len}")
        
            
    def _profiles_len(self):
        scroll_element = self.browser.find_element(By.CLASS_NAME, "isgrP")
        users = scroll_element.find_elements(By.TAG_NAME, 'li')
        return len(users)
    
    def _click_followers(self):
        self.browser.find_element(By.PARTIAL_LINK_TEXT, "seguid").click()

    def _click_following(self):
        self.browser.find_element(By.PARTIAL_LINK_TEXT, "seguindo").click()
    
    def show_followers(self):
        time.sleep(bit())
        self._click_followers()
        time.sleep(bit())
        self._scroll_profiles()
        
    def show_following(self):
        time.sleep(bit())
        self._click_following()
        time.sleep(bit())
        self._scroll_profiles()
        
    # TODO: lógica para listas vazias
    