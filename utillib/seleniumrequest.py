from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.chrome.options import Options
import pickle
import os,time,re
from html.parser import HTMLParser

from selenium.webdriver.firefox.options import Options as FirefoxOptions

class HTMLFilter(HTMLParser):
 text = ""
 def handle_data(self, data):
  self.text += data

class seleniumrequest:
 delay=10
 webdriverdict={}
 htmlparser = HTMLFilter()
 def __init__(self,display=True,*drivers):
#  display=False # todelete
  for driver in drivers:
   if driver not in self.webdriverdict:
    chrome_options = Options()
  #  chrome_options.add_argument("--disable-extensions");
#    prefs = {"profile.managed_default_content_settings.images": 2}
#    chrome_options.add_experimental_option("prefs",prefs)
    if not display:
     chrome_options.add_argument("--headless")
#    seleniumrequest.webdriverdict[driver] = webdriver.Chrome(executable_path='/usr/bin/chromedriver',options=chrome_options)
    seleniumrequest.webdriverdict[driver] = webdriver.Chrome(options=chrome_options)
#    seleniumrequest.webdriverdict[driver] = webdriver.Chrome(options=chrome_options)

    '''
    options = FirefoxOptions()
    if not display:
     options.add_argument("--headless")
    options.set_preference("dom.disable_open_during_load", False)
    options.set_preference('dom.popup_maximum', -1)
    options.set_preference("permissions.default.image",2)
    seleniumrequest.webdriverdict[driver] = webdriver.Firefox(executable_path='/usr/bin/geckodriver',options=options)
    '''

    seleniumrequest.webdriverdict[driver].delete_all_cookies()
    seleniumrequest.webdriverdict[driver].set_page_load_timeout(self.delay*12)

 def save_cookie(self, path, drivername):
  """drivername - 'default' or 'linkedin' ..."""
  if not os.path.exists(re.sub(r'(.*/).*$',r'\1',path)):
   os.makedirs(re.sub(r'(.*/).*$',r'\1',path))
  with open(path, 'wb') as filehandler:
   pickle.dump(self.webdriverdict[drivername].get_cookies(), filehandler)

 def load_cookie(self, path, drivername):
  """drivername - 'default' or 'linedin' ..."""
  with open(path, 'rb') as cookiesfile:
   cookies = pickle.load(cookiesfile)
   for cookie in cookies:
    self.webdriverdict[drivername].add_cookie(cookie)

 def getlink(self, url, drivername):
  print(f'seleniumrequest.getlink {drivername=} {url=}')
  count=10
  try:
   self.webdriverdict[drivername].get(url)
  except TimeoutException:
   print(f'timedout {url=}')
   pass
  ht=self.webdriverdict[drivername].execute_script("return document.documentElement.scrollHeight;")
#  while True and count:
  while count:
   count-=1
   prev_ht=self.webdriverdict[drivername].execute_script("return document.documentElement.scrollHeight;")
#   self.webdriverdict[drivername].execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
   [self.webdriverdict[drivername].execute_script("window.scrollTo(0, document.documentElement.scrollHeight*"+str(float(i/5))+");") for i in range(1,6) if not time.sleep(0.5)]
   time.sleep(2)
   ht=self.webdriverdict[drivername].execute_script("return document.documentElement.scrollHeight;")
   print(f'seleniumrequest.getlink {prev_ht=} {ht=}')
   if prev_ht==ht:
    break

 '''
 def wait(self, t_delay=None):
  delay = self.delay if t_delay == None else t_delay
  time.sleep(delay)

 def wait_for_element_ready(self, by, text, drivername):
  """drivername - 'default' or 'linedin' ..."""
  try:
   WebDriverWait(self.webdriverdict[drivername], self.delay).until(EC.presence_of_element_located((by, text)))
  except TimeoutException:
   print("wait_for_element_ready TimeoutException")
   pass
 '''

 def youtubevideolink(self, url=r'https://youtube.com/c/minhinc/videos', drivername='linkedin'):
  """drivername - 'default' or 'linedin' ..."""
  self.getlink(url,drivername)
  for i in range(4):
   print(f'seleniumrequest youtubevideolink wait {i=}')
   self.webdriverdict['linkedin'].execute_script("window.scrollBy(0,2500)")
   time.sleep(2)
#  links=self.webdriverdict[drivername].find_elements_by_xpath('//*[@id="video-title"]')
  links=self.webdriverdict[drivername].find_elements_by_xpath('//*[@id="video-title-link"]')
  for count,link in enumerate(links[:]):
   try:
    print(str(count)+'  '+link.get_attribute("href")+'  '+link.get_attribute("title"))
   except:
    links.remove(link)
  return [(link.get_attribute("href"),link.get_attribute("title")) for link in links]

 def htmltotext(self,html):
  self.htmlparser.feed(html)
  return self.htmlparser.text

 def getcode(self,country):
  if not os.path.exists('data'):
   os.mkdir('data')
  if not os.path.exists('data/country.txt'):
   self.getlink(r'http://witheveryone.angelfire.com/country.txt','linkedin')
   with open('data/country.txt','w') as file:
    file.write(self.webdriverdict['linkedin'].page_source)
  return re.sub('.*?#'+country+r'\s+[.](.*?)\s.*$',r'\1',self.htmltotext(open('data/country.txt').read()),flags=re.DOTALL|re.I)

 def email(self,text):
#  print('><seleniumrequest.email')
#  open('emailsource.txt','w').write(text)
#  return re.findall(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,6}\b",text)
  retval=[x.lower() for x in re.findall(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,6}\b",text) if not re.search(r'(\.{2,}|@\.|\.@)',x)]
  print(f'seleniumrequest.email {retval=}')
  return retval if len(retval) < 40 else []

 def pruneline(self,line):
  return re.sub(r'\s+[&,-:;.@#$%^*!]+','',line)

 @staticmethod
 def close(logout=True):
  for x in seleniumrequest.webdriverdict:
   if x=='linkedin' and logout:
#    if not re.search(r'linkedin.com',seleniumrequest.webdriverdict['linkedin'].current_url,flags=re.I):
    seleniumrequest.webdriverdict['linkedin'].get(r'https://www.linkedin.com')
    time.sleep(seleniumrequest.delay)
    seleniumrequest.webdriverdict['linkedin'].maximize_window()
    seleniumrequest.webdriverdict['linkedin'].find_element_by_xpath("//button[contains(@class,'global-nav__primary-link')][contains(.,'Me')]").click()
    time.sleep(1)
    seleniumrequest.webdriverdict['linkedin'].find_element_by_xpath('//a[@href="/m/logout/"]').click()
#    seleniumrequest.webdriverdict['linkedin'].find_element_by_xpath("//a[@class='global-nav__secondary-link mv1']").click()
    time.sleep(seleniumrequest.delay*2)
   seleniumrequest.webdriverdict[x].quit()
