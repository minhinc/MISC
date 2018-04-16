import re
import sys
from tkinter import *
#from Tkinter import *#python 2.7
class listwidgetc(Frame):
 def __init__(self,parent=None,widthp=20):
  Frame.__init__(self,parent)
  self.pack(side=LEFT,expand=NO,padx=5)
  frm=Frame(self)
  frm.pack(side=BOTTOM,fill=BOTH)
  self.lwt=Listbox(frm,height=4,width=widthp,selectmode=SINGLE,exportselection=False)
  self.lwt.pack(side=LEFT)
  sbar=Scrollbar(frm)
  sbar.config(command=self.lwt.yview)
  self.lwt.config(yscrollcommand=sbar.set)
  sbar.pack(side=RIGHT,fill=Y)
 def populate(self,row):
  self.lwt.delete(0,self.lwt.size()-1)
  for irow in row:
   self.lwt.insert(END,irow[0])
# def key(self,event,db):
#  print("key pressed")
#  print(event.char)
#  self.lwt.see([i for i,item in enumerate(db.get('country','name',orderby='id')) if re.search(r'^'+event.char,item[0],flags=re.I)][0])
#  self.lwt.activate([i for i,item in enumerate(db.get('country','name',orderby='id')) if re.search(r'^'+event.char,item[0],flags=re.I)][0])
if __name__=='__main__':
 listwidgetc().mainloop()
