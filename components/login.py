from loguru import logger

class Login():
    def __init__(self, browser):
        self.browser = browser
        self.email = "instalceu"
        self.password = "Italy2023"
        
    def login(self):
        self.browser.find_element_by_xpath('//*[@id="loginForm"]/div/div[1]/div/label/input').send_keys(self.email)
        self.browser.find_element_by_xpath('//*[@id="loginForm"]/div/div[2]/div/label/input').send_keys(self.password)
        self.browser.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]/button/div').click()
        logger.info(f"Login for {self.email}")