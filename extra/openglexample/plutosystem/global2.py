import re
import sys;sys.path.append('/home/minhinc/tmp')
from MISC.extra.shader import shader
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

  self.children.append(shader(objfile='ring2_015.obj',material_diffuse={'__UNKNOWN__':(1,1,1)},material_shininess=-1))
  self.children.append(shader(objfile='ring3_015.obj',material_diffuse={'__UNKNOWN__':(1,1,0.8)},material_shininess=-1))
  self.children.append(shader(objfile='ring4_015.obj',material_diffuse={'__UNKNOWN__':(0.2,0.2,0.8)},material_shininess=-1))
  self.children.append(shader(objfile='ring8_015.obj',material_diffuse={'__UNKNOWN__':(1,1,0)},material_shininess=-1))
  self.children.append(shader(objfile='ring10_015.obj',material_diffuse={'__UNKNOWN__':(1,1,0.8)},material_shininess=-1))
  self.children.append(shader(objfile='ring12_015.obj',material_diffuse={'__UNKNOWN__':(1,1,0.8)},material_shininess=-1))
  self.children.append(shader(objfile='ring14_015.obj',material_diffuse={'__UNKNOWN__':(0.8,0.8,0.1)},material_shininess=-1))
  self.children.append(shader(objfile='ellipse16_015_08.obj',material_diffuse={'__UNKNOWN__':(1,0.5,0.8)},material_shininess=-1))

  self.children.append(mars(objfile='sphere.obj',material_diffuse={'__UNKNOWN__':'mercury.jpeg'},material_shininess=-1,fixtransformation=[[2,0,0],['s',0.3,0.3,0.3]],tiltedangle=1))
  self.children.append(mars(objfile='sphere.obj',material_diffuse={'__UNKNOWN__':'venus.jpg'},material_specular=(0.3,0.3,0.3),material_shininess=-1,fixtransformation=[[3,0,0],['s',0.4,0.4,0.4]],tiltedangle=3))
  self.children.append(mars(objfile='sphere.obj',material_diffuse={'__UNKNOWN__':'earth.png'},material_shininess=-1,fixtransformation=[[4,0,0],['s',0.5,0.5,0.5]],tiltedangle=23))
#  self.children.append(mars(objfile='sphere.obj',material_diffuse={'__UNKNOWN__':'earth.png'},material_shininess=1,transformation=[['s',0.5,0.5,0.5]]))

  tmp=shader(objfile=None,transformation=[[-1,0,0]])
  tmp.children.append(shader(objfile='ring6_015.obj',material_diffuse={'__UNKNOWN__':(1,1,0.7)},material_shininess=-1))
  mars2=mars(objfile='sphere.obj',material_ambient=(0.2,0.2,0.2),material_diffuse={'__UNKNOWN__':'mars.jpg'},material_shininess=-1,fixtransformation=[[6,0,0],['s',0.36,0.36,0.36]],tiltedangle=25)
#  mars2.children.append(shader(objfile='rock2.obj',material_shininess=-1,fixtransformation=[[2.0,0,0],['s',0.3,0.3,0.3]]))
#  mars2.children.append(shader(objfile='rock1.obj',material_shininess=-1,fixtransformation=[[3.2,0,0],['s',12,12,12]]))
  tmp.children.append(mars2)
  self.children.append(tmp)

  self.children.append(mars(objfile='sphere.obj',material_diffuse={'__UNKNOWN__':'jupiter.jpg'},material_shininess=-1,fixtransformation=[[8,0,0],['s',0.8,0.8,0.8]],tiltedangle=3))
  self.children.append(mars(objfile='saturn.obj',material_diffuse={'Material.001':'saturnbody.jpg','Material.002':(1,0.5,0.2)},material_shininess=-1,fixtransformation=[[10,0,0],['s',0.5,0.5,0.5]],tiltedangle=27))
  self.children.append(mars(objfile='sphere.obj',material_diffuse={'__UNKNOWN__':'uranus.jpg'},material_shininess=1,fixtransformation=[[12,0,0],['s',0.7,0.7,0.7]],tiltedangle=98))
#  self.children.append(mars(objfile='sphere.obj',material_diffuse={'__UNKNOWN__':'neptune.jpg'},material_shininess=1,transformation=[[28,0,0,1],['s',0.7,0.7,0.7]]))
  self.children.append(mars(objfile='sphere.obj',material_diffuse={'__UNKNOWN__':'neptune.jpg'},material_shininess=1,fixtransformation=[[14,0,0],['s',0.7,0.7,0.7]],tiltedangle=28))
#  tmp=mars(objfile='sphere.obj',material_diffuse={'__UNKNOWN__':'uranus.jpg'},material_shininess=1,transformation=[['s',0.7,0.7,0.7]])
#  tmp.innerchildren.append(shader(objfile='sphere.obj',material_diffuse={'__UNKNOWN__':(1,0,0)},fixtransformation=[[0,0,1.18],['s',0.2,0.2,0.2]],material_ambient=(0.2,0.2,0.2),material_shininess=-2))
#  self.children.append(tmp)
#  self.children.append(mars(objfile='Saturn.obj',material_shininess=-1,fixtransformation=[[8,0,0],['s',0.8,0.8,0.8]],tiltedangle=3))

  tmp=shader(objfile=None)
  tmp.children.append(mars(objfile='sphere.obj',material_diffuse={'__UNKNOWN__':'PlutoColour.png'},material_shininess=-1,transformation=[['s',0.3,0.3,0.3]]))
#  tmp.children.append(mars(objfile='sphere.obj',material_diffuse={'__UNKNOWN__':'PlutoColour.png'},material_shininess=-1,fixtransformation=[[12,0,0]]))
  self.children.append(tmp)


 def keyboard(self,**kwarg):
  if type(kwarg['key'])==str and re.search(r'^[xyz]$',kwarg['key'],flags=re.I) and shader.utili.mode=='grand':
   return super().keyboard(**dict(kwarg,key=[1 if kwarg['key'].islower() else -1,1 if kwarg['key'] in 'xX' else 0,1 if kwarg['key'] in 'yY' else 0,1 if kwarg['key'] in 'zZ' else 0]))
  return super().keyboard(**kwarg)
