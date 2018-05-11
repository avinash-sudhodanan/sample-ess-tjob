import requests
from pprint import pprint
import os
import sys

class TJob():
	essApiUrl=os.environ['ET_ESS_API']
	print("ESS URL is: "+str(essApiUrl))
	if essApiUrl.startswith("http:"):
		proxyurl="http://" + essApiUrl.lstrip("http://").rstrip(":80/ess/api/r4") + ":8080/"
	elif essApiUrl.startswith("https://"):
		proxyurl="http://" + essApiUrl.lstrip("https://").rstrip(":80/ess/api/r4") + ":8080/"
	#proxyurl="http://" + str(sys.argv[1]) + ":8080/"
	proxies = {'http':proxyurl, 'https':proxyurl}
	def test_send_request(self,url):
		s=requests.Session()
		response=s.get(url, proxies=self.proxies,verify=False)
		print response.headers
		
if __name__=="__main__":
	tjob=TJob()
	tjob.test_send_request('http://www.mashable.com/')
	tjob.test_send_request('http://www.theplantlist.org/')
