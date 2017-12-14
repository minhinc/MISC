import datetime
import threading
import sys
import os
#import urllib.request
import urllib2
import re
from fetchm import fetchc
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
class sendmailc(fetchc):
 def __init__(self,next,wgt,db):
  fetchc.__init__(self,next,wgt,db)
  if not os.path.exists(r'./data'):
   os.mkdir('./data/')
  self.mailsent=[]
  self.vc=threading.Condition()
 def handle(self):
  for file in ('file.txt','file.html','file.gif'):
   if not os.path.exists(r'./data/'+file):
    self.push(self.wdgt.text2,'fetching '+file+'\n')
    open('./data/'+file,'wb').write(urllib2.urlopen(urllib2.Request('http://www.minhinc.com/misc/'+file,headers={'User-Agent': 'Mozilla/44.0.2'}),timeout=90).read())
  self.push(self.wdgt.text2,'fetching blocked.txt\n')
  open('./data/blocked.txt','wb').write(urllib2.urlopen(urllib2.Request('http://www.minhinc.com/about/blocked.txt',headers={'User-Agent': 'Mozilla/44.0.2'}),timeout=90).read())
  fetchc.handle(self)
  self.wdgt.state="password"
  self.wdgt.entry.delete(0,'end')
  self.wdgt.entry.insert(0,"Enter password")
 def message(self,strFrom,strTo):
  msgRoot=MIMEMultipart('related')
  msgRoot['Subject']='Embedded development with Qt'
  msgRoot['From']=strFrom
  msgRoot['To']=strTo
  msgRoot.preamble='This is a multi-part message in MIME format.'

  msgAlternative = MIMEMultipart('alternative')
  msgRoot.attach(msgAlternative)

  msgText = MIMEText(open(r'./data/file.txt').read())
  msgAlternative.attach(msgText)
  msgHTML=MIMEText(re.sub(r'XXX',strTo,open('./data/file.html').read()),'html')
  msgHTML.replace_header('Content-Type','text/html')
  msgAlternative.attach(msgHTML)

  fp=open('./data/file.gif','rb')
  msgImage=MIMEImage(fp.read())
  fp.close()
  msgImage.add_header('Content-ID','<image1>')
  msgImage.add_header('Content-Disposition','inline', filename='file.gif')
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
  self.fetching=True
  threading.Thread(target=self.producer,args=(1,)).start()
 def timer(self):
  print("mailsent")
  print(self.mailsent)
  self.vc.acquire()
  for mail in self.mailsent:
#   self.db.conn.execute('UPDATE track SET expire=? WHERE email=?',(int(re.sub('-','',str(datetime.date.today()+datetime.timedelta(days=60)))),mail))
    self.db.updatedate(mail)
#  self.db.conn.commit()
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
#  smtp.starttls()
#  smtp.ehlo()
  try:
#   smtp.connect('smtp.gmail.com:587')
   smtp.login('sales@minhinc.com',self.wdgt.password)
   self.push(self.wdgt.text2,'logged in to sg2plcpnl0068.prod.sin2.secureserver.net:465 through sales@minhinc.com\n')
   self.wdgt.text1.mark_set('insert','1.0')
#   self.mailsent=[]
   for line in [x for x in open(self.wdgt.filename) if not re.search(r'^\s*(#|$)',x)]:
    where=self.wdgt.text1.search(line,'insert','end')
    while where and self.wdgt.text1.search(r'^\s*#',re.sub(r'[.].*$',r'.0',where),re.sub(r'[.].*$',r'.end',where),regexp=True):
     where=self.wdgt.text1.search(line,re.sub(r'[.].*$',r'.end',where),'end')
#    for mail in line.split():
    for mail in [x for x in line.split() if re.match(r'(\b[A-Za-z0-9._%-]+\@\w+[.](?:\w+[.]?)*\b)',x) and not re.search(r"\b%s\b" % x, open('data/blocked.txt').read(),re.I)]:
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
