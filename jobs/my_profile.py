import time
from datetime import datetime
from loguru import logger
from models import session, User
from components.faker import bit
from sqlalchemy.exc import IntegrityError
from components.scrapper import MyFollowersScrapper
from components.scroll import ShowProfileList


MY_PROFILE = "ceuitalian"
URL = "https://www.instagram.com/"


class MyProfile:
    def __init__(self, browser=None, sleep_time=1):
        self.browser = browser
        self.sleep_time = sleep_time
        self.data = {"updated": 0, "created": 0, "errors":0}
        
    def update_my_followers(self, my_profile=MY_PROFILE):
        logger.warning(f"START to update my followers")
        self.browser.get(f"{URL}{my_profile}/") 
        time.sleep(self.sleep_time+bit())
        
        ShowProfileList(self.browser).show_followers()
        profiles_info = MyFollowersScrapper(self.browser).get_profiles_info()
        
        for profile in profiles_info:
            user = session.query(User).filter_by(url_name=profile['url_name']).first()
            if user:
                user.follow_me=True
                user.updated_at = datetime.now()
                self.data["updated"]+=1
            else:
                user = User(name=profile['name'], url_name=profile['url_name'], follow_me=True, i_follow=profile["i_follow"], got_from="STARTING_BASE")
                session.add(user)
                self.data["created"]+=1
            self._try_to_commit(session, user)

        logger.warning(f">> FINISH to update my followers")
        logger.warning(f">> UPDATED: {self.data['updated']} ")
        logger.warning(f">> CREATED: {self.data['created']} ")
        logger.warning(f">> DB ERRORS: {self.data['errors']} ")
        session.close()
        
    def update_my_following(self):
        logger.warning(f"START update following")
        self.browser.get(f"{URL}{MY_PROFILE}/") 
        time.sleep(self.sleep_time+bit())
        
        ShowProfileList(self.browser).show_following()
        profiles_info = MyFollowersScrapper(self.browser).get_profiles_info()
        
        for profile in profiles_info:
            user = session.query(User).filter_by(url_name=profile['url_name']).first()
            if user:
                user.i_follow=True
                user.updated_at = datetime.now()
                self.data["updated"]+=1
            else:
                user = User(name=profile['name'], url_name=profile['url_name'], i_follow=True, got_from="STARTING_BASE")
                session.add(user)
                self.data["created"]+=1
            self._try_to_commit(session, user)
            
        logger.warning(f">> FINISH update my following")
        logger.warning(f">> UPDATED: {self.data['updated']} ")
        logger.warning(f">> CREATED: {self.data['created']} ")
        logger.warning(f">> DB ERRORS: {self.data['errors']} ")
        session.close()
        
    def _try_to_commit(self, session, user):
        try:
            session.commit()
        except IntegrityError as error:
            self.data["errors"]+=1
            session.rollback()
            logger.error(f"{user.name} | {user.url_name}, could not be saved: {error}")
