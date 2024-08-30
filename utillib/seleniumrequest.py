from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
'''
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.proxy import Proxy, ProxyType
'''
from selenium.webdriver.chrome.options import Options
import threading
import concurrent.futures
import codecs
import os,sys,time,re;sys.path.append(os.path.expanduser('~')+'/tmp')
import traceback
from html.parser import HTMLParser
from MISC.utillib.util import utilcm,print
import MISC.utillib.request

#from selenium.webdriver.firefox.options import Options as FirefoxOptions

class HTMLFilter(HTMLParser):
 text = ""
 def handle_data(self, data):
  self.text += data

class seleniumrequestc:
 driverdc={}
 lastloginsc=None
 htmlparserc = HTMLFilter()
 lockc=None

 def __init__(self,**kwarg):
  print(f'E selenium.request.__init__ {self.driverdc=}')
#   traceback.print_stack()
  if seleniumrequestc.lockc==None:
   seleniumrequestc.lockc=threading.Lock()

 def getdriver(self,logins='',headlessb=False):
  if logins=='':
   if self.lastloginsc==None:
    print(f'C logins is empty string whereas there is not lastlogin, exiting...')
    sys.exit(-1)
   logins=self.lastloginsc
  if not logins in self.driverdc:
   chrome_options = Options()
   '''
   chrome_options.add_argument('--blink-settings=imagesEnabled=false')
   chrome_options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
   '''
   chrome_options.page_load_strategy = 'eager'
   if headlessb:
    chrome_options.headless = True
   seleniumrequestc.driverdc[logins or None] = webdriver.Chrome(options=chrome_options)
   seleniumrequestc.lastloginsc=logins or None
   print(f'I seleniumrequestc.getdriver new driver {seleniumrequestc.driverdc=} {seleniumrequestc.lastloginsc=}')
   traceback.print_stack()

  return self.driverdc[logins]

 def getconsolelink(self,urld,**kwarg):
  print(f'E selenium.getconsolelink {urld=} {kwarg=}')
#  return os.popen('lynx -dump '+url['link']).read()
#  data=os.popen('lynx -dump '+urld['link']).read()
  stream=os.popen('lynx -dump '+urld['link'])
  stream._stream.reconfigure(encoding='latin', newline="") # Now the stream is configured in the encoding 'latin'
  data=stream.read()
  data+=MISC.utillib.request.gets(urld['link'],get=True,retrycount=2)
  if 'postfunc' in urld:
   data=urld['postfunc'](data)
   print(f'I seleniumrequestc.getconsole {urld["link"]=} {data=}') if data else None
  return data

 def getlinkdata(self,*,url,**kwarg):
  '''url='http://msn.com','http://msn.com','http://doodle.com' '''
  print(f'E seleniumrequest.getlinkdata {(url,kwarg)=}')
  urld=utilcm.getdict(url)
  print(f'M seleniumrequest.getlinkdata {urld=}')
  if not len(urld):
   print(f'I seleniumrequest.getlinkdata url empty returning')
   return {}
  future_to_url={}
  executor=concurrent.futures.ThreadPoolExecutor(max_workers=len(urld))
  #todelete
  print(f'D ',f'{type(urld[0])=} {type(urld[0])==dict=} {urld[0]=}')
  future_to_url={(executor.submit(self.getconsolelink,x,**kwarg) if not 'selenium' in x else executor.submit(self.getlink,x,**kwarg)):count for count,x in enumerate([dict(link=x) if not type(x)==dict else x for x in urld.values()])}
  try:
   for future in concurrent.futures.as_completed(future_to_url,timeout=30 if not [xx for xx in url if 'selenium' in xx] else None):
    try:
     data=future.result()
    except Exception as exc:
     print(f'I selenium.getlinkdata exception generated for {urld[future_to_url[future]]=} {exc=} {type(exc)=}')
     urld[future_to_url[future]]=None
    else:
     urld[future_to_url[future]]=data
  except Exception as exc:
   print(f'C seleniumrequestc.getlinkdata as_completed exception {exc=} {type(exc)=}')
   [xx.cancel() if xx.running() else None for xx in future_to_url]
   for xx in range(len(urld)):
    urld[xx]=None if not type(urld[xx])==list and not type(urld[xx])==tuple else urld[xx]
#  print(f'D seleniumrequest.getlinkdata {urld=}')
  return urld

 def getlink(self, urld, **kwarg):
  '''pagecount=-1 -> get single page without scrolling
               0 -> get single compalete page
               >=1 ->get multiple page with scrolling (not complete page)'''
  print(f'E seleniumrequest.getlink {(urld,kwarg)=}')
  self.lockc.acquire()
  print(f'M seleniumrequest.getlink lock acquired {urld=} {self.lockc.locked()=}')
  try:
   self.getdriver().get(urld['link'])
   urld['pagecount']=-1 if not 'pagecount' in urld else urld['pagecount']
   while urld['pagecount']>=0:
    prev_ht=self.getdriver().execute_script("return document.documentElement.scrollHeight;")
    [self.getdriver().execute_script("window.scrollTo(0, document.documentElement.scrollHeight*"+str(float(i/5))+");") for i in range(1,6) if not time.sleep(0.5)]
    time.sleep(2)
    ht=self.getdriver().execute_script("return document.documentElement.scrollHeight;")
    print(f"M seleniumrequest.getlink {prev_ht=} {ht=} {urld['pagecount']=}")
    if urld['pagecount']==1 or urld['pagecount']==0 and prev_ht==ht:
     break
    urld['pagecount']-=1 if urld['pagecount']!=0 else 0
  except Exception as exc:
   print(f'C seleniumrequestc.getlink exception {urld["link"]=} {exc=} {type(exc)=}')
  finally:
   self.lockc.release()
  print(f'O seleniumrequest.getlink lock released {urld=} {self.lockc.locked()=}')
#  return self.getdriver().page_source
  data=self.getdriver().page_source
  if 'postfunc' in urld:
   data=urld['postfunc'](data)
   print(f'I seleniumrequest.getlink {urld["link"]=} {data=}') if data else None
  return data

 def youtubevideolink(self, url=r'https://youtube.com/c/minhinc/videos'):
  if self.lastloginsc==None:
   self.getdriver('default')
  self.getlinkdata(url=dict(link=url,selenium=True,pagecount=0))
  for i in range(4):
   print(f'M seleniumrequest youtubevideolink wait {i=}')
   self.getdriver().execute_script("window.scrollBy(0,2500)")
   time.sleep(2)
#  links=self.webdriverdict[drivername].find_elements_by_xpath('//*[@id="video-title"]')
  links=self.getdriver().find_elements_by_xpath('//*[@id="video-title-link"]')
  for count,link in enumerate(links[:]):
   try:
    print('M ',str(count)+'  '+link.get_attribute("href")+'  '+link.get_attribute("title"))
   except:
    links.remove(link)
  return utilcm.getdict([(link.get_attribute("href"),link.get_attribute("title")) for link in links])

 def execute_script(self,login=None,tabcount=0,scriptstr=None,url=None):
  print(f'E excute_script {login=} {tabcount=} {scriptstr=} {url=} {self.lock.locked()=} {len(self.webdriverdict[self.login].window_handles)=}')
#  print(f'><seleniumrequest.execute_script {(loginid,tabcount,scriptstr,url)=}')
  self.lock.acquire() if len(self.webdriverdict[self.login].window_handles)>1 else None
  print(f'M excute_script post lock acquire {self.lock.locked()=}')
  self.webdriverdict[login].switch_to.window(self.webdriverdict[login].window_handles[tabcount]) if len(self.webdriverdict[self.login].window_handles)>1 else None
  retval=self.webdriverdict[login].execute_script(scriptstr) if scriptstr else None
  retval=self.webdriverdict[login].get(url) if url else retval
  print(f'M excute_script pre lock release {self.lock.locked()=}')
  self.lock.release() if len(self.webdriverdict[self.login].window_handles)>1 else None
  print(f'O excute_script {scriptstr=} {url=} {login=} {tabcount=} {retval=} {self.lock.locked()=}')
  return retval

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
#  print(f'seleniumrequest.email {retval=}')
  return retval if len(retval) < 40 else []

 def pruneline(self,line):
  return re.sub(r'\s+[&,-:;.@#$%^*!]+','',line)

 @staticmethod
 def close(logout=True):
  for x in seleniumrequest.webdriverdict:
   if x=='linkedin' and logout:
#    if not re.search(r'linkedin.com',seleniumrequest.webdriverdict['linkedin'].current_url,flags=re.I):
    seleniumrequest.webdriverdict['linkedin'].get(r'https://www.linkedin.com')
    time.sleep(seleniumrequest.DELAY)
    seleniumrequest.webdriverdict['linkedin'].maximize_window()
    seleniumrequest.webdriverdict['linkedin'].find_element_by_xpath("//button[contains(@class,'global-nav__primary-link')][contains(.,'Me')]").click()
    time.sleep(1)
    seleniumrequest.webdriverdict['linkedin'].find_element_by_xpath('//a[@href="/m/logout/"]').click()
#    seleniumrequest.webdriverdict['linkedin'].find_element_by_xpath("//a[@class='global-nav__secondary-link mv1']").click()
    time.sleep(seleniumrequest.DELAY*2)
   seleniumrequest.webdriverdict[x].quit()

import MISC.utillib.util;MISC.utillib.util.cmc(__name__,MISC.utillib.util.mce(__name__,seleniumrequestc) or seleniumrequestc())
