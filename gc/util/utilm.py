import requests
from selenium import webdriver
import re
class utilc:
 def __init__(self,site=''):
  print("init %s" % site)
#  self.useragent={'User-Agent':'Chrome/60.0.3112.89'}
  self.client = requests.Session()
#  self.driver=webdriver.Chrome()
 def download(self,linkp):
#  print("link {}".format(linkp))
#  return self.client.get(link,headers=self.useragent).text
  return self.client.get(linkp,timeout=30).text
# def getlinkedin_1(self,link):
#  print("><getlinkedin %s" % link)
#  return self.client.get(link,timeout=20.0,headers=self.useragent).text
 def getgoogle(self,linkp,countp):
  linklist=[]
  for i in range(countp):
#   linklist.extend([x for x in re.findall(r'/url\?q=([^&]+)',self.client.get(r'https://www.google.com/search?q='+re.sub('\s+','+',linkp)+(r'&start='+str(i*10) if i else '')).text,flags=re.I) if not re.search(r'accounts.google',x,flags=re.I) and max([len(xx) for xx in re.findall(r'\d+',x)])<5])
   linklist.extend([x for x in re.findall(r'/url\?q=([^&]+)',self.client.get(r'https://www.google.com/search?q='+re.sub('\s+','+',linkp)+(r'&start='+str(i*10) if i else '')).text,flags=re.I) if not re.search(r'accounts.google',x,flags=re.I)])
#   self.driver.get(r'https://www.google.com/search?q='+re.sub('\s+','+',linkp)+(r'&start='+str(i*10) if i else ''))
#   linklist.extend([x for x in re.findall(r'<div class="r"><a href="([^"]+)',self.driver.page_source,flags=re.I) if len(x)<150 ])
  print("linkist {}".format(linklist))
  return linklist
 def close(self):
  self.client.close()
  #self.driver.close()
