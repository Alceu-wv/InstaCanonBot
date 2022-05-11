import time
from loguru import logger

class ShowProfileList():
    def __init__(self, browser, insistence=10, sleep_time=0.5):
        self.browser = browser
        self.sleep_time = sleep_time
        self.insistence = insistence
        
    def _scroll_profiles(self):
        repeated = 0
        while repeated != self.insistence:
            inicial_len = self._profiles_len()
            self.browser.execute_script("document.getElementsByClassName('isgrP')[0].scrollTop=document.getElementsByClassName('isgrP')[0].scrollTop+document.getElementsByClassName('isgrP')[0].scrollHeight")
            time.sleep(self.sleep_time)
            final_len = self._profiles_len()
            if final_len == inicial_len:
                repeated+=1
                
        logger.info(f"{self.__class__.__name__} >> _scroll_profiles >> Discovered users == {final_len}")
        
            
    def _profiles_len(self):
        scroll_element = self.browser.find_element_by_class_name("isgrP")
        users = scroll_element.find_elements_by_tag_name('li')
        return len(users)
    
    def _click_followers(self):
        self.browser.find_element_by_partial_link_text("seguid").click()
        time.sleep(self.sleep_time)

    def _click_following(self):
        self.browser.find_element_by_partial_link_text("seguindo").click()
        time.sleep(self.sleep_time)
    
    def show_followers(self):
        self._click_followers()
        self._scroll_profiles()
        
    def show_following(self):
        self._click_following()
        self._scroll_profiles()
        
    