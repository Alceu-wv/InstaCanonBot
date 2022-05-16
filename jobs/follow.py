import time
from datetime import datetime
from loguru import logger
from components.actions_meter import ActionsQuantityExceeded
from models import session, Profile
from components.faker import bit
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from sqlalchemy import or_

PROFILE = "ortoclinicacxs"
URL = "https://www.instagram.com/"

class Follow:
    def __init__(self, browser, actions_meter, sleep_time=1):
        self.browser = browser
        self.actions_meter = actions_meter
        self.sleep_time = sleep_time
        self.data = {"followed": 0, "already_following": 0, "errors":0}
            
    def _follow_user(self, profile=PROFILE):
        self.browser.get(f"{URL}{profile}/") 
        time.sleep(self.sleep_time+bit())      
        
        try:    
            follow_button = WebDriverWait(self.browser, 5+bit()).until(
                EC.presence_of_element_located((By.XPATH, "// div[contains(text(),\'Seguir')]"))
                )
            time.sleep(bit())
            follow_button.click()
            logger.info(f"Just followig {profile}!!!")
            self.data["followed"]+=1
            self.actions_meter.count_action()
        except TimeoutException:
            if self.browser.find_elements(By.XPATH, "//*[contains(text(), 'não está disponível')]"):
                self.data["errors"]+=1
                # TODO: deletar profile
            elif self.browser.find_elements(By.XPATH, "// div[contains(text(),\'Seguindo')]") or self.browser.find_elements(By.XPATH, "// div[contains(text(),\'Solicitado')]"):
                self.data["already_following"]+=1
            else:
                logger.error(f"Could not follow {profile}")
                self.data["errors"]+=1
        except ActionsQuantityExceeded as error:
            raise ActionsQuantityExceeded(self.data) from error
        
    def _update_followed_user(self, user):
        user.i_follow = True
        user.updated_at = datetime.now()
        session.add(user)
        session.commit()
        
    def follow_new_profiles(self):
        logger.warning(f"START follow new profiles")
        users = session.query(Profile).filter(or_(Profile.i_follow==None, Profile.i_follow==False)).all()
        for user in users:
            self._follow_user(user.url_name)
            self._update_followed_user(user)
        session.close()
        
        return self.data
           