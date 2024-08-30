import builtins
import sys;sys.path.append('/home/minhinc/tmp')
from MISC.utillib.util import *
from MISC.extra.openglutil import openglutilcm
from selenium.webdriver.common.keys import Keys
from unidecode import unidecode
from .seleniumrequest import seleniumrequestcm
from .databaserequest import databaserequestcm
from .machinelearningrequest import machinelearningrequestcm
import re,time
#from threading import Event

class linkedinc:
 def __init__(self):
  super(linkedinc,self).__init__()
  '''
  import signal
  self.exit=Event()
  for sig in ('TERM','HUP','INT'):
   signal.signal(getattr(signal,'SIG'+sig),lambda m,n:self.exit.set())
  '''

 def get(self):
  '''it would parse sys.argv for --tech variables'''
  print(f'D linkedin.get {sys.argv=}')
  urltmp=dict()
  for x in [list(x) for x in openglutilcm.getbuffer(utilcm.getarg('--tech',count=-1) or [],0,3,3)]:
   if seleniumrequestcm.lastloginsc!='linkedin':
    print(f'I linkedin.get Linked login is proceeding...')
    seleniumrequestcm.getdriver('linkedin',headlessb=utilcm.getarg('--headless'))
    seleniumrequestcm.getlinkdata(url=builtins.dict(link=r'https://www.linkedin.com/login',selenium=True))
    seleniumrequestcm.getdriver().find_element_by_id('username').send_keys('tominhinc@gmail.com')
    seleniumrequestcm.getdriver().find_element_by_id('password').send_keys('pinku76li')
    seleniumrequestcm.getdriver().find_element_by_id('password').send_keys(Keys.RETURN)
  #  if re.search('The login attempt seems suspicious. To finish signing in please enter the verification code we sent to your email address.',seleniumrequestcm.getdriver('linkedin').page_source,flags=re.I|re.DOTALL):
    if re.search('suspicious.*verification.*code.*email.*address',seleniumrequestcm.getdriver('linkedin').page_source,flags=re.I|re.DOTALL):
     print(f'M linkedin.__init__ verification code page detected, and sleeping for 60 seconds...')
     time.sleep(60)
     '''
     print(f'M linkedin.__init__, press ctrl+C to continue or wait for 2min(s)...')
     self.exit.wait(120)
    '''
   x[0]=machinelearningrequestcm.getmatching(x[0],*[y[0] for y in databaserequestcm.dbc.search2('tech','name',mode='get')],muteprint=True)[0]
   x[1]=machinelearningrequestcm.getmatching(x[1],*[re.sub(r'^(.*)\s+[.]\w+\s*$',r'\1',y[0]) for y in databaserequestcm.dbc.search2('country','name',mode='get')],muteprint=True)[0] if not re.search(r'(^http|@)',x[1]) else x[1]
   print(f'D linkedin.get new {x=}')
   for i in range(int(x[2])):
    seleniumrequestcm.getlinkdata(url=builtins.dict(selenium=True,pagecount=0,link='https://www.linkedin.com/jobs/search/?keywords='+('C%2B%2B' if x[0]=='c++' else 'python' if x[0]=='py' else 'opengl' if x[0]=='gl' else 'kivy' if x[0]=='kv' else 'Machine%20Learning' if x[0]=='ml' else x[0])+'&location='+re.sub(r'\s','%20',x[1])+(f'&start={i*25}' if i else '')))
    with open('test.html','w') as f:
     f.write(seleniumrequestcm.getdriver().page_source)
    print(f'M fetching page count {i+1} {i*25} -> {(i+1)*25}')
    [seleniumrequestcm.getdriver().execute_script('arguments[0].scrollTop = arguments[0].scrollHeight*'+str(float(j/25)), seleniumrequestcm.getdriver().find_element_by_css_selector("div.jobs-search-results-list")) for j in range(1,26) if not time.sleep(0.25)]
    for ii in seleniumrequestcm.getdriver().find_elements_by_xpath("//div[@class='artdeco-entity-lockup__subtitle ember-view']/span"):
     x.append(unidecode(seleniumrequestcm.pruneline(ii.text)))
#      print(f'{type(x)=} {x=}')
   urltmp.append(x[:2]+list(set(x[3:])))
   print(f'I linkedin.get {urltmp=}')
  return urltmp.copy()
import MISC.utillib.util;MISC.utillib.util.cmc(__name__,MISC.utillib.util.mce(__name__,linkedinc) or linkedinc())
