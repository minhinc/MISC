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
import smtplib

from seleniumrequest import seleniumrequest
from databaserequest import databaserequest
from machinelearningrequest import machinelearningrequest
import MISC.utillib.requestm as requestm

class YouTubeError(Exception):
 pass

class sendmail(seleniumrequest,databaserequest,machinelearningrequest):
 def __init__(self):
  super(sendmail,self).__init__(True,'linkedin')
  self.emailcount=2
#  self.MAXEMAIL=3
  self.MAXEMAIL=2
  self.smtp=smtplib.SMTP_SSL("smtp.gmail.com",465)
  time.sleep(2)
  self.smtp.ehlo()
  time.sleep(2)
  if not self.connect():
   print(f'connection failed tominhinc{self.emailcount}@gmail.com, exiting..')
   sys.exit(-1)

 def connect(self):
  while self.emailcount<=self.MAXEMAIL:
   for i in range(5):
    try:
     print(f'logging in to tominhinc{self.emailcount}@gmail.com ..')
     time.sleep(5)
#     self.smtp.login('tominhinc'+str(self.emailcount)+'@gmail.com','pinku76minh')
     self.smtp.login('tominhinc'+str(self.emailcount)+'@gmail.com',('nsbxmdsztbkydatl','roegsxqewlrydfao')[self.emailcount-1])
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
   setattr(sendmail.message,'youtubehreftext',self.youtubevideolink())
   requestm.syncyoutube(*[x[0] for x in sendmail.message.youtubehreftext])
   setattr(sendmail.message,'youtubetech',dict())
   setattr(sendmail.message,'techyoutubelist',dict())
   setattr(sendmail.message,'subject',re.split('\n',self.db.search2('tech','content','name','=','all',mode='get')[0][0]))
#  emailcontent=re.sub(r'\\n','\n',open(r'data/marketingemailtext.txt').read())
  emailcontent=open(r'data/marketingemailtext.txt').read()
  tech=self.db.search2('tech','name','id','=',self.db.search2('track','tech_id','email','=',strTo,mode='get')[0][0],mode='get')[0][0] if tech==None else tech
#  techyoutubelist=[(y[0],x) for x in self.getmatching('python' if tech=='py' else 'opengl' if tech=='gl' else 'c++' if tech=='cpp' else tech,*[x[1] for x in self.message.youtubehreftext],muteprint=True) for y in self.message.youtubehreftext if x in y]#[(href,title),(href,title)..] 
  if not tech in self.message.youtubetech:
   sendmail.message.youtubetech[tech]=self.db.search2('tech','content','name','=',tech.lower(),mode='get')[0][0]
  if not tech in sendmail.message.techyoutubelist:
   sendmail.message.techyoutubelist[tech]=[(y[0],x) for x in self.getmatching(self.db.search2('tech','content','name','=',tech.lower(),mode='get')[0][0],*[x[1] for x in self.message.youtubehreftext],muteprint=True,percent=60) for y in self.message.youtubehreftext if x in y]
   print(f'sendmail.message.techyoutubelist tech={tech} [tech]={sendmail.message.techyoutubelist[tech]}')
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
  msgHTML=MIMEText(re.sub(r'MMYY',calendar.month_name[(datetime.date.today()+datetime.timedelta(days=16)).month]+' '+str((datetime.date.today()+datetime.timedelta(days=16)).year),re.sub(r'XXX',strTo,re.sub(r'email=XXX','email='+self.db.get('track','uuid','email',strTo)[0][0],emailcontent,flags=re.DOTALL|re.I),flags=re.DOTALL|re.I),flags=re.DOTALL|re.I),'html')
#  msgHTML.replace_header('Content-Type','text/html' if "t" not in self.message.jsonemailcontent[tech] else self.message.jsonemailcontent[tech]["t"])
  msgHTML.replace_header('Content-Type','text/html')
  msgAlternative.attach(msgHTML)
  return msgRoot

 def get(self,*url):
  """\
  get()
  get(["qt",abc@one.com,123@two.com],["py",456@abc.com,def@three.com])\
  """
  print(f'{"################## sendmail.get ##################":^100}\n{url=!r:^100}')
  li=None
  if not (len(url)==3 and type(url[2])==int): # sending email when calling this module individually get(('comp pvt. ltd','qt','canada','pravinkumarsinha@gmail.com','tominhinc@gmail.com'),('ding dong pvt. ltd','cpp','india','tominhinc@gmail.com'))
   for i in url:
    for j in i[1:]:
     self.smtp.sendmail('Minh Inc <tominhinc'+str(self.emailcount)+'@gmail.com>',j,self.message('Minh Inc <tominhinc'+str(self.emailcount)+'@gmail.com>',j,self.getmatching(i[0],*[x[1] for x in self.db.get('tech')])[0]).as_string())
     print(f' email sent - {i}')
   if url:
    self.smtp.close()
    self.close(logout=False)
    return
   emaillist=[x[0] for x in self.db.search2('track','*','expire','<',re.sub('-','',(datetime.date.today()-datetime.timedelta(days=50)).isoformat()),'status','<',2,mode='get')]
   for count,i in enumerate(emaillist[:]):
    try:
     self.smtp.sendmail('Minh Inc <tominhinc'+str(self.emailcount)+'@gmail.com>',i,self.message('Minh Inc <tominhinc'+str(self.emailcount)+'@gmail.com>',i,self.db.search2('tech','name','id','=',self.db.search2('track','tech_id','email','=',i,mode='get')[0][0],mode='get')[0][0]).as_string())
#     print(f"try block tech {self.db.search2('tech','name','id','=',self.db.search2('track','tech_id','email','=',i,mode='get')[0][0],mode='get')[0][0]}")
    except Exception as e:
     print(f'exception {type(e)=} tech={self.db.search2("tech","name","id","=",self.db.search2("track","tech_id","email","=",i,mode="get")[0][0],mode="get")[0][0]} {i} -> minhinc{self.emailcount}@gmail.com')
     if type(e)==YouTubeError:
      pass
     else:
      emaillist.remove(i)
      if type(e)==smtplib.SMTPRecipientsRefused:
       self.db.delete('track','email',i)
      else:
       self.smtp.close()
       self.emailcount+=1
       if not self.connect():
        break
    else:
     print(f"{count+1}/{len(emaillist)} email sent ({self.emailcount}) {i}")
     if not li:
      li=i
     if not (count+1)%10:
      print(f'database updating... mid {count=} {li=} {i=} {emaillist.index(li)=} {emaillist.index(i)=}')
      self.db.search2('track',*[('expire',re.sub('-','',datetime.date.today().isoformat()),'email','=',x) for x in emaillist[emaillist.index(li):emaillist.index(i)]],mode='updatebulk')
      li=i
#     self.db.search2('track','expire',re.sub('-','',datetime.date.today().isoformat()),'email','=',i[0],mode='update')
   self.smtp.close()
   print(f'database updating... roughly {li=} {i=} {emaillist.index(li)=} {emaillist.index(i)=}')
#   self.db.search2('track',*[('expire',re.sub('-','',datetime.date.today().isoformat()),'email','=',x) for x in (emaillist[0:emaillist.index(i)+1] if i in emaillist else emaillist)],mode='updatebulk')
   self.db.search2('track',*[('expire',re.sub('-','',datetime.date.today().isoformat()),'email','=',x) for x in emaillist[emaillist.index(li):emaillist.index(i)+1]],mode='updatebulk') if li else None
   print(f'database updated')
   print(f'******  ALL EMAIL SENT  *******\n{url=!r:^100}\n***************************')
   if not os.path.isdir('logdir'):
    os.mkdir('logdir')
   os.system(r'python3 ../gc/seed.py print track > t.txt')
   os.system(r'python3 ../gc/seed.py print company >> t.txt')
   os.system(r'mv t.txt logdir/'+re.sub(r':','-',datetime.datetime.now().isoformat())+'.txt')
   toretain=sorted([re.sub(r'-','',re.sub(r'(.*?)T.*$',r'\1',x)) for x in os.listdir('logdir')],key=lambda x:int(x))[-10:]
   [os.remove(r'logdir/'+x) for x in os.listdir('logdir') if not re.sub(r'-','',re.sub(r'(.*?)T.*$',r'\1',x)) in toretain]
   self.close(logout=False)
