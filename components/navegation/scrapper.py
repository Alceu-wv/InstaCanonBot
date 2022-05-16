from loguru import logger
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from selenium.webdriver.common.by import By

class FollowersScrapper:
    def __init__(self, browser, total_profiles):
        self.browser = browser
        self.total_profiles = total_profiles
        self.data = {"shown": 0, "errors":0}
         
    def _profile_list(self):
        scroll_element = self.browser.find_element(By.CLASS_NAME, "isgrP")
        users = scroll_element.find_elements(By.TAG_NAME, 'li')
        return users
    
    def _get_name(self, profile):
        try:
            name = profile.find_element(By.TAG_NAME, 'span a span').text
        except NoSuchElementException:
            logger.error(f"Error scraping name from users scroll list")
            name = "not_found"
            self.data['errors']+=1
        return name
    
    def _get_url_name(self, profile):
        url_name = profile.find_element(By.CSS_SELECTOR, '[class="Jv7Aj mArmR MqpiF  "]').text
        return url_name
    
    def get_profiles_info(self):
        logger.warning(f"START to scrap profiles info")
        profiles_info = []
        profiles = self._profile_list()
        for user in profiles:
            try:
                logger.warning
                i_follow = any(["\nSeguir" in user.text, "\nSolicitado" in user.text])
                profiles_info.append({'name': self._get_name(user),
                                    'url_name': self._get_url_name(user),
                                    'i_follow': i_follow,
                                    })
                self.data['shown']+=1
            except StaleElementReferenceException:
                self.data['errors']+=1
                logger.error("Missing user in scroll list")
            
        logger.warning(f"FINISH to scrap profiles info")
        logger.warning(f">> TOTAL PROFILES: {self.total_profiles} ")
        logger.warning(f">> SHOWN: {self.data['shown']} ")
        logger.warning(f">> ERRORS: {self.data['errors']} ")
        return profiles_info
    