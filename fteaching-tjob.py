import unittest
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from pprint import pprint
import os
import sys
import requests
from urlparse import urlparse
import time

class PythonOrgSearch(unittest.TestCase):

    def setUp(self):
    	essApiUrl=os.environ['ET_ESS_API']
    	parsed_ess_url=urlparse(essApiUrl)
    	ess_url=parsed_ess_url.scheme+"://"+parsed_ess_url.netloc
    	print("ESS URL is: "+str(ess_url))
    	eusUrl=os.environ['ET_EUS_API']
    	print("EUS URL is: "+str(eusUrl))
    	ess_mitm_proxy_url=ess_url.rstrip(":80").lstrip("http://")
        options = webdriver.ChromeOptions()
        options.add_argument('--proxy-server='+ess_mitm_proxy_url+":8080")
        capabilities = options.to_capabilities()
        self.driver = webdriver.Remote(command_executor=eusUrl, desired_capabilities=capabilities)
        #self.driver = webdriver.Chrome(desired_capabilities=capabilities)
        #self.driver = webdriver.Firefox()
    def test_search_in_python_org(self):
        driver = self.driver
	if len(sys.argv)>1 and sys.argv[1] == "fullteaching-login":
		driver.get("https://52.50.3.12/#/")
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
	elif len(sys.argv)>1 and sys.argv[1] == "fullteaching-home":
		driver.get("https://52.50.3.12/#/")		
	else:
		driver.get("https://example.com")

    	essApiUrl=os.environ['ET_ESS_API']
    	parsed_ess_url=urlparse(essApiUrl)
    	ess_url=parsed_ess_url.scheme+"://"+parsed_ess_url.netloc
        re=requests.get(ess_url+"/ess/api/r4/start/")
        if "starting-ess" in re.text:
            req=requests.get(ess_url+'/ess/api/r4/status/')
            status=req.text
            while ("not-yet" in status):
                time.sleep(5)
                req=requests.get(ess_url+'/ess/api/r4/status/')
                status=req.text

    def tearDown(self):
        pass

if __name__ == "__main__":
	unittest.main()