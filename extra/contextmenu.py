import kivy;kivy.require('2.1.0')
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from debugwrite import print

class ContextMenu(DropDown):
 BUTTONWIDTHHEIGHT=(150,40)
 def __init__(self,parent,slot,*arg,**kwarg):#mode='external' for external control on on_touch_down
  '''\
    parent - parent of hidden button typically current widget on which contextmenu would be drawn
    slot - dropdown on_select button slot
  '''
  super(ContextMenu,self).__init__(**kwarg)
  print(f'><ContextMenu.__init__ parent={parent} slot={slot} arg={arg}')
  self.button=Button(text='invisible',size_hint=(None,None),width=self.BUTTONWIDTHHEIGHT[0],height=self.BUTTONWIDTHHEIGHT[1])
  self.button.parent=parent
  self.button.opacity=0
  self.button.disabled=True
  self.touch=None
  if arg:
   self.push(*arg)
  self.bind(on_select=slot)

 def push(self,*arg):
  print(f'><ContextMenu.push arg={arg} len(self.container.children)={len(self.container.children)} text={[x.text for x in self.container.children]}')
  for count,i in enumerate(arg):
   if len(self.container.children)>count:
    self.container.children[-1-count].text=i
    self.container.children[-1-count].disabled=False
    self.container.children[-1-count].opacity=1
    self.container.children[-1-count].size_hint_y=None
    self.container.children[-1-count].height=self.BUTTONWIDTHHEIGHT[1]
   else:
    button=Button(text=i,size_hint=(None,None),width=self.BUTTONWIDTHHEIGHT[0],height=self.BUTTONWIDTHHEIGHT[1])
    button.bind(on_release=lambda btn:self.select(btn.text))
    self.add_widget(button)
  for i in self.container.children[0:len(self.container.children)-len(arg)]:
   i.size_hint_y=None
   i.height=0
   i.opacity=0
   i.disabled=True
   print(f'<=>push {i.text}')

 def open(self,pos,*arg):
  if arg:
   self.push(*arg)
  print(f'><ContextMenu.open self={self} pos={pos}')
#  self.button.pos=tuple([x-self.button.parent.pos[count] for count,x in enumerate(pos)])
  self.button.pos=pos
  if not self.parent==None:
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
  return super(ContextMenu,self).on_touch_down(touch)

 def on_dismiss(self):
  print(f'><ContextMenu.on_dismiss self.touch={self.touch}')
  if self.touch:
   self.open(self.touch.pos)
  self.touch=None
