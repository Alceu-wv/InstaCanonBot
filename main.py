from jobs.check_in import instagram_check_in
from jobs.follow import Follow
from jobs.my_profile import MyProfile
from jobs.profiles_scrapper import ProfileScrapper
from jobs.unfollow import Unfollow
from post import TimelinePost

browser = instagram_check_in()

MyProfile(browser).update_my_followers()
MyProfile(browser).update_my_following()
ProfileScrapper(browser).get_another_profile_followers()
Follow(browser).follow_new_profiles()
Unfollow(browser).unfollow_who_dont_follow_back()

# TimelinePost(browser).post()

