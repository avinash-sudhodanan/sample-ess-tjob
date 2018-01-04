import unittest
import requests
import os
import sys

class TJob():
	
	#proxyurl="http://" + os.environ['ET_SUT_HOST'] + ":8080/"
	proxyurl="http://" + str(sys.argv[1]) + ":8080/"
	proxies = {'http':proxyurl, 'https':proxyurl}
	def test_send_request(self):
		s=requests.Session()
		response=s.get('http://www.mashable.com/', proxies=self.proxies,verify=False)
		print response.headers
		response=s.get('https://www.google.com/', proxies=self.proxies,verify=False)
		#response=s.get('http://etm:8091/')
		print response.headers
		response=s.get('https://www.facebook.com/', proxies=self.proxies,verify=False)
		print response.headers
		response=s.get('https://www.amazon.com/', proxies=self.proxies,verify=False)
		print response.headers
		#assert "Google" in response.text
		
if __name__=="__main__":
	tjob=TJob()
	tjob.test_send_request()

