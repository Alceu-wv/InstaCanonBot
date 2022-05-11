from loguru import logger
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException

class ProfileScrapper():
    def __init__(self, browser, sleep_time=1):
        self.browser = browser
        self.sleep_time = sleep_time
        
    def _profile_list(self):
        scroll_element = self.browser.find_element_by_class_name("isgrP")
        users = scroll_element.find_elements_by_tag_name('li')
        return users
    
    def _get_name(self, user):
        """inheritance"""
        pass
        
    def _get_url_name(self, user):
        """inheritance"""
        pass
    
    def get_profiles_info(self):
        """inheritance"""
        pass
    
class MyFollowersScrapper(ProfileScrapper):
    def _get_name(self, user):
        try:
            name = user.find_element_by_css_selector('[class="wFPL8 "]').text
        except NoSuchElementException:
            logger.error(f"Error obtaining name from users list")
            name = "not_found"
        return name
    
    def _get_url_name(self, user):
        url_name = user.find_element_by_css_selector('[class="Jv7Aj mArmR MqpiF  "]').text
        return url_name
    
    def get_profiles_info(self):
        profiles_info = []
        profiles = self._profile_list()
        for user in profiles:
            try:
                i_follow = "\nSeguir" not in user.text
                profiles_info.append({'name': self._get_name(user),
                                    'url_name': self._get_url_name(user),
                                    'i_follow': i_follow,
                                    })
            except StaleElementReferenceException:
                logger.error("Missing user in scroll list")
                continue
        return profiles_info
    

    