import os,sys,re;sys.path.append(os.path.expanduser('~')+r'/tmp')
import MISC.ffmpeg.libm
import kivy;kivy.require('2.1.0')
from kivy.config import Config
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.videoplayer import VideoPlayer
#from kivy.graphics import Color,Rectangle
from kivy.app import App
import json
import PIL
from MISC.ffmpeg.libm import libc
from MISC.extra.debugwrite import print
import MISC.extra.disablemultitouch
from MISC.extra.contextmenu import ContextMenu
from MISC.extra.filepopup import FilePopup

class VideoPlayerImageAnnotation(BoxLayout):
 def __init__(self,*arg,**kwarg):
  super(VideoPlayerImageAnnotation,self).__init__(*arg,**kwarg)
  libi=libc()
#  self.COLORTHRESHOLD=10 #second
  self.COLORTHRESHOLD=5 #second
  self.colormap=[(1,0,0,1),(1,1,0,1),(0,1,0,1),(0,0,0,0)]
  self.childpointer=0
  self.imagepointer=0
  self.imagelist=sorted(json.loads(open('annotation.jsa').read()),key=lambda m:float(libi.getsecond(m['timestamp'])))
  for i in self.imagelist:
   i['timestamp']=float(libi.getsecond(i['timestamp']))
#  self.flag=[-1]*len(self.children)
  self.flag=[-2]*len(self.children)
  print(f'<=>VideoPlayerImageAnnoation.__init__ self.imagelist={self.imagelist}  self.ids={len(self.ids)}')

class BlinkImage(Image):
 pass

class VideoPlayer2(VideoPlayer):
 def __init__(self,*arg,**kwarg):
  super(VideoPlayer2,self).__init__(*arg,**kwarg)
  self.libi=MISC.ffmpeg.libm.libc()
  self.vpia=VideoPlayerImageAnnotation()
  self.contextmenu=ContextMenu(self,self.on_slot)

 def on_slot(self,*arg):
  print(f'><VideoPlayer2.on_slot')
  if arg[0]==FilePopup:
   self.source=arg[1][0]
   self.state='play'
  elif arg[0]==self.contextmenu:
   if arg[1]=='open':
    FilePopup.get(self.on_slot,filters=('*.webm','*.mp4','*.mp3','*.wav'))
   elif arg[1]=='close':
    self.state='stop'
    if not os.path.exists('black.png'):
     PIL.Image.new('RGBA',(400,300),(0,0,0,255)).save('black.png')
    self._video.set_texture_from_resource('black.png')
    self.source=''
   elif arg[1]=='play' or arg[1]=='resume':
    self.state='play'
   elif arg[1]=='pause':
    self.state='pause'

 def on_touch_down(self,touch):
  print(f'><VideoPlayer2.on_touch_down rightclick touch={touch}')
  if touch.button=='right':
   self.contextmenu.open(touch.pos,*(('open',) if not self.source else ('open','pause','close') if self.state=='play' else ('open','resume','close')))
  super(VideoPlayer2,self).on_touch_down(touch)

 def seek(self,percent,precise=True):
  super(VideoPlayer2,self).seek(percent,precise)
  print(f'><VideoPlayer2.seek duration={self.duration} percent={percent} precise={precise}')
  value=self.duration*percent
  self.vpia.imagepointer=self.adjustimagepointer(self.duration*percent)
#  self.vpia.flag=[-1]*len(self.vpia.children)
  self.vpia.flag=[-2]*len(self.vpia.children)
  self.vpia.childpointer=0
  for i in range(len(self.vpia.children)):
   self.vpia.children[i].source=''
   self.vpia.children[i].opacity=0
  print(f'<=>VideoPlayer2.seek imagepointer={self.vpia.imagepointer}')
 def adjustimagepointer(self,timestamp):
  mini=0;maxi=len(self.vpia.imagelist)
  i=int(mini+(maxi-mini)/2)
  while((maxi-mini)>1):
   print(f'<=>VideoPlayer2.adjusttimestamp i={i} mini={mini} maxi={maxi} timestamp={timestamp}')
   if self.vpia.imagelist[i]['timestamp']<timestamp:
    mini=i
    i=int(mini+(maxi-mini)/2)
   elif self.vpia.imagelist[i]['timestamp']>timestamp:
    maxi=i
    i=int(mini+(maxi-mini)/2)
   else:
    break
  return i+1 if self.vpia.imagelist[i]['timestamp']<timestamp else i
 def on_position(self,instance,value):
#  print(f'><VideoPlayer2.on_position instance={instance} value={value} imagepointer={self.vpia.imagepointer} flag={self.vpia.flag}')
  super(VideoPlayer2,self).on_position(instance,value)
  count=0
  if self.vpia.parent==None:
   self.container.add_widget(self.vpia)
  for i in [i for i in range(min(len(self.vpia.imagelist)-self.vpia.imagepointer,len(self.vpia.children))) if (self.vpia.imagelist[self.vpia.imagepointer+i]['timestamp']-value) < self.vpia.COLORTHRESHOLD*3 and max((self.vpia.imagelist[self.vpia.imagepointer+i]['timestamp']-value)//self.vpia.COLORTHRESHOLD,-1) != self.vpia.flag[i]]:
   print(f'<=>VideoPlayer2.on_position i={i} imagepointer={self.vpia.imagepointer} value={value} flag={self.vpia.flag}')
   self.vpia.flag[i]=max((self.vpia.imagelist[self.vpia.imagepointer+i]['timestamp']-value)//self.vpia.COLORTHRESHOLD,-1)
   print(f'<=>VideoPlayer2.on_position flag={self.vpia.flag}')
   if self.vpia.imagelist[self.vpia.imagepointer+i]['timestamp'] >= value:
    self.vpia.children[(self.vpia.childpointer+i)%len(self.vpia.children)].kvbordercolor=[x/2 if i!=0 else x for x in self.vpia.colormap[min(int((self.vpia.imagelist[self.vpia.imagepointer+i]['timestamp']-value)/self.vpia.COLORTHRESHOLD),3)]]
    self.vpia.children[(self.vpia.childpointer+i)%len(self.vpia.children)].opacity=1
    self.vpia.children[(self.vpia.childpointer+i)%len(self.vpia.children)].source=self.vpia.imagelist[self.vpia.imagepointer+i]['source']
   else:
    print(f'<=>VideoPlayer.on_position i={i} imagepointer={self.vpia.imagepointer} childpointer={self.vpia.childpointer} count={count} value={value} imagelist={self.vpia.imagelist}')
    self.vpia.children[(self.vpia.childpointer+i)%len(self.vpia.children)].source=''
    self.vpia.children[(self.vpia.childpointer+i)%len(self.vpia.children)].opacity=0
    count+=1
#  self.vpia.imagelist[0:count]=''
  if count:
#   [self.vpia.flag.append(self.vpia.flag.pop(0)) for i in range(count)]
#   self.vpia.flag=[-1]*len(self.vpia.children)
   self.vpia.flag=[-2]*len(self.vpia.children)
   self.vpia.childpointer=(self.vpia.childpointer+count)%len(self.vpia.children)
   self.vpia.imagepointer=self.vpia.imagepointer+count
   self.on_position(self,value)
#   self.vpia.children[self.vpia.childpointer].kvbordercolor=self.vpia.colormap[min(int((self.vpia.imagelist[self.vpia.imagepointer]['timestamp']-value)//self.vpia.COLORTHRESHOLD),3)]
   print(f'<=>VideoPlayer2.on_position value={value} count={count} flag={self.vpia.flag} imagepointer={self.vpia.imagepointer} self.vpia.childpointer={self.vpia.childpointer}')

class VideoAnnotationApp(App):
 def build(self):
  return VideoPlayer2()

if __name__=='__main__':
 VideoAnnotationApp().run()
