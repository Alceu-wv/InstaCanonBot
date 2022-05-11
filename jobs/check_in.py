import time
from selenium import webdriver
from components.dismiss import Dismiss
from components.login import Login
from components.faker import bit

URL = "https://www.instagram.com/"
CHROMEDRIVER = "./components/chromedriver.exe"

def instagram_check_in():
    # browser = webdriver.Chrome(CHROMEDRIVER)
    
    options = webdriver.ChromeOptions() 
    options.add_argument("start-maximized")
    options.add_argument('--disable-logging')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    browser = webdriver.Chrome(options=options, executable_path=CHROMEDRIVER)
    
    browser.get(URL)
    time.sleep(2+bit())
    
    Login(browser).login()
    
    dismiss = Dismiss(browser)
    dismiss.dismiss_save_login()
    dismiss.dismiss_active_notifications()
    
    return browser