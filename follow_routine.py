from loguru import logger
from components.actions_meter import ActionsMeter, ActionsQuantityExceeded
from components.browser import start_browser
from components.reporter import Reporter
from jobs.check_in import instagram_check_in
from jobs.follow import Follow
from models import Routine, User, session


MY_PROFILE = "ceuitalian"
user = session.query(User).filter_by(url_name=MY_PROFILE).first()
routine = Routine(name="FOLLOW", user_id=user.id)
session.add(routine)
session.commit()
session.expunge_all()

reporter  = Reporter()
try:
    actions_meter = ActionsMeter(user)
    browser = start_browser()
    instagram_check_in(browser, user)
except ActionsQuantityExceeded as exception:
    logger.error(exception)
    exit()

try:
    follow_data = Follow(browser, actions_meter).follow_new_profiles()
    reporter.follow_report(follow_data)
    
    reporter.make_final_report(routine, user)
    session.close()
except ActionsQuantityExceeded as exception:
    logger.error("Parei, parei...")
    reporter.follow_report(exception.args[0])
    reporter.make_final_report(routine, user, str(exception))
    session.close()   
