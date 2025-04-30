from abc import ABC, abstractmethod
class _graphicscard(ABC):
 def __init__(self,*arg,**argkw):
  print(f'>< {arg=} {argkw=}')
  self.vertshader=[]
  self.fragshader=[]
 def push(self,objfile_):

 def compile(self,*,vertshader_,fragshader_):
  if not [x for x in self.vertshader if x==vertshader]:
   compilte
   self.vertshader.append(vertshader_)
  if not [x for x in self.fragshader if x==fragshader]:
   compilte
   self.fragshader.append(fragshader_)
