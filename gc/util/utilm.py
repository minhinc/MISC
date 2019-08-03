import requests
from bs4 import BeautifulSoup
import urllib.request as urllib2
import os
import re

import html.parser
import subprocess

class utilc:
 def __init__(self,site=''):
  print("init %s" % site)
  self.useragent={'User-Agent':'Chrome/60.0.3112.89'}
  self.client = requests.Session()
  if site=='linkedin':
   HOMEPAGE_URL = 'https://www.linkedin.com'
   LOGIN_URL = 'https://www.linkedin.com/uas/login-submit'
#   html = self.client.get(HOMEPAGE_URL).content
   html = self.client.get(HOMEPAGE_URL,headers=self.useragent).content
   soup = BeautifulSoup(html, "html.parser")
   try:
    csrf = soup.find(id="loginCsrfParam-login")['value']
    login_information = {
     'session_key':re.split('\n',open(os.path.expanduser('~/passwd')).read())[5],
     'session_password':re.split('\n',open(os.path.expanduser('~/passwd')).read())[6],
     'loginCsrfParam': csrf,
    }
    self.client.post(LOGIN_URL, data=login_information)
   except:
    print('linkedin login failed')
 def download(self,link):
  print("link {}".format(link))
  return self.client.get(link,headers=self.useragent).text
 def getlinkedin_1(self,link):
  print("><getlinkedin %s" % link)
  return self.client.get(link,timeout=20.0,headers=self.useragent).text
 def getlinkedin_2(self,link):
#  print("><getlinkedin %s" % link)
  try:
#   output=subprocess.check_output(['egrep','-o','[A-Za-z0-9._%-]+\@(\w|-)+[.](\w+|[.]|-)*'],input=self.client.get(link,timeout=20.0).content).decode('utf-8')
   return subprocess.check_output(['egrep','-o','[A-Za-z0-9._%-]+\@(\w|-)+[.](\w+|[.]|-)*'],input=self.client.get(link,timeout=20.0).content).decode('utf-8')
#   return output
  except Exception as er:
   if type(er)==FileNotFoundError:
    print("egrep not found!!! add egrep in PATH")
#    return output
#   elif type(er)==subprocess.CalledProcessError:
#    print("no email found")
   return ''
 def close(self):
  self.client.close()
