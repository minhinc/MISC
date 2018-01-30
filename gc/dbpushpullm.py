#import msilib
import datetime
import re
import string
from fetchm import fetchc
import databasem
import uuid
class dbpushpullc(fetchc):
 def __init__(self,next,wdgt,db):
  fetchc.__init__(self,next,wdgt,db)
  self.wdgt.lwcountry.lwt.bind('<<ListboxSelect>>',self.onselect)
  self.wdgt.lwcountry.lwt.bind('<Key>',self.key)
 def handle(self):
  self.wdgt.lwtech.populate(self.db.get('tech','name'))
  self.wdgt.lwcountry.populate(self.db.get('country','name',orderby='id'))
  self.wdgt.lwmtopic.populate(self.db.get('mtopic','name',orderby='id'))
  self.wdgt.show()
  fetchc.handle(self)
 def get(self):
  companyname=None
  matchobj=None
  if not len(self.wdgt.lwtech.lwt.curselection())*len(self.wdgt.lwcity.lwt.curselection())*len(self.wdgt.lwcountry.lwt.curselection())*len(self.wdgt.lwmtopic.lwt.curselection()):
   self.wdgt.entry.delete(0,'end')
   self.wdgt.entry.insert(0,'select all list')
  else:
   self.wdgt.save()
   for line in open(self.wdgt.filename):
    matchobj=re.match(r'^\s*#\s*(.*)\s*$',line,re.I)
    if(not matchobj):
     matchobj=re.match(r'^\s*(.+?) (\b[A-Za-z0-9._%-]+\@\w+[.](?:\w+[.]?)*\b)',line,re.I)
     companyname=re.sub(r'\s*','',string.capwords(matchobj.group(1).lower()))
     self.db.fill('company',((companyname,''),))
     self.push(self.wdgt.text2,"%s" % (companyname))
     for email in [ email for email in line.split() if re.match(r'(\b[A-Za-z0-9._%-]+\@\w+[.](?:\w+[.]?)*\b)',email,re.I) ]:
      self.db.fill('track',((email.lower(),str(uuid.uuid4()),self.db.get('company','id','name',companyname)[0][0], self.db.get('tech','id','name',self.wdgt.lwtech.lwt.get(self.wdgt.lwtech.lwt.curselection()[0]))[0][0], self.db.get('city','id','name',self.wdgt.lwcity.lwt.get(self.wdgt.lwcity.lwt.curselection()[0]))[0][0], self.db.get('country','id','name',self.wdgt.lwcountry.lwt.get(self.wdgt.lwcountry.lwt.curselection()[0]))[0][0], int(re.sub('-','',datetime.date.today().isoformat()))),))
      self.push(self.wdgt.text2," %s" % (email))
     self.push(self.wdgt.text2,"\n")
   self.wdgt.text1.delete('1.0','end')
   companyname='NULL'
#   for row in self.db.conn.execute('SELECT track.email,company.name FROM track JOIN company ON track.company_id=company.id WHERE ?>=track.expire ORDER BY track.company_id',(int(re.sub('-','',datetime.date.today().isoformat())),)):
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
  self.wdgt.lwcountry.lwt.see([i for i,item in enumerate(self.db.get('country','name',orderby='id')) if re.search(r'^'+event.char,item[0],flags=re.I)][0]+1)
 def onselect(self,event):
  print("List Box Select")
  countryid=self.db.get('country','id','name',self.wdgt.lwcountry.lwt.get(self.wdgt.lwcountry.lwt.curselection()[0]))[0][0]
  print("countryid %d" % countryid)
  self.wdgt.lwcity.populate(self.db.get('city','name','country',countryid))
