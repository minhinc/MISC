import re
class fetchc:
 def __init__(self,next,wgt,db):
  self.wdgt=wgt
  self.next=next
  self.db=db
  self.fetching=False
  self.timerid=None
 def handle(self):
  self.wdgt.btn.config(text='fetch',state='normal',command=self.get)
  self.wdgt.entry.config(state='normal')
  self.wdgt.text1.config(state='normal')
  self.wdgt.text2.config(state='normal')
  self.wdgt.entry.delete(0,'end')
  self.wdgt.text1.delete('1.0','end')
  self.wdgt.text2.delete('1.0','end')
  if(self.wdgt.filename):
   self.wdgt.text1.insert('1.0',open(self.wdgt.filename).read())
  self.wdgt.master.update()
 def push(self,wdgt,line):
  wdgt.config(state='normal')
  wdgt.insert('end',line)
  wdgt.see('end')
  self.wdgt.master.update()
  wdgt.config(state='disabled')
  self.wdgt.master.update()
 def addtag(self,line):
  where=self.wdgt.text1.search(line,'insert','end')
  while where and self.wdgt.text1.search(r'^\s*#',re.sub(r'[.].*$',r'.0',where),re.sub(r'[.].*$',r'.end',where),regexp=True):
   where=self.wdgt.text1.search(line,re.sub(r'[.].*$',r'.end',where),'end')
  if where:
   pasteit=where+('+%dc' % len(line))
   self.wdgt.text1.tag_remove('demo','1.0','end')
   self.wdgt.text1.tag_add('demo',where,pasteit)
   self.wdgt.text1.tag_config('demo',background='#004000',foreground='#ffffff')
   self.wdgt.text1.mark_set('insert',pasteit)
   self.wdgt.text1.see('insert')
   self.wdgt.master.update()
  return where
 def get(self):
  print('fetch::get')
 def fetch(self,event):
  print('fetch::fetch')
 def clean(self):
  self.wdgt.btn.config(text='Done')
  self.wdgt.entry.config(state='disabled')
  self.wdgt.btn.config(state='disabled')
  self.wdgt.text1.config(state='disabled')
  self.wdgt.text2.config(state='disabled')
  self.wdgt.master.update()
  if self.next:
   self.next.handle()
