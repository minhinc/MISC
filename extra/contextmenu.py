import kivy;kivy.require('2.3.0')
import kivy.uix.button,kivy.uix.dropdown,kivy.uix.image,kivy.uix.label
from kivy.core.window import Window
from kivy.graphics import *
from .config import _configi;from .config import _configi as print

class _singletonmc(type):
 _instances={}
 def __call__(cls, *args, **kwargs):
  if cls not in cls._instances:
   cls._instances[cls]=super(_singletonmc,cls).__call__(*args,**kwargs)
  return cls._instances[cls]

class _contextmenuc(metaclass=_singletonmc):
 '''\
 Multi-Layer Hybrid ContectMenu for GUI application
 _contextmenui.open(('Add',('Remove',)),('Ok',('Cancel',)))\
 '''
 buttonwht=(140,34)
 imagewht=(buttonwht[0]//12,buttonwht[1]//3)
 horizontaloffset,verticaloffset=-1,buttonwht[1]-buttonwht[1]//12
 def __init__(self,**kwarg):
  '''\
  Initializer for contextmenu. Singleton class and generally instantiated through QML style 'at module parsing stage' available through '_contextmenui' attribute of the module
  **kwarg:dict - keyword arguments, generally no arguments
  _contextmenuc()#right now instantiated through QML singleton framework and available as _contextmenui attribute of the contextmenu module
  -> None\
  '''
  super(_contextmenuc,self).__init__(**kwarg)
  print(f'>< {kwarg=}')
  _configi.cac(self,('freewidgetl','btnh','txtt','activedropdownl','cb','menurightb'))
  self.freewidgetl=[]
  self.btnh,self.txtt,self.cb=None,None,None
  self.menurightb=True
  self.activedropdownl=[]
  _configi.cac(self.btnh,('dropdownw',))
  Window.bind(mouse_pos=self.on_mousehover)

 def dropdownclose(self,*, btnh_, addtofreelist_=False):
  print(f'>< {btnh_=} {addtofreelist_=}')
  if btnh_==None:
   return
  [self.dropdownclose(btnh_=i.btnh, addtofreelist_=addtofreelist_) for i in btnh_.dropdownw.container.children]
  if addtofreelist_==True:
   for i in btnh_.dropdownw.container.children:
    self.freewidgetl.append(i)
    if len(i.children)>0:
     self.freewidgetl.extend(i.children)
     [i.remove_widget(x) for x in i.children[:]]
   btnh_.dropdownw.clear_widgets()
   self.freewidgetl.append(btnh_.dropdownw)
   self.freewidgetl.append(btnh_)
  else:
   btnh_.dropdownw.dismiss()

 def on_mousehover(self,window_,pos_):
  '''\
  Mouse movement tracking on SDL Window
  window_:SDL Core Window - SDL Core Window
  pos_:tuple - new position of the mouse in screen coordinate\
  '''
#  print(f'>< {window_=} {pos_=}')
  btn=None
  activedropdown=[x for x in self.activedropdownl if x.collide_point(*pos_)]
  if activedropdown:
   for count,i in enumerate(activedropdown[-1].container.children):
    i.canvas.after.clear()
    if i.collide_point(pos_[0] - i.parent.parent.pos[0], pos_[1] - i.parent.parent.pos[1]):
     with i.canvas.after:
      Color(0.1,0.1,0.1,0.4)
      i.back_rect=Rectangle(pos=(activedropdown[-1].width//40,count*_contextmenuc.buttonwht[1]+activedropdown[-1].height//20),size=(int(_contextmenuc.buttonwht[0]*0.85),int(_contextmenuc.buttonwht[1]*0.9)))
    if i.btnh and i.btnh.dropdownw.attach_to and not i.collide_point(pos_[0] - i.parent.parent.pos[0], pos_[1] - i.parent.parent.pos[1]) and i.btnh.dropdownw in self.activedropdownl:
     print(f'<=> case 1 {i.text=}')
     self.dropdownclose(btnh_=i.btnh, addtofreelist_=False)
     self.activedropdownl.remove(i.btnh.dropdownw)
     if not btn==None:
      break
    elif i.btnh and not i.btnh.dropdownw.attach_to and i.collide_point(pos_[0] - i.parent.parent.pos[0], pos_[1] - i.parent.parent.pos[1]):
     print(f'<=> case 2 {i.text=}')
     btn=i
    elif i.btnh and i.btnh.dropdownw.attach_to and i.collide_point(pos_[0] - i.parent.parent.pos[0], pos_[1] - i.parent.parent.pos[1]):
     [ii.canvas.after.clear() for ii in i.btnh.dropdownw.container.children]
   if not btn==None:
    print(f'<=> Clearedd {btn.text=} {btn.btnh.dropdownw=} {activedropdown=}')
    self.activedropdownl.append(btn.btnh.dropdownw)
    btn.btnh.parent=self.btnh.parent
    if btn.parent.parent.pos[0]+2*_contextmenuc.buttonwht[0] > Window.width and self.menurightb==True:
     self.menurightb=False
    if self.menurightb==True:
     btn.btnh.pos=(btn.parent.parent.pos[0]+_contextmenuc.buttonwht[0]+_contextmenuc.horizontaloffset,btn.parent.parent.pos[1]+btn.pos[1]+_contextmenuc.verticaloffset)
    else:
     btn.btnh.pos=(btn.parent.parent.pos[0]-_contextmenuc.buttonwht[0],btn.parent.parent.pos[1]+btn.pos[1]+_contextmenuc.verticaloffset)
    btn.btnh.parent=self.btnh.parent
    print(f'<=> {btn.text=} {btn.btnh.dropdownw.container.children[0].text=} {len(btn.btnh.dropdownw.container.children)=} {btn.btnh.pos=} {pos_=} {btn.parent.parent.pos=}')
    btn.btnh.dropdownw.open(btn.btnh)

 def dropdowndismiss(self,dropdown_):
  print(f'>< {dropdown_=}')
  #dropdown_.on_dismiss()
  self.activedropdownl.remove(dropdown_) if dropdown_ in self.activedropdownl else None
  self.menurightb=True
  [i.canvas.after.clear() for i in dropdown_.container.children]
#  return False

 def dropdownselect(self,*dropdown_):
  print(f'>< {dropdown_=}')
  [x.dismiss() for x in self.activedropdownl if not x==dropdown_[0]]
  self.cb(dropdown_[1])

 def dropdowntouchdown(self,*dropdown_):
  print(f'>< {dropdown_=}')
  dropdown=None
  if not dropdown_[0].collide_point(*Window.mouse_pos):
   dropdown=[x for x in self.activedropdownl if x.collide_point(*Window.mouse_pos)]
   if not dropdown==[]:
    for i in dropdown[0].container.children:
     if i.collide_point(Window.mouse_pos[0]-dropdown[0].pos[0],Window.mouse_pos[1]-dropdown[0].pos[1]):
      i.dispatch('on_release')
      break
   [x.dismiss() for x in self.activedropdownl]

 def getimage(self,txtt_,count_=1):
#  print(f'>< {txtt_=} {count_=}')
  count=count_
  for i in txtt_:
   if len(i)>1 and 'sequence'==_configi.type(i[1]):
    count=max(self.getimage(i[1],count_=count_+1),count)
#  print(f'<> {txtt_=} {count=} {count_=}')
  if count_==1:
   if count>2:
    return 'arrowr.png'
   elif count>1:
    return 'arrowy.png'
   else:
    return 'arrow.png'
  else:
   return count

 def createdropdown(self, txtt_):
  '''\
  Create DropDown hierarchy from txtt_\
  '''
  print(f'>< {txtt_=}')
  btnh=self.getbuttondropdown(type_=kivy.uix.button.Button)
  [setattr(btnh,k,v) for k,v in dict(size_hint=(None,None),width=_contextmenuc.buttonwht[0],height=0,opacity=0,disabled=True).items()]
  btnh.dropdownw=self.getbuttondropdown(type_=kivy.uix.dropdown.DropDown,attach_to=None,parent=None)
  btnh.dropdownw.bind(on_dismiss=self.dropdowndismiss)
  btnh.dropdownw.bind(on_touch_down=self.dropdowntouchdown)
  btnh.dropdownw.bind(on_select=self.dropdownselect)
  for count,i in enumerate(txtt_):
   btnh.dropdownw.add_widget(self.getbuttondropdown(type_=kivy.uix.button.Button, size_hint=(None,None),width=_contextmenuc.buttonwht[0],height=_contextmenuc.buttonwht[1],opacity=1,disabled=False,text=i[0] if len(i)>1 and 'sequence'==_configi.type(i[1]) else i,parent=None))
   btnh.dropdownw.container.children[0].add_widget(self.getbuttondropdown(type_=kivy.uix.image.Image,source=self.getimage(i[1]),size=_contextmenuc.imagewht,pos=(_contextmenuc.buttonwht[0]-(3*_contextmenuc.imagewht[0])//2,(len(txtt_)-count-1)*_contextmenuc.buttonwht[1]+_contextmenuc.buttonwht[1]//2-_contextmenuc.imagewht[1]//2))) if len(i)>1 and 'sequence'==_configi.type(i[1]) else None
   btnh.dropdownw.container.children[0].bind(on_release=lambda btn:btnh.dropdownw.select(btn.text))
   btnh.dropdownw.container.children[0].btnh=self.createdropdown(i[1]) if len(i)>1 and 'sequence' == _configi.type(i[1]) else None
  return btnh

 def getbuttondropdown(self,type_,**kwarg_):
  '''Get DropDown/Button/Image widget from cache self.freewidgetl or create a new
  type_:kivy.uix.button.Button|kivy.uix.dropdown.DropDown|kivy.uix.image.Image - type of the widget to be created
  kwarg_:dict - key:value pair for the attributes of Button or DropDown or Image
  -> Button or DropDown or Image\
  '''
#  print(f'>< {type_=} {kwarg_=}')
  instance=[x for x in self.freewidgetl if type(x)==type_]
#  print(f'<=> {instance=}')
  if instance:
   [setattr(instance[0],k,v) for k,v in kwarg_.items()]
   self.freewidgetl.remove(instance[0])
   return instance[0]
  else:
   #return type_==kivy.uix.button.Button and kivy.uix.button.Button(**kwarg_) or type_==kivy.uix.dropdown.DropDown and kivy.uix.dropdown.DropDown(**kwarg_) or type_==kivy.uix.image.Image and kivy.uix.image.Image(**kwarg_)
   instance=type_==kivy.uix.button.Button and kivy.uix.button.Button(**kwarg_) or type_==kivy.uix.dropdown.DropDown and kivy.uix.dropdown.DropDown(**kwarg_) or type_==kivy.uix.image.Image and kivy.uix.image.Image(**kwarg_)
   if type_==kivy.uix.dropdown.DropDown:
    with instance.canvas.after:
     Color(0.5,0,0)
     instance.back_line=Line(width=1.2)
    instance.bind(pos=lambda *dropdown_:setattr(dropdown_[0].back_line,'points',[dropdown_[0].pos[0]+dropdown_[0].width//10,dropdown_[0].pos[1]+dropdown_[0].height-2,dropdown_[0].pos[0]+dropdown_[0].width-dropdown_[0].width//10,dropdown_[0].pos[1]+dropdown_[0].height-2]))
   return instance

 def open(self,**kwarg_):
  '''open contextmenu popup window. kwarg_ keywords are
   txtt_:tuple -> tuple of text, in case of multi-level contextmenu then recursive tuple of tuples. Defaults to last txtt_ passed as argument to open() function.
   parent_:Widget ->  Defaults to widget class calling this open() function
   pos_:tuple -> Mouse position defaults to Window.mouse_pos
   callbackfn_:function -> callback function need to be called once menuitem button pressed defaults to cb() function of widget class calling this open() function
   open(txtt_=(('Add',('Remove',)),('Ok',('Cancel',))))#propulate top level dropdown against instance/root hidden button
   open(txtt_=('One','Two'))#populate or show dropdown menu against hidden button btnh
   -> None\
  '''
  print(f'>< {kwarg_=}')
  _configi.cmh(kwarg_,('txtt_','parent_','pos_','callbacfn_'))
  kwarg_['txtt_']==self.txtt  if not 'txtt_' in kwarg_ else kwarg_['txtt_']
  if not kwarg_['txtt_']==self.txtt:
   self.dropdownclose(btnh_=self.btnh,addtofreelist_=True) if self.btnh else None
   self.btnh=self.createdropdown(kwarg_['txtt_'])
  self.activedropdownl=[self.btnh.dropdownw]
  self.txtt=kwarg_['txtt_']
  self.btnh.parent,self.btnh.pos=(kwarg_['parent_'] if 'parent_' in kwarg_ else _configi.getcallinginstance()),kwarg_['pos_'] if 'pos_' in kwarg_ else Window.mouse_pos
  self.cb=self.btnh.parent.cb if not 'callbackfn_' in kwarg_ else kwarg_['callbackfn_']
  self.menurightb=True
  self.btnh.dropdownw.open(self.btnh)
  print(f'<=> {self.btnh.parent=} {self.btnh.pos=}')
from MISC.extra.config import _configi;_configi.cmc(__name__,_contextmenuc)
