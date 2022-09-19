import re,importlib
from io import StringIO
import sys
import kivy;kivy.require('2.1.0')
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.properties import ListProperty
from kivy.app import App
from MISC.extra.debugwrite import print

class TermBoxLayout(BoxLayout):
 def __init__(self,*arg,**kwarg):
  super(TermBoxLayout,self).__init__(*arg,**kwarg)
  print(f'><TermBoxLayout.__init__ arg={arg} kwarg={kwarg}')

 def set(self,*arg):
#  print(f'><TermBoxLayout.set arg={arg}')
  print(f'TermBoxLayout.set arg={arg}')
  if not arg[0] in globals():
   globals()[arg[0]]=importlib.import_module(arg[0])
  tmpvar=sys.stdout
  sys.stdout=tmpvar2=StringIO()
  print(eval(arg[0]+'.'+arg[1]+'('+','.join(x for x in arg[2:] if x)+')'))
  sys.stdout=tmpvar
#  self.ids['textinput'].text='\n'.join(' >>>'+x for x in re.split('\n',re.sub(r'^(.*?)\s*$',r'\1',tmpvar2.getvalue(),flags=re.I|re.DOTALL)))
  self.ids['textinput'].text='\n'.join(' '+x for x in re.split('\n',re.sub(r'^(.*?)\s*$',r'\1',tmpvar2.getvalue(),flags=re.I|re.DOTALL)))
  self.ids['label'].text=arg[0]+'.'+arg[1]+'()'

 def get(self):
  return self.ids['textinput'].text

class TermApp(App):
 def build(self):
  x=TermBoxLayout()
  globals()['test']=importlib.import_module('test')
  x.set('test','func2')
  return x

if __name__=='__main__':
 TermApp().run()
