from components.browser import start_browser
from jobs.check_in import instagram_check_in
from jobs.follow import Follow
from jobs.my_profile import MyProfile
from jobs.profiles_scrapper import ProfileScrapper
from jobs.unfollow import Unfollow
from post import TimelinePost

MY_PROFILE = "astro.sol.lua"
ANOTHER_PROFILE = "iarafelix"

browser = start_browser()
instagram_check_in(browser)

MyProfile(browser).update_my_followers(MY_PROFILE)
MyProfile(browser).update_my_following(MY_PROFILE)
ProfileScrapper(browser).get_another_profile_followers(ANOTHER_PROFILE)
Follow(browser).follow_new_profiles()

# Unfollow(browser).unfollow_who_dont_follow_back()

# TimelinePost(browser).post()

