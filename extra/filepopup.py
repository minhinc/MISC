import re,os
import kivy;kivy.require('2.1.0')
#import disablemultitouch
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserIconView,FileChooserListView
from kivy.lang import Builder

class FileChooserBoxLayout(BoxLayout):
 def __init__(self,*arg,**kwarg):
  super(FileChooserBoxLayout,self).__init__(*arg,**kwarg)
  print(f'><FileChooserBoxLayout {arg=} {kwarg=}')

kvstring='''
#:kivy 2.1.0
#:import re re
<FileChooserBoxLayout>:
 orientation:'vertical'
 padding:10
 spacing:10
 FileChooserIconView:
  id:filechoosericonviewid
  path:'./'
  filters:[r'*.png',r'*.jpg',r'*.gif',r'*.jpeg']
  multiselect:False
 Button:
  id:buttonid
  size_hint_x:0.5
  size_hint_y:None
  pos_hint:{'center_x':0.5}
  height:40
  text:'Ok'
'''

Builder.load_string(kvstring)

class FilePopup(Popup):
 '''call get(slot,options) passing slot def and catch on
    on_file_selection. arg->(FilePopup,[<file1>,<file2>])
    options are class attributes for FileChooserIconView,i.e. filters,
    i.e FilePopup(self.on_slot,filter=('*.mp4'),multiselect=True)'''
 def __init__(self,*arg,**kwarg):
  self.filechooserboxlayout=FileChooserBoxLayout()
  super(FilePopup,self).__init__(title="Load image(s)",content=self.filechooserboxlayout,size_hint=(0.8,0.8))
  self.register_event_type('on_file_selection')
  self.filechooserboxlayout.ids['buttonid'].bind(on_release=self.on_slot)

 def get(self,slot,**kwarg):
  print(f'{kwarg=}')
  self.bind(on_file_selection=slot)
  for key,value in kwarg.items():
   exec("self.filechooserboxlayout.ids['filechoosericonviewid']."+key+"=value")
  print(f"{self.filechooserboxlayout.ids['filechoosericonviewid'].filters=}")
  self.open()

 def on_slot(self,*arg,**kwarg):
  print(f'><on_slot')
  if arg[0]==self.filechooserboxlayout.ids['buttonid']:
   self.dismiss()
   self.dispatch('on_file_selection',self.filechooserboxlayout.ids['filechoosericonviewid'].selection)
  return self.filechooserboxlayout.ids['filechoosericonviewid'].selection

 def on_file_selection(self,*arg):
  print(f'><FilePopup.on_file_selection {arg=}')

FilePopup=FilePopup()
