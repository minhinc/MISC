import datetime
import threading
import sys
import os
import re
import zipfile
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from fetchm import fetchc
class sendmailc(fetchc):
 def __init__(self,next,wgt,db):
  fetchc.__init__(self,next,wgt,db)
  self.mtopicdir=None
  self.mailsent=[]
  self.vc=threading.Condition()
 def handle(self):
  self.mtopicdir=str(self.db.get('tech','id','name',self.wdgt.lwtech.lwt.get(self.wdgt.lwtech.lwt.curselection()[0]))[0][0])+'.'+str(self.db.get('city','id','name',self.wdgt.lwcity.lwt.get(self.wdgt.lwcity.lwt.curselection()[0]))[0][0])+'.'+str(self.db.get('country','id','name',self.wdgt.lwcountry.lwt.get(self.wdgt.lwcountry.lwt.curselection()[0]))[0][0])
  if not os.path.exists(self.mtopicdir):
   if not os.path.isfile(self.mtopicdir+'.zip'):
    if os.system("wget -q "+'www.minhinc.com/advertisement/'+self.mtopicdir+'.zip'):
     print("no www.minhinc.com/advertisement/%s.zip" % self.mtopicdir)
     self.push(self.wdgt.text2,"no www.minhinc.com/advertisement/%s.zip\n" % self.mtopicdir)
     self.mtopicdir='1'
     if os.system('wget -q www.minhinc.com/advertisement/1.zip'):
      print("no www.minhinc.com/advertisement/%s.zip" % self.mtopicdir)
      self.push(self.wdgt.text2,"no www.minhinc.com/advertisement/%s.zip\n" % self.mtopicdir)
      return False
   zip_ref=zipfile.ZipFile(self.mtopicdir+'.zip','r')
   zip_ref.extractall('.')
   zip_ref.close()
  self.subject=[re.sub(r'.*<!--\s*subject\s*(.*)\s*-->\s*$','\\1',line) for line in open(self.mtopicdir+'/file.html') if re.search('<!--\s*subject\s*.*-->\s*$',line)][0]
  print("mtopicdir %s %s " % (self.mtopicdir,self.subject) )
#  self.mtopicdir=str(self.db.get('mtopic','id','name',self.wdgt.lwmtopic.lwt.get(self.wdgt.lwmtopic.lwt.curselection()[0]))[0][0])
  fetchc.handle(self)
  self.wdgt.state="password"
  self.wdgt.entry.delete(0,'end')
  self.wdgt.entry.insert(0,"Enter password")
 def message(self,strFrom,strTo):
  msgRoot=MIMEMultipart('related')
  msgRoot['Subject']=self.subject
  msgRoot['From']=strFrom
  msgRoot['To']=strTo
  msgRoot.preamble='This is a multi-part message in MIME format.'

  msgAlternative = MIMEMultipart('alternative')
  msgRoot.attach(msgAlternative)

  msgHTML=MIMEText(re.sub(r'XXX',strTo,re.sub(r'email=XXX','email='+self.db.get('track','uuid','email',strTo)[0][0],open(self.mtopicdir+'/file.html').read())),'html')
  msgHTML.replace_header('Content-Type','text/html')
  msgAlternative.attach(msgHTML)

#  for i in range(1,self.db.get('mtopic','ic','id',self.mtopicdir)[0][0]+1):
  for i in [i for i in os.listdir(self.mtopicdir) if i!='file.html']:
   print("files %s" % i)
   fp=open(self.mtopicdir+'/'+i,'rb')
   msgImage=MIMEImage(fp.read())
   fp.close()
   msgImage.add_header('Content-ID','<image'+re.sub(r'file(\d+).*$','\\1',i)+'>')
   msgImage.add_header('Content-Disposition','inline', filename=i)
   msgRoot.attach(msgImage)

  return msgRoot
 def get(self):
#  if not self.mtopicinst:
#   module=__import__(self.mtopicdir)
#   my_class=getattr(module,'mtopicc')
#   self.mtopicinst=getattr(__import__(self.mtopicdir),'mtopicc')(self.db)
#   self.mtopicinst=my_class(self.db)
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
  self.fetching=True
  threading.Thread(target=self.producer,args=(1,)).start()
 def timer(self):
  print("mailsent")
  print(self.mailsent)
  self.vc.acquire()
  for mail in self.mailsent:
    self.db.updatedate(mail)
  self.wdgt.after_cancel(self.timerid)
  self.mailsent=[]
  print('added to database')
  self.push(self.wdgt.text2,'Added to Database\n')
  self.wdgt.master.update()
  self.vc.notify()
  self.vc.release()
  self.clean()
 def producer(self,arg):
  import smtplib
#  smtp=smtplib.SMTP("smtp.gmail.com",587)
  smtp=smtplib.SMTP_SSL("sg2plcpnl0068.prod.sin2.secureserver.net",465)
  smtp.ehlo()
  try:
   smtp.login('sales@minhinc.com',self.wdgt.password)
   self.push(self.wdgt.text2,'logged in to sg2plcpnl0068.prod.sin2.secureserver.net:465 through sales@minhinc.com\n')
   self.wdgt.text1.mark_set('insert','1.0')
   for line in [x for x in open(self.wdgt.filename) if not re.search(r'^\s*(#|$)',x)]:
    where=self.wdgt.text1.search(line,'insert','end')
    while where and self.wdgt.text1.search(r'^\s*#',re.sub(r'[.].*$',r'.0',where),re.sub(r'[.].*$',r'.end',where),regexp=True):
     where=self.wdgt.text1.search(line,re.sub(r'[.].*$',r'.end',where),'end')
    for mail in [x for x in line.split() if re.match(r'(\b[A-Za-z0-9._%-]+\@\w+[.](?:\w+[.]?)*\b)',x) and self.db.get('track','status','email',x)[0][0]!=2]:
     self.push(self.wdgt.text2,"%s" % (mail+' '))
     smtp.sendmail('sales@minhinc.com',mail,self.message('Minh INC <sales@minhinc.com>',mail).as_string())
     self.mailsent.append(mail)
     self.addtag(mail)
     self.push(self.wdgt.text2,'...\n')
    if len(self.mailsent):
     self.timerid=self.wdgt.after(50,self.timer)
     self.wdgt.master.update()
     self.vc.acquire()
     self.vc.wait()
     print("wait over")
     self.vc.release()
    self.wdgt.text1.config(state='normal')
    if where: self.wdgt.text1.insert(where,'#')
    open(self.wdgt.filename,'w').write(self.wdgt.text1.get('1.0','end'+'-1c'))
    self.wdgt.text1.config(state='disabled')
    self.wdgt.master.update()
  except:
   self.push(self.wdgt.text2,'Network Error\n')
   self.wdgt.btn.config(text='fetch',state='normal')
  else:
   print("over")
   self.push(self.wdgt.text2,'over\n')
#  finally:
   smtp.quit()
   self.fetching=False
#  self.timerid=self.wdgt.after(500,self.timer)
  print('sendmailc::get')
