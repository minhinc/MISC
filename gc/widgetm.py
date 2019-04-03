import re
import sys
from tkinter import *
#from Tkinter import *#for python2.7
import listwidgetm
class scrolledtextc(Frame):
 def __init__(self,parent=None):
  Frame.__init__(self,parent)
  self.filename=None
  self.password=None
  self.od=self.nd=None
  self.state=None
  self.pack(expand=YES,fill=BOTH)

  self.frm=Frame(self)
  self.frm.pack(side=BOTTOM,expand=YES,fill=X)
  self.btn=Button(self.frm,text='fetch',padx=40,font=('helvetica',14,'normal'))
  self.btn.pack(side=RIGHT)
  self.lbl=Label(self.frm,text='  Minh Inc  ',font=('Tw Cen MT',30,'bold'),fg='#204020')
  self.lbl.pack(side=RIGHT)
  self.entry=Entry(self.frm,width=50)
  self.entry.pack(side=LEFT,expand=NO,fill=X)
  self.entry.bind('<Return>',self.fetch)
  self.entryc=Entry(self.frm,width=5,background='#004000')
  self.entryc.pack(side=LEFT,expand=NO,fill=X)

  self.frm2=Frame(self)
  self.lwtech=listwidgetm.listwidgetc(self.frm2,8)
  self.lwcity=listwidgetm.listwidgetc(self.frm2,12)
  self.lwcountry=listwidgetm.listwidgetc(self.frm2)
#  self.lwmtopic=listwidgetm.listwidgetc(self.frm2)

  self.m=PanedWindow(self)
  self.m.pack(expand=YES,fill=BOTH)
  tf1=Frame(self.m) 
  tf1.pack(expand=YES,fill=BOTH)
  tf2=Frame(self.m)
  tf2.pack(expand=YES,fill=BOTH)
  sbar1=Scrollbar(tf1)
  sbar2=Scrollbar(tf2)
  self.text1=Text(tf1,relief=SUNKEN,font=('Tw Cen MT',12,'normal'))
  self.text2=Text(tf2,relief=SUNKEN,font=('Tw Cen MT',9,'normal'))
  sbar1.config(command=self.text1.yview)
  self.text1.config(yscrollcommand=sbar1.set)
  sbar2.config(command=self.text2.yview)
  self.text2.config(yscrollcommand=sbar2.set)
  sbar1.pack(side=RIGHT,fill=Y)
  self.text1.pack(side=LEFT,expand=YES,fill=BOTH)
  sbar2.pack(side=RIGHT,fill=Y)
  self.text2.pack(side=RIGHT,expand=YES,fill=BOTH)
  self.m.add(tf1)
  self.m.add(tf2)
  self.text1.config(width=50)
  self.text2.config(width=50)
 def hide(self):
  self.frm2.pack_forget()
 def show(self):
  self.frm.pack_forget()
  self.m.pack_forget()
  self.frm.pack(side=BOTTOM,expand=YES,fill=X)
  self.frm2.pack(side=BOTTOM,anchor=SW,expand=NO) 
  self.m.pack(side=BOTTOM,expand=YES,fill=BOTH)
 def save(self):
  open(self.filename,'w').write(self.text1.get(1.0,'end'+'-1c'))
 def fetch(self,event):
  matchobjsas=re.match(r'^\s*[<:](\w+[.]\w+)',self.entry.get())
  matchobj=re.match(r'/?(.*)/(.*)/?',self.entry.get())
  matchobjopn=re.match(r'^\s*(\w+[.]\w+)',self.entry.get())
  if(self.state and self.state=="password"):
   self.password=self.entry.get()
   self.state=None
  elif(self.state and self.state=="filename"):
   self.filename=self.entry.get()
   self.state=None
  elif(matchobjsas):
   self.filename=matchobjsas.group(1)
   open(matchobjsas.group(1),'w').write(self.text1.get(1.0,'end'+'-1c'))
  elif(matchobj):
   self.od=self.text1.get('1.0','end'+'-1c')
   self.nd=re.sub(matchobj.group(1),matchobj.group(2),self.od,flags=re.M)
   self.text1.delete('1.0','end')
   self.text1.insert('1.0',self.nd)
  elif(self.entry.get()=='u' or self.entry.get()=='U'):
   if(self.text1.get('1.0','end'+'-1c')==self.nd):
    self.text1.delete('1.0','end')
    self.text1.insert('1.0',self.od)
   else:
    self.text1.delete('1.0','end')
    self.text1.insert('1.0',self.nd)
  elif(matchobjopn):
   self.filename=matchobjopn.group(1)
   self.text1.delete('1.0','end')
   self.text1.insert('1.0',open(matchobjopn.group(1)).read())
if __name__=='__main__':
 root=Tk()
 if len(sys.argv) > 1:
  st=scrolledtextc(file=sys.argv[1])
 else:
  st=scrolledtextc(text='Words\ngo here')
 root.bind('<Key-Escape>',show)
 root.mainloop()
