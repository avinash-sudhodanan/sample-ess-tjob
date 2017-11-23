import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os

class PythonOrgSearch(unittest.TestCase):

    def setUp(self):
        selenium_hub=os.environ['ET_EUS_API']
        print selenium_hub
        driver = webdriver.Remote(command_executor=selenium_hub,desired_capabilities={'browserName': 'firefox', 'javascriptEnabled': True})

    def test_search_in_python_org(self):
        driver = self.driver
        driver.get("https://github.com")
        assert "GitHub" in driver.title
        elem = driver.find_element_by_name("q")
        elem.send_keys("dzitkowskik")
        elem.send_keys(Keys.RETURN)
        assert "No results found." not in driver.page_source

    def tearDown(self):
        print("OK")

if __name__ == "__main__":
    unittest.main()
