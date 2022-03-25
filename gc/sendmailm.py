import calendar
import datetime
import threading
import sys
import os
import re
import zipfile
import time
import random
from PIL import Image
import string
import urllib.request as urllib2
sys.path.append('..')
from utillib import requestm
#import urllib2#for python 2.7
import shutil
import json
import mimetypes
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email import encoders
import smtplib
from fetchm import fetchc
class sendmailc(fetchc):
 def __init__(self,next,wgt,db):
  fetchc.__init__(self,next,wgt,db)
  self.mailsent=[]
  self.vc=threading.Condition()
#  self.downloadimage=dict()
  self.jsonemailcontent=dict()
  self.misc=dict()
 def handle(self):
  fetchc.handle(self)
  self.wdgt.state="password"
  self.wdgt.entry.delete(0,'end')
  self.wdgt.entry.insert(0,"Enter password")
 def message(self,strFrom,strTo):
  tech=self.db.get('tech','name','id',self.db.get('track','tech_id','email',strTo)[0][0])[0][0]
  print(f'><message {strFrom=} {strTo=} {tech=}')
  if not tech in self.jsonemailcontent:
   self.jsonemailcontent[tech]=json.loads(re.sub(r'\\\n',r'\\n',self.db.get('tech','content','id',self.db.get('track','tech_id','email',strTo)[0][0])[0][0]))
   self.misc[tech]=dict()
   self.misc[tech]['randomnumber']=random.randrange(0,len(self.jsonemailcontent[tech]["youtube"]),1)
   self.jsonemailcontent[tech]["1"]=re.sub(r'youtubeimagewidth',str(requestm.youtubeimage(self.jsonemailcontent[tech]['youtube'][self.misc[tech]['randomnumber']][1])[1][0])+'px',re.sub(r'youtubeid',self.jsonemailcontent[tech]["youtube"][self.misc[tech]['randomnumber']][1],re.sub(r'youtubetitle',self.jsonemailcontent[tech]["youtube"][self.misc[tech]['randomnumber']][0],self.jsonemailcontent[tech]["1"],flags=re.DOTALL|re.I),flags=re.DOTALL|re.I),flags=re.DOTALL|re.I)
   print("tech {} random {}".format(tech,self.misc[tech]['randomnumber']))
   print(f'{self.jsonemailcontent[tech]["1"]=}')
  msgRoot=MIMEMultipart('related')
  msgRoot['Subject']=re.sub(r'^\s*<!--(.*?)-->.*',r'\1',self.jsonemailcontent[tech]["1"],flags=re.DOTALL) if "s" not in self.jsonemailcontent[tech] else self.jsonemailcontent[tech]["s"]
  msgRoot['From']=strFrom
  msgRoot['To']=strTo
  msgRoot['reply-to']='Minh Inc <sales@minhinc.com>'
  msgRoot.preamble='This is a multi-part message in MIME format.'

  msgAlternative = MIMEMultipart('alternative')
  msgRoot.attach(msgAlternative)

#  print("mail {}".format(self.jsonemailcontent[tech]["1"]))
  msgHTML=MIMEText(re.sub(r'MMYY',calendar.month_name[(datetime.date.today()+datetime.timedelta(days=16)).month]+' '+str((datetime.date.today()+datetime.timedelta(days=16)).year),re.sub(r'XXX',strTo,re.sub(r'email=XXX','email='+self.db.get('track','uuid','email',strTo)[0][0],self.jsonemailcontent[tech]["1"],flags=re.DOTALL|re.I),flags=re.DOTALL|re.I),flags=re.DOTALL|re.I),'html')
  msgHTML.replace_header('Content-Type','text/html' if "t" not in self.jsonemailcontent[tech] else self.jsonemailcontent[tech]["t"])
  msgAlternative.attach(msgHTML)
  print('message datastructure filled')
  return msgRoot
 def get(self):
  if not self.wdgt.password:
   self.wdgt.entry.delete(0,'end')
   self.wdgt.entry.insert(0,'Enter password')
   self.wdgt.state="password" 
   return
  if(self.wdgt.btn['text']=='fetch'):
   self.wdgt.save()
   self.wdgt.btn.config(state='disabled',text='transferring')
   self.wdgt.entry.delete(0,'end')
   self.wdgt.text1.config(state='disabled')
   self.wdgt.entry.config(state='disabled')
   self.wdgt.text2.config(state='disabled')
   self.wdgt.master.update()
  threading.Thread(target=self.producer,args=(1,)).start()
 def timerupdate(self):
  self.vc.acquire()
  for mail in self.mailsent:
    self.db.updatedate(mail)
  self.mailsent=[]
  self.push(self.wdgt.text2,'Added to Database\n')
  self.vc.notify()
  self.vc.release()
 def producer(self,arg):
  count=1
  smtp=smtplib.SMTP_SSL("smtp.gmail.com",465)
  smtp.ehlo()
#  smtp.starttls()
  try:
   smtp.login('tominhinc1@gmail.com',self.wdgt.password)
   self.push(self.wdgt.text2,'logged in to smtp.gmail.com:587 through tominhinc1@gmail.com\n')
   self.wdgt.text1.mark_set('insert','1.0')
   for line in [x for x in open(self.wdgt.filename) if not re.search(r'^\s*(#|$)',x)]:
    where=self.wdgt.text1.search(line,'insert','end')
    while where and self.wdgt.text1.search(r'^\s*#',re.sub(r'[.].*$',r'.0',where),re.sub(r'[.].*$',r'.end',where),regexp=True):
     where=self.wdgt.text1.search(line,re.sub(r'[.].*$',r'.end',where),'end')
    for mail in [x for x in line.split() if re.match(r'(\b[A-Za-z0-9._%-]+\@[\w-]+[.](?:\w+[.]?)*\b)',x) and self.db.get('track','status','email',x)[0][0]<2]:
     self.push(self.wdgt.text2,"%s" % (mail+' '))
     smtp.sendmail('tominhinc1@gmail.com',mail,self.message('Minh Inc <tominhinc1@gmail.com>',mail).as_string())
     print("message sent : %s" % count)
     count=count+1
     if count>250:
      raise RuntimeError("250 limit crossed")
     self.mailsent.append(mail)
     self.addtag(mail)
     self.push(self.wdgt.text2,'...\n')
    if len(self.mailsent):
     self.vc.acquire()
     self.wdgt.after(0,self.timerupdate)
     self.vc.wait()
     self.vc.release()
    self.wdgt.text1.config(state='normal')
    if where: self.wdgt.text1.insert(where,'#')
    open(self.wdgt.filename,'w').write(self.wdgt.text1.get('1.0','end'+'-1c'))
    self.wdgt.text1.config(state='disabled')
  except Exception as er:
   self.push(self.wdgt.text2,'Error : '+str(er)+'\n')
   self.wdgt.btn.config(text='fetch',state='normal')
  else:
   self.push(self.wdgt.text2,'over\n')
   self.wdgt.after(0,lambda:self.clean)
  finally:
   smtp.quit()
  print('sendmailc::get')
