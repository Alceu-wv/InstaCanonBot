from datetime import datetime
from loguru import logger
from models import Routine, User, session

class Reporter:
    report_data = {}
    
    def make_final_report(self, routine, user, exception=None):
        user = session.query(User).filter(User.id==user.id).first()
        routine = session.query(Routine).filter(Routine.id==routine.id).first()
        routine.follow_unfollows = self.report_data.get("followed", self.report_data.get("unfollowed", 0))
        routine.errors = self.report_data.get("errors", self.report_data.get("db_errors", 0))
        routine.miss_actions = self.report_data.get("already_following", self.report_data.get("already_unfollowing", 0))
        routine.total_actions = routine.follow_unfollows
        routine.report = str(self.report_data)
        routine.finished_at = datetime.now()
        routine.exception = exception
        user.last_routine_date = datetime.now()
        session.commit()
        session.close()
        
    def profile_scrapper_report(self, data):
        logger.warning(f"FINISH to get another profile followers")
        logger.warning(f">> UPDATED: {data['updated']} ")
        logger.warning(f">> CREATED: {data['created']} ")
        logger.warning(f">> DB ERRORS: {data['errors']} ")
        self.report_data = {**self.report_data, **data}
        
    def follow_report(self, data):
        logger.warning(f"FINISH follow new profiles")
        logger.warning(f">> FOLLOWED: {data['followed']} ")
        logger.warning(f">> ALREADY FOLLOWING: {data['already_following']} ")
        logger.warning(f">> DB ERRORS: {data['errors']} ")
        self.report_data = {**self.report_data, **data}
        
    def unfollow_report(self, data):
        logger.warning(f">> FINISH to unfollow who dont follow back")
        logger.warning(f">> UNFOLLOWED: {data['unfollowed']}")
        logger.warning(f">> ERRORS: {data['errors']}")
        self.report_data = {**self.report_data, **data}
        
    def update_my_followings_report(self, data):
        logger.warning(f">> FINISH to update my following")
        logger.warning(f">> UPDATED: {data['following_updated']} ")
        logger.warning(f">> CREATED: {data['following_created']} ")
        logger.warning(f">> DB ERRORS: {data['following_errors']} ")
        self.report_data = {**self.report_data, **data}
        
    def update_my_followers_report(self, data):
        logger.warning(f">> FINISH to update my followers")
        logger.warning(f">> UPDATED: {data['followers_updated']} ")
        logger.warning(f">> CREATED: {data['followers_created']} ")
        logger.warning(f">> DB ERRORS: {data['followers_errors']} ")
        self.report_data = {**self.report_data, **data}
        