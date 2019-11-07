import unittest
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from pprint import pprint
import os
import sys
import requests
from urlparse import urlparse
import time

url=""
class PythonOrgSearch(unittest.TestCase):

	def setUp(self):
		"""
		This function reads the necessary environment variables and cleans them
		"""
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
		capabilities['elastestTimeout'] = 0
		self.driver = webdriver.Remote(command_executor=eusUrl, desired_capabilities=capabilities)
		
		#-=Begin debug code for selenium=-#
		"""
		proxies = {'http': ess_mitm_proxy_url+":8080",'https': ess_mitm_proxy_url+":8080"}
		requests.get('http://example.org', proxies=proxies)
		self.driver = webdriver.Chrome(desired_capabilities=capabilities)
		"""
		#self.driver = webdriver.Firefox()
		
		#-=End debug code for selenium=-#

	def test_configure_ess(self):
		"""
		This function calls the ESS API to configure the test
		"""
		driver = self.driver
		essApiUrl=os.environ['ET_ESS_API']

		parsed_ess_url=urlparse(essApiUrl)
		ess_url=parsed_ess_url.scheme+"://"+parsed_ess_url.netloc
		sut_login_state=self.sutLogic(driver)
		if sut_login_state=="Done":
			parsed_sut_url=urlparse(url)
			scan_url=parsed_sut_url.scheme+"://"+parsed_sut_url.netloc
			print(scan_url)
			print(url)
			re=requests.post(ess_url+"/ess/api/r4/start/",json={"sites": [scan_url]})
			#Checking the status of the scan
			if "starting-ess" in re.text:
				req=requests.get(ess_url+'/ess/api/r4/status/')
				status=req.text
				while ("not-yet" in status):
					time.sleep(5)
					req=requests.get(ess_url+'/ess/api/r4/status/')
					status=req.text
	def sutLogic(self,driver):
		"""
		This function executes the actions that needs to be performed on a web browser for interacting with the SuT
		"""
		driver.get(url)
		time.sleep(10) #Wait until the actions on the browser has finished
		print("Waiting")
		while(driver.current_url not in ["https://elastest.io/","https://elastest.io"]):
                        time.sleep(2) #Wait until the actions on the browser has finished
			print(".", )
		return "Done"

	def tearDown(self):
		pass

if __name__ == "__main__":
	if len(sys.argv)>1:
		url=sys.argv[1]
		del sys.argv[1]
	unittest.main()
