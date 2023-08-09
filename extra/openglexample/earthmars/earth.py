import re
import sys;sys.path.append('/home/minhinc/tmp')
from MISC.extra.shader import shader
from .moon import moon
class earth(shader):
 def __init__(self,*arg,**kwarg):
  super().__init__(**dict({'objfile':'sphere.obj','material_diffuse':{'__UNKNOWN__':'earth.png'},'fixtransformation':[[4,0,0],['s',0.6,0.6,0.6]],'material_ambient':(0.3,0.3,0.3)},**kwarg))
  self.children.append(shader(objfile='ring.obj',material_shininess=-1,fixtransformation=[['s',3,3,3]]))
  self.children.append(moon())
  '''
  earth2.children.append(moon(objfile='sphere.obj',material_diffuse={'__UNKNOWN__':'moon.png'},transformation=[[20,1,0,0]],fixtransformation=[[3,0,0],['s',0.5,0.5,0.5]]))
  earth2.children.append(moon(objfile='ring.obj',material_shininess=-1,fixtransformation=[[20,1,0,0],['s',3,3,3]]))
  '''

 def keyboard(self,**kwarg):
  rotationaxis=None
  if not hasattr(self,'extratransformation'):
   setattr(self,'extratransformation',[])
  return super().keyboard(**kwarg,transformation=self.extratransformation if shader.utili.mode!='grand' else self.transformation)
