from selenium.webdriver.common.keys import Keys
from unidecode import unidecode
from seleniumrequest import seleniumrequest
from databaserequest import databaserequest
from machinelearningrequest import machinelearningrequest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import datetime
import os,time,re
import requests
import time

class linkedin(seleniumrequest,databaserequest,machinelearningrequest):
 def __init__(self,display=True):
  super(linkedin,self).__init__(display,'linkedin')
  '''
  if os.path.exists("data/cookies.txt"):
   super(linkedin,self).getlink(r"https://www.linkedin.com/",'linkedin')
   self.load_cookie("data/cookies.txt",'linkedin')
   super(linkedin,self).getlink(r"https://www.linkedin.com/",'linkedin')
  else:
  '''
  super(linkedin,self).getlink(r'https://www.linkedin.com/login','linkedin')
  self.webdriverdict['linkedin'].find_element_by_id('username').send_keys('tominhinc1@gmail.com')
  self.webdriverdict['linkedin'].find_element_by_id('password').send_keys('pinku76li')
  self.webdriverdict['linkedin'].find_element_by_id('password').send_keys(Keys.RETURN)
  time.sleep(self.delay)
  # self.save_cookie("data/cookies.txt",'linkedin')

 def get(self,*url):
  """url
  get("artifical intelligence","mexico",10)
  get([['company A',r'http://linkedin.com/qt'],['company B',r'http://linkedin.com/cpp']])"""
  print(f'{"################linkedin.get############":^100}\n{url=!r:^100}')
  clickonshowmorejobbutton=True
  companyhref=dict()
  fetchstr_l=[]
  href=''
  if len(url)==3 and type(url[2])==int:
   for i in range(url[2]):
    super(linkedin,self).getlink('https://www.linkedin.com/jobs/search/?keywords='+('C%2B%2B' if url[0]=='cpp' else 'python' if url[0]=='py' else 'opengl' if url[0]=='gl' else 'kivy' if url[0]=='kv' else 'Machine%20Learning' if url[0]=='ml' else url[0])+'&location='+re.sub(r'\s','%20',self.getmatching(url[1],*re.findall(r'^.*?#(.*)?\s+[.]\w{2}',open(r'data/country.txt').read(),flags=re.M),muteprint=True)[0])+'&locationId='+self.getcode(self.getmatching(url[1],*re.findall(r'^.*?#(.*)?\s+[.]\w{2}',open(r'data/country.txt').read(),flags=re.M),muteprint=True)[0])+'%3A0&start='+str(i*25),'linkedin')
    print(f'fetching page count {i+1} {i*25} -> {(i+1)*25}')
    [self.webdriverdict['linkedin'].execute_script('arguments[0].scrollTop = arguments[0].scrollHeight*'+str(float(i/25)), self.webdriverdict['linkedin'].find_element_by_css_selector("div.jobs-search-results-list")) for i in range(1,26) if not time.sleep(0.25)]
    with open('test.html','w') as f:
     f.write(self.webdriverdict['linkedin'].page_source)
#    for count,i in enumerate(self.webdriverdict['linkedin'].find_elements_by_xpath("//a[@class='job-card-container__link job-card-container__company-name ember-view']")):
    for count,i in enumerate(self.webdriverdict['linkedin'].find_elements_by_xpath("//div[@class='artdeco-entity-lockup__subtitle ember-view']/span")):
#    for count,i in enumerate(self.webdriverdict['linkedin'].find_elements_by_xpath("//div[@class='artdeco-entity-lockup__subtitle ember-view']/div")):
     companyname=unidecode(self.pruneline(i.text)+self.DELIMITER+url[0]+self.DELIMITER+url[1] if i.text and not re.search(r'^\s+$',i.text) else '')
     try:
      href=i.get_attribute('href')
     except:
      href=''
#      continue
     href='' if not href else href
     print(f'^linkedin {count} {companyname=} {href=}')
     fetchstr_l.append([companyname, href if href and self.validlink(href) else '']) if companyname and companyname+':'+href not in companyhref and self.validlink(self.googlelink(re.split(self.DELIMITER,companyname)[0])) else None
     if companyname:
      companyhref[companyname+':'+href]=None
     fetchstr_l[-1].pop() if fetchstr_l and not fetchstr_l[-1][-1] else None
    print(f'<=>linkedin {count=}')
    if count==0:
     break
  print(f'{len(fetchstr_l)=}')
  return [list(tup1) for tup1 in {tuple(item) for item in fetchstr_l }]
