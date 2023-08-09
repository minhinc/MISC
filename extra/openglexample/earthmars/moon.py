import re
import sys;sys.path.append('/home/minhinc/tmp')
from MISC.extra.shader import shader
class moon(shader):
 def __init__(self,*arg,**kwarg):
  super().__init__(**dict({'objfile':'sphere.obj','material_diffuse':{'__UNKNOWN__':'moonmap2k.jpg'},'fixtransformation':[[3,0,0],['s',0.64,0.64,0.64]]},**kwarg))
 def keyboard(self,**kwarg):
  if type(kwarg['key'])==str and re.search(r'^s$',kwarg['key'],flags=re.I):
   return super().keyboard(**dict(kwarg,transformation=self.fixtransformation))
  elif type(kwarg['key'])==str and re.search(r'^y$',kwarg['key'],flags=re.I):
   if shader.utili.mode!='grand':
    return super().keyboard(**dict(kwarg,key=[0.2,0,1,0]))
   else:
    return super().keyboard(**dict(kwarg,key=[round(360/28,3),0,1,0]))
  return super().keyboard(**kwarg)
