import os,re
import time
import datetime
import uuid
import sys;sys.path.append(os.path.expanduser('~')+r'/tmp')
#import MISC.utillib.databasem as databasem
from MISC.utillib.util import Util
import databasem
from machinelearningrequest import machinelearningrequest

class databaserequest:
 EXPIREDAY=60
 db=databasem.databasec(False)
 if not db.conn:
  print(f'databaserequest.__init__ database could not be connected')
  sys.exit(-1)
 db.search2('linkvisited','date','<',re.sub(r'-','',(datetime.date.today()-datetime.timedelta(days=EXPIREDAY)).isoformat()),mode='delete')
 DELIMITER=Util.DELIMITER
 junkemail=r'^(?:'+(''.join([x[0]+'|' for x in db.search2('junkemail','name','name','R','.*',mode='get')]))[:-1]+')$'
# junkextn=r'^(?:'+(''.join([x[0]+'|' for x in db.get('junkextension')]))[:-1]+')$'
 junkextn=r'^(?:.*[.]7z.*|.*[.]aspx$|.*[.]cms$|.*[.]cp*?$|.*[.]doc.*|.*[.]ece.*|.*[.]cgi.*|.*[.]hotels[.]com.*|.*[./]jobs?[./].*|.*[.]indeed[.].*|.*[.]php$|.*[.]ppt.*|.*[.]rar.*|.*[.]txt.*|.*[.]xls.*|.*[.]xml.*|.*[.]zip.*|.*\bbz\b.*|.*\bpdf\b.*)$'

 def __init__(self):
  super(databaserequest,self).__init__()

 def mutelink(self,link):
  return re.sub(r'[^a-zA-Z0-9._%-]','_',link)

 def validlink(self,j): #returns bool
  return not re.search(self.junkextn,j,flags=re.I) and (not self.db.search2('linkvisited','name','=',self.mutelink(j),mode='search') or self.db.search2('linkvisited','name','=',self.mutelink(j),'date','<',re.sub(r'-','',(datetime.date.today()-datetime.timedelta(days=self.EXPIREDAY)).isoformat()),mode='search'))

 def linkupdatebulk(self,j):
#  print(f'linkupdatebulk {j=}')
  self.db.search2('linkvisited',*[(self.mutelink(x),re.sub('-','',datetime.date.today().isoformat())) for x in j],mode='insertbulk')
 def linkupdate(self,j,checkupdate=True):
  if not self.db.search2('linkvisited','name','=',self.mutelink(j),mode='search'):
   self.db.search2('linkvisited',self.mutelink(j),re.sub('-','',datetime.date.today().isoformat()),mode='insert')
  elif checkupdate and self.db.search2('linkvisited','name','=',self.mutelink(j),'date','<',re.sub('-','',(datetime.date.today()-datetime.timedelta(days=self.EXPIREDAY)).isoformat()),mode='search'):
   self.db.search2('linkvisited','date',re.sub('-','',datetime.date.today().isoformat()),'name','=',self.mutelink(j),mode='update')
  else:
   self.db.search2('linkvisited','date',re.sub('-','',datetime.date.today().isoformat()),'name','=',self.mutelink(j),mode='update')

 def googlelink(self,j): #takes company name
  return r'https://www.google.com/search?q='+re.sub(r'\s+','+',j)+r'&btnG=Search'

 def appendjunkextensions(self,weburl,trimurl=False):
  if trimurl:
   weburl=re.sub(r'(?:^|$)',r'.*',re.sub(r'[.]',r'[.]',re.sub(r'(?:https?://)?(?:www[.])?(.*?)(?:/.*|$)',r'\1',weburl)))
  self.junkextn=re.sub(r'\)\$',r'|'+weburl+r')$',self.junkextn) if not re.search(r'\^\(\?:\)\$',self.junkextn) else re.sub(r'\)\$',weburl+r')$',self.junkextn)
  print(f'<>databaserequestc.appendjunkextensions {self.junkextn=}')
