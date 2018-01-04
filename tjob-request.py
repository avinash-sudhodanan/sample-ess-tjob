import unittest
import requests
import os
import sys

class TJob():
	proxyurl="http://" + str(sys.argv[1]) + ":8080/"
	proxies = {'http':proxyurl, 'https':proxyurl}
	def test_send_request(self,url):
		s=requests.Session()
		response=s.get(url, proxies=self.proxies,verify=False)
		print response.headers
		
if __name__=="__main__":
	tjob=TJob()
	tjob.test_send_request('http://www.mashable.com/')
	tjob.test_send_request('https://www.google.com/')
	tjob.test_send_request('https://www.facebook.com/')
	tjob.test_send_request('https://www.amazon.com/')
