import sys;sys.path.append('/home/minhinc/tmp')
from MISC.utillib.util import *
from MISC.extra.openglutil import openglutilcm
from selenium.webdriver.common.keys import Keys
from unidecode import unidecode
from .seleniumrequest import seleniumrequestcm
from .databaserequest import databaserequestcm
from .machinelearningrequest import machinelearningrequestcm
import re,time

class linkedinc:
 def __init__(self):
  super(linkedinc,self).__init__()
  '''
  import signal
  self.exit=Event()
  for sig in ('TERM','HUP','INT'):
   signal.signal(getattr(signal,'SIG'+sig),lambda m,n:self.exit.set())
  '''

 def get(self,*,tech,country,pagecount):
  if not 'linkedin' in seleniumrequestcm.driverdc:
   print(f'I linkedin.get Linked login is proceeding...')
   seleniumrequestcm.getdriver('linkedin',headlessb=utilcm.getarg('--headless'))
   seleniumrequestcm.getlinkdata(url=builtins.dict(link=r'https://www.linkedin.com/login',selenium=True))
   seleniumrequestcm.getdriver().find_element_by_id('username').send_keys('tominhinc@gmail.com')
   seleniumrequestcm.getdriver().find_element_by_id('password').send_keys('pinku76li')
   seleniumrequestcm.getdriver().find_element_by_id('password').send_keys(Keys.RETURN)
   #  if re.search('The login attempt seems suspicious. To finish signing in please enter the verification code we sent to your email address.',seleniumrequestcm.getdriver('createcompany').page_source,flags=re.I|re.DOTALL):
   if re.search('suspicious.*verification.*code.*email.*address',seleniumrequestcm.getdriver('createcompany').page_source,flags=re.I|re.DOTALL):
    print(f'M createcompany.__init__ verification code page detected, and sleeping for 60 seconds...')
    time.sleep(60)
    '''
    print(f'M createcompany.__init__, press ctrl+C to continue or wait for 2min(s)...')
    self.exit.wait(120)
    '''
   for i in range(pagecount):
    seleniumrequestcm.getlinkdata(url=dict(selenium=True,pagecount=0,link='https://www.linkedin.com/jobs/search/?keywords='+('C%2B%2B' if tech=='c++' else 'python' if tech=='py' else 'opengl' if tech=='gl' else 'kivy' if tech=='kv' else 'Machine%20Learning' if tech=='ml' else tech)+'&location='+re.sub(r'\s','%20',country)+(f'&start={i*25}' if i else '')))
    utilcm.print(f'M {i*25} -> {(i+1)*25}')
    [seleniumrequestcm.getdriver().execute_script('arguments[0].scrollTop = arguments[0].scrollHeight*'+str(float(j/25)), seleniumrequestcm.getdriver().find_element_by_css_selector("div.jobs-search-results-list")) for j in range(1,26) if not time.sleep(0.25)]
    return [unidecode(seleniumrequestcm.pruneline(ii.text)) for ii in seleniumrequestcm.getdriver().find_elements_by_xpath("//div[@class='artdeco-entity-lockup__subtitle ember-view']/span")]

class createcompanyc:
 def __init__(self,*arg,**kwarg):
  super(createcompanyc,self).__init__()
  self.client=[]
  if 'client' in kwarg:
   self.client=kwarg[client]

 def get(self):
  '''it would parse sys.argv for --tech variables add --company to sys.argv (not pretty though!)'''
  print(f'D createcompany.get {sys.argv=}')
  for x in [list(x) for x in openglutilcm.getbuffer(utilcm.getarg('--tech',count=-1) or [],0,3,3)]:
   x[0]=machinelearningrequestcm.getmatching(x[0],*[y[0] for y in databaserequestcm.dbc.search2('tech','name',mode='get')],muteprint=True)[0]
   x[1]=machinelearningrequestcm.getmatching(x[1],*[re.sub(r'^(.*)\s+[.]\w+\s*$',r'\1',y[0]) for y in databaserequestcm.dbc.search2('country','name',mode='get')],muteprint=True)[0] if not re.search(r'(^http|@)',x[1]) else x[1]
   sys.argv.append('--company' if not utilcm.getarg('--company',count=1,remove=False) else '\n')
   sys.argv.extend([self.client[i].get(tech=x[0],country=x[1],pagecount=x[2]) for i in range(len(self.client))])
   utilcm.print(f'I new {sys.argv=}')
import MISC.utillib.util;MISC.utillib.util.cmc(__name__,MISC.utillib.util.mce(__name__,createcompanyc) or createcompanyc(client=linkedin()))
