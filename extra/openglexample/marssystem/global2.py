import re
import sys;sys.path.append('/home/minhinc/tmp')
from MISC.extra.shader import shader
from .earth import earth
from .mars import mars
class global2(shader):
 def __init__(self,*arg,**kwarg):
#  super().__init__(**dict({'objfile':None},**kwarg))
  super().__init__(**dict({'objfile':'sphere.obj','material_diffuse':{'__UNKNOWN__':'sun.png'},'material_ambient':(2,2,2),'light_position':(0,0,0,1),'light_specular':(0.2,0.2,0.2),'light_diffuse':(1.0,1.0,1.0),'light_ambient':(0.2,0.2,0.2)},fixtransformation=[['s',1,1,1]],**kwarg))
  self.children.append(shader(objfile=None,light_position=(0,0,1,0),light_specular=(0.2,0.2,0.2),light_diffuse=(0.6,0.6,0.6),light_ambient=(0.1,0.1,0.1)))
  self.children.append(shader(objfile=None,light_position=(0,0,-1,0),light_specular=(0.2,0.2,0.2),light_diffuse=(0.6,0.6,0.6),light_ambient=(0.1,0.1,0.1)))
  self.children.append(shader(objfile=None,light_position=(1,0,0,0),light_specular=(0.2,0.2,0.2),light_diffuse=(0.6,0.6,0.6),light_ambient=(0.1,0.1,0.1)))
  self.children.append(shader(objfile=None,light_position=(-1,0,0,0),light_specular=(0.2,0.2,0.2),light_diffuse=(0.6,0.6,0.6),light_ambient=(0.1,0.1,0.1)))
  self.children.append(shader(objfile=None,light_position=(0,-1,0,0),light_specular=(0.2,0.2,0.2),light_diffuse=(0.6,0.6,0.6),light_ambient=(0.1,0.1,0.1)))
  self.children.append(shader(objfile=None,light_position=(0,1,0,0),light_specular=(0.2,0.2,0.2),light_diffuse=(0.6,0.6,0.6),light_ambient=(0.1,0.1,0.1)))
  self.children.append(shader(objfile='axis.obj',material_shininess=-2))
  self.children.append(mars(fixtransformation=[[6,0,0],['s',0.4,0.4,0.4],[25,0,0,1]]))
#  self.children.append(shader(objfile='satelite.obj'))

 def keyboard(self,**kwarg):
  if type(kwarg['key'])==str and re.search(r'^[xyz]$',kwarg['key'],flags=re.I) and shader.utili.mode=='grand':
   return super().keyboard(**dict(kwarg,key=[1 if kwarg['key'].islower() else -1,1 if kwarg['key'] in 'xX' else 0,1 if kwarg['key'] in 'yY' else 0,1 if kwarg['key'] in 'zZ' else 0]))
  return super().keyboard(**kwarg)
