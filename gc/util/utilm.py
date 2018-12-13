import requests
from bs4 import BeautifulSoup
import urllib.request as urllib2
import os
import re

import html.parser

class utilc:
 def __init__(self,site=''):
  print("init %s" % site)
  if site=='linkedin':
   self.client = requests.Session()
   HOMEPAGE_URL = 'https://www.linkedin.com'
   LOGIN_URL = 'https://www.linkedin.com/uas/login-submit'
   html = self.client.get(HOMEPAGE_URL).content
   soup = BeautifulSoup(html, "html.parser")
   csrf = soup.find(id="loginCsrfParam-login")['value']
   login_information = {
    'session_key':re.split('\n',open(os.path.expanduser('~/passwd')).read())[5],
    'session_password':re.split('\n',open(os.path.expanduser('~/passwd')).read())[6],
    'loginCsrfParam': csrf,
   }
   self.client.post(LOGIN_URL, data=login_information)
 def download(self,link):
  return repr(urllib2.urlopen(urllib2.Request(link,headers={'User-Agent': 'Mozilla/44.0.2'}),timeout=90).read().decode('utf-8'))
 def getlinkedin_1(self,link):
  html_parser = html.parser.HTMLParser()
  print("><getlinkedin %s" % link)
  return self.client.get(link,timeout=20.0).text
 def getlinkedin_2(self,link):
  print("><getlinkedin %s" % link)
  data=self.client.get(link,timeout=20.0).text
  if re.search(r'@',data):
   print("email found:")
   return data
  else:
   return ''
