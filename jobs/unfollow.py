import time
from datetime import datetime
from loguru import logger
from models import session, User
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from sqlalchemy import or_

PROFILE = "ortoclinicacxs"
URL = "https://www.instagram.com/"

class Unfollow:
    def __init__(self, browser=None, sleep_time=1):
        self.browser = browser
        self.sleep_time = sleep_time
        self.errors = 0
    
    def _update_unfollowed_user(self, user):
        user.i_follow = False
        user.updated_at = datetime.now()
        session.add(user)
        session.commit()
    
    def _unfollow_user(self, profile=PROFILE):
        self.browser.get(f"{URL}{profile}/") 
        time.sleep(self.sleep_time*2)
        try:
            unfollow_button = WebDriverWait(self.browser, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[class="_5f5mN    -fzfL     _6VtSN     yZn4P   "]'))
            )
            unfollow_button.click()
            modal = self.browser.find_element_by_class_name('piCib')
            confirmation_button = modal.find_element_by_tag_name('button')
            confirmation_button.click()
            logger.info(f"Just stop followig {profile}!!!")
        except TimeoutException:
            self.errors+=1
            logger.error(f"Could not unfollow {profile}, probably already not following")
        
    def unfollow_who_dont_follow_back(self):
        logger.warning(f"START to unfollow who dont follow back")
        users = session.query(User).filter(or_(User.follow_me==None, User.follow_me==False)).all()[:9]
        for user in users:
            self._unfollow_user(user.url_name)
            time.sleep(self.sleep_time)
            self._update_unfollowed_user(user)
        session.close()
        logger.warning(f">> FINISH to unfollow who dont follow back")
        logger.warning(f">> UNFOLLOWED: {len(users) - self.errors}")
        logger.warning(f">> ERRORS: {self.errors}")
            