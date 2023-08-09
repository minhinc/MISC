import re,os
import kivy;kivy.require('2.1.0')
import disablemultitouch
from kivy.core.window import Window
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.lang import Builder
from contextmenu import ContextMenu
from filepopup import FilePopup
from debugwrite import print

kvstring='''
#:kivy 2.1.0
#:import re re
<ClickImage>:
 canvas.before:
  Color:
   rgba: 0.267, 0.267, 0.267, 1
  Rectangle:
   pos: self.pos
   size: self.size
 Label:
  id:labelid
  size:self.texture_size
  font_size:'18sp'
  pos:[root.width*0.9-self.width,root.height-2*self.height]
  text:'[color=#666666]'+(root.source[root.source.rindex(r'/')+1:] if root.source and root.source.count(r'/') else root.source if root.source else '')+'[/color]'
  markup:True
'''
Builder.load_string(kvstring)

class ClickImage(Image):
 def __init__(self,*arg,**kwarg):
  super(ClickImage,self).__init__(*arg,**kwarg)
  print(f'><ClickImage.__init__ windowtype={type(Window)} ids={self.ids}')
  self.imagelist=None
  self.source=''
  self.imagepointer=0
  self._keyboard=None
  self.contextmenu=ContextMenu(self,self.on_slot,"Open")

 def _keyboard_closed(self):
  print(f'><ClickImage._keyboard_closed')
  self._keyboard.unbind(on_key_down=self.on_slot)
  self._keyboard=None

 def on_slot(self, *arg,**kwarg):
  print(f'><ClickImage.on_slot arg={arg}')
  if arg[0]==self.contextmenu:
   if re.search(r'^o',arg[1],flags=re.I):
    FilePopup.get(self.on_slot,filters=('*.jpeg','*.jpg','*.png','*.gif'),multiselect=True)
  elif arg[0]==FilePopup:
   self.imagelist=sorted(arg[1],key=lambda m:float(re.sub('^.*?([\d+.]+)(?:[.][^.]+)?$',r'\1',m)) if re.search(r'\d+([.].*)?$',m) else 0)
   print(f'<=>ClickImage.on_slot self.imagelist={self.imagelist}')
   self.imagepointer=0
   self.source=self.imagelist[self.imagepointer]
   print(f'<=>ClickImage.on_slot self.source={self.source} self.imagelist={self.imagelist} self.imagepointer={self.imagepointer}')
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
  return ClickImage()

if __name__=='__main__':
 ClickImageApp().run()
