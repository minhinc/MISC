import threading,time
import os
import re
import datetime
import sys
import urllib.request as urllib2
#import urllib2#for python2.7
from fetchm import fetchc
sys.path.append('..')
#from util.utilm import utilc
from utillib import requestm
#import util.googlesearch
class getcontactc(fetchc):
 def __init__(self,next,wgt,db):
  fetchc.__init__(self,next,wgt,db)
 def handle(self):
  fetchc.handle(self)
  self.wdgt.state="filenname"
  self.wdgt.entry.delete(0,'end')
  self.wdgt.entry.insert(0,"Enter file name")
  self.wdgt.entryc.insert(0,"1")
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
   self.wdgt.entryc.config(state='disabled')
   self.fetching=True
   threading.Thread(target=self.producer,args=(10,)).start()
 def producer(self,arg):
  self.wdgt.text1.mark_set('insert','1.0')
  mail=[]
  linklist=[]
#  utili=utilc('utilm')
  #junkextn=r'^('+(''.join([x[0]+'|' for x in self.db.get('junkextension')]))[:-1]+')$'
  junkextn=r'('+(''.join([x[0]+'|' for x in self.db.get('junkextension')]))[:-1]+')'
  junkemail=r'^('+(''.join([x[0]+'|' for x in self.db.get('junkemail')]))[:-1]+')$'
  with open(re.sub(r'^(.*)[.]txt$','\\1',self.wdgt.filename)+'_people.txt','a') as file:
   file.write("%s#----------------%s" % ('\n' if os.stat(re.sub(r'^(.*)[.]txt$','\\1',self.wdgt.filename)+'_people.txt').st_size else '',str(datetime.datetime.now())))
  for line in [ line for line in open(self.wdgt.filename).read().split('\n') if not re.search('^\s*(#|$)',line) and not self.db.search('linkvisited',re.sub(r'[^a-zA-Z0-9._%-]','_','https://www.google.co.in/search?q='+re.sub('\s+','+',line)+r'&btnG=Search',flags=re.I)) ]:
   if not self.fetching:
    break
   self.addtag(re.sub(r'(^\s*|\s*$)','',line))
   try:
#    linklist=utili.getgoogle(line,int(self.wdgt.entryc.get()))
    linklist=requestm.getgoogle(line,int(self.wdgt.entryc.get()))
    self.db.fill('linkvisited',((re.sub(r'[^a-zA-Z0-9._%-]','_','https://www.google.co.in/search?q='+re.sub('\s+','+',line)+r'&btnG=Search'),),))
    self.db.update('linkvisited','date',int(re.sub('-','',datetime.date.today().isoformat())),'name',re.sub(r'[^a-zA-Z0-9._%-]','_','https://www.google.co.in/search?q='+re.sub('\s+','+',line)+r'&btnG=Search'))
    for x in [ x for x in set(linklist) if not self.db.search('linkvisited',re.sub(r'[^a-zA-Z0-9._%-]','_',x,flags=re.I)) and not re.search(junkextn,x,flags=re.I)]:
     self.push(self.wdgt.text2,"%s\n" % (x))
     try:
#      mail.extend([ x for x in re.findall(r'([A-Za-z0-9._%-]+\@[\w-]+[.](?:\w+[.]?)*\b)',utili.download(x)) if not re.search(junkemail,x,flags=re.I) ])
      mail.extend([ x for x in re.findall(r'([A-Za-z0-9._%-]+\@[\w-]+[.](?:\w+[.]?)*\b)',requestm.gets(x,head=True,get=True)) if not re.search(junkemail,x,flags=re.I) ])
     except Exception as e:
      self.push(self.wdgt.text2,'error:'+x,type(e),'\n')

    self.db.fill('linkvisited',[ (re.sub(r'[^a-zA-Z0-9._%-]','_',x),int(re.sub('-','',datetime.date.today().isoformat()))) for x in set(linklist) if not self.db.search('linkvisited',re.sub(r'[^a-zA-Z0-9._%-]','_',x,flags=re.I)) and not re.search(junkextn,x,flags=re.I) ],fetchmany=True)
   except:
    self.push(self.wdgt.text2,'google error\n')
   if len(set(mail)):
    if len(set(mail))<40:
     self.push(self.wdgt.text2,'#'+re.sub(r'(^\s*|\s*$)','',line)+'\n'+' '.join(set(mail))+'\n')
     with open(re.sub(r'^(.*)[.]txt$','\\1',self.wdgt.filename)+'_people.txt','a') as file:
      file.write("%s%s" % ('\n' if os.stat(re.sub(r'^(.*)[.]txt$','\\1',self.wdgt.filename)+'_people.txt').st_size else '',re.sub(r'(^\s*|\s*$)','',line).capitalize()+' '+' '.join(sorted(set([x.lower() for x in mail]),key=lambda x:0 if re.sub(r'.*?@(.).*',r'\1',x).lower()==line[0].lower() else 1))))
    else:
     print('--not included--#'+re.sub(r'(^\s*|\s*$)','',line)+'\n'+' '.join(set(mail)))
   mail=[]
  self.wdgt.filename=re.sub(r'^(.*)[.]txt$','\\1',self.wdgt.filename)+'_people.txt'
#  utili.close()
  self.wdgt.after(3000,self.clean)
