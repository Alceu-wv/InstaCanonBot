import time
from datetime import datetime
from loguru import logger
from sqlalchemy.exc import IntegrityError
from selenium.webdriver.common.by import By
from models import session, Profile
from components.faker import bit
from components.navegation.scrapper import FollowersScrapper
from components.navegation.scroll import ShowProfileList


URL = "https://www.instagram.com/"

class ProfileScrapper:
    def __init__(self, browser=None, sleep_time=1):
        self.browser = browser
        self.sleep_time = sleep_time
        self.data = {"updated": 0, "created": 0, "errors":0}
        self.followers_data = {"total_followers": 0}
        self.following_data = {"total_following": 0}
        
    def check_total_profile_numbers(self):
        followers_bar = self.browser.find_element(By.TAG_NAME, "ul").text.split("\n")
        total_profile_posts = followers_bar[0].split(" ")[0]
        total_profile_followers = int(followers_bar[1].split(" ")[0].replace('.',""))
        total_profile_following = int(followers_bar[2].split(" ")[0].replace('.',""))
        self.followers_data["total_followers"] = total_profile_followers
        self.following_data["total_following"] = total_profile_following
        
    def get_another_profile_followers(self, another_profile):
        logger.warning(f"START to get another profile followers")
        self.browser.get(f"{URL}{another_profile}/") 
        time.sleep(self.sleep_time+bit())
        self.check_total_profile_numbers()
        # TODO: lógica para listas muito grandes
        ShowProfileList(self.browser).show_followers(self.followers_data["total_followers"])
        profiles_info = FollowersScrapper(self.browser, self.followers_data["total_followers"]).get_profiles_info()
        
        for p in profiles_info:
            profile = session.query(Profile).filter_by(url_name=p['url_name']).first()
            if profile:
                profile.updated_at = datetime.now()
                self.data["updated"]+=1
            else:
                profile = Profile(name=p['name'], url_name=p['url_name'], i_follow=p['i_follow'], got_from=another_profile)
                self.data["created"]+=1
                session.add(profile)
            self._try_to_commit(session, profile)

        session.close()
        return self.data     
        
    def _try_to_commit(self, session, user):
        try:
            session.commit()
        except IntegrityError as error:
            self.data["errors"]+=1
            session.rollback()
            logger.error(f"{user.name} | {user.url_name}, could not be saved: {error}")
    