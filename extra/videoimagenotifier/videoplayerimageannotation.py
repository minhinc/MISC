import os,sys;sys.path.append(os.path.expanduser('~')+r'/tmp')
import kivy;kivy.require('2.1.0')
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.videoplayer import VideoPlayer
from kivy.graphics import Color,Rectangle
from kivy.app import App
import json
from MISC.ffmpeg.libm import libc

class VideoPlayerImageAnnotation(BoxLayout):
 def __init__(self,*arg,**kwarg):
  super(VideoPlayerImageAnnotation,self).__init__(*arg,**kwarg)
  libi=libc()
#  self.imagelist=[]
  self.COLORTHRESHOLD=10 #second
  self.colormap=[(1,0,0,1),(1,1,0,1),(0,1,0,1),(0,0,0,0)]
  self.childpointer=0
  self.imagelist=sorted(json.loads(open('annotation.jsa').read()),key=lambda m:float(libi.getsecond(m['timestamp'])))
  for i in self.imagelist:
   i['timestamp']=float(libi.getsecond(i['timestamp']))
  for i in range(min(len(self.imagelist),len(self.children))):
   self.children[i].source=self.imagelist[i]['source']
  print(f'<=>VideoPlayerImageAnnoation.__init__ self.imagelist={self.imagelist}  self.ids={len(self.ids)}')

class BlinkImage(Image):
 pass

class VideoPlayer2(VideoPlayer):
 def __init__(self,*arg,**kwarg):
  super(VideoPlayer2,self).__init__(*arg,**kwarg)
  self.vpia=VideoPlayerImageAnnotation()
 def on_position(self,instance,value):
  super(VideoPlayer2,self).on_position(instance,value)
  count=0
#  print(f'><VideoPlayer2.on_position self={self} instance={instance} value={value}')
  if self.vpia.parent==None:
   self.container.add_widget(self.vpia)
  for i in [i for i in range(min(len(self.vpia.imagelist),len(self.vpia.children))) if (self.vpia.imagelist[i]['timestamp']-value) <= self.vpia.COLORTHRESHOLD*3]:
#   print(f'<=>VideoPlayer.on_position i={i} childpointer={self.vpia.childpointer} count={count}')
   if self.vpia.imagelist[i]['timestamp'] >= value:
    self.vpia.children[(self.vpia.childpointer+i)%len(self.vpia.children)].kvbordercolor=[x/2 if i!=0 else x for x in self.vpia.colormap[min(int((self.vpia.imagelist[i]['timestamp']-value)/self.vpia.COLORTHRESHOLD),3)]]
   else:
    print(f'<=>VideoPlayer.on_position i={i} childpointer={self.vpia.childpointer} count={count} value={value} imagelist={self.vpia.imagelist}')
    if count+len(self.vpia.children) < len(self.vpia.imagelist):
     self.vpia.children[(self.vpia.childpointer+i)%len(self.vpia.children)].source=self.vpia.imagelist[len(self.vpia.children)+count]['source']
     self.vpia.children[(self.vpia.childpointer+i)%len(self.vpia.children)].kvbordercolor=[x/2 for x in self.vpia.colormap[min(int((self.vpia.imagelist[count+len(self.vpia.children)]['timestamp']-value)/self.vpia.COLORTHRESHOLD),3)]]
    else:
     self.vpia.children[(self.vpia.childpointer+i)%len(self.vpia.children)].opacity=0
#    self.vpia.children[(self.vpia.childpointer+i)%len(self.vpia.children)].reload()
    count+=1
  self.vpia.imagelist[0:count]=''
  self.vpia.childpointer=(self.vpia.childpointer+count)%len(self.vpia.children)
#  print(f'<=>VideoPlayer2.on_position self.vpia.children[0].source={self.vpia.children[0].source}')

class VideoAnnotationApp(App):
 def build(self):
  return VideoPlayer2(source=sys.argv[1],state='play')

if __name__=='__main__':
 VideoAnnotationApp().run()
