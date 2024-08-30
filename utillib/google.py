import sys;sys.path.append('/home/minhinc/tmp')
from selenium.webdriver.common.keys import Keys
from MISC.utillib.util import utilcm,print
from MISC.utillib.seleniumrequest import seleniumrequestcm
from MISC.utillib.databaserequest import databaserequestcm
from MISC.utillib.machinelearningrequest import machinelearningrequestcm
import datetime
import re,os,uuid,time
from unidecode import unidecode

class googlec:
 def __init__(self):
  super(googlec,self).__init__()


 def get(self,urld):
  print(f'E google get {urld=}')
  for x in urld.values():
   for count,j in enumerate(range(2,len(x))):
    """
    seleniumrequestcm.getlinkdata(url=dict(pagecount=1,link=databaserequestcm.googlelink(x[j]+' '+x[0]+' '+x[1]),selenium=True))
    '''
    print('google.get --saving page source--')
    open('rest.html','w').write(self.webdriverdict[self.LOGIN].page_source)
    '''
    urllink=[re.sub(r'(.*linkedin[.].*?/company/[a-zA-Z0-9-]+).*',r'\1',ii.get_attribute('href'),flags=re.I) for ii in seleniumrequestcm.getdriver().find_elements_by_xpath("//div[@class='yuRUbf']//a[@jsname='UWckNb']") if databaserequestcm.linkupdate(ii.get_attribute('href'),checkupdate=True) and (not re.search(r'[.]\w+$',ii.get_attribute('href')) or re.search(r'[.](html|htm|php|cgi)$',ii.get_attribute('href')))]
    """
    urllink=[yy for xx in seleniumrequestcm.getlinkdata(url=["'"+databaserequestcm.googlelink(x[j]+' '+x[0]+' '+x[1])+('' if not ii else fr'&start={ii*20}')+"'" for ii in range(2)]).values() for yy in re.findall(r'q=(https?.*?)(?=&)',xx,flags=re.I) if not re.search('(support|accounts)[.]google[.]com',yy,flags=re.I)] 
    print(f'M googlec.get google urlink recevied {urllink=}')
#    urllink=[re.sub(r'(.*linkedin[.].*?/company/[a-zA-Z0-9-]+).*',r'\1',ii,flags=re.I) for ii in urllink if databaserequestcm.linkupdate(ii,checkupdate=True) and (not re.search(r'[.]\w+$',ii) or re.search(r'[.](html|htm|php|cgi)$',ii))]
    urllink=[re.sub(r'(.*linkedin[.].*?/company/[a-zA-Z0-9-]+).*',r'\1',ii,flags=re.I) for ii in urllink if not re.search(r'[.]\w+$',ii) or re.search(r'[.](html|htm|php|cgi)$',ii)]
    print(f'M googlec.get google links to be fetched 1 {urllink=}')
    urllink=[dict(link=xx,selenium=True,pagecount=1,postfunc=seleniumrequestcm.email) if re.search('https?://(\w+[.])?linkedin',xx,flags=re.I) and not re.search('job',xx,flags=re.I) and not utilcm.getarg('--nolinkedin',removearg=False) else dict(link=xx,postfunc=seleniumrequestcm.email) for count,xx in enumerate(urllink) if not [y for y in urllink[count+1:] if re.sub(r'.*/company/(.*)',r'\1',xx)==re.sub(r'.*/company/(.*)',r'\1',y)]]
    print(f'M googlec.get google links to be fetched 2 {urllink=}')
#    email=machinelearningrequestcm.getmatching(x[j],*set([z for y in seleniumrequestcm.getlinkdata(url=urllink) for z in seleniumrequestcm.email(y)]),email=True,percent=60,muteprint=True)[0:4]
    email=machinelearningrequestcm.getmatching(x[j],*set([yy for xx in seleniumrequestcm.getlinkdata(url=urllink).values() for yy in utilcm.getlist(xx) if yy]),email=True,percent=60,muteprint=True)[0:4]
    print(f'I ###########\ngoogle.get {count+1}/{len(x)-1} {x[j]=} {email=}\n#############')
    databaserequestcm.dbc.search2('company',0,unidecode(x[j]),mode='insert') if not databaserequestcm.dbc.search2('company','name','=',unidecode(x[j]),mode='search') else None
    databaserequestcm.dbc.search2('track',*[(z,str(uuid.uuid4()),databaserequestcm.dbc.search2('company','id','name','=',unidecode(x[j]),mode='get')[0][0],databaserequestcm.dbc.search2('tech','id','name','=',x[0],mode='get')[0][0],databaserequestcm.dbc.search2('country','id','name','R','^'+x[1]+r'.*',mode='get')[0][0],re.sub(r'-','',(datetime.date.today()-datetime.timedelta(days=databaserequestcm.expiredayc)).isoformat()),0,0) for z in email],mode='insertbulk')

  '''
  print(f'I google.get ######### CHECKING EMAIL VALIDITY ###########')
  seleniumrequestcm.getdriver().get('https://email-checker.net')
#  seleniumrequestcm.getdriver().switch_to.window(self.webdriverdict[self.LOGIN].window_handles[0]) if len(self.webdriverdict[self.LOGIN].window_handles)>1 else None
  for i in databaserequestcm.dbc.search2('track','email','date','<=',re.sub(r'-','',(datetime.date.today()-datetime.timedelta(days=databaserequestcm.expiredayc)).isoformat()),mode='get'):
   seleniumrequestcm.getdriver().find_element_by_xpath('//input[@type="email"]').clear()
   seleniumrequestcm.getdriver().find_element_by_xpath('//input[@type="email"]').send_keys(i[0])
   seleniumrequestcm.getdriver().find_element_by_xpath('//button[@type="submit"]').send_keys(Keys.RETURN)
   time.sleep(2)
   while True:
    try:
     if not re.search('span.*green',seleniumrequestcm.getdriver().find_element_by_xpath('//div[@class="summary"]//h2').get_attribute("innerHTML"),flags=re.I):
#      databaserequestcm.dbc.search2('track','email','=',i[0],mode='delete')
      print(f'I google.get deleted email {i[0]=}')
     else:
      print(f'I google.get email validity passed {i=}')
    except Exception as ec:
     print(f'C google.get exception raised {i=} {ec=}')
     time.sleep(5)
    else:
     break
  '''
import MISC.utillib.util;MISC.utillib.util.cmc(__name__,MISC.utillib.util.mce(__name__,googlec) or googlec())
