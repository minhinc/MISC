from abc import ABC,abstractmethod

class _shapec(ABC):
 @abstractmethod
 def __init__(self,*, internaltransformation_=None, objfile_=None, graphicscard_=None):
  print(f'>< {internaltransformation_=} {objfile_}=')
  self.internaltransformation=internaltransformation_
  self.objfile=objfile_
  self.graphicscard=graphicscard_

 @abstractmethod
 def draw(self,*,externaltransformation_):
  print(f'>< {externaltransformation_=}')
  self.graphicscard.createvaovbo(self.objfile_)
  drawfromarray
