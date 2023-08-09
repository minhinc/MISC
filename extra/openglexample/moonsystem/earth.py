import re
import sys;sys.path.append('/home/minhinc/tmp')
from MISC.extra.shader import shader
class earth(shader):
 def __init__(self,*arg,**kwarg):
#  super().__init__(**dict({'objfile':'sphere.obj','material_diffuse':{'__UNKNOWN__':'earth.png'},'fixtransformation':[[4,0,0],['s',0.2,0.2,0.2]],'material_ambient':(0.3,0.3,0.3)},**kwarg))
  super().__init__(**dict({'objfile':'sphere.obj','material_diffuse':{'__UNKNOWN__':'2_no_clouds_16k.png'},'fixtransformation':[[4,0,0],['s',0.4,0.4,0.4]],'material_ambient':(0.3,0.3,0.3)},**kwarg))
  '''
  earth2.children.append(moon(objfile='sphere.obj',material_diffuse={'__UNKNOWN__':'moon.png'},transformation=[[20,1,0,0]],fixtransformation=[[3,0,0],['s',0.2,0.2,0.2]]))
  earth2.children.append(moon(objfile='ring.obj',material_shininess=-1,fixtransformation=[[20,1,0,0],['s',3,3,3]]))
  '''

 '''
 def keyboard(self,**kwarg):
  rotationaxis=None
  if not hasattr(self,'extratransformation'):
   setattr(self,'extratransformation',[])
  if type(kwarg['key'])==str and re.search(r'^s$',kwarg['key'],flags=re.I):
   return super().keyboard(**dict(kwarg,transformation=self.fixtransformation))
  elif type(kwarg['key'])==str and re.search(r'^y$',kwarg['key'],flags=re.I) and shader.utili.mode!='grand':
   return super().keyboard(**dict(kwarg,key=[15,0,1,0],transformation=self.extratransformation))
  elif type(kwarg['key'])==str and re.search(r'^y$',kwarg['key'],flags=re.I) and shader.utili.mode=='grand':
   angle=sum([x[0] for x in self.transformation])
   if 0<=angle<=90:
    rotationaxis=(0-angle)/90,(90-angle)/90
   elif 90<=angle<=180:
    rotationaxis=(angle-180)/90,(90-angle)/90
   elif 180<=angle<=270:
    rotationaxis=(angle-180)/90,(angle-270)/90
   else:
    rotationaxis=(360-angle)/90,(angle-270)/90
#   self.extratransformation=[[0,rotationaxis[0],0,rotationaxis[1]]]+[x for x in self.extratransformation if x[2]]
   self.extratransformation=[[0,rotationaxis[0],0,rotationaxis[1]]]+[x for x in self.extratransformation if x[2]]
   return super().keyboard(**dict(kwarg,key=[360/365*(-1 if kwarg['key']=='y' else 1),0,1,0]))
  return super().keyboard(**kwarg)
 '''
 def keyboard(self,**kwarg):
#  print(f'TEST earth keyboard {kwarg=}')
  rotationaxis=None
  if not hasattr(self,'extratransformation'):
   setattr(self,'extratransformation',[])
  if type(kwarg['key'])==str and re.search(r'^y$',kwarg['key'],flags=re.I) and shader.utili.mode!='grand':
   return super().keyboard(**dict(kwarg,key=[360/365*(-1 if kwarg['key']=='y' else 1),0,1,0],transformation=self.extratransformation))
  elif type(kwarg['key'])==str and re.search(r'^z$',kwarg['key'],flags=re.I) and shader.utili.mode!='grand':
   return super().keyboard(**dict(kwarg,key=[1*(-1 if kwarg['key']=='Z' else 1),0,0,1],transformation=self.extratransformation))
  elif type(kwarg['key'])==str and re.search(r'^x$',kwarg['key'],flags=re.I) and shader.utili.mode=='grand':
   return super().keyboard(**dict(kwarg,key=[1*(-1 if kwarg['key']=='X' else 1),1,0,0]))
  return super().keyboard(**kwarg,transformation=self.extratransformation if shader.utili.mode!='grand' else self.transformation)
