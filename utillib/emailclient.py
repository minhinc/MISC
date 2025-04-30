#!/usr/bin/env python
# Import SendinBlue library
import sys,os,re;sys.path.append('/home/minhinc/tmp')
import json
from MISC.extra.config import _configi as print
from MISC.extra.config import _configi
from MISC.extra.config import _configi
from abc import ABC, abstractmethod

#brevo email
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException

#gmail setup
import smtplib
from email.mime.text import MIMEText


class _emailclientc(ABC):
 def __init__(self,*args,**kwargs):
  self.api_instance=None
  self.sentcount=0
  self.name='Minh INC.'
  self.email='tominhinc@gmail.com'

 @abstractmethod
 def password(self):
  print(f'>< ')

 @abstractmethod
 def connect(self):
  print(f'>< emailclient.connect')

 def sendmail(self,tol_,subject_=None,htmlmessage_=None):
  print(f'>< {tol_=} {subject_=} {htmlmessage_=}')
  if subject_==None or htmlmessage_==None:
   print(f'C emailclientc htmlmessage or title cannot be None, exiting..')
   raise Exception("emailclientc htmlmessage or subject cannot be None...")
  if self.api_instance==None:
   self.connect()
  for recipient in ([tol_] if not _configi.type(tol_)=='sequence' else tol_):
   self.sendmail2(recipient,subject_,htmlmessage_)
   self.sentcount+=1
   print(f'<=> msg sent to {recipient}')


class _brevoemailclientc(_emailclientc):
 def __init__(self,*args,**kwargs):
  super(_brevoemailclientc,self).__init__(*args,**kwargs)

 def password(self):
  return "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"

 def connect(self):
  print(f'>< connecting Brevo')
  configuration = sib_api_v3_sdk.Configuration()
  configuration.api_key['api-key'] = self.password()
  self.api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

 def sendmail2(self,recipient_,subject_=None,htmlmessage_=None):
  api_response = self.api_instance.send_transac_email(sib_api_v3_sdk.SendSmtpEmail(to=[{"email":self.email,"name":self.name} for x in [recipient_]],reply_to={"email":self.email,"name":self.name}, html_content=htmlmessage_, sender={"name": self.name, "email": self.email}, subject=subject_))

class _gmailemailclientc(_emailclientc):
 def __init__(self,*args,**kwargs):
  super(_gmailemailclientc,self).__init__(*args,**kwargs)

 def password(self):
  return "crho gaei wbgn jnza"

 def connect(self):
  print(f'>< connecting gmail')
  self.api_instance=smtplib.SMTP_SSL('smtp.gmail.com', 465)
  self.api_instance.login(self.email, self.password())

 def sendmail2(self,recipient_,subject_=None,htmlmessage_=None):
  msg=MIMEText(htmlmessage_) if not re.search(r'<html>.*</html>',htmlmessage_,flags=re.DOTALL|re.I) else MIMEText(htmlmessage_,'html')
  msg['Subject']=subject_
  msg['From']=f"{self.name} <{self.email}>"
  msg['To']=recipient_
  self.api_instance.sendmail(self.email, recipient_, msg.as_string())

_configi.cmc(__name__,_brevoemailclientc)
_configi.cmc(__name__,_gmailemailclientc)
