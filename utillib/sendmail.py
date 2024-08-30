import sys,os,re;sys.path.append(os.path.expanduser('~')+r'/tmp/')
import datetime,random,calendar
from MISC.utillib.emailclient import *
from MISC.utillib.database import databasecm
from MISC.utillib.databaserequest import databaserequestcm
from MISC.utillib.machinelearningrequest import machinelearningrequestcm
from MISC.utillib.util import utilcm
import json

class sendmailc:
 emailclientc=[brevoemailclientcm]
 videoattributedc=None
 def __init__(self,*arg,**kwarg):
  super(sendmailc,self).__init__(*arg,**kwarg)

 def get_to_subject_htmlmessage(self,email):
  subject=utilcm.getarg('--emailsubject',count=2,removearg=False) or utilcm.exec(re.split(r'(?:\n|\\n)',re.sub(r'%',databasecm.search2('tech','name','id','=',databasecm.search2('track','tech_id','email','=',email,mode='get')[0][0],mode='get')[0][0].lower(),databasecm.search2('tech','content','name','=','all',mode='get')[0][0])))[random.randint(0,len(utilcm.arg)-1)]
  youtubetitle=utilcm.exec(machinelearningrequestcm.getmatching(subject,*[x['title'] for x in self.videoattributedc],muteprint=True,percent=60))[random.randint(0,len(utilcm.arg)-1)]
  return dict(to=email,subject=subject,htmlmessage=re.sub(r'youtubeimagewidth','640px',re.sub(r'youtubetitle',youtubetitle,re.sub('youtubeid',self.videoattributedc[[count for count in range(len(self.videoattributedc)) if self.videoattributedc[count]['title']==youtubetitle][0]]['id'],re.sub('XXX',databasecm.search2('track','uuid','email','=',email,mode='get')[0][0],re.sub(r'\\n','\n',re.sub('youtubemonthyear',calendar.month_name[datetime.datetime.now().month]+' '+str(datetime.datetime.now().year),re.sub('youtubesubject',subject,open(r'data/marketingemailtext.txt').read(),flags=re.DOTALL|re.I),flags=re.DOTALL|re.I),flags=re.DOTALL|re.I),flags=re.DOTALL|re.I),flags=re.DOTALL|re.I),flags=re.DOTALL|re.I)))

 def get(self,*arg,**kwarg):
  if not sendmailc.videoattributedc:
   print(f'I sendmailc.__init__ loading json from youtube.com/@minhinc, please wait..')
   sendmailc.videoattributedc=json.loads('['+re.sub(r',\s*$','',re.sub('}}\\n','}},',os.popen('yt-dlp -j --flat-playlist https://www.youtube.com/@minhinc').read(),flags=re.DOTALL),flags=re.DOTALL)+']')
  count=0
  for xx in [x[0] for count,x in enumerate(databaserequestcm.dbc.search2('track','*','date','<=',re.sub('-','',(datetime.date.today()-datetime.timedelta(days=databaserequestcm.expiredayc)).isoformat()),'status','<',2,mode='get'))]:
   try:
    print(f'D sendmailc.get {xx=} {self.get_to_subject_htmlmessage(xx)=}')
    sendmailc.emailclientc[count].sendmail(**self.get_to_subject_htmlmessage(xx))
    databasecm.search2('track','date',re.sub('-','',datetime.date.today().isoformat()),'email','=',xx,mode='update')
   except Exception as exc:
    print(f'C sendmailc.get Exception {count=} {exc=}, trying another emailclient...')
    count+=1
    if len(sendmailc.emailclientc)<=count:
     print(f'I sendmailc.get All email clients tried, exiting...')
     sys.exit(-1)
import MISC.utillib.util;MISC.utillib.util.cmc(__name__,MISC.utillib.util.mce(__name__,sendmailc) or sendmailc())
