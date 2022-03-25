import datetime
import re
import string
import time
import uuid
from fetchm import fetchc
import MISC.utillib.databasem as databasem
class dbpushpullc(fetchc):
 def __init__(self,next,wdgt,db):
  fetchc.__init__(self,next,wdgt,db)
  self.eventchar=''
  self.ctime=time.time()
  self.wdgt.lwcountry.lwt.bind('<<ListboxSelect>>',self.onselect)
  self.wdgt.lwcountry.lwt.bind('<Key>',self.key)
 def handle(self):
  self.wdgt.lwtech.populate(self.db.get('tech','name',orderby='id'))
  self.wdgt.lwcountry.populate(self.db.get('country','name',orderby='id'))
  self.wdgt.show()
  fetchc.handle(self)
  self.wdgt.entry.config(state='disabled')
 def get(self):
  companyname=None
  matchobj=None
#  self.db.delete('linkvisited','date',int(re.sub('-','',datetime.date.today().isoformat()))-59)
  self.db.delete('linkvisited','date',int(re.sub('-','',(datetime.date.today()-datetime.timedelta(days=50)).isoformat())))
  if not len(self.wdgt.lwtech.lwt.curselection())*len(self.wdgt.lwcity.lwt.curselection())*len(self.wdgt.lwcountry.lwt.curselection()):
   self.wdgt.entry.delete(0,'end')
   self.wdgt.entry.insert(0,'select all list')
  else:
   self.wdgt.save()
   for line in open(self.wdgt.filename):
    matchobj=re.match(r'^\s*#\s*(.*)\s*$',line,flags=re.I)
    if(not matchobj):
     matchobj=re.match(r'^\s*(.+?) (\b[A-Za-z0-9._%-]+\@[\w-]+[.](?:\w+[.]?)*\b)',line,flags=re.I)
     companyname=re.sub(r'\s*','',string.capwords(matchobj.group(1).lower()))
     self.db.fill('company',((companyname,''),))
     self.push(self.wdgt.text2,"%s" % (companyname))
     for email in [ email for email in line.split() if re.match(r'(\b[A-Za-z0-9._%-]+\@[\w-]+[.](?:\w+[.]?)*\b)',email,flags=re.I) ]:
      self.db.fill('track',((email.lower(),str(uuid.uuid4()),self.db.get('company','id','name',companyname)[0][0], self.db.get('tech','id','name',self.wdgt.lwtech.lwt.get(self.wdgt.lwtech.lwt.curselection()[0]))[0][0], self.db.get('city','id','name',self.wdgt.lwcity.lwt.get(self.wdgt.lwcity.lwt.curselection()[0]))[0][0], self.db.get('country','id','name',self.wdgt.lwcountry.lwt.get(self.wdgt.lwcountry.lwt.curselection()[0]))[0][0], int(re.sub('-','',datetime.date.today().isoformat()))),))
      self.push(self.wdgt.text2," %s" % (email))
     self.push(self.wdgt.text2,"\n")
   self.wdgt.text1.delete('1.0','end')
   companyname='NULL'
   for row in self.db.getemailcompany():
    if(companyname!=row[1]):
     if(companyname=='NULL'):
      self.push(self.wdgt.text1,"%s %s" % (row[1],row[0]))
     else:
      self.push(self.wdgt.text1,"\n%s %s" % (row[1],row[0]))
     companyname=row[1]
    else:
     self.push(self.wdgt.text1," %s" % (row[0]))
   self.wdgt.hide()
   self.wdgt.save()
   self.clean()
 def key(self,event):
  if (time.time()-self.ctime)<3:
   self.eventchar=self.eventchar+event.char
  else:
   self.eventchar=event.char
  self.ctime=time.time()
  self.wdgt.lwcountry.lwt.see([i for i,item in enumerate(self.db.get('country','name',orderby='id')) if re.search(r'^'+self.eventchar,item[0])][0]+1)
 def onselect(self,event):
  countryid=self.db.get('country','id','name',self.wdgt.lwcountry.lwt.get(self.wdgt.lwcountry.lwt.curselection()[0]))[0][0]
  self.wdgt.lwcity.populate(self.db.get('city','name','country',countryid,orderby='id'))
