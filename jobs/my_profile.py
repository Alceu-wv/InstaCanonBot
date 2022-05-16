import time
from datetime import datetime
from loguru import logger
from models import session, Profile
from components.faker import bit
from sqlalchemy.exc import IntegrityError
from selenium.webdriver.common.by import By
from components.navegation.scrapper import FollowersScrapper
from components.navegation.scroll import ShowProfileList


URL = "https://www.instagram.com/"


    def __init__(self, browser=None, sleep_time=1):
        self.browser = browser
        self.sleep_time = sleep_time
        self.followers_data = {"total_followers": 0, "followers_updated": 0, "followers_created": 0, "followers_errors":0}
        self.following_data = {"total_following": 0, "following_updated": 0, "following_created": 0, "following_errors":0}
        
    def check_total_profile_numbers(self):
        followers_bar = self.browser.find_element(By.TAG_NAME, "ul").text.split("\n")
        total_profile_posts = followers_bar[0].split(" ")[0]
        total_profile_followers = int(followers_bar[1].split(" ")[0].replace('.',""))
        total_profile_following = int(followers_bar[2].split(" ")[0].replace('.',""))
        self.followers_data["total_followers"] = total_profile_followers
        self.following_data["total_following"] = total_profile_following
    
    def update_my_followers(self, my_url_name):
        logger.warning(f"START to update my followers")
        self.browser.get(f"{URL}{my_url_name}/") 
        time.sleep(self.sleep_time+bit())
        self.check_total_profile_numbers()
        
        ShowProfileList(self.browser).show_followers(self.followers_data["total_followers"])
        profiles_info = FollowersScrapper(self.browser, self.followers_data["total_followers"]).get_profiles_info()
        
        for p in profiles_info:
            profile = session.query(Profile).filter_by(url_name=p['url_name']).first()
            if profile:
                profile.follow_me=True
                profile.updated_at = datetime.now()
                self.followers_data["followers_updated"]+=1
            else:
                profile = Profile(name=p['name'], url_name=p['url_name'], follow_me=True, i_follow=p["i_follow"], got_from="STARTING_BASE")
                session.add(profile)
                self.followers_data["followers_created"]+=1
            self._try_to_commit(session, profile)
        
        session.close()
        return self.followers_data
        
    def update_my_following(self, url_name):
        logger.warning(f"START update following")
        self.browser.get(f"{URL}{url_name}/") 
        time.sleep(self.sleep_time+bit())
        self.check_total_profile_numbers()
        
        ShowProfileList(self.browser).show_following(self.following_data["total_following"])
        profiles_info = FollowersScrapper(self.browser, self.following_data["total_following"]).get_profiles_info()
        
        for p in profiles_info:
            profile = session.query(Profile).filter_by(url_name=p['url_name']).first()
            if profile:
                profile.i_follow=True
                profile.updated_at = datetime.now()
                self.following_data["following_updated"]+=1
            else:
                profile = Profile(name=p['name'], url_name=p['url_name'], i_follow=True, got_from="STARTING_BASE")
                session.add(profile)
                self.following_data["following_created"]+=1
            self._try_to_commit(session, profile)
            
        session.close()
        return self.following_data
        
    def _try_to_commit(self, session, user):
        try:
            session.commit()
        except IntegrityError as error:
            self.data["errors"]+=1
            session.rollback()
            logger.error(f"{user.name} | {user.url_name}, could not be saved: {error}")
