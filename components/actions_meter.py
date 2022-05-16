from loguru import logger
from datetime import datetime, timedelta
from models import Routine, session

class ActionsQuantityExceeded(Exception):
    pass

class ActionsMeter:
    def __init__(self, user):
        self.user = user
        self.performed_actions_today = 0
        self.performed_actions_last_hour = 0
        self.hour_limit = user.max_actions_hour
        self.today_limit = user.max_actions_day
        self._retrieve_past_max_actions()
        session.expunge_all()
        
    def _retrieve_past_max_actions(self):
        if session.query(Routine).filter(Routine.finished_at!=None).all():
            self._retrieve_last_hour_actions()
            self._retrieve_today_performed_actions()
        logger.warning(f"Ready to start. Avaible actions to perform is {self.user.max_actions_hour - self.performed_actions_last_hour}")
        
    def _retrieve_today_performed_actions(self):
        yesterday = datetime.now()-timedelta(days=1)
        last_routines = session.query(Routine).filter(Routine.finished_at > yesterday, Routine.user_id==self.user.id).all()
        today_actions = sum([row.total_actions for row in last_routines])
        self.performed_actions_today = today_actions
        self._verify_today_limit()
        
    def _retrieve_last_hour_actions(self):
        one_hour_ago = datetime.now()-timedelta(hours=1)
        last_hour_routines = session.query(Routine).filter(Routine.finished_at > one_hour_ago, Routine.user_id==self.user.id).all()
        last_hour_actions = sum([row.total_actions for row in last_hour_routines])
        self.performed_actions_last_hour = last_hour_actions
        self._verify_hour_limit()
    
    def _verify_today_limit(self):
        if self.performed_actions_today > self.today_limit:
            raise ActionsQuantityExceeded(f"Performed actions today: {self.performed_actions_today}. Maximum is: {self.user.max_actions_day}")

    def _verify_hour_limit(self):
        if self.performed_actions_last_hour > self.hour_limit:
            raise ActionsQuantityExceeded(f"Performed actions last hour: {self.performed_actions_last_hour}. Maximum is: {self.user.max_actions_hour}")
    
    def count_action(self, action=1):
        self.performed_actions_last_hour += action
        self._verify_hour_limit()
        self.performed_actions_today += action
        self._verify_today_limit()
