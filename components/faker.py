from loguru import logger
from random import random

def bit():
    time = 0
    while time < 0.1:
        time = random()
    logger.info(f"waited for {round(time, 2)} seconds")
    return time