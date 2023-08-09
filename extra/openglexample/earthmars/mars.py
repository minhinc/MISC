import re
import sys;sys.path.append('/home/minhinc/tmp')
from MISC.extra.shader import shader
from .moon import moon
class mars(shader):
 def __init__(self,*arg,**kwarg):
#  super().__init__(**dict({'objfile':'sphere.obj','material_diffuse':{'__UNKNOWN__':'mars.jpg'},'fixtransformation':[[8,0,0],['s',0.6,0.6,0.6]],'extratransformation':[[25,0,0,1]],'material_ambient':(0.3,0.3,0.3)},**kwarg))
#  super().__init__(**dict({'objfile':'sphere.obj','material_diffuse':{'__UNKNOWN__':'mars.jpg'},'extratransformation':[[25,0,0,1]],'material_ambient':(0.3,0.3,0.3)},**kwarg))
  super().__init__(**dict({'objfile':'sphere.obj','material_diffuse':{'__UNKNOWN__':'mars.jpg'},'material_ambient':(0.3,0.3,0.3)},**kwarg))
#  self.innerchildren.append(shader(objfile='cubestick.obj',material_emission=(1,1,1),material_diffuse={'Material':(1,1,1)},material_ambient=(0.2,0.2,0.2)))
  self.children.append(shader(objfile='ring.obj',material_shininess=-1,material_diffuse={'__UNKNOWN__':(1,0.8,0.8)},fixtransformation=[['s',1.4,1.4,1.4]]))
  self.children.append(shader(objfile='ring.obj',material_shininess=-1,material_diffuse={'__UNKNOWN__':(1,1,0.8)},fixtransformation=[['s',4,4,4]]))
#  self.children.append(shader(objfile='ring.obj',material_shininess=-1,material_diffuse={'__UNKNOWN__':(1,0.8,1)},transformation=[[40,1,0,0],[-30,0,0,1]],fixtransformation=[['s',2,2,2]]))
  self.children.append(shader(objfile='rock1.obj',material_shininess=-1,fixtransformation=[[180,0,1,0],[1.4,0,0],['s',10,10,10]]))
  self.children.append(shader(objfile='rock2.obj',material_shininess=-1,fixtransformation=[[180,0,1,0],[4,0,0],['s',0.2,0.2,0.2]]))
#  self.children.append(shader(objfile='satelite.obj',transformation=[[40,1,0,0],[-30,0,0,1]],fixtransformation=[[2,0,0],[80,1,0,0],[30,0,1,0],[30,0,0,1],['s',0.04,0.04,0.04]]))
  '''
  earth2.children.append(moon(objfile='sphere.obj',material_diffuse={'__UNKNOWN__':'moon.png'},transformation=[[20,1,0,0]],fixtransformation=[[3,0,0],['s',0.5,0.5,0.5]]))
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
#   self.extratransformation=[[25,rotationaxis[0],0,rotationaxis[1]]]+[x for x in self.extratransformation if x[2]]
   self.extratransformation=[[0,rotationaxis[0],0,rotationaxis[1]]]+[x for x in self.extratransformation if x[2]]
   return super().keyboard(**dict(kwarg,key=[360/365,0,1,0]))
  return super().keyboard(**kwarg)
  '''
 def keyboard(self,**kwarg):
  rotationaxis=None
  if not hasattr(self,'extratransformation'):
   setattr(self,'extratransformation',[])
  return super().keyboard(**kwarg,transformation=self.extratransformation if shader.utili.mode!='grand' else self.transformation)
