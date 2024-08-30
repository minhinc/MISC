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

  self.children.append(shader(objfile='ring6_015.obj',material_diffuse={'__UNKNOWN__':(0.7,0.7,0.8)},material_shininess=-1))
  self.children.append(shader(objfile='ellipse16_015_08.obj',material_diffuse={'__UNKNOWN__':(1,0.8,0.8)},material_shininess=-1))


  self.children.append(mars(objfile='sphere.obj',material_diffuse={'__UNKNOWN__':'mercury.jpeg'},transformation=[[2.2,0,0]]))
  self.children.append(mars(objfile='sphere.obj',material_diffuse={'__UNKNOWN__':'venus.jpg'},transformation=[[4.4,0,0]]))
  earth=mars(objfile='sphere.obj',material_diffuse={'__UNKNOWN__':'earth.png'},transformation=[[6.6,0,0]])
  earth.children.append(mars(objfile='sphere.obj',material_diffuse={'__UNKNOWN__':'moon.png'},material_shininess=-1,fixtransformation=[[2,0,0],['s',0.3,0.3,0.3]],extratransformation=[[90,0,1,0]]))
  self.children.append(earth)

  '''
  mars2=mars(objfile='sphere.obj',material_ambient=(0.2,0.2,0.2),material_diffuse={'__UNKNOWN__':'mars.jpg'},transformation=[[8.8,0,0]])
  mars2.children.append(shader(objfile='rock2.obj',material_shininess=-1,fixtransformation=[[180,0,1,0],[1.4,0,0],['s',0.2,0.2,0.2]]))
  mars2.children.append(shader(objfile='rock1.obj',material_shininess=-1,fixtransformation=[[180,0,1,0],[4,0,0],['s',10,10,10]]))
  self.children.append(mars2)
  '''
  self.children.append(mars(objfile='sphere.obj',material_ambient=(0.2,0.2,0.2),material_diffuse={'__UNKNOWN__':'mars.jpg'},transformation=[[8.8,0,0]]))


  self.children.append(mars(objfile='sphere.obj',material_diffuse={'__UNKNOWN__':'jupiter.jpg'},transformation=[[11,0,0]]))
  self.children.append(mars(objfile='saturn.obj',material_diffuse={'Material.001':'saturnbody.jpg','Material.002':(1,0.5,0.2)},transformation=[[14.6,0,0],['s',1.15,1.15,1.15]]))
  self.children.append(mars(objfile='sphere.obj',material_diffuse={'__UNKNOWN__':'uranus.jpg'},transformation=[[18.2,0,0]]))
  self.children.append(mars(objfile='sphere.obj',material_diffuse={'__UNKNOWN__':'neptune.jpg'},transformation=[[20.4,0,0]]))
#  self.children.append(mars(objfile='saturn.obj',material_diffuse={'Material.001':'saturnbody.jpg','Material.002':(1,0.5,0.2)},transformation=[[14.6,0,0],['s',1.15,1.15,1.15]]))
#  self.children.append(mars(objfile='sphere.obj',material_diffuse={'__UNKNOWN__':'uranus.jpg'},transformation=[[18.2,0,0]]))
#  self.children.append(mars(objfile='sphere.obj',material_diffuse={'__UNKNOWN__':'neptune.jpg'},transformation=[[20.4,0,0]]))

  pluto3=shader(objfile=None)
  pluto2=mars(objfile='sphere.obj',material_diffuse={'__UNKNOWN__':'PlutoColour.png'},transformation=[[22.6,0,0]])
#  pluto2.children.append(shader(objfile='sphere.obj',material_diffuse={'__UNKNOWN__':'io.jpg'},material_shininess=-1,fixtransformation=[[20,0,1,0],[1.5,0,0],['s',0.15,0.15,0.15]]))
  pluto2.children.append(shader(objfile='sphere.obj',material_diffuse={'__UNKNOWN__':'europa.jpeg'},material_shininess=-1,fixtransformation=[[60,0,1,0],[2.0,0,0],['s',0.5,0.5,0.5]]))
  pluto2.children.append(shader(objfile='rock2.obj',material_shininess=-1,fixtransformation=[[220,0,1,0],[3.0,0,0],['s',0.14,0.14,0.14]]))
  pluto2.children.append(shader(objfile='rock1.obj',material_shininess=-1,fixtransformation=[[220,0,1,0],[3.6,0,0],['s',12,12,12]]))
#  pluto2.children.append(shader(objfile='sphere.obj',material_diffuse={'__UNKNOWN__':'ganymede.jpg'},material_shininess=-1,fixtransformation=[[100,0,1,0],[3.0,0,0],['s',0.14,0.14,0.14]]))
#  pluto2.children.append(shader(objfile='sphere.obj',material_diffuse={'__UNKNOWN__':'triton.jpg'},material_shininess=-1,fixtransformation=[[160,0,1,0],[3.8,0,0],['s',0.3,0.3,0.3]]))
#  pluto2.children.append(shader(objfile='sphere.obj',material_diffuse={'__UNKNOWN__':'titan.jpg'},material_shininess=-1,fixtransformation=[[260,0,1,0],[4.9,0,0],['s',0.15,0.15,0.15]]))
  pluto2.children.append(shader(objfile='rock1.obj',material_shininess=-1,fixtransformation=[[220,0,1,0],[4.4,0,0],['s',10,10,10]]))
  pluto2.children.append(shader(objfile='rock2.obj',material_shininess=-1,fixtransformation=[[220,0,1,0],[5.0,0,0],['s',0.08,0.08,0.08]]))
  pluto3.children.append(pluto2)
  self.children.append(pluto3)


 def keyboard(self,**kwarg):
  if type(kwarg['key'])==str and re.search(r'^[xyz]$',kwarg['key'],flags=re.I) and shader.utili.mode=='grand':
   return super().keyboard(**dict(kwarg,key=[1 if kwarg['key'].islower() else -1,1 if kwarg['key'] in 'xX' else 0,1 if kwarg['key'] in 'yY' else 0,1 if kwarg['key'] in 'zZ' else 0]))
  return super().keyboard(**kwarg)
