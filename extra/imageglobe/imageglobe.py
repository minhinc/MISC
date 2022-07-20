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
    Color, Translate, Rotate, Mesh, UpdateNormalMatrix,BindTexture,Rectangle,Scale
import time
from objloader import ObjFile
import io
from PIL import Image,ImageDraw
from scipy.spatial import minkowski_distance
import math


class Renderer(Widget):
    PUSAND=('142.4158E','10.7240S')
    TARIFA=('5.606W','36.014N')
    CABOSANLUCAS=('109.5456W','22.5323N')
    FIXEDLONGLAT=[('142.4158E','10.7240S'),('5.606W','36.014N'),('109.5456W','22.5323N')]
    def __init__(self, **kwargs):
     if len(sys.argv)<3:
      print('''\
  ---usage---
  python3 blender.py <longitude,latitude> <mapname> [<x1,y1> <x2,y2>]
  python3 blender.py '24E,12S' globepolitical.png
  Image searched in ~/tmp/MISC/image
  x1,y1 x2,y2 (PUSAND,TERIFA) searched in ~/tmp/MISC/image/index.txt
  python3 blender.py '24E,12S' ./globepolitical.png 1836,574 991,308''')
     def gdegree(tup,pos):
      if type(tup)==tuple:
       tup=','.join(tup)
      tup=re.sub(r'[SsWw]','*-1',re.sub(r'[NnEe]','*1',tup))
      return eval(re.split(',',tup)[pos])
     xy=None
     degree=[]
     self.sourcefile=os.path.expanduser('~')+r'/tmp/imageglobe/'+sys.argv[2] if not re.search(r'/',sys.argv[2]) else sys.argv[2]
     self.backimage=Image.open(self.sourcefile).convert('RGBA')
     image=Image.open(os.path.expanduser('~')+r'/tmp/imageglobe/icon.png' if not re.search(r'/',sys.argv[2]) else 'icon.png').convert('RGBA')
     image=image.resize((image.width*self.backimage.width//2048,image.height*self.backimage.width//2048))
     print(f'<=>__init self.sourcefile={self.sourcefile}')
     if not re.search(r'/',sys.argv[2]):
      xy=re.split(r'\s+',re.sub('^.*?'+sys.argv[2]+r'\s+(.*?)[\n$].*',r'\1',open(re.sub(r'^(.*)/.*$',r'\1'+r'/index.txt',self.sourcefile)).read(),flags=re.DOTALL))
     else:
      xy=sys.argv[3:]
     print(f'<=>__init__ xy={xy}')
     for xyi in list(itertools.combinations(xy,2)):
#     self.degree=(((gdegree(x1y1,0)-(((gdegree(x1y1,0)-gdegree(x2y2,0))/(gdegree(self.PUSAND,0)-gdegree(self.TARIFA,0)))*(gdegree(self.PUSAND,0)-gdegree(sys.argv[1],0))))/self.backimage.width)*360-90,90-((gdegree(x1y1,1)-(((gdegree(x1y1,1)-gdegree(x2y2,1))/(gdegree(self.PUSAND,1)-gdegree(self.TARIFA,1)))*(gdegree(self.PUSAND,1)-gdegree(sys.argv[1],1))))/self.backimage.height)*180)
      print(f'xyi={xyi}')
      PUSAND=self.FIXEDLONGLAT[[count for count in range(len(xy)) if xy[count]==xyi[0]][0]]
      TARIFA=self.FIXEDLONGLAT[[count for count in range(len(xy)) if xy[count]==xyi[1]][0]]
      degree.append((((gdegree(xyi[0],0)-(((gdegree(xyi[0],0)-gdegree(xyi[1],0))/(gdegree(PUSAND,0)-gdegree(TARIFA,0)))*(gdegree(PUSAND,0)-gdegree(sys.argv[1],0))))/self.backimage.width)*360-90,90-((gdegree(xyi[0],1)-(((gdegree(xyi[0],1)-gdegree(xyi[1],1))/(gdegree(PUSAND,1)-gdegree(TARIFA,1)))*(gdegree(PUSAND,1)-gdegree(sys.argv[1],1))))/self.backimage.height)*180))
     self.degree=(sum(x[0] for x in degree)/len(degree),sum(x[1] for x in degree)/len(degree))
     if abs(abs(self.degree[0])-abs(90+gdegree(sys.argv[1],0)))<2 and abs(abs(self.degree[1])-abs(gdegree(sys.argv[1],1)))<2:
      self.degree=(90+gdegree(sys.argv[1],0),gdegree(sys.argv[1],1))
     self.backimage.paste(image,(int(self.backimage.width*(self.degree[0]+90)/360)-image.width//2,int(self.backimage.height*(90-self.degree[1])/180)-image.height),image)
     self.duration=5
     self.totaldistance=360+(self.degree[0] if self.degree[0] >=0 else 360+self.degree[0])
     self.beginspeed=(self.totaldistance*2)/self.duration # integration((0-y)t/duration+y))=distance
     print(f'<=>__init__ self.degree={self.degree} self.beginspeed={self.beginspeed} self.duration={self.duration}')
     self.angleprefix=self.bindtexture=self.rot=self.reftime=None
     self.canvas = RenderContext(compute_normal_mat=True)
     self.canvas.shader.source = resource_find('simple.glsl')
#        self.scene = ObjFile(resource_find("monkey.obj"))
     self.scene = ObjFile(resource_find("sphere_uv_62_32_1m_orth.obj"))
#     Window.borderless=True
#     Window.maximize()
     super(Renderer, self).__init__(**kwargs)
     with self.canvas:
      self.cb = Callback(self.setup_gl_context)
      PushMatrix()
      self.setup_scene()
      PopMatrix()
      self.cb = Callback(self.reset_gl_context)
     self.reftime=time.time()
#     Clock.schedule_interval(self.update_glsl, 1/60. )
     Clock.schedule_interval(self.update_glsl, 1/60. )

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
      print(f'self.angleprefix={self.angleprefix}')
      self.reftime=time.time()
      difftime=min(self.duration,time.time()-self.reftime)
      self.duration=abs(self.degree[1])/10
      self.bindtexture.texture.blit_buffer(self.backimage.convert('RGB').tobytes(),colorfmt='rgb')
     self.rot.angle=self.rot==self.roty and self.angleprefix*((-(difftime**2)*(self.beginspeed/(self.duration*2))+difftime*self.beginspeed)%360) or self.angleprefix*(difftime/self.duration)*abs(self.degree[1])
     self.scle.xyz=[min(1.0,0.5+(0.5*(self.rot==self.roty and difftime or self.duration))/self.duration) for x in self.scle.xyz]
    def setup_scene(self):
        self.bindtexture=BindTexture(source=self.sourcefile,index=1)
        self.canvas['texture0']=1
       #Translate(0,0,-3)
        self.scle=Scale(0.5,0.5,0.5)
        self.rot=self.roty = Rotate(0, 0, 1, 0)
        self.angleprefix=-1
        self.rotx=Rotate(0,1,0,-1)
        m = list(self.scene.objects.values())[0]
        texturemin=min(range(len([m.vertices[count] for count in range(len(m.vertices)) if (count+1)%8==7])),key=[m.vertices[count] for count in range(len(m.vertices)) if (count+1)%8==7].__getitem__)
        xmin=min(range(len([m.vertices[count] for count in range(len(m.vertices)) if (count+1)%8==1])),key=[m.vertices[count] for count in range(len(m.vertices)) if (count+1)%8==1].__getitem__)
        print(f'xmin={m.vertices[xmin*8:xmin*8+8]} texturemin={m.vertices[texturemin*8:texturemin*8+8]}')
        minkowskilist=[minkowski_distance([-1.0,0.0,0.0,0.0,0.5],x,2) for x in [m.vertices[count:count+3]+m.vertices[count+6:count+8] for count in range(len(m.vertices)) if (count+1)%8==1]]
        minkmindistance=min(range(len(minkowskilist)),key=minkowskilist.__getitem__)
        print(f'texturemin={texturemin} xmin={xmin} minkmindistance={minkmindistance}')# m.vertices={[m.vertices[count:count+3]+m.vertices[count+6:count+8] for count in range(len(m.vertices)) if (count+1)%8 ==1]}')
        m.vertices=[float(1.0-x) if not (count+1)%8 else x for count,x in enumerate(m.vertices)]
#        UpdateNormalMatrix()
        self.mesh = Mesh(
            vertices=m.vertices,
            indices=m.indices,
            fmt=m.vertex_format,
            mode='triangles',
        )
    def on_size(self,*arg):
     print(f'on_size arg={arg}')
     asp = self.width / float(self.height)
     proj = Matrix().view_clip(-asp, asp, -1.0, 1.0, -2,2, 0)
     self.canvas['projection_mat'] = proj


class RendererApp(App):
    def build(self):
        return Renderer()


if __name__ == "__main__":
    RendererApp().run()
