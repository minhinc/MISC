import re
import sys;sys.path.append('/home/minhinc/tmp')
from MISC.extra.shader import shader
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
#  sky=shader(objfile='plane1.5.obj',material_diffuse={'__UNKNOWN__':'ASYSM1022_07.jpg'},fixtransformation=[[6,0,0],[90,1,0,0],['s',1.5,1.5,1.5]])
  sky=shader(objfile='plane23.obj',material_diffuse={'__UNKNOWN__':'pexels-photo-1624496.png'},fixtransformation=[[6,0,0],[90,1,0,0]])
  self.children.append(sky)
#  sky.children.append(shader(objfile='sphere.obj',material_diffuse={'__UNKNOWN__':'mars.jpg'},transformation=[[-0.65,0,-0.2],['s',0.1,0.1,0.1]]))
  mars=shader(objfile='sphere.obj',material_diffuse={'__UNKNOWN__':'mars.jpg'},transformation=[[5.8,0.82,0],['s',0.005,0.005,0.005]])
#  mars=shader(objfile='sphere.obj',material_diffuse={'__UNKNOWN__':'mars.jpg'},transformation=[[5.8,0.82,0],['s',0.05,0.05,0.05]])
  mars.children.append(shader(objfile='rock1.obj',material_shininess=-1,fixtransformation=[[180,0,1,0],[1.3,0,0],['s',10,10,10]]))
  mars.children.append(shader(objfile='rock2.obj',material_shininess=-1,fixtransformation=[[180,0,1,0],[2.80,0,0],['s',0.2,0.2,0.2]]))
  self.children.append(mars)

 def keyboard(self,**kwarg):
  if type(kwarg['key'])==str and re.search(r'^[xyz]$',kwarg['key'],flags=re.I) and shader.utili.mode=='grand':
   return super().keyboard(**dict(kwarg,key=[1 if kwarg['key'].islower() else -1,1 if kwarg['key'] in 'xX' else 0,1 if kwarg['key'] in 'yY' else 0,1 if kwarg['key'] in 'zZ' else 0]))
  return super().keyboard(**kwarg)
