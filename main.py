from components.actions_meter import ActionsMeter
from components.browser import start_browser
from components.reporter import Reporter
from jobs.check_in import instagram_check_in
from jobs.follow import Follow
from jobs.my_profile import MyProfile
from jobs.profiles_scrapper import ProfileScrapper
from jobs.unfollow import Unfollow
from models import User, session
from post import TimelinePost

MY_PROFILE = "astro.sol.lua"
ANOTHER_PROFILE = "iarafelix"

url_name="astro.sol.lua"
password="Daniela2050"
new_user = User(url_name=url_name, password=password)
user = session.query(User).filter_by(url_name=url_name).first()
if not user:
    user = new_user
    
actions_meter = ActionsMeter(user)
reporter  = Reporter
browser = start_browser()
instagram_check_in(browser, user)

MyProfile(browser).update_my_followers(MY_PROFILE)
MyProfile(browser).update_my_following(MY_PROFILE)
ProfileScrapper(browser).get_another_profile_followers(ANOTHER_PROFILE)
Follow(browser, actions_meter).follow_new_profiles()

# Unfollow(browser).unfollow_who_dont_follow_back()

# TimelinePost(browser).post()

