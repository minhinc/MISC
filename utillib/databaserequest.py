import os,re
import time
import datetime
import uuid
import sys;sys.path.append(os.path.expanduser('~')+r'/tmp')
from MISC.utillib.util import utilcm
from MISC.utillib.database import databasecm
#import databasem
from MISC.utillib.machinelearningrequest import machinelearningrequestcm

class databaserequestc:
 expiredayc=60
# db=databasem.databasec(False)
 dbc=databasecm
 if not databasecm.conn:
  print(f'databaserequest.__init__ database could not be connected')
  sys.exit(-1)
 databasecm.search2('linkvisited','date','<',re.sub(r'-','',(datetime.date.today()-datetime.timedelta(days=expiredayc)).isoformat()),mode='delete')
 DELIMITER=utilcm.kwargc['delimiter']
 junkemail=r'^(?:'+(''.join([x[0]+'|' for x in databasecm.search2('junkemail','name','name','R','.*',mode='get')]))[:-1]+')$'
# junkextn=r'^(?:'+(''.join([x[0]+'|' for x in db.get('junkextension')]))[:-1]+')$'
 junkextn=r'^(?:.*[.]7z.*|.*[.]aspx$|.*[.]cms$|.*[.]cp*?$|.*[.]doc.*|.*[.]ece.*|.*[.]cgi.*|.*[.]hotels[.]com.*|.*[./]jobs?[./].*|.*[.]indeed[.].*|.*[.]php$|.*[.]ppt.*|.*[.]rar.*|.*[.]txt.*|.*[.]xls.*|.*[.]xml.*|.*[.]zip.*|.*\bbz\b.*|.*\bpdf\b.*)$'

 def __init__(self,**kwarg):
  super(databaserequestc,self).__init__()

 def mutelink(self,link):
  return re.sub(r'[^a-zA-Z0-9._%-]','_',link)

 def validlink(self,j): #returns bool
  return not re.search(self.junkextn,j,flags=re.I) and (not databasecm.search2('linkvisited','name','=',self.mutelink(j),mode='search') or databasecm.search2('linkvisited','name','=',self.mutelink(j),'date','<',re.sub(r'-','',(datetime.date.today()-datetime.timedelta(days=self.expiredayc)).isoformat()),mode='search'))

 def linkupdatebulk(self,j):
#  print(f'linkupdatebulk {j=}')
  databasecm.search2('linkvisited',*[(self.mutelink(x),re.sub('-','',datetime.date.today().isoformat())) for x in j],mode='insertbulk')

 def linkupdate(self,j,checkupdate=True):
  retval=True
  if not databasecm.search2('linkvisited','name','=',self.mutelink(j),mode='search'):
   databasecm.search2('linkvisited',self.mutelink(j),re.sub('-','',datetime.date.today().isoformat()),mode='insert')
  elif checkupdate and databasecm.search2('linkvisited','name','=',self.mutelink(j),'date','<',re.sub('-','',(datetime.date.today()-datetime.timedelta(days=self.expiredayc)).isoformat()),mode='search') or not checkupdate:
   databasecm.search2('linkvisited','date',re.sub('-','',datetime.date.today().isoformat()),'name','=',self.mutelink(j),mode='update')
  else:
   retval=False
  '''
  elif checkupdate and databasecm.search2('linkvisited','name','=',self.mutelink(j),'date','<',re.sub('-','',(datetime.date.today()-datetime.timedelta(days=self.expiredayc)).isoformat()),mode='search'):
   databasecm.search2('linkvisited','date',re.sub('-','',datetime.date.today().isoformat()),'name','=',self.mutelink(j),mode='update')
  else:
   databasecm.search2('linkvisited','date',re.sub('-','',datetime.date.today().isoformat()),'name','=',self.mutelink(j),mode='update')
  '''
  return retval

 def googlelink(self,j): #takes company name
#  return r'https://www.google.com/search?q='+re.sub(r'\s+','+',j)+r'&btnG=Search'
  return r'https://www.google.com/search?q='+re.sub(r'\s+','+',j)

 def appendjunkextensions(self,weburl,trimurl=False):
  if trimurl:
   weburl=re.sub(r'(?:^|$)',r'.*',re.sub(r'[.]',r'[.]',re.sub(r'(?:https?://)?(?:www[.])?(.*?)(?:/.*|$)',r'\1',weburl)))
  self.junkextn=re.sub(r'\)\$',r'|'+weburl+r')$',self.junkextn) if not re.search(r'\^\(\?:\)\$',self.junkextn) else re.sub(r'\)\$',weburl+r')$',self.junkextn)
  print(f'<>databaserequestc.appendjunkextensions {self.junkextn=}')
import MISC.utillib.util;MISC.utillib.util.cmc(__name__,MISC.utillib.util.mce(__name__,databaserequestc) or databaserequestc())
