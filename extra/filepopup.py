import re,os
import kivy;kivy.require('2.1.0')
#import disablemultitouch
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserIconView,FileChooserListView
from contextmenu import ContextMenu
from kivy.lang import Builder
from debugwrite import print

class FileChooserBoxLayout(BoxLayout):
 def __init__(self,*arg,**kwarg):
  super(FileChooserBoxLayout,self).__init__(*arg,**kwarg)
  print(f'><FileChooserBoxLayout {arg} {kwarg}')

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
  filters:[r'*.txt']
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

class MyFilePopup(Popup):
 '''call get(slot,options) passing slot def and catch on
    on_file_selection. arg->(MyFilePopup,[<file1>,<file2>])
    options are class attributes for FileChooserIconView,i.e. filters,
    i.e MyFilePopup(self.on_slot,filter=('*.mp4'),multiselect=True)'''
 def __init__(self,*arg,**kwarg):
  self.filechooserboxlayout=FileChooserBoxLayout()
  super(MyFilePopup,self).__init__(title="Load image(s)",content=self.filechooserboxlayout,size_hint=(0.8,0.8))
  self.register_event_type('on_file_selection')
  self.filechooserboxlayout.ids['buttonid'].bind(on_release=self.on_slot)
  self.contextmenu=ContextMenu(self,self.on_slot,"All","None")

 def get(self,slot,**kwarg):
  print(f'><MyFilePopup.get {kwarg}')
  self.bind(on_file_selection=slot)
  for key,value in kwarg.items():
   exec("self.filechooserboxlayout.ids['filechoosericonviewid']."+key+"=value")
  print(f"{self.filechooserboxlayout.ids['filechoosericonviewid'].filters}")
  self.open()

 def on_slot(self,*arg,**kwarg):
  print(f'><on_slot')
  if arg[0]==self.contextmenu:
   if re.search(r'^A',arg[1],flags=re.I):
    self.filechooserboxlayout.ids['filechoosericonviewid'].selection=[self.filechooserboxlayout.ids['filechoosericonviewid'].path+r'/'+x for x in os.listdir(self.filechooserboxlayout.ids['filechoosericonviewid'].path) if not os.path.isdir(self.filechooserboxlayout.ids['filechoosericonviewid'].path+r'/'+x) and re.search(r'[.]',x) and re.sub(r'^.*([.].*)$',r'\1',x) in [re.sub(r'^.*([.].*)$',r'\1',y) for y in self.filechooserboxlayout.ids['filechoosericonviewid'].filters]]
   elif re.search(r'^N',arg[1],flags=re.I):
    self.filechooserboxlayout.ids['filechoosericonviewid'].selection=[]
  if arg[0]==self.filechooserboxlayout.ids['buttonid']:
   self.dismiss()
   self.dispatch('on_file_selection',self.filechooserboxlayout.ids['filechoosericonviewid'].selection)
#  return self.filechooserboxlayout.ids['filechoosericonviewid'].selection

 def on_touch_down(self,touch):
  if touch.button=='right':
   self.contextmenu.open(touch.pos)
  return super(MyFilePopup,self).on_touch_down(touch)

 def on_file_selection(self,*arg):
  print(f'><MyFilePopup.on_file_selection {arg}')

FilePopup=MyFilePopup()
