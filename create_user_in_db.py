from loguru import logger
from models import User, session

URL_NAME="ceuitalian"
PASSWORD="Italy2023"
new_user = User(url_name=URL_NAME, password=PASSWORD, max_actions_hour=150, max_actions_day=500)

session.add(new_user)
session.commit()

logger.info(f"{new_user} created!")
