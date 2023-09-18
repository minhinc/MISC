import re
import numpy as np
import sys;sys.path.append('/home/minhinc/tmp')
from MISC.extra.shader import shader
#from .moon import moon
class mars(shader):
 def __init__(self,*arg,**kwarg):
#  super().__init__(**dict({'objfile':'sphere.obj','material_diffuse':{'__UNKNOWN__':'mars.jpg'},'material_ambient':(0.3,0.3,0.3),'fixtransformation':[[25,0,1,0]]},**kwarg))
  super().__init__(**dict({'objfile':'sphere.obj','material_diffuse':{'__UNKNOWN__':'mars.jpg'},'material_ambient':(0.1,0.1,0.1)},**kwarg))
  self.tiltedangle=kwarg['tiltedangle'] if 'tiltedangle' in kwarg else 0
#  self.children.append(shader(objfile='cubestick3.obj',material_emission=(1,1,1),material_diffuse={'Material':(1,1,1) if not 'material_diffuse_texture' in kwarg else kwarg['material_diffuse_texture']},material_ambient=(0.2,0.2,0.2),material_shininess=-1 if not 'cubestick' in kwarg or kwarg['cubestick']==True else -2))
  self.children.append(shader(objfile='cubestick3.obj',material_emission=(1,1,1),material_diffuse={'Material':(1,1,1) if not 'material_diffuse_texture' in kwarg else kwarg['material_diffuse_texture']},material_ambient=(0.2,0.2,0.2),material_shininess=-1))
#  self.innerchildren.append(shader(objfile='sphere.obj',material_diffuse={'__UNKNOWN__':(1,0,0)},fixtransformation=[[0,0,1.18],['s',0.2,0.2,0.2]],material_ambient=(0.2,0.2,0.2),material_shininess=-1))


 def keyboard(self,**kwarg):
#  print(f'TEST mars.keyboard {kwarg=}')
  rotationaxis=None
  if not hasattr(self,'extratransformation'):
   setattr(self,'extratransformation',[])
  elif type(kwarg['key'])==str and re.search(r'^y$',kwarg['key'],flags=re.I) and shader.utili.mode!='grand':
   return super().keyboard(**dict(kwarg,key=[15,0,1,0],transformation=self.extratransformation))
  elif type(kwarg['key'])==str and re.search(r'(^y$|0\s*,\s*1\s*,\s*0\s*\])',kwarg['key'],flags=re.I) and shader.utili.mode=='grand':
#   print(f'rotation {kwarg=}')
   self.fixtransformation=[x for x in self.fixtransformation if len(x)==3 or x[0]=='s']+[[self.tiltedangle,shader.utili.settlematrix(self.transformation)[:,0][2],0,shader.utili.settlematrix(self.transformation)[:,2][2]]] if type(shader.utili.settlematrix(self.transformation))==np.matrix else self.fixtransformation
  return super().keyboard(**kwarg,transformation=self.extratransformation if shader.utili.mode!='grand' else self.transformation)
