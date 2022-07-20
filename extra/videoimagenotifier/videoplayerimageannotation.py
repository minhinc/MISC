import os,sys,re;sys.path.append(os.path.expanduser('~')+r'/tmp')
import MISC.ffmpeg.libm
import kivy;kivy.require('2.1.0')
from kivy.config import Config
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.videoplayer import VideoPlayer
#from kivy.graphics import Color,Rectangle
from kivy.app import App
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.popup import Popup
import json
from MISC.ffmpeg.libm import libc
Config.set('input','mouse','mouse,disable_multitouch')
Config.remove_option('input',r'%(name)s')

class VideoPlayerImageAnnotation(BoxLayout):
 def __init__(self,*arg,**kwarg):
  super(VideoPlayerImageAnnotation,self).__init__(*arg,**kwarg)
  libi=libc()
  self.COLORTHRESHOLD=10 #second
  self.colormap=[(1,0,0,1),(1,1,0,1),(0,1,0,1),(0,0,0,0)]
  self.childpointer=0
  self.imagepointer=0
  self.imagelist=sorted(json.loads(open('annotation.jsa').read()),key=lambda m:float(libi.getsecond(m['timestamp'])))
  for i in self.imagelist:
   i['timestamp']=float(libi.getsecond(i['timestamp']))
  self.flag=[-1]*len(self.children)
  print(f'<=>VideoPlayerImageAnnoation.__init__ self.imagelist={self.imagelist}  self.ids={len(self.ids)}')

class BlinkImage(Image):
 pass

class FileDialogFileChooserIconView(FileChooserIconView):
 def __init__(self,*arg,**kwarg):
  super(FileDialogFileChooserIconView,self).__init__(*arg,**kwarg)
  self.path=r'./'
  self.filters=['*.webm','*.mp4','*.mp3','*.wav']
  self._popup=Popup(title="Load video file",content=self,size_hint=(0.8,0.8))
 def openclose(self,*arg):
  print(f'><FileDialogFileChooserIconView.openclose arg={arg}')
  self._popup.open() if arg else self._popup.dismiss()

class ContextMenu(DropDown):
 def __init__(self,*arg,**kwarg):
  super(ContextMenu,self).__init__(*arg,**kwarg)
  self.button=Button(text='dingdong',size_hint=(None,None),width=200,height=40)
  self.button.opacity=0
  self.button.disabled=True
  self.touch=None
 def open(self,pos):
  print(f'><ContextMenu.open self={self} pos={pos}')
  self.button.pos=pos
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

class VideoPlayer2(VideoPlayer):
 def __init__(self,*arg,**kwarg):
  super(VideoPlayer2,self).__init__(*arg,**kwarg)
  self.libi=MISC.ffmpeg.libm.libc()
  self.vpia=VideoPlayerImageAnnotation()
  self._popup=FileDialogFileChooserIconView()
  self._popup.bind(on_submit=self.on_submit)
  self.contextmenu=ContextMenu()
  self.contextmenu.bind(on_select=self._popup.openclose)
  button=Button(text='Open',size_hint=(None,None),width=200,height=40)
  button.bind(on_release=lambda btn:self.contextmenu.select(btn.text))
  self.contextmenu.add_widget(button)
 def on_touch_down(self,touch):
  print(f'><VideoPlayer2.on_touch_down rightclick touch={touch}')
  if touch.button=='right':
   if self.contextmenu.button.parent==None:
    self.container.add_widget(self.contextmenu.button)
   self.contextmenu.open(touch.pos)
  super(VideoPlayer2,self).on_touch_down(touch)
 def on_submit(self,*arg):
  print(f'><VideoPlayer2.on_selection arg={arg}')
  self._popup.openclose()
  if re.search('(video|audio)',self.libi.exiftool(arg[1][0],'MIME Type'),flags=re.I):
   self.source=arg[1][0]
   self.state='play'
 def seek(self,percent,precise=True):
  super(VideoPlayer2,self).seek(percent,precise)
  print(f'><VideoPlayer2.seek duration={self.duration} percent={percent} precise={precise}')
  value=self.duration*percent
  self.vpia.imagepointer=self.adjustimagepointer(self.duration*percent)
  self.vpia.flag=[-1]*len(self.vpia.children)
  self.vpia.childpointer=0
  for i in range(len(self.vpia.children)):
   self.vpia.children[i].source=''
   self.vpia.children[i].opacity=0
  print(f'<=>VideoPlayer2.seek imagepointer={self.vpia.imagepointer}')
  '''
   if tmpimagepoiner>self.vpia.imagepointer:
    self.vpia.childpointer+=(self.tmpimagepointer-self.vpia.imagepointer)%len(self.vpia.children)
    for i in range((self.tmpimagepointer-self.vpia.imagepointer)%len(self.vpia.children)):
     if len(self.vpia.imagelist)-self.vpia.tmpimagepoiner>=len(self.vpia.children)+i:
      self.vpia.children[(self.childpointer+1)%len(self.vpia.children)].source=self.vpia.imagelist[tmpimagepointer+i].source
     else:
      self.vpia.children[i].opacity=0
    self.vpia.childpointer=(self.tmpimagepointer-self.vpia.imagepointer)%len(self.vpia.children)
   elif tmpimagepointer<self.vpia.imagepointer:
    for i in range((self.vpia.imagepointer-tmpimagepointer)%len(self.vpia.children)):
     if (self.vpia.imagepointer+(tmpimagepointer-i)%len(self.vpia.children))>len(self.vpia.imagelist):
      self.vpia.children[(self.vpia.childpointer-i)%len(self.vpia.children)].opacity=0
     else:
      self.vpia.children[(self.vpia.childpointer-i)%len(self.vpia.children)].source=(self.vpia.imagelist[(self.vpia.imagepointer+(tmpimagepointer-i)%len(self.vpia.children)].source
     if len(self.vpia.imagelist
  '''
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
  '''
  if value<self.vpia.colorthresholdbegin or value > self.vpia.colorthresholdbegin+self.vpia.COLORTHRESHOLD:
   tmpimagepointer=self.vpia.imagepointer
   self.vpia.imagepointer=adjustimagepointer(value)
   tmpimagepointer=tmpimagepointer-self.vpia.imagepointer
   if tmpimagepoiner>self.vpia.imagepointer:
    for i in range((self.tmpimagepointer-self.vpia.imagepointer)%len(self.vpia.children)):
     if len(self.vpia.imagelist)-self.vpia.imagepoiner>len(self.vpia.children)+i:
      self.vpia.children[i].source=self.vpia.imagelist[self.vpia.imagepoiner+len(self.vpia.children)+i].source
     else:
      self.vpia.children[i].opacity=0
    self.vpia.childpointer=(self.tmpimagepointer-self.vpia.imagepointer)%len(self.vpia.children)
   elif tmpimagepointer<self.vpia.imagepointer:
    for i in range((self.vpia.imagepointer-tmpimagepointer)%len(self.vpia.children)):
     if (self.vpia.imagepointer+(tmpimagepointer-i)%len(self.vpia.children))>len(self.vpia.imagelist):
      self.vpia.children[(self.vpia.childpointer-i)%len(self.vpia.children)].opacity=0
     else:
      self.vpia.children[(self.vpia.childpointer-i)%len(self.vpia.children)].source=(self.vpia.imagelist[(self.vpia.imagepointer+(tmpimagepointer-i)%len(self.vpia.children)].source
     if len(self.vpia.imagelist
  '''
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
    '''
     self.vpia.children[(self.vpia.childpointer+i)%len(self.vpia.children)].source=self.vpia.imagelist[self.vpia.imagepointer+len(self.vpia.children)+count]['source']
    if count+len(self.vpia.children) < (len(self.vpia.imagelist)-self.vpia.imagepointer):
     self.vpia.children[(self.vpia.childpointer+i)%len(self.vpia.children)].source=self.vpia.imagelist[self.vpia.imagepointer+len(self.vpia.children)+count]['source']
     self.vpia.children[(self.vpia.childpointer+i)%len(self.vpia.children)].opacity=1
     self.vpia.children[(self.vpia.childpointer+i)%len(self.vpia.children)].kvbordercolor=[x/2 for x in self.vpia.colormap[min(int((self.vpia.imagelist[self.vpia.imagepointer+count+len(self.vpia.children)]['timestamp']-value)/self.vpia.COLORTHRESHOLD),3)]]
    else:
     self.vpia.children[(self.vpia.childpointer+i)%len(self.vpia.children)].opacity=0
     self.vpia.children[(self.vpia.childpointer+i)%len(self.vpia.children)].source=''
    '''
    count+=1
#  self.vpia.imagelist[0:count]=''
  if count:
#   [self.vpia.flag.append(self.vpia.flag.pop(0)) for i in range(count)]
   self.vpia.flag=[-1]*len(self.vpia.children)
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
