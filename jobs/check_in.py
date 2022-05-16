import time

from components.navegation.dismiss import Dismiss
from components.navegation.login import Login
from components.faker import bit

URL = "https://www.instagram.com/"


def instagram_check_in(browser, user):   
    browser.get(URL)
    time.sleep(2+bit())
    
    Login(browser, user).login()
    
    dismiss = Dismiss(browser)
    dismiss.dismiss_save_login()
    dismiss.dismiss_active_notifications()
