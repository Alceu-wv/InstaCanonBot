from loguru import logger
from components.actions_meter import ActionsQuantityExceeded
from components.browser import start_browser
from components.reporter import Reporter
from jobs.check_in import instagram_check_in
from jobs.my_profile import MyProfile
from models import Routine, User, session


MY_PROFILE = "ceuitalian"
user = session.query(User).filter_by(url_name=MY_PROFILE).first()
routine = Routine(name="MY_PROFILE_NUMBERS", user_id=user.id)
session.add(routine)
session.commit()
reporter  = Reporter()
# session.expunge_all()


browser = start_browser()
user = session.query(User).filter_by(url_name=MY_PROFILE).first()
instagram_check_in(browser, user)

try:
    my_follower_data = MyProfile(browser).update_my_followers(MY_PROFILE)
    reporter.update_my_followers_report(my_follower_data)

    my_following_data = MyProfile(browser).update_my_following(MY_PROFILE)
    reporter.update_my_followings_report(my_following_data)
    
    reporter.make_final_report(routine, user)
except ActionsQuantityExceeded as exception:
    logger.error("Parei, parei...")
    reporter.make_final_report(routine, user, exception)