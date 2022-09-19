import re,os
import sys;sys.path.append(os.path.expanduser('~')+r'/tmp/')
import kivy;kivy.require('2.1.0')
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
import MISC.extra.disablemultitouch
from load import LoadBoxLayout
from func import InplaceBoxLayout,FuncGridLayout
from term import TermBoxLayout
from MISC.extra.debugwrite import print

class TopBoxLayout(BoxLayout):
 def __init__(self,*arg,**kwarg):
  super(TopBoxLayout,self).__init__(*arg,**kwarg)
  print(f'><LoadBoxLayout.__init__ ids={self.ids}')
  self._popup=None
  self.modulefuncarg=[]
  self.loadboxlayout=LoadBoxLayout()
  self.loadboxlayout.bind(on_loadboxlayout=self.defaultcallback)
  self.ids['funcgridlayout'].bind(on_funcgridlayout=self.defaultcallback)
 def filebutton(self, *arg):
  print(f'><TopBoxLayout.filebutton arg={arg} self={self}')
  if re.search(r'^load$',self.ids['button'].text,flags=re.I):
   self._popup = Popup(title="Load file", content=self.loadboxlayout,size_hint=(0.9, 0.9)) if not self._popup else self._popup
   self._popup.open()
  elif re.search(r'^ok$',self.ids['button'].text,flags=re.I):
   self.ids['termboxlayout'].size_hint_y=0.7
   self.ids['funcgridlayout'].size_hint_y=0.1
   self.modulefuncarg[2:]=self.ids['funcgridlayout'].get()
   self.ids['termboxlayout'].set(*self.modulefuncarg)
   self.ids['button'].text='Quit'
  elif re.search(r'^quit$',self.ids['button'].text,flags=re.I):
   App.get_running_app().stop()
 def defaultcallback(self,instance,value):
  print(f'><TopBoxLayout.defaultcallback instance={instance} value={value}')
  if instance==self.loadboxlayout:
   if self._popup:
    self._popup.dismiss()
   if value:
    self.modulefuncarg[0:2]=value
    self.ids['funcgridlayout'].set(*value)
  elif instance==self.ids['funcgridlayout']:
   self.ids['termboxlayout'].size_hint_y=1
   self.ids['funcgridlayout'].size_hint_y=1
   if value and not re.search(r'^\s*$',value):
    self.ids['button'].text='Ok'
   else:
    self.ids['button'].text='Load'
class MyApp(App):
 def build(self):
  return TopBoxLayout()
if __name__=='__main__':
 MyApp().run()
