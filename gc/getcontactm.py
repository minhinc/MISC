import threading,time
import os
import re
import datetime
import sys
import urllib.request as urllib2
#import urllib2#for python2.7
from fetchm import fetchc
sys.path.append('./util')
from util.utilm import utilc
class getcontactc(fetchc):
 def __init__(self,next,wgt,db):
  fetchc.__init__(self,next,wgt,db)
 def handle(self):
  fetchc.handle(self)
  self.wdgt.state="filenname"
  self.wdgt.entry.delete(0,'end')
  self.wdgt.entry.insert(0,"Enter file name")
 def get(self):
  if(self.fetching):
   self.fetching=False
   self.push(self.wdgt.text2,'fetch cancelled...\n')
   return
  if(self.wdgt.btn['text']=='fetch'):
   if(not self.wdgt.filename):
    self.wdgt.state="filename"
    self.wdgt.entry.delete(0,'end')
    self.wdgt.entry.insert(0,"Enter file name")
    return
   #self.wdgt.save()
   self.wdgt.btn.config(text='block')
   self.wdgt.entry.delete(0,'end')
   self.wdgt.text1.config(state='disabled')
   self.wdgt.entry.config(state='disabled')
   self.fetching=True
   threading.Thread(target=self.producer,args=(10,)).start()
 def producer(self,arg):
  self.wdgt.text1.mark_set('insert','1.0')
  mail=[]
  utili=utilc('linkedin')
  junkextn=r'^('+(''.join([x[0]+'|' for x in self.db.get('junkextension')]))[:-1]+')$'
  junkemail=r'^('+(''.join([x[0]+'|' for x in self.db.get('junkemail')]))[:-1]+')$'
  with open(re.sub(r'^(.*)[.]txt$','\\1',self.wdgt.filename)+'_people.txt','a') as file:
   file.write("%s#----------------%s" % ('\n' if os.stat(re.sub(r'^(.*)[.]txt$','\\1',self.wdgt.filename)+'_people.txt').st_size else '',str(datetime.datetime.now())))
  for line in [ line for line in open(self.wdgt.filename).read().split('\n') if not re.search('^\s*(#|$)',line) and not self.db.search('linkvisited',re.sub(r'[^a-zA-Z0-9._%-]','_','https://www.google.co.in/search?q='+re.sub('\s+','+',line)+r'&btnG=Search',flags=re.I)) ]:
   if not self.fetching:
    break
   self.addtag(re.sub(r'(^\s*|\s*$)','',line))
   try:
#    data=repr(urllib2.urlopen(urllib2.Request('https://www.google.co.in/search?q='+re.sub('\s+','+',line)+r'&btnG=Search',headers={'User-Agent': 'Mozilla/44.0.2'}),timeout=90).read())
    data=repr(urllib2.urlopen(urllib2.Request(r'http://www.google.com/search?source=hp&ei=zR1UW_zFCpv8rQGCkYiwAw&q='+re.sub('\s+','+',line)+r'&oq='+re.sub('\s+','+',line),headers={'User-Agent': 'Mozilla/44.0.2'}),timeout=90).read().decode('utf-8'))
    self.db.fill('linkvisited',((re.sub(r'[^a-zA-Z0-9._%-]','_','https://www.google.co.in/search?q='+re.sub('\s+','+',line)+r'&btnG=Search'),),))
    self.db.update('linkvisited','date',int(re.sub('-','',datetime.date.today().isoformat())),'name',re.sub(r'[^a-zA-Z0-9._%-]','_','https://www.google.co.in/search?q='+re.sub('\s+','+',line)+r'&btnG=Search'))
    for x in [ x for x in re.findall(r'url\?q=(http[^&]+)',data) if not self.db.search('linkvisited',re.sub(r'[^a-zA-Z0-9._%-]','_',x,flags=re.I)) and not re.search(junkextn,x,flags=re.I)]:
     self.push(self.wdgt.text2,"%s\n" % (x))
     try:
      #mail.extend([ x for x in re.findall(r'([A-Za-z0-9._%-]+\@\w+[.](?:\w+[.]?)*\b)',repr(urllib2.urlopen(urllib2.Request(x,headers={'User-Agent': 'Mozilla/44.0.2'}),timeout=10).read())) if not re.search(junkemail,x,flags=re.I) ])
      mail.extend([ x for x in re.findall(r'([A-Za-z0-9._%-]+\@\w+[.](?:\w+[.]?)*\b)',utili.getlinkedin_2(re.sub(r'(.*//).*?[.](linkedin.*)',r'\1\2',x)) if re.search(r'linkedin.com',x,flags=re.I) else utili.download(x)) if not re.search(junkemail,x,flags=re.I) ])
     except:
      self.push(self.wdgt.text2,'error:'+x+'\n')
    self.db.fill('linkvisited',[ (re.sub(r'[^a-zA-Z0-9._%-]','_',x),int(re.sub('-','',datetime.date.today().isoformat()))) for x in re.findall(r'url\?q=(http[^&]+)',data) if not self.db.search('linkvisited',re.sub(r'[^a-zA-Z0-9._%-]','_',x,flags=re.I)) and not re.search(junkextn,x,flags=re.I) ],fetchmany=True)
   except:
    self.push(self.wdgt.text2,'google error\n')
   if len(set(mail)):
    if len(set(mail))<100:
     self.push(self.wdgt.text2,'#'+re.sub(r'(^\s*|\s*$)','',line)+'\n'+' '.join(set(mail))+'\n')
     with open(re.sub(r'^(.*)[.]txt$','\\1',self.wdgt.filename)+'_people.txt','a') as file:
      file.write("%s%s" % ('\n' if os.stat(re.sub(r'^(.*)[.]txt$','\\1',self.wdgt.filename)+'_people.txt').st_size else '',re.sub(r'(^\s*|\s*$)','',line)+' '+' '.join(set([x.lower() for x in mail]))))
    else:
     print('--not included--#'+re.sub(r'(^\s*|\s*$)','',line)+'\n'+' '.join(set(mail)))
   mail=[]
  self.wdgt.filename=re.sub(r'^(.*)[.]txt$','\\1',self.wdgt.filename)+'_people.txt'
  self.wdgt.after(3000,self.clean)
