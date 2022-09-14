import sys,re,os
import itertools
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.resources import resource_find
from kivy.graphics.transformation import Matrix
from kivy.graphics.opengl import glEnable, glDisable, GL_DEPTH_TEST
from kivy.graphics import RenderContext, Callback, PushMatrix, PopMatrix, \
    Color, Translate, Rotate, Mesh, UpdateNormalMatrix,BindTexture,Rectangle,Scale,InstructionGroup
import time
from objloader import ObjFile
import io
from PIL import Image,ImageDraw
from scipy.spatial import minkowski_distance
import math
sys.path.append(os.path.expanduser('~')+r'/tmp/')
import MISC.extra.disablemultitouch
from MISC.ffmpeg.utilm import utilc


class Renderer(Widget):
 def __init__(self, **kwargs):
  if len(sys.argv)<3:
   print('''\
  ---usage---
  python3 imageglobe.py <longitude,latitude> <mapimage> [annotation string]
  python3 imageglobe.py '24E,12S' globepolitical.png 'Mariana Trench'
  python3 imageglobe.py '24E,12S' globepolitical.png
  Image searched in ~/tmp/imageglobe/ coordinate searched in ~/tmp/MISC/image/index.txt''')
   sys.exit(-1)
  def gdegree(tup,pos=None):#23E,45S -> (23,-45)
   if type(tup)==tuple:
    tup=','.join(tup)
   tup=re.sub(r'[SsWw]','*-1',re.sub(r'[NnEe]','*1',tup))
   return tuple(eval(x) for x in re.split(',',tup))[pos if pos else slice(0,None)]
  xy=None
  degree=[]
  xylonglat=[[0,0],[0,0]]
  tempvar1=None
  iconimage=self.annotationimage=None
  utili=utilc();utili.setvideo(re.sub(r'^.*\n\s+([\dx]+)\s+.*?[*].*$',r'\1',utili.libi.system(r'xrandr --current',popen=True),flags=re.DOTALL))
  self.sourcefile=os.path.expanduser('~')+r'/tmp/imageglobe/'+sys.argv[2] if not re.search(r'/',sys.argv[2]) else sys.argv[2]
  self.backimage=Image.open(self.sourcefile).convert('RGBA')
  iconimage=Image.open(os.path.expanduser('~')+r'/tmp/imageglobe/icon.png' if not re.search(r'/',sys.argv[2]) else 'icon.png').convert('RGBA')
  iconimage=iconimage.resize((iconimage.width*self.backimage.width//2048,iconimage.height*self.backimage.width//2048))
  if len(sys.argv)>3:
   self.annotationimage=utili.text2image(sys.argv[3],size=1.0,stroke=6,textcolor=(255,255,0,255))
  longlat=[gdegree(x) for x in re.split(r'\s+',re.sub(r'\s*,\s*',',',re.sub('^.*?([\d.]+\s*[EWNSewns].*[\d.]+\s*[EWNSewns])\s+.*$',r'\1',open(os.path.expanduser('~')+r'/tmp/imageglobe/index.txt').read(),flags=re.DOTALL)))]
  xy=[gdegree(x) for x in re.split(r'\s+',re.sub('^.*?'+sys.argv[2]+r'\s+(.*?)[\n$].*',r'\1',open(re.sub(r'^(.*)/.*$',r'\1'+r'/index.txt',self.sourcefile)).read(),flags=re.DOTALL))]
  print(f'<=>Renderer.__init__ {longlat=} {xy=}')
  for xyi in list(itertools.combinations(zip(xy,longlat),2)):
   xylonglat=((xylonglat[0][0]+abs(xyi[1][0][0]-xyi[0][0][0]),xylonglat[0][1]+abs(xyi[1][0][1]-xyi[0][0][1])),(xylonglat[1][0]+abs(xyi[1][1][0]-xyi[0][1][0]),xylonglat[1][1]+abs(xyi[1][1][1]-xyi[0][1][1])))
  print(f'{xylonglat=}')
  tempvar1=[0,0]
  for count,i in enumerate(longlat):
   tempvar1[0]+=xy[count][0]+((gdegree(sys.argv[1])[0]-i[0])*xylonglat[0][0])/xylonglat[1][0]
   tempvar1[1]+=xy[count][1]+((i[1]-gdegree(sys.argv[1])[1])*xylonglat[0][1])/xylonglat[1][1]
  tempvar1[0]/=len(longlat)
  tempvar1[1]/=len(longlat)
  print(f'{tempvar1=}')
  self.degree=((tempvar1[0]*360)/self.backimage.width-90,90-(tempvar1[1]*180)/self.backimage.height)
  print(f'TEST {self.degree=} {1/math.cos(math.pi*self.degree[1]/180)=}')
  iconimage=iconimage.resize((int(iconimage.width/abs(math.cos(self.degree[1]*math.pi/180))),iconimage.height))
  self.backimage.paste(iconimage,(int((self.backimage.width*(self.degree[0]+90))/360)-iconimage.width//2,int((self.backimage.height*(90-self.degree[1]))/180)-iconimage.height),iconimage)
  self.duration=5
  self.totaldistance=360+(self.degree[0] if self.degree[0] >=0 else 360+self.degree[0])
  self.beginspeed=(self.totaldistance*2)/self.duration # integration((0-y)t/duration+y))=distance
  self.scalefactor=1.0
  print(f'<=>__init__ {self.degree=} {self.beginspeed=} {self.duration=}')
  self.angleprefix=self.bindtexture=self.rot=self.reftime=None
  self.instructions=InstructionGroup()
  self.canvas = RenderContext(compute_normal_mat=True)
  self.canvas.shader.source = resource_find('kivy.glsl')
#        self.scene = ObjFile(resource_find("monkey.obj"))
  self.scene = ObjFile(resource_find("sphere_uv_62_32_1m_orth.obj"))
  self.cube1 = RenderContext(compute_normal_mat=True,use_parent_projection=True)
  self.cube1.shader.source = resource_find('kivy1.glsl')
  self.cube2 = RenderContext(compute_normal_mat=True,use_parent_projection=True)
  self.cube2.shader.source = resource_find('kivy2.glsl')

  self.instructions.add(self.cube1)
#  self.instructions.add(self.cube2)
  self.canvas.add(self.instructions)
  Window.borderless=True
  Window.maximize()
  self.initcanvas()
  super(Renderer, self).__init__(**kwargs)
 def initcanvas(self,cube2=False):
  with self.canvas:
   self.cb = Callback(self.setup_gl_context)
   PushMatrix()
#   self.setup_scene()
   self.setup_cube1()
   self.setup_cube2() if cube2 else None
   PopMatrix()
   self.cb = Callback(self.reset_gl_context)
  '''
  self.reftime=time.time()
  Clock.schedule_interval(self.update_glsl, 1/60. )
  '''

 def setup_gl_context(self, *args):
  glEnable(GL_DEPTH_TEST)

 def reset_gl_context(self, *args):
  glDisable(GL_DEPTH_TEST)

 def update_glsl(self, delta):
  difftime=min(self.duration,time.time()-self.reftime)
  if (difftime>=self.duration and self.rot==self.roty):
   tanvalue=math.tan(-self.rot.angle*math.pi/180)
   self.rotx.axis=(1 if min(abs(tanvalue),1)<1 else 1/abs(tanvalue),0, -tanvalue if min(abs(tanvalue),1)<1 else -1*(tanvalue/abs(tanvalue)))
   self.rot=self.rotx
   self.angleprefix=self.degree[1]/abs(self.degree[1])*(-1 if 90<(self.degree[0]+360)%360<270 else 1)
   print(f'<=>update_glsl self.angleprefix={self.angleprefix}')
   self.reftime=time.time()
   difftime=min(self.duration,time.time()-self.reftime)
   self.duration=abs(self.degree[1])/10
   self.bindtexture.texture.blit_buffer(self.backimage.convert('RGB').tobytes(),colorfmt='rgb')
   self.cube1.ask_update()
   self.cube2.ask_update()
#   self.canvas.ask_update()
  elif (difftime>=self.duration and self.rot==self.rotx):
   if self.scalefactor==1.0:
    print('TEST rotxx')
    self.instructions.add(self.cube2)
    self.setup_cube2()
    self.canvas.ask_update()
   self.scalefactor+=pow(2,-15+2*(time.time()-self.reftime-self.duration))
  self.rot.angle=self.rot==self.roty and self.angleprefix*((-(difftime**2)*(self.beginspeed/(self.duration*2))+difftime*self.beginspeed)%360) or self.angleprefix*(difftime/self.duration)*abs(self.degree[1])
#  self.scle.xyz=[min(1.0,0.5+(0.5*(self.rot==self.roty and difftime or self.duration))/self.duration) for x in self.scle.xyz]
  self.scle.xyz=[min(2.0,0.5+(0.5*(self.rot==self.roty and difftime or self.scalefactor*self.duration))/self.duration) for x in self.scle.xyz]
  if not self.scalefactor==1.0:
   self.scle2.xyz=[min(2.0,0.5+(0.5*(self.scalefactor*self.duration))/self.duration) for x in self.scle2.xyz]

 def setup_cube1(self):
  with self.cube1:
   Callback(self.setup_gl_context)
   PushMatrix()
   self.bindtexture=BindTexture(source=self.sourcefile,index=1)
   self.cube1['texture1']=1
 #Translate(0,0,-3)
   self.scle=Scale(0.5,0.5,0.5)
   self.rot=self.roty = Rotate(0, 0, 1, 0)
   self.angleprefix=-1
   self.rotx=Rotate(0,1,0,-1)
   m = list(self.scene.objects.values())[0]
   m.vertices=[float(1.0-x) if not (count+1)%8 else x for count,x in enumerate(m.vertices)]
#        UpdateNormalMatrix()
   self.mesh = Mesh(
      vertices=m.vertices,
      indices=m.indices,
      fmt=m.vertex_format,
      mode='triangles',
  )
   PopMatrix()
   Callback(self.reset_gl_context)

 def setup_cube2(self):
  with self.cube2:
   Callback(self.setup_gl_context)
   PushMatrix()
   self.bindtexture2=BindTexture(source=self.annotationimage,index=2)
   self.cube2['texture2']=2
   self.scle2=Scale(0.5,0.5,0.5)
   self.mesh2=Mesh(vertices=(0.07,0.22,1.0,0.0,0.0, 0.07,0.09,1.0,0.0,1.0, 0.44,0.09,1.0,1.0,1.0, 0.44,0.22,1.0,1.0,0.0),
                     indices=(0,1,3,3,1,2),
                     fmt=[(b'vPosition', 3, 'float'), (b'vTexCoords0', 2, 'float')],
                     mode='triangles',  
                )

   PopMatrix()
   Callback(self.reset_gl_context)

 def on_size(self,*arg):
  print(f'on_size arg={arg}')
  asp = self.width / float(self.height)
  proj = Matrix().view_clip(-asp, asp, -1.0, 1.0, -2,2, 0)
  self.canvas['projection_mat'] = proj

 def on_touch_down(self,*arg):
  if not hasattr(self.on_touch_down.__func__,'pressed'):
   setattr(self.on_touch_down.__func__,'pressed',False)
  if not self.on_touch_down.__func__.pressed:
   print(f'Rendered.on_touch_down pressed={self.on_touch_down.__func__.pressed}')
   self.reftime=time.time()
   Clock.schedule_interval(self.update_glsl, 1/60. )
   self.on_touch_down.__func__.pressed=True


class RendererApp(App):
    def build(self):
        return Renderer()


if __name__ == "__main__":
    RendererApp().run()
