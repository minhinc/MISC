import threading,time
import os
import re
from fetchm import fetchc
#import urllib.request
import urllib2
class getcontactc(fetchc):
 def __init__(self,next,wgt,db):
  fetchc.__init__(self,next,wgt,db)
  if not os.path.exists(r'./data'):
   os.mkdir('./data')
  if not os.path.isfile(r'./data/link.txt'):
   open(r'./data/link.txt','a')
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
   self.wdgt.save()
   self.wdgt.btn.config(text='block')
   self.wdgt.entry.delete(0,'end')
   self.wdgt.text1.config(state='disabled')
   self.wdgt.entry.config(state='disabled')
   self.fetching=True
   threading.Thread(target=self.producer,args=(10,)).start()
 def timer(self):
  self.wdgt.filename=re.sub(r'^(.*)[.]txt$','\\1',self.wdgt.filename)+'_people.txt'
  self.wdgt.after_cancel(self.timerid)
  self.clean()
 def producer(self,arg):
  self.wdgt.text1.mark_set('insert','1.0')
  mail=[]
  junkstr=junkemail=r'^('
  for i in self.db.get('junkextension'):
   junkstr=junkstr+i[0]+r'|'
  junkstr=re.sub(r'\|$',r')$',junkstr)
  for i in self.db.get('junkemail'):
   junkemail=junkemail+i[0]+r'|'
  junkemail=re.sub(r'\|$',r')$',junkemail)
  print("junkstr %s" % junkstr)
  print("selffetching %d junkemail %s" % (self.fetching,junkemail))
  for line in [ line for line in open(self.wdgt.filename) if not re.search('^\s*(#|$)',line) and not self.db.search('linkvisited',re.sub(r'[^a-zA-Z0-9._%-]','_','https://www.google.co.in/search?q='+re.sub('\s+','+',line)+r'&btnG=Search',flags=re.I)) and self.fetching ]:
   self.addtag(re.sub(r'(^\s*|\s*$)','',line))
   try:
    data=repr(urllib2.urlopen(urllib2.Request('https://www.google.co.in/search?q='+re.sub('\s+','+',line)+r'&btnG=Search',headers={'User-Agent': 'Mozilla/44.0.2'}),timeout=90).read())
    self.db.fill('linkvisited',((re.sub(r'[^a-zA-Z0-9._%-]','_','https://www.google.co.in/search?q='+re.sub('\s+','+',line)+r'&btnG=Search'),),))
    for x in [ x for x in re.findall(r'url\?q=(http[^&]+)',data) if not self.db.search('linkvisited',re.sub(r'[^a-zA-Z0-9._%-]','_',x,flags=re.I)) and not re.search(junkstr,x,flags=re.I) and self.fetching ]:
     self.push(self.wdgt.text2,"%s\n" % (x))
     try:
      data=repr(urllib2.urlopen(urllib2.Request(x,headers={'User-Agent': 'Mozilla/44.0.2'}),timeout=10).read())
      self.db.fill('linkvisited',((re.sub(r'[^a-zA-Z0-9._%-]','_',x), ), ))
      mail.extend([ x for x in re.findall(r'([A-Za-z0-9._%-]+\@\w+[.](?:\w+[.]?)*\b)',data) if not re.search(junkemail,x,flags=re.I) ])
      print("mail" % mail)
     except:
      self.push(self.wdgt.text2,'error:'+x+'\n')
      pass
   except:
    self.push(self.wdgt.text2,'google error\n')
    pass
   if len(set(mail)):
    self.push(self.wdgt.text2,'#'+re.sub(r'(^\s*|\s*$)','',line)+'\n'+' '.join(set(mail))+'\n')
    open(re.sub(r'^(.*)[.]txt$','\\1',self.wdgt.filename)+'_people.txt','a').write('\n'+re.sub(r'(^\s*|\s*$)','',line)+' '+' '.join(set([x.lower() for x in mail])))
    mail=[]
  self.fetching=False
  self.timerid=self.wdgt.after(500,self.timer)
