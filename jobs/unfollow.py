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

class Unfollow:
    def __init__(self, browser, actions_meter, sleep_time=1):
        self.browser = browser
        self.actions_meter = actions_meter
        self.sleep_time = sleep_time
        self.data = {"unfollowed": 0, "already_unfollowing": 0, "errors":0}
    
    def _update_unfollowed_user(self, user):
        user.i_follow = False
        user.updated_at = datetime.now()
        session.add(user)
        session.commit()
    
    def _unfollow_user(self, profile=PROFILE):
        self.browser.get(f"{URL}{profile}/") 
        time.sleep(self.sleep_time+bit())
        try:
            unfollow_button = WebDriverWait(self.browser, 5+bit()).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[class="_5f5mN    -fzfL     _6VtSN     yZn4P   "]'))
            )
            time.sleep(bit())
            unfollow_button.click()
            modal = self.browser.find_element(By.CLASS_NAME, 'piCib')
            confirmation_button = modal.find_element(By.TAG_NAME, 'button')
            time.sleep(bit()/2)
            confirmation_button.click()
            logger.info(f"Just stop followig {profile}!!!")
            self.actions_meter.count_action()
            self.data["unfollowed"]+=1
        except TimeoutException:
            self.data["errors"]+=1 #TODO: verificar lógica errors!=miss_actions
            logger.error(f"Could not unfollow {profile}, probably already not following")
        except ActionsQuantityExceeded as error:
            raise ActionsQuantityExceeded(self.data) from error
        
    def unfollow_who_dont_follow_back(self):
        logger.warning(f"START to unfollow who dont follow back")
        profiles = session.query(Profile).filter(or_(Profile.follow_me==None, Profile.follow_me==False)).all()
        for profile in profiles:
            self._unfollow_user(profile.url_name)
            self._update_unfollowed_user(profile)
        session.close()
        return self.data
            