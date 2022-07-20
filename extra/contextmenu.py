import kivy;kivy.require('2.1.0')
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown

class ContextMenu(DropDown):
 BUTTONWIDTHHEIGHT=(150,40)
 def __init__(self,parent,slot,mode,*arg,**kwarg):#mode='external' for external control on on_touch_down
  super(ContextMenu,self).__init__(**kwarg)
  print(f'ContextMenu.__init__ parent={parent} slot={slot} mode={mode} arg={arg}')
  self.button=Button(text='invisible',size_hint=(None,None),width=self.BUTTONWIDTHHEIGHT[0],height=self.BUTTONWIDTHHEIGHT[1])
  self.button.parent=parent
  self.button.opacity=0
  self.button.disabled=True
  self.touch=None
  self._mode=self.mode=mode
  for i in arg:
   button=Button(text=i,size_hint=(None,None),width=self.BUTTONWIDTHHEIGHT[0],height=self.BUTTONWIDTHHEIGHT[1])
   button.bind(on_release=lambda btn:self.select(btn.text))
   self.add_widget(button)
  self.bind(on_select=slot)
 def push(self,*arg):
  print(f'><ContextMenu.push arg={arg} len(self.container.children)={len(self.container.children)} text={[x.text for x in self.container.children]}')
  for count,i in enumerate(arg):
   if len(self.container.children)>count:
    self.container.children[-1-count].text=i
    self.container.children[-1-count].disabled=False
    self.container.children[-1-count].opacity=1
   else:
    button=Button(text=i,size_hint=(None,None),width=self.BUTTONWIDTHHEIGHT[0],height=self.BUTTONWIDTHHEIGHT[1])
    button.bind(on_release=lambda btn:self.select(btn.text))
    self.add_widget(button)
  for i in self.children[len(arg):-1]:
   i.opacity=0
   i.disabled=True
 def open(self,pos):
  print(f'><ContextMenu.open self={self} pos={pos} self.mode={self.mode} self._mode={self._mode}')
  self.button.pos=tuple([x-self.button.parent.pos[count] for count,x in enumerate(pos)])
  if not self.parent==None:
   self._mode=None
   self.dismiss()
  else:
   super(ContextMenu,self).open(self.button)
 def on_touch_down(self,touch):
  print(f'><ContextMenu.on_touch_down touch={touch}')
  if touch.button=='right':
   if not self.collide_point(*touch.pos):
    self.touch=touch
   else:
    self.touch=None
  if not touch.button=='right' or self.mode==None:
   return super(ContextMenu,self).on_touch_down(touch)
 def on_dismiss(self):
  print(f'><ContextMenu.on_dismiss self.touch={self.touch} __mode={self.mode}')
  if self.touch and self._mode==None:
   self.open(self.touch.pos)
   self.touch=None
   self._mode=self.mode
  self.touch=None
