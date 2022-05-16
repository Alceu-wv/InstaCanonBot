from loguru import logger
from components.actions_meter import ActionsQuantityExceeded
from components.browser import start_browser
from components.reporter import Reporter
from jobs.check_in import instagram_check_in
from jobs.profiles_scrapper import ProfileScrapper
from models import Routine, User, session

MY_PROFILE = "ceuitalian"
ANOTHER_PROFILE = "zodiaco.sincero"
user = session.query(User).filter_by(url_name=MY_PROFILE).first()
routine = Routine(name="GET_ANOTHER_PROFILE_FOLLOWERS", user_id=user.id)
session.add(routine)
session.commit()
session.expunge_all()

reporter  = Reporter()
browser = start_browser()
instagram_check_in(browser, user)

try:
    profile_scrap_data = ProfileScrapper(browser).get_another_profile_followers(ANOTHER_PROFILE)
    reporter.profile_scrapper_report(profile_scrap_data)
    
    reporter.make_final_report(routine, user)
    session.close()
except ActionsQuantityExceeded as exception:
    logger.error("Parei, parei...")
    reporter.make_final_report(routine, user, exception.args[0])
    session.close()