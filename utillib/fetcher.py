import threading
from unidecode import unidecode
from seleniumrequest import seleniumrequest
from databaserequest import databaserequest
from machinelearningrequest import machinelearningrequest
import MISC.utillib.requestm as requestm
from MISC.utillib.util import Util
import datetime,re,uuid

class fetcher(seleniumrequest,databaserequest,machinelearningrequest):
 def __init__(self,display=True):
  super(fetcher,self).__init__(display,'linkedin')
  self.linkedinurl=[]
  self.linkedinemail=[]
  self.thread=threading.Thread(target=self.getlinkedin)
  self.threadcondition=threading.Condition()
  self.threadevent=threading.Event()
  self.thread.start()

 def get(self,i,file,companyname=None):
  """uRl
  get("companyx france",r"http://lotusinc.com/","companyy nigeria",r"http://asadtech.com/")"""
  email=[]
  getsdata=None
  [i.append(re.sub(r'/*$',r'',x)+r'/about') for x in i[:] if re.search(r'youtube[.]com',x,flags=re.I) and not re.search(r'/watch\?',x,flags=re.I) and not re.search(r'youtube[.]com.*/about',x,flags=re.I)]
  print(f'{"###########fetcher.get###############":^100}\n{i=!r:^100}')
  self.threadcondition.acquire()
  self.linkedinemail=[]
  self.linkedinurl=[x for x in i[1:] if re.search(r'^https?://.*linkedin.com/',x,flags=re.I)]
  self.companyname=companyname
  self.threadcondition.notify()
  self.threadcondition.release()
  for j in [x for x in i[1:] if re.search(r'^https?://',x,flags=re.I) and not re.search(r'^https:?//.*linkedin.com/',x,flags=re.I)]:
   if re.search(self.junkextn,j,flags=re.I):
    continue
   getsdata=requestm.gets(j,get=True,retrycount=2)
   self.appendjunkextensions(j,trimurl=True) if getsdata[1]==0 else None
   email.extend(set([x for x in self.email(getsdata[0]) if not re.search(self.junkemail,x,flags=re.I)]))
  print(f'------ main thread waiting..')
  self.threadcondition.acquire()
  self.linkupdatebulk(list([self.googlelink(re.split(self.DELIMITER,i[0])[0])])+i[1:])
  email.extend(set(self.linkedinemail))
#  email=[x for x in self.getmatching(re.split(self.DELIMITER,i[0])[0],*email,email=True,percent=self.EXPIREDAY) if not self.db.search2('track','email','=',x,mode='search')] if len(email) else []
  email=[x for x in self.getmatching(re.split(self.DELIMITER,i[0])[0],*email,email=True,percent=60) if not self.db.search2('track','email','=',x,mode='search')] if len(email) else []
  file.write(' '.join(re.split(self.DELIMITER,i[0]))+' '+' '.join(email[:4])+' #'+' '.join(email[4:])+'\n')
  file.flush()
  print(f'fetcher.get <>{email[:4]}')
#  self.db.search2('company',0,Util.converttolatin1(re.split(self.DELIMITER,i[0])[0]),mode='insert') if not self.db.search2('company','name','=',Util.converttolatin1(re.split(self.DELIMITER,i[0])[0]),mode='search') else None
  self.db.search2('company',0,unidecode(re.split(self.DELIMITER,i[0])[0]),mode='insert') if not self.db.search2('company','name','=',unidecode(re.split(self.DELIMITER,i[0])[0]),mode='search') else None
  if len(email):
#   emaildata=(str(uuid.uuid4()),self.db.search2('company','id','name','=',re.split(self.DELIMITER,i[0])[0].encode('utf-8').decode('unicode_escape'),mode='get')[0][0],self.db.search2('tech','id','name','=',re.split(self.DELIMITER,i[0])[1],mode='get')[0][0],101,self.db.search2('country','id','name','=',re.split(self.DELIMITER,i[0])[2],mode='get')[0][0],re.sub('-','',(datetime.date.today()-datetime.timedelta(days=60)).isoformat()),0,0)
#   emaildata=(self.db.search2('company','id','name','=',Util.converttolatin1(re.split(self.DELIMITER,i[0])[0]),mode='get')[0][0],self.db.search2('tech','id','name','=',re.split(self.DELIMITER,i[0])[1],mode='get')[0][0],self.db.search2('country','id','name','=',re.split(self.DELIMITER,i[0])[2],mode='get')[0][0],re.sub('-','',(datetime.date.today()-datetime.timedelta(days=60)).isoformat()),0,0)
   emaildata=(self.db.search2('company','id','name','=',unidecode(re.split(self.DELIMITER,i[0])[0]),mode='get')[0][0],self.db.search2('tech','id','name','=',re.split(self.DELIMITER,i[0])[1],mode='get')[0][0],self.db.search2('country','id','name','=',re.split(self.DELIMITER,i[0])[2],mode='get')[0][0],re.sub('-','',(datetime.date.today()-datetime.timedelta(days=60)).isoformat()),0,0)
#   self.db.search2('track',*[(x,*emaildata) for x in email[0:4]],mode='fillbulk')
   self.db.search2('track',*[(x,str(uuid.uuid4()),*emaildata) for x in email[0:4]],mode='insertbulk')
  self.threadcondition.release()
  self.threadevent.wait()
  self.threadevent.clear()
#  print(f'thread event waited')
  return self.companyname

 def getlinkedin(self):
  removelist=[]
  while True:
   self.threadcondition.acquire()
   print(f'--------waiting')
   self.threadcondition.wait()
   print(f'--------waited')
   if not self.linkedinurl and not type(self.linkedinurl)==list:
    self.threadcondition.release()
    break;
   for j in self.linkedinurl:# if re.search(r'^https?://.*linkedin.com/',x,flags=re.I)]:
    if not j in removelist:
     self.getlink(j,'linkedin') if re.search('linkedin.com',j,flags=re.I) else None
     if re.search(r'linkedin.com/company/\d+?/*$',j):
      [removelist.append(x) for x in self.linkedinurl[self.linkedinurl.index(j)+1:] if re.sub(r'.*/company/(.*?)/*$',r'\1',x,flags=re.I)==re.sub(r'.*/company/(.*?)/*$',r'\1',self.webdriverdict['linkedin'].current_url,flags=re.I)]
      print(f'fetcher {removelist=}')
     self.linkedinemail.extend([x for x in self.email(self.webdriverdict['linkedin'].page_source) if not re.search(self.junkemail,x,flags=re.I)])
   removelist=[]
   self.threadcondition.release()
   self.getlink(self.googlelink(re.split(self.DELIMITER,self.companyname)[0]+' '+self.getmatching(re.split(self.DELIMITER,self.companyname)[2],*re.findall(r'^.*?#(.*)?\s+[.]\w{2}',open('data/country.txt').read(),flags=re.M),muteprint=True)[0]),'linkedin') if self.companyname else None
#   print(f'------ waiting2 acaure {self.companyname=}')
   self.threadcondition.acquire()
   self.companyname=[x for x in set([re.sub(r'^(.*?)/+$',r'\1',x.get_attribute('href')) for x in self.webdriverdict['linkedin'].find_elements_by_xpath("//div[@class='yuRUbf']/a[1]")]) if self.validlink(x)] if self.companyname else []
   self.threadcondition.release()
   self.threadevent.set()
#   print(f'------ threadevent set')
  print(f'threading getting out')


 def quitthread(self):
  print(f'><fetcher.quitthread')
  self.threadcondition.acquire()
  self.linkedinurl=None
  self.threadcondition.notify()
  self.threadcondition.release()
  self.thread.join()
  print(f'<>fetcher.quitthread')
