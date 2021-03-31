import smtplib
import time
import imaplib
import email
import sys
import re
import os

# -------------------------------------------------
#
# Utility to read email from Gmail Using Python
#
# ------------------------------------------------
class getoutofloop(Exception):
 pass
def printanddelete(mail,index,msg,email_from,email_subject):
 if len(sys.argv)==4 or (msg.get_content_type()==r'text/plain' or msg.get_content_type==r'text/html') and (re.search(r'Mail Delivery (?:Sub)?system',email_from,flags=re.I) or re.search(r'boxbe-notifications@boxbe.com',email_from,flags=re.I) or re.search(r'^\s*Undeliverable:',email_subject,flags=re.I) or re.search(r'^\s*failure notice\s*$',email_subject,flags=re.I) or re.search(r'^\s*(Automatic reply:|Rejected:|Out of Office)',email_subject,flags=re.I) or re.search(r'your ticket has been created',email_subject,flags=re.I)) :
  payload = msg.get_payload(decode=True)
  if payload:
   print " ".join(set([imail for imail in re.findall(r'([A-Za-z0-9._%-]+\@[\w-]+[.](?:\w+[.]?)*\b)',payload,flags=re.I) if not re.search(r'(tominhinc.?@gmail.com|.*?@minhinc.com|mx.google.com|pravinkumarsinha@gmail.com)\s*$',imail,re.I)]))
   with open('t.txt','a+') as file:
    file.write("{}\n".format(" ".join(set([imail for imail in re.findall(r'([A-Za-z0-9._%-]+\@[\w-]+[.](?:\w+[.]?)*\b)',payload,flags=re.I) if not re.search(r'(tominhinc.?@gmail.com|.*?@minhinc.com|mx.google.com|pravinkumarsinha@gmail.com)\s*$',imail,re.I)]))))
   mail.store(index, '+FLAGS', '\\Deleted')
   return True
 return False

def read_email_from_gmail():
 try:
  mail = imaplib.IMAP4_SSL('imap.gmail.com',993)
  mail.login(sys.argv[1],sys.argv[2])
  if len(sys.argv)==4 and sys.argv[3]=='sentmail':
   mail.select('[Gmail]/Sent Mail')
  else:
   mail.select('inbox')

  type, data = mail.search(None, 'ALL')
  mail_ids = data[0]

  id_list = mail_ids.split()   
  first_email_id = int(id_list[0])
  latest_email_id = int(id_list[-1])

  for i in range(latest_email_id,first_email_id, -1):
   typ, data = mail.fetch(i, '(RFC822)' )

   for response_part in data:
    try:
     if isinstance(response_part, tuple):
      msg = email.message_from_string(response_part[1])
      email_subject = msg['subject']
      email_from = msg['from']
 #     print 'From : ' + email_from + '\n'
 #     print 'Subject : ' + email_subject + '\n'
 
      if msg.is_multipart():
       for part in msg.walk():
        if printanddelete(mail,i,part,msg['from'],msg['subject']):
         raise getoutofloop
      else:
       if printanddelete(mail,i,msg,msg['from'],msg['subject']):
        raise getoutofloop   
    except getoutofloop:
     pass
  mail.expunge()
  mail.close()
  mail.logout()
 except Exception, e:
  print str(e) 
if len(sys.argv)<=2:
 print('Usage:')
 print('python read.py <emailaddress> <emailpassword> [allinbox|sentmail]')
 print('--Note-- Emails will not be cleared from database if third argument i.e. allinbox/sentmail specified')
 print('python read.py tominhinc1@gmail.com mypassword')
 print('python read.py tominhinc1@gmail.com mypassword allinbox')
 print('python read.py tominhinc1@gmail.com mypassword sentmail')
 exit(1)
if len(sys.argv)>=4:
 print("********* Emails will not be deleted from database ********")
 print("Press any key to discontinue, press Y/y to continue")
 inpt=raw_input()
 if not inpt or not re.search(r'^(y|Y)',inpt):
  exit(1) 
open('t.txt','w+').close()
read_email_from_gmail()
if len(sys.argv)==3:
 print('--------- Deleting from database --------------')
 os.system('python3 seed.py delete track email `cat t.txt`')
