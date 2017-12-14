#from tkinter import *
from Tkinter import *#for python 2.x
class listwidgetc(Frame):
 def __init__(self,parent=None):
  Frame.__init__(self,parent)
  self.pack(side=LEFT,expand=NO,padx=5)
  frm=Frame(self)
  frm.pack(side=BOTTOM,fill=BOTH)
  self.lwt=Listbox(frm,height=4,selectmode=SINGLE,exportselection=False)
  self.lwt.pack(side=LEFT)
  self.lwt.bind("<Key>",self.key)
  sbar=Scrollbar(frm)
  sbar.config(command=self.lwt.yview)
  self.lwt.config(yscrollcommand=sbar.set)
  sbar.pack(side=RIGHT,fill=Y)
 def populate(self,row):
  self.lwt.delete(0,self.lwt.size()-1)
  for irow in row:
   self.lwt.insert(END,irow[0])
 def key(self,event):
  print("key pressed")
  print(event.char)
if __name__=='__main__':
 listwidgetc().mainloop()
