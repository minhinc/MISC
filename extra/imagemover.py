import re,os
import kivy;kivy.require('2.1.0')
import disablemultitouch
from kivy.core.window import Window
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserIconView,FileChooserListView
from kivy.lang import Builder
from contextmenu import ContextMenu
kvstring='''
#:kivy 2.1.0
#:import re re
ClickImage:
# on_source:setattr(labelid,'text',root.source[root.source.rindex(r'/')+1:] if root.source.count(r'/') else '')
 Label:
  id:labelid
  size:self.texture_size
  font_size:'24sp'
#  pos_hint:{'right':0.8,'top':0.8}
  pos:[root.width*0.9-self.width,root.height-2*self.height]
#  font_size:int(root.width/60)
  text:root.source[root.source.rindex(r'/')+1:] if root.source.count(r'/') else ''
#  text_size:self.width,None
#  height:self.texture_size[1]
<FileChooserBoxLayout>:
 orientation:'vertical'
 padding:10
 spacing:10
 FileChooserIconViewCustom:
  id:filechoosericonviewid
  path:'./'
  filters:[r'*.png',r'*.jpg',r'*.gif',r'*.jpeg']
  multiselect:True
 Button:
  id:buttonid
  size_hint_x:0.5
  size_hint_y:None
  pos_hint:{'center_x':0.5}
  height:40
  text:'Ok'
'''
#Builder.load_string(kvstring)
class FileChooserBoxLayout(BoxLayout):
 pass
class FileChooserIconViewCustom(FileChooserIconView):
 def __init__(self,*arg,**kwarg):
  super(FileChooserIconViewCustom,self).__init__(*arg,**kwarg)
  self.contextmenu=ContextMenu(self,self.on_slot,None,"All","None")
 def on_touch_down(self,touch):
  print(f'><FileChooserIconViewCustom.on_touch_down touch={touch} pos={self.pos} size={self.size}')
  super(FileChooserIconViewCustom,self).on_touch_down(touch)
  if touch.button=='right':
   self.contextmenu.open(touch.pos)
  return True
 def on_slot(self,*arg):
  print(f'><FileChooserIconViewCustom.on_slot arg={arg} self.path={self.path}')
  if arg[0]==self.contextmenu:
   if re.search(r'^a',arg[1],flags=re.I):
    self.selection=[self.path+r'/'+x for x in os.listdir(self.path) if not os.path.isdir(self.path+r'/'+x) and re.search(r'[.](png|jpeg|jpg|giff)$',self.path+r'/'+x,flags=re.I)]
   elif re.search(r'^n',arg[1],flags=re.I):
    self.selection=[]
class ClickImage(Image):
 def __init__(self,*arg,**kwarg):
  super(ClickImage,self).__init__(*arg,**kwarg)
  print(f'<=>ClickImage.windowtype={type(Window)}')
  self.imagelist=None
  self.source=''
  self.imagepointer=0
  self._keyboard=None
  self.contextmenu=ContextMenu(self,self.on_slot,None,"Open")
  self.filechooserboxlayout=FileChooserBoxLayout()
  self._popup=Popup(title="Load image(s)",content=self.filechooserboxlayout,size_hint=(0.8,0.8))
  self.filechooserboxlayout.ids['buttonid'].bind(on_release=self.on_slot)
 def _keyboard_closed(self):
  print(f'><ClickImage._keyboard_closed')
  self._keyboard.unbind(on_key_down=self.on_slot)
  self._keyboard=None
 def on_slot(self, *arg,**kwarg):
  print(f'><ClickImage.on_slot arg={arg}')
  if arg[0]==self.contextmenu:
   if re.search(r'^o',arg[1],flags=re.I):
    self._popup.open()
  elif arg[0]==self.filechooserboxlayout.ids['buttonid']:
   self._popup.dismiss()
   self.imagelist=sorted(self.filechooserboxlayout.ids['filechoosericonviewid'].selection,key=lambda m:int(re.sub(r'.*?(\d+)([.].*)?$',r'\1',m)) if re.search(r'\d+([.].*)?$',m) else 0)
   print(f'<=>ClickImage.on_slot self.imagelist={self.imagelist}')
   self.imagepointer=0
   self.source=self.imagelist[self.imagepointer]
   self.reload()
   self._keyboard=Window.request_keyboard(self._keyboard_closed,self,'text')
   self._keyboard.bind(on_key_down=self.on_slot)
  elif arg[0]==self._keyboard:
   if arg[1][1] in ['up','down','left','right'] and self.imagelist:
    self.imagepointer=max(0,self.imagepointer-1) if arg[1][1] in ['left','down'] else min(len(self.imagelist)-1,self.imagepointer+1)
    self.source=self.imagelist[self.imagepointer]
    print(f'<=>CickImage.on_slot self.imagelist={self.imagelist} self.source={self.source} self.imagepointer={self.imagepointer}')
    self.reload()
 def on_touch_down(self,touch):
  print(f'><ClickImage.on_touch_down touch={touch}')
  if touch.button=='right':
   self._keyboard.release() if self._keyboard else None
   self.contextmenu.open(touch.pos)
  return super(ClickImage,self).on_touch_down(touch)
class ClickImageApp(App):
 def build(self):
  return Builder.load_string(kvstring)
#  return ClickImage()
if __name__=='__main__':
 app=ClickImageApp()
 app.run()
