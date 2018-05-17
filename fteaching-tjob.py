import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pprint import pprint
import os
import sys

class PythonOrgSearch(unittest.TestCase):

    def setUp(self):
	essApiUrl=os.environ['ET_ESS_API']
	print("ESS URL is: "+str(essApiUrl))
	eusUrl=os.environ['ET_EUS_API']
	print("EUS URL is: "+str(eusUrl))

	self.driver = webdriver.Remote(command_executor=eusUrl,desired_capabilities={'browserName': 'firefox', 'javascriptEnabled': True})

    def test_search_in_python_org(self):
        driver = self.driver
        driver.get("https://github.com")
        assert "GitHub" in driver.title
        elem = driver.find_element_by_name("q")
        elem.send_keys("dzitkowskik")
        elem.send_keys(Keys.RETURN)
        assert "No results found." not in driver.page_source

    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()
