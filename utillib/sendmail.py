import calendar
import datetime
import sys,os,re;sys.path.append(os.path.expanduser('~')+r'/tmp/')
import random
import time
import uuid
#import json
import mimetypes
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email import encoders
from MISC.utillib.util import Util
import smtplib
import subprocess,shlex

from seleniumrequest import seleniumrequest
from databaserequest import databaserequest
from machinelearningrequest import machinelearningrequest
import MISC.utillib.requestm as requestm

class YouTubeError(Exception):
 pass

class sendmail(seleniumrequest,databaserequest,machinelearningrequest):
 def __init__(self,subprocess=False):
  super(sendmail,self).__init__(True,'linkedin')
  self.MAXEMAIL=3
  self.subprocess=subprocess
  self.emailcount=int(re.sub(r'^.*(\d+)$',r'\1',open(r'logdir/emailcount.txt','r').read()) if os.path.exists(r'logdir/emailcount.txt') else 1)%self.MAXEMAIL+1 
  processemail=False
  if not subprocess:
#   os.remove(r'logdir/seleniumdump.html') if os.path.exists(r'logdir/seleniumdump.html') else None
   open(r'logdir/emailcount.txt','w').write(str(self.emailcount))
  else:
   open(r'logdir/emailcount.txt','a').write(f' {self.emailcount}')
  self.smtp=smtplib.SMTP_SSL("smtp.gmail.com",465)
  time.sleep(2)
  self.smtp.ehlo()
  time.sleep(2)
  if not self.connect():
   print(f'connection failed tominhinc{self.emailcount}@gmail.com, exiting..')
   sys.exit(-1)
  if not subprocess:
   if Util.ftp('get','unsubscribe','track.txt'):
    self.db.search2('message',*[(0,x) for x in set(re.findall(r'^\S+\s+2\s+(.*?)\s*$',open('track.txt').read(),flags=re.M)) if not self.db.search2('message','name','=',x,mode='search')],mode='insertbulk')
    self.db.search2('track',*[('status',2,'email','=',x) for x in re.findall(r'^(\S+)\s+2\s+.*$',open('track.txt').read(),flags=re.M)],mode='updatebulk')
    self.db.search2('track',*[('message',int(self.db.search2('message','id','name','=',x[1],mode='get')[0][0]),'email','=',x[0]) for x in re.findall(r'^(\S+)\s+2\s+(.*?)\s*$',open('track.txt').read(),flags=re.M)],mode='updatebulk')
   os.system('python3 ../gc/seed.py print track > track.txt')
   Util.ftp('put','unsubscribe','track.txt')
   if Util.ftp('get','online','message.txt','lastemailsent.txt'):
    for i in re.split('\n',open('message.txt').read()):
     if i==re.split('\n',open('lastemailsent.txt').read())[0]:
      processemail=i
      continue
     print(f'TEST {i=} {re.split(Util.DELIMITER,i)=}')
     if len(re.split(Util.DELIMITER,i))==7 and processemail:
      self.smtp.sendmail('tominhinc@gmail.com',['tominhinc@gmail.com'],"From: Minh Inc <tominhinc@gmail.com>\nTo: Minh Inc <tominhinc@gmail.com>\nSubject: Online Training\n\n"+"\n".join(["Name","Tech","Email","Attachment","Message","Training Required Date","Sent On"][count]+" : "+re.split(Util.DELIMITER,i)[count] for count in range(len(re.split(Util.DELIMITER,i)))))
      processemail=i
     elif len(re.split(Util.DELIMITER,i))==4 and processemail:
      self.smtp.sendmail('tominhinc@gmail.com',['tominhinc@gmail.com'],"From: Minh Inc <tominhinc@gmail.com>\nTo: Minh Inc <tominhinc@gmail.com>\nSubject: Contact Us\n\n"+"\n".join(["Name","Email","Message","Sent On"][count]+" : "+re.split(Util.DELIMITER,i)[count] for count in range(len(re.split(Util.DELIMITER,i)))))
      processemail=i
     elif len(re.split(Util.DELIMITER,i))==6 and processemail:
      self.smtp.sendmail('tominhinc@gmail.com',['tominhinc@gmail.com'],"From: Minh Inc <tominhinc@gmail.com>\nTo: Minh Inc <tominhinc@gmail.com>\nSubject: Ask a programming question\n\n"+"\n".join(["Name","Tech","Email","Attachment","Message","Sent On"][count]+" : "+re.split(Util.DELIMITER,i)[count] for count in range(len(re.split(Util.DELIMITER,i)))))
      processemail=i
    if processemail:
     open('lastemailsent.txt','w').write(processemail)
     Util.ftp('put','online','lastemailsent.txt')

 def connect(self):
  while self.emailcount<=self.MAXEMAIL:
   for i in range(5):
    try:
     print(f'logging in to tominhinc{self.emailcount}@gmail.com ..')
     time.sleep(5)
#     self.smtp.login('tominhinc'+str(self.emailcount)+'@gmail.com','pinku76minh')
     self.smtp.login('tominhinc'+str(self.emailcount)+'@gmail.com',('nsbxmdsztbkydatl','roegsxqewlrydfao','qwawwvdkiaxsacib')[self.emailcount-1])
    except:
     print(f'login error - tominhinc{self.emailcount}@gmail.com')
     self.smtp.close()
    else:
     print(f'successfully connected with tominhinc{self.emailcount}')
     break
   else:
    self.emailcount+=1
    if self.emailcount>self.MAXEMAIL:
     print(f'All emails count {self.MAXEMAIL} reached...')
     return False
#     sys.exit(-1)
    continue
   break
  else:
   print(f'return false')
   return False
  print(f'return true')
  return True

 def message(self,strFrom,strTo,tech=None):
#  print(f'message {strFrom=} {strTo=} {tech=}')
  if not hasattr(sendmail.message,'youtubehreftext'):
   if not os.path.exists(r'data/marketingemailtext.txt'):
    open(r'data/marketingemailtext.txt','w').write(requestm.get(r'https://witheveryone.angelfire.com/marketingemailtext.txt',get=True))
#   setattr(sendmail.message,'youtubehreftext',self.youtubevideolink(r'file://'+os.path.abspath('.')+r'/logdir/seleniumdump.html' if os.path.exists(r'logdir/seleniumdump.html') else r'https://youtube.com/@minhinc/videos'))
   setattr(sendmail.message,'youtubehreftext',self.youtubevideolink(r'https://youtube.com/@minhinc/videos'))
   requestm.syncyoutube(*[x[0] for x in sendmail.message.youtubehreftext])
   requestm.preparemainfront(sendmail.message.youtubehreftext[0],self.webdriverdict['linkedin'].find_elements_by_xpath('//*[@id="subscriber-count"]')[0].text)
#   open(r'logdir/seleniumdump.html','w').write(self.webdriverdict['linkedin'].page_source) if not os.path.exists(r'logdir/seleniumdump.html') else None
   setattr(sendmail.message,'youtubetech',dict())
   setattr(sendmail.message,'techyoutubelist',dict())
   setattr(sendmail.message,'subject',re.split(r'(?:\n|\\n)',self.db.search2('tech','content','name','=','all',mode='get')[0][0]))
#  emailcontent=re.sub(r'\\n','\n',open(r'data/marketingemailtext.txt').read())
  emailcontent=open(r'data/marketingemailtext.txt').read()
  tech=self.db.search2('tech','name','id','=',self.db.search2('track','tech_id','email','=',strTo,mode='get')[0][0],mode='get')[0][0] if tech==None else tech
#  techyoutubelist=[(y[0],x) for x in self.getmatching('python' if tech=='py' else 'opengl' if tech=='gl' else 'c++' if tech=='cpp' else tech,*[x[1] for x in self.message.youtubehreftext],muteprint=True) for y in self.message.youtubehreftext if x in y]#[(href,title),(href,title)..] 
  if not tech in self.message.youtubetech:
   sendmail.message.youtubetech[tech]=self.db.search2('tech','content','name','=',tech.lower(),mode='get')[0][0]
  if not tech in sendmail.message.techyoutubelist:
   sendmail.message.techyoutubelist[tech]=[(y[0],x) for x in self.getmatching(self.db.search2('tech','content','name','=',tech.lower(),mode='get')[0][0],*[x[1] for x in self.message.youtubehreftext],muteprint=True,percent=60) for y in self.message.youtubehreftext if x in y]
   print(f'<=>sendmail.message.techyoutubelist tech={tech} [tech]={sendmail.message.techyoutubelist[tech]}')
  if not sendmail.message.techyoutubelist[tech]:
   raise YouTubeError()
  randomnumber=random.randrange(0,len(sendmail.message.techyoutubelist[tech]),1)
  youtubeid=re.sub(r'^.*?\?v=(.*)$',r'\1',sendmail.message.techyoutubelist[tech][randomnumber][0])
  emailcontent=re.sub(r'youtubetech',self.message.youtubetech[tech],re.sub(r'youtubeimagewidth',str(requestm.youtubeimage(youtubeid)[1][0])+'px',re.sub(r'youtubeid',youtubeid,re.sub(r'youtubetitle',sendmail.message.techyoutubelist[tech][randomnumber][1],emailcontent,flags=re.DOTALL|re.I),flags=re.DOTALL|re.I),flags=re.DOTALL|re.I))
#  print(f"{tech=} \n{randomnumber=} \n{youtubeid=} \n{self.message.techyoutubelist=} \n{self.message.emailcontent=} \n{self.message.youtubetech=} \n{self.message.subject=}")
  print(f"{tech=} {randomnumber=} {youtubeid=} \"{self.message.techyoutubelist[tech][randomnumber][1]}\" ",end='')
#  os.system(r'cd ~/tmp/MISC/image;~/tmp/ftp.sh -f put image ./'+youtubeid+'.jpg') if not os.path.exists(os.path.expanduser('~')+r'/tmp/MISC/image/'+youtubeid+'.jpg') else None
  msgRoot=MIMEMultipart('related')
#  msgRoot['Subject']=re.sub(r'^\s*<!--(.*?)-->.*',r'\1',self.message.jsonemailcontent[tech]["1"],flags=re.DOTALL) if "s" not in self.message.jsonemailcontent[tech] else self.message.jsonemailcontent[tech]["s"]
#  msgRoot['Subject']=self.db.search2('tech','content','name','=',tech.lower(),mode='get')[0][0]
  randomnumber=random.randrange(0,len(sendmail.message.subject),1)
  msgRoot['Subject']=re.sub(r'%',self.message.youtubetech[tech],sendmail.message.subject[randomnumber])
  print(f"\"{msgRoot['Subject']}\" ",end='')
  msgRoot['From']=strFrom
  msgRoot['To']=strTo
  msgRoot['reply-to']='Minh Inc <tominhinc@gmail.com>'
  msgRoot.preamble='This is a multi-part message in MIME format.'

  msgAlternative = MIMEMultipart('alternative')
  msgRoot.attach(msgAlternative)

#  print("mail {}".format(self.message.jsonemailcontent[tech]["1"]))
  msgHTML=MIMEText(re.sub(r'MMYY',calendar.month_name[(datetime.date.today()+datetime.timedelta(days=16)).month]+' '+str((datetime.date.today()+datetime.timedelta(days=16)).year),re.sub(r'XXX',strTo,re.sub(r'email=XXX','email='+self.db.search2('track','uuid','email','=',strTo,mode='get')[0][0],emailcontent,flags=re.DOTALL|re.I),flags=re.DOTALL|re.I),flags=re.DOTALL|re.I),'html')
#  msgHTML.replace_header('Content-Type','text/html' if "t" not in self.message.jsonemailcontent[tech] else self.message.jsonemailcontent[tech]["t"])
  msgHTML.replace_header('Content-Type','text/html')
  msgAlternative.attach(msgHTML)
  return msgRoot

 def get(self,*url):
  """\
  get()\
  get(10)#ten emails only\
  get('abc@one.com','123@two.com')\
  """
  print(f'{"################## sendmail.get ##################":^100}\n{url=!r:^100}')
  lc=0
  if not (len(url)==3 and type(url[2])==int): # sending email when calling this module individually get(('comp pvt. ltd','qt','canada','pravinkumarsinha@gmail.com','tominhinc@gmail.com'),('ding dong pvt. ltd','cpp','india','tominhinc@gmail.com'))
   emaillist=[x[0] for count,x in enumerate(self.db.search2('track','*','date','<',re.sub('-','',(datetime.date.today()-datetime.timedelta(days=50)).isoformat()),'status','<',2,mode='get')) if len(url)==1 and type(url[0])==int and count<url[0] or url and x[0] in url or not url]
   print(f'<=>sendmail.get {emaillist=}')
   for count,i in enumerate(emaillist[:]):
    try:
     self.smtp.sendmail('Minh Inc <tominhinc'+str(self.emailcount)+'@gmail.com>',i,self.message('Minh Inc <tominhinc'+str(self.emailcount)+'@gmail.com>',i,self.db.search2('tech','name','id','=',self.db.search2('track','tech_id','email','=',i,mode='get')[0][0],mode='get')[0][0]).as_string())
#     print(f"try block tech {self.db.search2('tech','name','id','=',self.db.search2('track','tech_id','email','=',i,mode='get')[0][0],mode='get')[0][0]}")
    except Exception as e:
     print(f'<=>sendmail.get exception {e=} {type(e)=} tech={self.db.search2("tech","name","id","=",self.db.search2("track","tech_id","email","=",i,mode="get")[0][0],mode="get")[0][0]} {i} -> minhinc{self.emailcount}@gmail.com')
     if type(e)==YouTubeError:
      pass
     else:
      emaillist.remove(i)
      if type(e)==smtplib.SMTPRecipientsRefused:
       self.db.delete('track','email',i)
      else:
       self.smtp.close()
       self.db.search2('track',*[('date',re.sub('-','',datetime.date.today().isoformat()),'email','=',x) for x in emaillist[lc:count]],mode='updatebulk')
#       if not self.emailcount==self.MAXEMAIL:
       if not len(re.findall(r'\d+',open(r'logdir/emailcount.txt').read()))==self.MAXEMAIL:
        subprocess.call(shlex.split(r'python3 -c "import os,sys;sys.path.append(os.path.expanduser(\"~\")+r\"/tmp/\");import MISC.utillib.sendmail as sendmail;s=sendmail.sendmail(subprocess=True);s.get()"'))
       break
    else:
     print(f"{count+1}/{len(emaillist)} email sent ({self.emailcount}) {i}")
     if not (count+1)%10:
      print(f'database updating... {lc} -> {count}')
      self.db.search2('track',*[('date',re.sub('-','',datetime.date.today().isoformat()),'email','=',x) for x in emaillist[lc:count+1]],mode='updatebulk')
      lc=count+1
     elif count==len(emaillist)-1:
      print(f'--- ALL MAIL SENT({len(emaillist)}) ---')
      self.db.search2('track',*[('date',re.sub('-','',datetime.date.today().isoformat()),'email','=',x) for x in emaillist[lc:count+1]],mode='updatebulk')
#     self.db.search2('track','expire',re.sub('-','',datetime.date.today().isoformat()),'email','=',i[0],mode='update')
   self.smtp.close()
   print(f'database updated')
   print(f'******  ALL EMAIL SENT  *******\n{url=!r:^100}\n***************************')
   if not os.path.isdir('logdir'):
    os.mkdir('logdir')
   if not self.subprocess:
    os.system(r'python3 ../gc/seed.py print > dbbackup.txt')
    os.system(r'rm dbbackup.7z')
    os.system(r'7z a dbbackup.7z dbbackup.txt')
    os.system(r'~/tmp/ftp.sh mput misc dbbackup.7z')
    os.system(r'mv dbbackup.txt logdir/'+re.sub(r':','-',datetime.datetime.now().isoformat())+'.txt')
   toretain=sorted([re.sub(r'-','',re.sub(r'(.*?)T.*$',r'\1',x)) for x in os.listdir('logdir') if re.search(r'\d+[.]txt$',x)],key=lambda x:int(x))[-10:]
   [os.remove(r'logdir/'+x) for x in os.listdir('logdir') if re.search(r'\d+[.]txt$',x) and not re.sub(r'-','',re.sub(r'(.*?)T.*$',r'\1',x)) in toretain]
#   open(r'logdir/emailcount.txt','w').write(str(self.emailcount))
   self.close(logout=False)
