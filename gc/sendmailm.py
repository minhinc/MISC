import datetime
import threading
import sys
import os
import re
import zipfile
import time
import urllib.request as urllib2
#import urllib2#for python 2.7
import shutil
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from fetchm import fetchc
class sendmailc(fetchc):
 def __init__(self,next,wgt,db):
  fetchc.__init__(self,next,wgt,db)
  self.emailtodir={}
  self.mailsent=[]
  self.vc=threading.Condition()
 def handle(self):
  fetchc.handle(self)
  self.wdgt.state="password"
  self.wdgt.entry.delete(0,'end')
  self.wdgt.entry.insert(0,"Enter password")
 def message(self,strFrom,strTo):
  topicdir_l=self.downloadzipfile(str(self.db.get('track','tech_id','email',strTo)[0][0])+'.'+str(self.db.get('track','city_id','email',strTo)[0][0])+'.'+str(self.db.get('track','country_id','email',strTo)[0][0]))
  msgRoot=MIMEMultipart('related')
  msgRoot['Subject']=[re.sub(r'.*<!--\s*subject\s*(.*)\s*-->\s*$','\\1',line,flags=re.I) for line in open(topicdir_l+'/file.html') if re.search('<!--\s*subject\s*.*-->\s*$',line)][0]
  msgRoot['From']=strFrom
  msgRoot['To']=strTo
  msgRoot.preamble='This is a multi-part message in MIME format.'

  msgAlternative = MIMEMultipart('alternative')
  msgRoot.attach(msgAlternative)

  msgHTML=MIMEText(re.sub(r'XXX',strTo,re.sub(r'email=XXX','email='+self.db.get('track','uuid','email',strTo)[0][0],open(topicdir_l+'/file.html').read())),'html')
  msgHTML.replace_header('Content-Type','text/html')
  msgAlternative.attach(msgHTML)

  for i in [i for i in os.listdir(topicdir_l) if i!='file.html']:
   fp=open(topicdir_l+'/'+i,'rb')
   msgImage=MIMEImage(fp.read())
   fp.close()
   msgImage.add_header('Content-ID','<image'+re.sub(r'file(\d+).*$','\\1',i)+'>')
   msgImage.add_header('Content-Disposition','inline', filename=i)
   msgRoot.attach(msgImage)
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
    for mail in [x for x in line.split() if re.match(r'(\b[A-Za-z0-9._%-]+\@\w+[.](?:\w+[.]?)*\b)',x) and self.db.get('track','status','email',x)[0][0]<2]:
     self.push(self.wdgt.text2,"%s" % (mail+' '))
     smtp.sendmail('sales@minhinc.com',mail,self.message('Minh INC <sales@minhinc.com>',mail).as_string())
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
  except:
   self.push(self.wdgt.text2,'Network Error\n')
   self.wdgt.btn.config(text='fetch',state='normal')
  else:
   self.push(self.wdgt.text2,'over\n')
   self.wdgt.after(0,lambda:self.clean)
  finally:
   smtp.quit()
  print('sendmailc::get')
 def downloadzipfile(self,topicdir_p):
  if topicdir_p in self.emailtodir and os.path.exists(self.emailtodir[topicdir_p]) and (time.time()-os.stat(self.emailtodir[topicdir_p]).st_ctime)<7200:
   return self.emailtodir[topicdir_p]
  topicdir_l=topicdir_p
  self.push(self.wdgt.text2,"\n")
  while True:
   try:
    data=urllib2.urlopen(urllib2.Request('http://www.minhinc.com/advertisement/'+topicdir_p+'.zip',headers={'User-Agent': 'Mozilla/44.0.2'}),timeout=90).read()
    self.push(self.wdgt.text2,"found www.minhinc.com/advertisement/%s.zip\n" % topicdir_p)
    with open(topicdir_p+'.zip','wb') as file:
     file.write(data)
    break
   except:
    self.push(self.wdgt.text2,"no www.minhinc.com/advertisement/%s.zip\n" % topicdir_p)
    if re.search(r'\d+[.]\d+[.]\d+',topicdir_p):
     topicdir_p=re.sub(r'([^.]*)[.][^.]*[.]([^.]*)','\\1.x.\\2',topicdir_p)
    elif re.search(r'\d+[.]x[.]\d+',topicdir_p):
     if int(re.sub(r'.*[.](\d+)','\\1',topicdir_p))%100!=1:
      topicdir_p=re.sub(r'([^.]*).*','\\1.x.'+str(int(re.sub(r'.*[.](\d+)','\\1',topicdir_p))-int(re.sub(r'.*[.](\d+)','\\1',topicdir_p))%100+1),topicdir_p)
     else:
      topicdir_p=re.sub(r'([^.]*).*','\\1.x.x',topicdir_p)
    else:
     topicdir_p='x.x.x'
  self.emailtodir[topicdir_l]=topicdir_p
  shutil.rmtree(topicdir_p,ignore_errors=True)
  zip_ref=zipfile.ZipFile(topicdir_p+'.zip','r')
  zip_ref.extractall('.')
  zip_ref.close()
  return topicdir_p
