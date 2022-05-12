from loguru import logger
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from selenium.webdriver.common.by import By

class ProfileScrapper():
    def __init__(self, browser):
        self.browser = browser
        # TODO: dados
         
    def _profile_list(self):
        scroll_element = self.browser.find_element(By.CLASS_NAME, "isgrP")
        users = scroll_element.find_elements(By.TAG_NAME, 'li')
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
            name = user.find_element(By.CSS_SELECTOR, '[class="_7UhW9   xLCgt      MMzan    _0PwGv              fDxYl     "]').text
        except NoSuchElementException:
            logger.error(f"Error obtaining name from users scroll list")
            name = "not_found"
            # TODO: corrigir e salvar erros 
        return name
    
    def _get_url_name(self, user):
        url_name = user.find_element(By.CSS_SELECTOR, '[class="Jv7Aj mArmR MqpiF  "]').text
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
                # TODO: corrigir e salvar erros
        return profiles_info
    

    