import kivy;kivy.require('2.3.0')
import kivy.uix.boxlayout
import kivy.uix.button
import kivy.uix.label
import kivy.app
import sys,os,re;sys.path.append(os.path.expanduser('~')+'/tmp')
#import MISC.ffmpeg.gifm,MISC.ffmpeg.utilm,MISC.ffmpeg.libm

class _genericbar(kivy.uix.boxlayout.BoxLayout):
 def __init__(self,*,mode_='text',**kwarg):
  super(_genericbar,self).__init__(**kwarg)
  self.child=[]
  self.mode=mode_
  if re.search(r'^g',mode_,flags=re.I):
   print(f'{self.__class__=} {self.__class__.__subclasses__()=}')
   [self.child.append(i()) for i in self.__class__.__subclasses__()]

 def boxlayout(def, hashd_):
  tboxlayout=None
  if [x for x in hashd_ if type(x)==int]:
   tboxlayout=kivy.uix.boxlayout.BoxLayout('orientation'='horizontal' if not 'horizontal' in hashd_ else hashd_['orientation'])
   [tboxlayout.add_widget(self.boxlayout(hashd_[i])) for i in [x for x in hashd_ if type(x)==int]]
  else:
   tboxlayout=self.createwidge(hashd_)
  return tboxlayout
 def on_right_click(self):
  bind('on_click',add,self.add)
  bind('on_click',remove,self.remove)
  bind('on_click',ok,self.ok)
 def add(self):
  self.add_widget(self.hbar)
 def delete(self,point_):
  del ([x for x in self.child if (collidepoint,x)] or [None]][0]
 def filebrowser(self,wgt_):
  [x for x in self.child if x.mime()==mime(wdt_.text)][0]
class _text(_genericbar):
 def __init__(self):
  pass

class _app(kivy.app.App):
 def build(self):
  return _genericbar(mode_='g')

if __name__=='__main__':
 if len(sys.argv)>1 and re.search(r'^mode=g',sys.argv[1],flags=re.I):
  _app().run()
 else:
  print(f'this is text mode')
