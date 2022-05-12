from selenium import webdriver

CHROMEDRIVER = "./components/chromedriver.exe"

def start_browser():   
    options = webdriver.ChromeOptions() 
    options.add_argument("start-maximized")
    options.add_argument('--disable-logging')
    # options.add_experimental_option('excludeSwitches', ['enable-logging'])
    browser = webdriver.Chrome(options=options, executable_path=CHROMEDRIVER)
    
    return browser