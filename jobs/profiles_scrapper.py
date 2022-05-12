import time
from datetime import datetime
from loguru import logger
from sqlalchemy.exc import IntegrityError
from models import session, User
from components.faker import bit
from components.scrapper import MyFollowersScrapper
from components.scroll import ShowProfileList


URL = "https://www.instagram.com/"

class ProfileScrapper:
    def __init__(self, browser=None, sleep_time=1):
        self.browser = browser
        self.sleep_time = sleep_time
        self.data = {"updated": 0, "created": 0, "errors":0}
        
    def get_another_profile_followers(self, another_profile):
        logger.warning(f"START to get another profile followers")
        self.browser.get(f"{URL}{another_profile}/") 
        time.sleep(self.sleep_time+bit())
        
        # TODO: lógica para listas muito grandes
        ShowProfileList(self.browser).show_followers()
        profiles_info = MyFollowersScrapper(self.browser).get_profiles_info()
        
        for profile in profiles_info:
            user = session.query(User).filter_by(url_name=profile['url_name']).first()
            if user:
                user.updated_at = datetime.now()
                self.data["updated"]+=1
            else:
                user = User(name=profile['name'], url_name=profile['url_name'], i_follow=profile['i_follow'], got_from=another_profile)
                self.data["created"]+=1
                session.add(user)
            self._try_to_commit(session, user)
        
        logger.warning(f"FINISH to get another profile followers")
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
    