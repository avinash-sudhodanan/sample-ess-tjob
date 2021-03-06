from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.proxy import Proxy, ProxyType
from pprint import pprint
import os
import sys
import requests
from urlparse import urlparse
import time
import json

class PrivacyCheckTest():
    ess_url = ""
    ess_mitm_proxy_url = ""
    eus_url = ""
    def setUp(self):
        states = ["logged_in_student","logged_in_teacher"]
    	essApiUrl=os.environ['ET_ESS_API'] #get ESS API endpoint info. via env. var.
    	parsed_ess_url=urlparse(essApiUrl) #converting to parsed URL to check for protocol and path
    	self.ess_url=parsed_ess_url.scheme+"://"+parsed_ess_url.netloc
    	print("ESS URL is: "+str(self.ess_url))
    	self.eus_url = os.environ['ET_EUS_API'] #get EUS API endpoint info. via env. var.
    	print("EUS URL is: "+str(self.eus_url))
    	self.ess_mitm_proxy_url = self.ess_url.rstrip(":80").lstrip("http://") #get ESS ZAP endpoint info. via ESS env. var.
        #begin selenium via EUS code (with ZAP as proxy)
    	options = webdriver.ChromeOptions()
    	options.add_argument('--proxy-server='+self.ess_mitm_proxy_url+":8080")
        options.add_argument('--ignore-certificate-errors')
	options.add_argument('--no-sandbox')
	options.add_argument('--window-size=1420,1080')
	options.add_argument('--headless')
	options.add_argument('--disable-gpu')

        #self.driver = webdriver.Remote(command_executor=eusUrl, desired_capabilities=capabilities)
        #end selenium via EUS code (with ZAP as proxy)

    	#begin debug code
    	#proxies = {'http': ess_mitm_proxy_url+":8080",'https': ess_mitm_proxy_url+":8080"}
    	#requests.get('http://example.org', proxies=proxies)
        #self.driver = webdriver.Chrome(desired_capabilities=capabilities)
    	#self.driver = webdriver.Firefox()

        #proxy =  ess_mitm_proxy_url+":8080"
        #firefox_capabilities = webdriver.DesiredCapabilities.FIREFOX
        #firefox_capabilities['marionette'] = True
        #firefox_capabilities['proxy'] = {
        #    "proxyType": "MANUAL",
        #    "httpProxy": proxy,
        #    "ftpProxy": proxy,
        #    "sslProxy": proxy
        #}
        #self.driver = webdriver.Firefox(capabilities=firefox_capabilities)
        #end debug code

    def logged_in_student(self, url, not_visited_url_state_map, phase, state_name):
        re=requests.post(self.ess_url+"/ess/api/r4/startstate/",json={"statename": "logged_in_student", "phase": phase}) #tell ESS API which state script is going to start
        status=re.text
        #Begin set firefox proxy and open it
        """
        proxy =  "127.0.0.1"+":8080"
        proxy = self.ess_mitm_proxy_url
        firefox_capabilities = webdriver.DesiredCapabilities.FIREFOX
        firefox_capabilities['marionette'] = True
        firefox_capabilities['proxy'] = {
            "proxyType": "MANUAL",
            "httpProxy": proxy,
            "ftpProxy": proxy,
            "sslProxy": proxy
        }
        driver = webdriver.Firefox(capabilities=firefox_capabilities) #uncomment during debugging
        """
        # End set firefox proxy for debugging

        #Begin chrome proxy for demo
        #options = webdriver.ChromeOptions()
    	#options.add_argument('--proxy-server='+self.ess_mitm_proxy_url+":8080")
    	#capabilities = options.to_capabilities()
        #driver = webdriver.Remote(command_executor=self.eus_url, desired_capabilities=capabilities)
        #driver.set_page_load_timeout(15)
	options = webdriver.ChromeOptions()
    	options.add_argument('--proxy-server='+self.ess_mitm_proxy_url+":8080")
        options.add_argument('--ignore-certificate-errors')
	options.add_argument('--no-sandbox')
	options.add_argument('--window-size=1420,1080')
	options.add_argument('--headless')
	options.add_argument('--disable-gpu')
	driver = webdriver.Chrome(chrome_options=options) #do not use EUS remote driver
        driver.set_page_load_timeout(60)
        #End set firefox proxy and open it
        if "State script starting noted" in status:

            driver.get(url)
            #Being full teaching login code
            login_launch = driver.find_element_by_xpath("//*[@id=\"navigation-bar\"]/div/ul/li[2]/a")
            login_launch.click()
            username = driver.find_element_by_id("email")
            username.send_keys("student1@gmail.com")
            password = driver.find_element_by_id("password")
            password.send_keys("pass")
            login_btn = driver.find_element_by_id("log-in-btn")
            login_btn.click()
            time.sleep(5)
            settings_btn = driver.find_element_by_id("settings-button")
            settings_btn.click()
            driver.get(url+"api-video-sessions/get-sessionid-token/1")
            driver.get(url+"api-video-sessions/get-sessionid-token/2")
            driver.get(url+"api-video-sessions/get-sessionid-token/3")
            driver.get(url+"api-video-sessions/get-sessionid-token/4")
            driver.get(url+"api-video-sessions/get-sessionid-token/5")
            #End full teaching login code
            """
            #begin login code google.com
            login_launch = driver.find_element_by_id("gb_70")
            login_launch.click()
            username = driver.find_element_by_id("identifierId")
            username.send_keys("am107cs018@gmail.com")
            time.sleep(2)
            username_submit = driver.find_element_by_id("identifierNext")
            username_submit.click()
            time.sleep(3)
            password = driver.find_element_by_css_selector("input[type=\"password\"]")
            password.send_keys("thisisavinashs")
            login_btn = driver.find_element_by_id("passwordNext")
            login_btn.click()
            time.sleep(3)
            #end login code google
            """
            if phase != "First":
                print("State is "+state_name)
                print("URLs to be visited are :")
                #visiting URLs that were not visited in that state normally
                for url in list(not_visited_url_state_map.keys()):
                    try:
                        if state_name in not_visited_url_state_map[url]:
                            driver.get(str(url))
                            time.sleep(1)
                            print(str(url))
                    except:
                        print("Timeout exception occured for "+str(url))
            re = requests.post(self.ess_url+"/ess/api/r4/finishstate/",json={"statename": "logged_in_student","phase":phase}) #tell ESS API which state script is going to end
            status = re.text
            if "State script finish noted" in status:
                print "State script execution finished"
        try:
            driver.quit()
        except:
            print("WebDriver was closed automatically. Captcha detected?")

    def logged_in_teacher(self, url, not_visited_url_state_map, phase, state_name):
        re=requests.post(self.ess_url+"/ess/api/r4/startstate/",json={"statename": "logged_in_teacher", "phase": phase}) #tell ESS API which state script is going to start
        status=re.text
        #Begin set firefox proxy and open it
        """
        proxy =  "127.0.0.1"+":8080"
        proxy = self.ess_mitm_proxy_url
        firefox_capabilities = webdriver.DesiredCapabilities.FIREFOX
        firefox_capabilities['marionette'] = True
        firefox_capabilities['proxy'] = {
            "proxyType": "MANUAL",
            "httpProxy": proxy,
            "ftpProxy": proxy,
            "sslProxy": proxy
        }
        driver = webdriver.Firefox(capabilities=firefox_capabilities) #uncomment during debugging
        """
        # End set firefox proxy for debugging

        #Begin chrome proxy for demo
        #options = webdriver.ChromeOptions()
    	#options.add_argument('--proxy-server='+self.ess_mitm_proxy_url+":8080")
    	#capabilities = options.to_capabilities()
        #driver = webdriver.Remote(command_executor=self.eus_url, desired_capabilities=capabilities)
        #driver.set_page_load_timeout(15)
	options = webdriver.ChromeOptions()
    	options.add_argument('--proxy-server='+self.ess_mitm_proxy_url+":8080")
        options.add_argument('--ignore-certificate-errors')
	options.add_argument('--no-sandbox')
	options.add_argument('--window-size=1420,1080')
	options.add_argument('--headless')
	options.add_argument('--disable-gpu')
	driver = webdriver.Chrome(chrome_options=options) #do not use EUS remote driver
        driver.set_page_load_timeout(60)
        #End set firefox proxy and open it
        if "State script starting noted" in status:

            driver.get(url)
            #Being full teaching login code
            login_launch = driver.find_element_by_xpath("//*[@id=\"navigation-bar\"]/div/ul/li[2]/a")
            login_launch.click()
            username = driver.find_element_by_id("email")
            username.send_keys("teacher@gmail.com")
            password = driver.find_element_by_id("password")
            password.send_keys("pass")
            login_btn = driver.find_element_by_id("log-in-btn")
            login_btn.click()
            time.sleep(5)
            settings_btn = driver.find_element_by_id("settings-button")
            settings_btn.click()
            driver.get(url+"api-video-sessions/get-sessionid-token/1")
            driver.get(url+"api-video-sessions/get-sessionid-token/2")
            driver.get(url+"api-video-sessions/get-sessionid-token/3")
            driver.get(url+"api-video-sessions/get-sessionid-token/4")
            driver.get(url+"api-video-sessions/get-sessionid-token/5")
            #End full teaching login code
            """
            #begin login code google.com
            login_launch = driver.find_element_by_id("gb_70")
            login_launch.click()
            username = driver.find_element_by_id("identifierId")
            username.send_keys("am107cs018@gmail.com")
            time.sleep(2)
            username_submit = driver.find_element_by_id("identifierNext")
            username_submit.click()
            time.sleep(3)
            password = driver.find_element_by_css_selector("input[type=\"password\"]")
            password.send_keys("thisisavinashs")
            login_btn = driver.find_element_by_id("passwordNext")
            login_btn.click()
            time.sleep(3)
            #end login code google
            """
            if phase != "First":
                print("State is "+state_name)
                print("URLs to be visited are :")
                #visiting URLs that were not visited in that state normally
                for url in list(not_visited_url_state_map.keys()):
                    try:
                        if state_name in not_visited_url_state_map[url]:
                            driver.get(str(url))
                            time.sleep(1)
                            print(str(url))
                    except:
                        print("Timeout exception occured for "+str(url))
            re = requests.post(self.ess_url+"/ess/api/r4/finishstate/",json={"statename": "logged_in_teacher","phase":phase}) #tell ESS API which state script is going to end
            status = re.text
            if "State script finish noted" in status:
                print "State script execution finished"
        try:
            driver.quit()
        except:
            print("WebDriver was closed automatically. Captcha detected?")

    def logged_out(self, url, not_visited_url_state_map, phase, state_name):
    	re = requests.post(self.ess_url+"/ess/api/r4/startstate/",json={"statename": "logged_out", "phase": phase}) #tell ESS API which state script is going to start
        status = re.text
        #Begin set firefox proxy and open it
        """
        proxy =  "127.0.0.1"+":8080"
        firefox_capabilities = webdriver.DesiredCapabilities.FIREFOX
        firefox_capabilities['marionette'] = True
        firefox_capabilities['proxy'] = {
            "proxyType": "MANUAL",
            "httpProxy": proxy,
            "ftpProxy": proxy,
            "sslProxy": proxy
        }
        driver = webdriver.Firefox(capabilities=firefox_capabilities)
        """
        #Begin chrome proxy for demo
        #options = webdriver.ChromeOptions()
    	#options.add_argument('--proxy-server='+self.ess_mitm_proxy_url+":8080")
    	#capabilities = options.to_capabilities()
        #driver = webdriver.Remote(command_executor=self.eus_url, desired_capabilities=capabilities)
        #driver.set_page_load_timeout(15)
	options = webdriver.ChromeOptions()
    	options.add_argument('--proxy-server='+self.ess_mitm_proxy_url+":8080")
        options.add_argument('--ignore-certificate-errors')
	options.add_argument('--no-sandbox')
	options.add_argument('--window-size=1420,1080')
	options.add_argument('--headless')
	options.add_argument('--disable-gpu')
	driver = webdriver.Chrome(chrome_options=options) #do not use EUS remote driver
        driver.set_page_load_timeout(60)
        #End set firefox proxy and open it

        if "State script starting noted" in status:
            driver.get(url)
            if phase != "First":
                print("State is "+state_name)
                print("URLs to be visited are :")
                #visiting URLs that were not visited in that state normally
                for url in list(not_visited_url_state_map.keys()):
                    try:
                        if state_name in not_visited_url_state_map[url]:
                            driver.get(str(url))
                            time.sleep(1)
                            print(str(url))
                    except:
                        print("Timeout exception occured for "+str(url))
            re=requests.post(self.ess_url+"/ess/api/r4/finishstate/",json={"statename": "logged_out","phase":phase}) #tell ESS API which state script is going to end
            status=re.text
            if "State script finish noted" in status:
                print "State script execution finished"
        try:
            driver.quit()
        except:
            print("WebDriver was closed automatically. Captcha detected?")

    def start_privacy_check(self):
    	re=requests.post(self.ess_url+"/ess/api/r4/startprivacycheck/",json={"states": ["logged_in_student","logged_in_teacher"],"browser":"chrome","browser_version":"60.0"}) #tell ESS API which state script is going to start
        status=json.loads(re.text)["status"]
    	#Checking the status of the scan
    	if "Start Privacy Check" in status:
                not_visited_url_state_map = json.loads(re.text)["not_visited_url_state_map"]
                #pprint(url_map)

                self.logged_in_student(sys.argv[1],not_visited_url_state_map,"Second","logged_in_student")
                self.logged_in_teacher(sys.argv[1],not_visited_url_state_map,"Second","logged_in_teacher")

    def end_privacy_check(self):
        re=requests.get(self.ess_url+"/ess/api/r4/endprivacycheck/") #tell ESS API which state script is going to end
        status=re.text
        print("Finished privacy check")
        print(status)

    def execute_tjob(self, url):
        self.setUp()
        self.logged_in_student(url,[],"First","logged_in_student")
        self.logged_in_teacher(url,[],"First","logged_in_teacher")
        self.start_privacy_check()


if __name__ == "__main__":
    if len(sys.argv)>1:
        tjob = PrivacyCheckTest()
        tjob.execute_tjob(sys.argv[1])
        tjob.end_privacy_check()
