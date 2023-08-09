import re
import sys;sys.path.append('/home/minhinc/tmp')
from MISC.extra.shader import shader
from .moon import moon
from .mars import mars
class global2(shader):
 def __init__(self,*arg,**kwarg):
  super().__init__(**dict({'objfile':'sphere.obj','material_diffuse':{'__UNKNOWN__':'sun.png'},'material_ambient':(2,2,2),'light_position':(0,0,0,1),'light_specular':(0.2,0.2,0.2),'light_diffuse':(1.0,1.0,1.0),'light_ambient':(0.2,0.2,0.2)},**kwarg))
  self.children.append(shader(objfile=None,light_position=(0,0,1,1),light_specular=(0.2,0.2,0.2),light_diffuse=(0.3,0.3,0.3),light_ambient=(0.1,0.1,0.1)))
  self.children.append(shader(objfile=None,light_position=(0,0,-1,1),light_specular=(0.2,0.2,0.2),light_diffuse=(0.3,0.3,0.3),light_ambient=(0.1,0.1,0.1)))
  self.children.append(shader(objfile=None,light_position=(1,0,0,1),light_specular=(0.2,0.2,0.2),light_diffuse=(0.3,0.3,0.3),light_ambient=(0.1,0.1,0.1)))
  self.children.append(shader(objfile=None,light_position=(-1,0,0,1),light_specular=(0.2,0.2,0.2),light_diffuse=(0.3,0.3,0.3),light_ambient=(0.1,0.1,0.1)))
  self.children.append(shader(objfile=None,light_position=(0,-1,0,1),light_specular=(0.2,0.2,0.2),light_diffuse=(0.3,0.3,0.3),light_ambient=(0.1,0.1,0.1)))
  self.children.append(shader(objfile=None,light_position=(0,1,0,1),light_specular=(0.2,0.2,0.2),light_diffuse=(0.3,0.3,0.3),light_ambient=(0.1,0.1,0.1)))
  self.children.append(shader(objfile='axis.obj',material_shininess=-2))
  self.children.append(shader(objfile='ring2.obj',material_diffuse={'__UNKNOWN__':(1,1,1)},fixtransformation=[['s',4,4,4]],material_shininess=-2))
#  self.children.append(moon(fixtransformation=[[4,0,0]]))
#  self.children.append(shader(objfile='sphere.obj',material_diffuse={'__UNKNOWN__':'earth3.png'},transformation=[[0,-14,-10],[-90,0,1,0]]))
  self.children.append(shader(objfile='sphere.obj',material_diffuse={'__UNKNOWN__':'earth3.png'},transformation=[[12,0,4],[90,0,1,0]]))
#  self.children.append(shader(objfile='plane31.obj',material_diffuse={'__UNKNOWN__':'moonsurfacebootstar_t.png'},fixtransformation=[[0,-14,-14],[90,1,0,0],['s',3,3,3]]))
#  self.children.append(shader(objfile='plane31.obj',material_diffuse={'__UNKNOWN__':'moonsurfacebootstar_t.png'},fixtransformation=[[6,3,-11],[90,1,0,0],['s',3,3,3]]))
#  self.children.append(shader(objfile='plane21.obj',material_diffuse={'__UNKNOWN__':'moonsurfacec_t.png'},fixtransformation=[[0,-18,0],[90,1,0,0]]))
#  self.children.append(shader(objfile='plane21.obj',material_diffuse={'__UNKNOWN__':'moonsurfacec_t.png'},fixtransformation=[[6,3,0],['s',1.5,1.5,1.5],[90,1,0,0]]))
#  self.children.append(moon(fixtransformation=[[4,0,0],[90,1,0,0]]))

 def keyboard(self,**kwarg):
  if type(kwarg['key'])==str and re.search(r'^[xyz]$',kwarg['key'],flags=re.I) and shader.utili.mode=='grand':
   return super().keyboard(**dict(kwarg,key=[1 if kwarg['key'].islower() else -1,1 if kwarg['key'] in 'xX' else 0,1 if kwarg['key'] in 'yY' else 0,1 if kwarg['key'] in 'zZ' else 0]))
  return super().keyboard(**kwarg)
