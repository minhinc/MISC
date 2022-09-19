import re,importlib,sys
import kivy;kivy.require('2.1.0')
from kivy.uix.dropdown import DropDown
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.button import Button
from kivy.app import App
from MISC.extra.debugwrite import print

class LoadBoxLayout(BoxLayout):
 dropdown=DropDown()
 def __init__(self,*arg,**kwarg):
  super(LoadBoxLayout,self).__init__(*arg,**kwarg)
  self.modulename=None
  self.register_event_type('on_loadboxlayout')
  self.buttonlist=[]
  print(f'<=>LoadBoxLayout.__init__ self.ids["button"].text={self.ids["button"].text}')
  self.dropdown.bind(on_select=lambda instance,text:setattr(self.ids['button'],'text',text))
  print(f'<>LoadBoxLayout.__init__ ids={len(self.ids)}')
 def load(self,path,filename,mode):
  print(f'><LoadBoxLayout.load path={path} filename={filename} mode={mode} self={self}')
  if len(filename) and re.search(r'[.]py$',filename[0]) and re.search(r'^selection$',mode,flags=re.I):
   if not re.sub(r'^(.*)/.*$',r'\1',filename[0]) in sys.path:
    sys.path[0:0]=[re.sub(r'^(.*)/.*$',r'\1',filename[0])]
   self.modulename=re.sub(r'.*/(.*)[.]\w+$',r'\1',filename[0])
   print(f'<=>modulename={self.modulename}')
   self.ids['button'].height=40
   self.ids['button'].size_hint_x=1
   self.ids['button'].pos_hint={'center_x':0.5,'top':1}
   self.ids['button'].text=self.modulename
   self.ids['button'].background_color=1,0,0,1
   if not self.modulename in globals():
    globals()[self.modulename]=importlib.import_module(self.modulename)
   for count,i in enumerate([i for i in dir(globals()[self.modulename]) if not re.search(r'^__',i)]):
    if len(self.buttonlist)<=count:
     self.buttonlist.append(Button(size_hint_y=None,height=40))
     self.buttonlist[-1].bind(on_release=lambda btn:self.dropdown.select(btn.text))
     self.dropdown.add_widget(self.buttonlist[-1])
    self.buttonlist[count].text=i
    self.buttonlist[count].opacity=1.0
    self.buttonlist[count].disabled=False
    print(f'<=>LoadBoxLayout.load i={i}')
   for i in self.buttonlist[count+1:]:
    print(f'<=>LoadBoxLayout.load i={i} opacity={i.opacity} i.text={i.text}')
    i.opacity=0
    i.disabled=True
   print(f'<=>LoadBoxLayout.load self.ids["button"].text={self.ids["button"].text}')
   self.dropdown.open(self.ids['button'])
  elif re.search(r'^load$',mode,flags=re.I) and self.modulename:
   print(f'<=>LoadBoxLayout.load dispatching {(self.modulename,self.ids["button"].text)}')
   self.dispatch('on_loadboxlayout',(self.modulename,self.ids['button'].text))
 def cancel(self):
  print(f'><LoadBoxLayout.cancel')
  self.dispatch('on_loadboxlayout',None)
 def on_loadboxlayout(self,*arg):
  print(f'><LoadBoxLayout.on_LoadBoxLayout_moduleloadevent arg={arg}')

class LoadApp(App):
 def build(self):
  return LoadBoxLayout()

if __name__=='__main__':
 LoadApp().run()
