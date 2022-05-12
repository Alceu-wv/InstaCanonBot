import time

from components.dismiss import Dismiss
from components.login import Login
from components.faker import bit

URL = "https://www.instagram.com/"


def instagram_check_in(browser):   
    browser.get(URL)
    time.sleep(2+bit())
    
    Login(browser).login()
    
    dismiss = Dismiss(browser)
    dismiss.dismiss_save_login()
    dismiss.dismiss_active_notifications()
