import time
from selenium import webdriver
from components.dismiss import Dismiss
from components.login import Login

URL = "https://www.instagram.com/"
CHROMEDRIVER = "./components/chromedriver.exe"

def instagram_check_in():
    browser = webdriver.Chrome(CHROMEDRIVER)
    browser.get(URL)
    time.sleep(2)
    
    Login(browser).login()
    
    dismiss = Dismiss(browser)
    dismiss.dismiss_save_login()
    dismiss.dismiss_active_notifications()
    
    return browser