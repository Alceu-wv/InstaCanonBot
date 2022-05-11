import time

class Search:
    def __init__(self, browser, sleep_time=1):
        self.browser = browser
        self.sleep_time = sleep_time
        
    def search_profile(self, profile):
        self.browser.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/div[1]/div').click()
        time.sleep(self.sleep_time)
        self.browser.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/input').send_keys(profile)
        time.sleep(self.sleep_time*2)
        self.browser.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/div[3]/div/div[2]/div/div[1]/a/div').click()
        time.sleep(self.sleep_time*2)
    