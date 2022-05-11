import time
from datetime import datetime
from loguru import logger
from models import session, User
from components.faker import bit
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from sqlalchemy import or_

PROFILE = "ortoclinicacxs"
URL = "https://www.instagram.com/"

class Follow:
    def __init__(self, browser=None, sleep_time=1):
        self.browser = browser
        self.sleep_time = sleep_time
            
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
        except TimeoutException:
            logger.error(f"Could not follow {profile}, probably already following")
        
    def _update_followed_user(self, user):
        user.i_follow = True
        user.updated_at = datetime.now()
        session.add(user)
        session.commit()
        
    def follow_new_profiles(self):
        logger.warning(f"START follow new profiles")
        users = session.query(User).filter(or_(User.i_follow==None, User.i_follow==False)).all()[:9]
        for user in users:
            self._follow_user(user.url_name)
            self._update_followed_user(user)
        session.close()
        logger.warning(f"FINISH follow new profiles")
           