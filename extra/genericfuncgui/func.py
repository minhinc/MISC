import re,importlib
import inspect
import kivy;kivy.require('2.1.0')
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.properties import ListProperty
from kivy.app import App
from MISC.extra.debugwrite import print

class InplaceBoxLayout(BoxLayout):
 pass
class FuncGridLayout(GridLayout):
 def __init__(self,*arg,**kwarg):
  super(FuncGridLayout,self).__init__(*arg,**kwarg)
  self.inplaceboxlayout=[]
  self.register_event_type('on_funcgridlayout')
 def set(self,modulename,funcname):
  print(f'><FuncGridLayout.set modulename={modulename} funcname={funcname}')
  if not modulename in globals():
   print(f'<=>FuncGridLayout.set modulename={modulename}')
   globals()[modulename]=importlib.import_module(modulename)
#  for count,i in enumerate(eval(modulename+'.'+funcname+'.__code__.co_varnames')):
  for count,i in enumerate(inspect.signature(eval(modulename+'.'+funcname)).parameters.items()):
   print(f'<=>FuncGridLayout.set i={i}')
   if len(self.inplaceboxlayout)<=count:
    self.inplaceboxlayout.append(InplaceBoxLayout())
    self.add_widget(self.inplaceboxlayout[-1])
    self.inplaceboxlayout[-1].ids['textinput'].bind(text=self.inplaceboxlayouttextchanged)
   self.inplaceboxlayout[count].ids['label'].text=('*' if i[1].kind==inspect._ParameterKind.VAR_POSITIONAL else '**' if i[1].kind==inspect._ParameterKind.VAR_KEYWORD else '')+i[1].name+(r'('+re.sub(r'^.*class\s+[\'"](.*?)[\'"].*$',r'\1',str(type(i[1].default) if i[1].default!=inspect._empty else i[1].annotation))+r')' if i[1].annotation!=inspect._empty or i[1].default!=inspect._empty else '')
   if i[1].default!=inspect._empty:
    self.inplaceboxlayout[count].ids['textinput'].text=str(i[1].default)
   self.inplaceboxlayout[count].opacity=1.0
   self.inplaceboxlayout[count].disabled=False
  for i in self.inplaceboxlayout[count+1:]:
   i.opacity=0
   i.disabled=True
 def inplaceboxlayouttextchanged(self,instance,text):
  print(f'><FuncGridLayout.inplaceboxlayouttextchanged instance={instance} text={text}')
#  self.dispatch('on_funcgridlayout',text)
  self.dispatch('on_funcgridlayout',''.join(x.ids['textinput'].text for x in self.inplaceboxlayout))
 def get(self):
  return [str(x.ids['textinput'].text) for x in self.inplaceboxlayout]
 def on_funcgridlayout(self,*arg):
  pass
  print(f'><FuncGridLayout.on_funcgridlayout arg={arg}')

class FuncApp(App):
 def build(self):
  x=FuncGridLayout()
  globals()['test']=importlib.import_module('test')
  x.set('test','func2')
  return x

if __name__=='__main__':
 FuncApp().run()
