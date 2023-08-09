import sys,os;sys.path.append(os.path.expanduser('~')+'/tmp')
from MISC.extra.shader import shader
from wheel import wheel
class loco(shader):
 def __init__(self,*arg,**kwarg):
  super().__init__(**dict({'objfile':'car2.obj'},**kwarg))
  self.children.append(wheel(objfile='wheel.obj',fixtransformation=[[-2.4,-0.1,1.25],['s',0.10,0.10,0.10],[90,1,0,0]],material_diffuse=[(1,0,0),'Material.004'],orientation='left'))
  self.children.append(wheel(objfile='wheel.obj',fixtransformation=[[1.66,-0.1,1.25],['s',0.10,0.10,0.10],[90,1,0,0]],material_diffuse=[(0,1,0),'Material.004'],orientation='left'))
  self.children.append(wheel(objfile='wheel.obj',fixtransformation=[[-2.4,-0.1,-1.25],['s',0.10,0.10,0.10],[-90,1,0,0]],material_diffuse=[(0,0,1),'Material.004'],orientation='right'))
  self.children.append(wheel(objfile='wheel.obj',fixtransformation=[[1.66,-0.1,-1.25],['s',0.10,0.10,0.10],[-90,1,0,0]],material_diffuse=[(1,1,0),'Material.004'],orientation='right'))
  self.children.append(shader(objfile='planefilled.obj',fixtransformation=[[-3.5,0.35,1.12],['s',0.10,1,0.10],[90,1,0,0],[90,0,0,1]],material_diffuse=[(10,10,10),'__UNKNOWN__']))
  self.children.append(shader(objfile='planefilled.obj',fixtransformation=[[-3.5,0.35,-1.11],['s',0.10,1,0.10],[90,1,0,0],[90,0,0,1]],material_diffuse=[(10,10,10),'__UNKNOWN__']))
  self.children.append(shader(objfile=None,fixtransformation=[[-3.7,0,0]],light_position=(0,0,0,1),light_diffuse=(10,10,10),light_spotdirection=(1,0,0),light_spotangle=30))#light_spotangle'=40,light_spotexponent'=0}))
