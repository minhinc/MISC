import sys,os,re;sys.path.append(os.path.expanduser('~')+r'/tmp')
import kivy;kivy.require('2.1.0')
from kivy.clock import Clock
import kivy.uix.image
from kivy.app import App
from kivy.lang import Builder
from kivy.graphics import Rectangle
from PIL import Image
import MISC.extra.disablemultitouch
import sys
from scipy.spatial import minkowski_distance

def diff(image1_p,image2_p):
 image1buf=Image.open(image1_p).convert('RGB').tobytes()
 image2buf=Image.open(image2_p).convert('RGB').tobytes()
 i=maxdistance=minkdistance=0
 while i<len(image1buf):
  minkdistance=minkowski_distance([int(x) for x in image1buf[i:i+3]],[int(x) for x in image2buf[i:i+3]],2)
  print(f'processing image1buf={[int(x) for x in image1buf[i:i+3]]} image2buf={[int(x) for x in image2buf[i:i+3]]} minkdistance={minkdistance} i={i} maxdistance={maxdistance}') if minkdistance>maxdistance else None
  maxdistance=max(minkdistance,maxdistance)
  i+=3
 print(f'<>diff {maxdistance=}')
 return image1buf,image2buf,maxdistance

class MyWidget(kivy.uix.widget.Widget):
 def __init__(self,*arg,**kwarg):
  super(MyWidget,self).__init__(*arg,**kwarg)
  self.distanceindex=0
  self.distancedelta=1
  if len(sys.argv)>3:
   self.distancedelta=int(sys.argv[1])
   sys.argv[1:2]=[]
  self.image1,self.image2,self.maxdistance=diff(sys.argv[1],sys.argv[2])
  self.rec=None
  with self.canvas:
   self.rec=Rectangle(source=sys.argv[1])
  self.counter=0
  [os.remove(r'logdir/'+i) for i in os.listdir(r'logdir') if re.search(r'^.*/'+re.sub(r'(.*)[.].*$',r'\1',sys.argv[1]),i,flags=re.I)]
  Clock.schedule_interval(self.update_glsl,1/2)

# def on_touch_down(self,touch):
 def update_glsl(self,delta):
  self.distanceindex=min(self.distanceindex+self.distancedelta,self.maxdistance)
  self.rec.texture.blit_buffer(bytes([int(int(self.image1[count])+((int(self.image2[count])-int(self.image1[count]))*self.distanceindex)/self.maxdistance) for x in range(int(len(self.image1)/3)) for count in range(x*3,x*3+3)]),colorfmt='rgb')
  self.counter+=1
  self.canvas.ask_update()
  self.rec.texture.save(r'logdir/'+re.sub(r'(.*)[.].*$',r'\1',sys.argv[1])+str(self.counter).zfill(3)+'.png',flipped=False) if self.distanceindex!=self.maxdistance else None
  print(f'<>MyImage.on_touch_down {self.distanceindex}/{self.maxdistance}')

#  super(MyWidget,self).on_touch_down(touch)
 def on_size(self,*arg):
  print(f'><MyWidget.on_size {arg=}')
  self.rec.size=(min(self.width,self.height),min(self.width,self.height))
  self.rec.pos=(self.center_x-self.rec.size[0]/2,self.center_y-self.rec.size[1]/2)

class MyImageApp(App):
 def build(self):
#  return Builder.load_string(kv_string)
  return MyWidget()

if __name__=='__main__':
 MyImageApp().run()
