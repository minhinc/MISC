from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys;sys.path.append(os.path.expanduser('~')+r'/tmp/')
from MISC.extra.debugwrite import print
from kivy.resources import resource_find
from objloader import ObjFile
import re,numpy as np,math


class Utilc:
 @staticmethod
 def normalize(vec):
  hypo=np.linalg.norm(vec)
  return [x/hypo for x in vec] if hypo else vec

 @staticmethod
 def getnormalvector(vertices):
  '''vertices - ((1,0,1),(1,-1,0))...'''
  normal=[]
  for x in [np.cross((vertices[count+1][0]-vertices[count][0],vertices[count+1][1]-vertices[count][1],vertices[count+1][2]-vertices[count][2]),(vertices[count+2][0]-vertices[count+1][0],vertices[count+2][1]-vertices[count+1][1],vertices[count+2][2]-vertices[count+1][2])) for count in range(len(vertices)) if not count%3]:
   normal.extend([tuple(Utilc.normalize(x)) for count in range(3)])
  return normal

 @staticmethod
 def display(**kwarg):
  print(f'><Utilc.display kwarg={kwarg}')
  for i in [i for i in ['color','diffuse'] if i in kwarg]:
   if type(kwarg[i][0])!=tuple:
    kwarg[i]=[kwarg[i]]*len(kwarg['vertices'])
   if 'normal' in kwarg and 'sidecolor' in kwarg:
#    kwarg[i]=[kwarg['sidecolor'][countl][1] if kwarg['normal'][count]==kwarg['sidecolor'][countl][0] else x for count,x in enumerate(kwarg[i]) for countl in range(len(kwarg['sidecolor']))]
    for count,x in enumerate(kwarg[i]):
     for countl in range(len(kwarg['sidecolor'])):
      if kwarg['normal'][count]==kwarg['sidecolor'][countl][0]:
       kwarg[i][count]=kwarg['sidecolor'][countl][1]
  glMaterialfv(GL_FRONT,GL_AMBIENT,kwarg['ambient'] if 'ambient' in kwarg else (0.2,0.2,0.2,1.0))
  glMaterialfv(GL_FRONT,GL_SPECULAR,kwarg['specular'] if 'specular' in kwarg else (0,0,0,1.0))
  glMaterialfv(GL_FRONT,GL_SHININESS,kwarg['shininess'] if 'shininess' in kwarg else 0)
  glMaterialfv(GL_FRONT,GL_DIFFUSE,kwarg['diffuse']) if 'diffuse' in kwarg and not type(kwarg['diffuse'][0])==tuple else None
  for i in kwarg['indices']:
   glBegin(GL_TRIANGLES)
   for j in i:
    glColor3fv(kwarg['color'][j][:3]) if 'color' in kwarg else None
    glNormal3fv(kwarg['normal'][j]) if 'normal' in kwarg else None
    glMaterialfv(GL_FRONT,GL_DIFFUSE,kwarg['diffuse'][j]) if 'diffuse' in kwarg and type(kwarg['diffuse'][0])==tuple else None
    glVertex3fv(kwarg['vertices'][j])
   glEnd()

 @staticmethod
 def getbuffer(vertices,begin,span,length):
  '''\
  vertices - interleaved buffer vertices,normal,color,texture
  begin - begin count in interleaved buffer
  span - begin+count in interleaved buffer
  length - length of one unit i.e. vertices+normal+color+texture
  vertices=2,3,1,4,5,6,1,4,5,6,2,5,6,3,2,4.... begin=3 span=3 length=8 [(4,5,6),(5,6,3)]\
  '''
  return [tuple([int(vertices[count+begin+x]) if int(vertices[count+begin+x])==vertices[count+begin+x] else vertices[count+begin+x] for x in range(span)]) for count in range(len(vertices)) if not count%length]

 @staticmethod
 def keyboard(key,transformation):
  key=bytes(key)
  print(f'><Utilc.keyboard key={key} transformation={transformation}')
  if re.search(r'^[lrudnf]$',key.decode()):
   transformation.append([float(key==b'l' and -0.1 or key==b'r' and 0.1),float(key==b'd' and -0.1 or key==b'u' and 0.1), float(key==b'n' and 0.1 or key==b'f' and -0.1)])
  elif re.search(r'^[xyzXYZ]$',key.decode()):
   transformation.append([10*(-1 if key.decode().isupper() else 1),1 if re.search(r'^[xX]$',key.decode()) else 0,1 if re.search(r'^[yY]$',key.decode()) else 0,1 if re.search(r'^[zZ]$',key.decode()) else 0])
  if len(transformation)>1 and len(transformation[-1])==len(transformation[-2]):
   if len(transformation[-1])==3:
    for i in range(3):
     transformation[-1][i]+=transformation[-2][i]
    transformation[-2:-1]=[]
   elif [i for i in range(1,4) if transformation[-1][i]!=0 and transformation[-1][i]==transformation[-2][i]]:
    transformation[-1][0]+=transformation[-2][0]
    transformation[-2:-1]=[]
 @staticmethod
 def pprint(**kwarg):
  print(f'{"":#>40}')
  for i in kwarg:
   print(f'{i+str(kwarg[i]):>40}')
  print(f'{"":#>40}')
 
class Shape:
 def __init__(self,*arg,**kwarg):
  '''kwarg['obj'] - objectfile
  kwarg['diffuse'] - diffuse'''
  print(f'<=>Shape.__init__ arg={arg} kwarg={kwarg}')
  self.m=list(ObjFile(resource_find(kwarg['obj'])).objects.values())[0]
  self.vertices=Utilc.getbuffer(self.m.vertices,0,3,8)
  self.normal=Utilc.getbuffer(self.m.vertices,3,3,8)
  self.indices=Utilc.getbuffer(self.m.indices,0,3,3)

 def display(self,**kwarg):
  '''\
  kwarg['normalize'] - vertices/normalize size would change
  kwarg['color'] - (normalvector,color) side of model would change\
  '''
  print(f'><Shape.display')
#  Utilc.display(vertices=[tuple([y/('normalize' in kwarg and kwarg['normalize'] or 1) for y in x]) for x in self.vertices],normal=self.normal,indices=self.indices,**kwarg)
  Utilc.display(vertices=self.vertices,normal=self.normal,indices=self.indices,**kwarg)

class Pyramid(Shape):
 def __init__(self,*arg,**kwarg):
  self.vertices=((1,0,0),(-1,0,0),(0,0,-1), (-1,0,0),(1,0,0),(0,0,1), (1,0,0),(0,0,-1),(0,1,0), (0,0,-1),(-1,0,0),(0,1,0), (-1,0,0),(0,0,1),(0,1,0), (0,0,1),(1,0,0),(0,1,0))
  self.indices= ((0,1,2),(3,4,5),(6,7,8),(9,10,11),(12,13,14),(15,16,17))
  self.color=[(0,1,0) if x==(1,0,0) or x==(-1,0,0) else (0,0,1) if x==(0,0,-1) or x==(0,0,1) else (1,0,0) for x in self.vertices]
  self.normal=Utilc.getnormalvector(self.vertices)
  print(f'<=>pyramid.__init__ vertices={self.vertices} color={self.color} normal={self.normal} indices={self.indices}')

 '''
 def display(self):
  print(f><pyramid.display')
  glEnableClientState(GL_COLOR_ARRAY)
  glEnableClientState(GL_VERTEX_ARRAY)
  glColorPointer(3,GL_FLOAT,0,self.color)
  glVertexPointer(3,GL_INT,0,self.vertices)
  for i in range(6):
   glDrawElements(GL_TRIANGLES,3,GL_UNSIGNED_BYTE,surface[i])

#  glDrawElements(GL_TRIANGLES,6*3,GL_UNSIGNED_BYTE,self.indices)
 '''
 def display(self,**kwarg):
  if not 'color' in kwarg and hasattr(self,'color'):
   kwarg['color']=kwarg['diffuse']=self.color
  super(Pyramid,self).display(**kwarg)
