from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from PIL import Image
import sys;sys.path.append(os.path.expanduser('~')+r'/tmp/')
from MISC.extra.debugwrite import print
from MISC.extra.imageglobe.objloader import ObjFile
import numpy
import re,numpy as np,math
from MISC.utillib.util import utilcm


class openglutilc:
 def __init__(self):
  self.mode='local'
  self.distancetransformation={'x':[],'y':[],'z':[]}

 def normalize(self,vec):
  '''vec - (1,4,7)'''
  hypo=np.linalg.norm(vec)
  return [x/hypo for x in vec] if hypo else vec

 def getnormalvector(self,vertices,normalize=True):
  '''vertices - ((-1,0,0),(1,0,0),(1,1,-1),...)'''
  normal=[]
  for x in [np.cross((vertices[count+1][0]-vertices[count][0],vertices[count+1][1]-vertices[count][1],vertices[count+1][2]-vertices[count][2]),(vertices[count+2][0]-vertices[count+1][0],vertices[count+2][1]-vertices[count+1][1],vertices[count+2][2]-vertices[count+1][2])) for count in range(len(vertices)) if not count%3]:
   print(f'TEST {x=}')
   normal.extend([tuple(Utilc.normalize(x)) for count in range(3)]) if normalize else normal.append(tuple(x))
  return normal

 def drawaxis(self,linewidth=1,linelength=0.5):
  glDisable(GL_LIGHTING)
  print(f'drawaxis {linewidth=} {linelength=}')
#  tmp1=glGetMaterialfv(GL_FRONT,GL_DIFFUSE),glGetMaterialfv(GL_FRONT,GL_EMISSION)
  glLineWidth(linewidth)
  for i in zip((((-linelength,0,0),(2*linelength,0,0)),((0,-linelength,0),(0,2*linelength,0)),((0,0,-linelength),(0,0,2*linelength))),((0.5,0,0),(0,0.5,0),(0,0,0.5))):
   glBegin(GL_LINES)
#   if not tmp:
   glColor3f(*i[1])
#   else:
#    glMaterialfv(GL_FRONT,GL_DIFFUSE,(0,0,0,1.0))
#    glMaterialfv(GL_FRONT,GL_EMISSION,(*i[1],1.0))
   glVertex3f(*i[0][0])
   glVertex3f(*i[0][1])
   glEnd()
#  glMaterialfv(GL_FRONT,GL_DIFFUSE,tmp1[0])
#  glMaterialfv(GL_FRONT,GL_EMISSION,tmp1[1])
  glEnable(GL_LIGHTING)

 def display(self,**kwarg):
  print(f'><Utilc.display kwarg={kwarg.keys()}')
  for i in [i for i in ['color','diffuse'] if i in kwarg]:
   if type(kwarg[i][0])!=tuple:
    kwarg[i]=[kwarg[i]]*len(kwarg['vertices'])
   if 'normal' in kwarg and 'sidecolor' in kwarg:
#    kwarg[i]=[kwarg['sidecolor'][countl][1] if kwarg['normal'][count]==kwarg['sidecolor'][countl][0] else x for count,x in enumerate(kwarg[i]) for countl in range(len(kwarg['sidecolor']))]
    for count,x in enumerate(kwarg[i]):
     for countl in range(len(kwarg['sidecolor'])):
      if kwarg['normal'][count]==kwarg['sidecolor'][countl][0]:
       kwarg[i][count]=kwarg['sidecolor'][countl][1]
  if glGetBoolean(GL_LIGHTING) and (not 'texture' in kwarg or len(kwarg['texture'])==1):
   print(f'-------- multi texture   ')
   glMaterialfv(GL_FRONT,GL_AMBIENT,kwarg['ambient'] if 'ambient' in kwarg else (0.2,0.2,0.2,1.0))
   glMaterialfv(GL_FRONT,GL_SPECULAR,kwarg['specular'] if 'specular' in kwarg else (0,0,0,1.0))
   glMaterialfv(GL_FRONT,GL_SHININESS,kwarg['shininess'] if 'shininess' in kwarg else 0)
   glMaterialfv(GL_FRONT,GL_DIFFUSE,kwarg['diffuse']) if 'diffuse' in kwarg and not type(kwarg['diffuse'][0])==tuple else None
  if 'mode' in kwarg:
   for i in kwarg['indices']:
    glBegin(GL_TRIANGLES)
    for j in i:
     glColor3fv(kwarg['color'][j][:3]) if 'color' in kwarg else None
     glNormal3fv(kwarg['normal'][j]) if 'normal' in kwarg else None
     glMaterialfv(GL_FRONT,GL_DIFFUSE,kwarg['diffuse'][j]) if 'diffuse' in kwarg and type(kwarg['diffuse'][0])==tuple else None
     glVertex3fv(kwarg['vertices'][j])
    glEnd()
  elif not 'texture' in kwarg or len(kwarg['texture'])==1:
   glEnableClientState(GL_VERTEX_ARRAY)
   glEnableClientState(GL_NORMAL_ARRAY) if 'normal' in kwarg else None
   if 'texture' in kwarg:
    glEnableClientState(GL_TEXTURE_COORD_ARRAY)
    glEnable(GL_TEXTURE_2D)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE)
    glBindTexture(GL_TEXTURE_2D,kwarg['texture'][0])
   glVertexPointer(3,GL_FLOAT,0,kwarg['vertices'])
   glNormalPointer(GL_FLOAT,0,kwarg['normal']) if 'normal' in kwarg else None
   glTexCoordPointer(2,GL_FLOAT,0,kwarg['texcoord']) if 'texture' in kwarg else None
   glDrawArrays(GL_TRIANGLES, 0, int(len(kwarg['vertices'])/3))
   if 'texture' in kwarg:
    glDisable(GL_TEXTURE_2D)
    glDisableClientState(GL_TEXTURE_COORD_ARRAY)
   glDisableClientState(GL_NORMAL_ARRAY) if 'normal' in kwarg else None
   glDisableClientState(GL_VERTEX_ARRAY)
  elif 'texture' in kwarg:
   for count in range(len(kwarg['texture'])):
    glActiveTexture(GL_TEXTURE0+count)
    glClientActiveTexture(GL_TEXTURE0+count)
    glMaterialfv(GL_FRONT,GL_SPECULAR,kwarg['specular']) if glGetBoolean(GL_LIGHTING) and 'specular' in kwarg else None
    glMaterialfv(GL_FRONT,GL_SHININESS,kwarg['shininess']) if glGetBoolean(GL_LIGHTING) and 'shininess' in kwarg else None
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, kwarg['texture'][count])
    glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE if not count else GL_DECAL)
    glEnableClientState(GL_VERTEX_ARRAY)
    glVertexPointer(3,GL_FLOAT,0,kwarg['vertices'])
    glEnableClientState(GL_NORMAL_ARRAY) if 'normal' in kwarg else None
    glNormalPointer(GL_FLOAT,0,kwarg['normal']) if 'normal' in kwarg else None
    glEnableClientState(GL_TEXTURE_COORD_ARRAY)
    glTexCoordPointer(2,GL_FLOAT,0,kwarg['texcoord'])
  
   glDrawArrays(GL_TRIANGLES, 0, int(len(kwarg['vertices'])/3))
   glDisableClientState(GL_VERTEX_ARRAY)
   glDisableClientState(GL_NORMAL_ARRAY) if 'normal' in kwarg else None
   glDisableClientState(GL_TEXTURE_COORD_ARRAY)
   glDisable(GL_TEXTURE_2D)
   for count in range(len(kwarg['texture'][:-1])):
    glActiveTexture(GL_TEXTURE0+count)
    glClientActiveTexture(GL_TEXTURE0+count)
    glDisableClientState(GL_VERTEX_ARRAY)
    glDisableClientState(GL_NORMAL_ARRAY) if 'normal' in kwarg else None
    glDisableClientState(GL_TEXTURE_COORD_ARRAY)
    glDisable(GL_TEXTURE_2D)

 def getbuffer(self,vertices,begin,span,length,maketuple=True):
  '''\
  vertices - interleaved buffer vertices,normal,color,texture
  begin - begin count in interleaved buffer
  span - begin+count in interleaved buffer
  length - length of one unit i.e. vertices+normal+color+texture
  vertices=2,3,1,4,5,6,1,4,5,6,2,5,6,3,2,4.... begin=3 span=3 length=8 [(4,5,6),(5,6,3)]\
  '''
  if maketuple==True:
   return [tuple([vertices[count+begin+x] for x in range(span)]) for count in range(len(vertices)) if not count%length]
  else:
   return [y for count in range(len(vertices)) if not count%length for y in vertices[count+begin:count+begin+span]]
#  return [tuple([int(vertices[count+begin+x]) if int(vertices[count+begin+x])==vertices[count+begin+x] else vertices[count+begin+x] for x in range(span)]) for count in range(len(vertices)) if not count%length]

 def settlematrix(self,transformation):
  def getmatrix(transformation):
   if transformation[1]==1:
    return np.matrix([[1,0,0],[0,math.cos(math.pi*transformation[0]/180),-math.sin(math.pi*transformation[0]/180)],[0,math.sin(math.pi*transformation[0]/180),math.cos(math.pi*transformation[0]/180)]])
   elif transformation[2]==1:
    return np.matrix([[math.cos(math.pi*transformation[0]/180),0,math.sin(math.pi*transformation[0]/180)],[0,1,0],[-math.sin(math.pi*transformation[0]/180),0,math.cos(math.pi*transformation[0]/180)]])
   else:
    return np.matrix([[math.cos(math.pi*transformation[0]/180),-math.sin(math.pi*transformation[0]/180),0],[math.sin(math.pi*transformation[0]/180),math.cos(math.pi*transformation[0]/180),0],[0,0,1]])
  tmpmatrix=[x for x in transformation if len(x)==4 and not x[0]=='s']
  tmp=getmatrix(tmpmatrix[-2])@getmatrix(tmpmatrix[-1]) if len(tmpmatrix)>=2 else getmatrix(tmpmatrix[-1]) if len(tmpmatrix)==1 else None
  for i in range(len(tmpmatrix)-3,-1,-1):
   tmp=getmatrix(tmpmatrix[i])@tmp
  print(f'<>settlematrix {tmp=}')
  return tmp

 def keyboard(self,key,transformation):
  key=type(key)==bytes and key.decode() or type(key)==tuple and list(key) or key
#  key=[float(x) for x in re.findall('-?\d+(?:[.]\d+)?',key)] if key[0]=='[' or key[0]=='(' else key
  key=[float(re.sub(r'[\[\]]','',x)) if re.search('-?\d+(?:[.]\d+)?',x) else re.sub(r'[\[\]]','',x) for x in re.split(',',key)] if key[0]=='[' or key[0]=='(' else key
#  key=[float(re.sub(r'[\[\]\'"f]','',x)) if re.search('-?\d+(?:[.]\d+)?',x) else re.sub(r'[\[\]]','',x) for x in re.split(',',key)] if key[0]=='[' or key[0]=='(' else key
  '''
  if key[0]=='[' or key[0]=='(':
   if re.search('f',key,flags=re.I):
    while [xx for xx in transformation if len(xx)==3]:
     transformation.pop([count for count in range(len(transformation)) if len(transformation[count])==3][0])
   key=[float(re.sub(r'[\[\]\'"f]','',x)) if re.search('-?\d+(?:[.]\d+)?',x) else re.sub(r'[\[\]]','',x) for x in re.split(',',key)] if key[0]=='[' or key[0]=='(' else key
  '''
#  print(f'E Utilc.keyboard key={key} transformation={transformation} {self.mode=}')
  if type(key)==str and re.search(r'^[rRuUnN]$',key) or len(key)==3:
   '''
   if not type(key)==str:
    transformation[0:0]=[key]
   elif self.mode=='grand':
   '''
   if self.mode=='grand':
#    transformation[0:0]=[[float(key=='R' and -0.1 or key=='r' and 0.1),float(key=='U' and -0.1 or key=='u' and 0.1), float(key=='n' and 0.1 or key=='N' and -0.1)]]
    transformation[0:0]=[[float(key=='R' and -0.1 or key=='r' and 0.1),float(key=='U' and -0.1 or key=='u' and 0.1), float(key=='n' and 0.1 or key=='N' and -0.1)]] if type(key)==str else [key]
   else:
#    transformation.append([0,0,0,0]) if not len(transformation) else None
    transformation.append([0,0,0,0]) if not len([x for x in transformation if len(x)==4 and not x[0]=='s']) else None
    '''
    if re.search(r'^[Rr]$',key):
     transformation[0:0]=(self.settlematrix(transformation)[:,0]*(-0.1 if key=='R' else 0.1)).reshape(1,3).tolist()
    elif re.search(r'^[uU]$',key):
     transformation[0:0]=(self.settlematrix(transformation)[:,1]*(-0.1 if key=='U' else 0.1)).reshape(1,3).tolist()
    else:
     transformation[0:0]=(self.settlematrix(transformation)[:,2]*(-0.1 if key=='N' else 0.1)).reshape(1,3).tolist()
    '''
    if type(key)==str and re.search(r'^[Rr]$',key) or not type(key)==str and key[0]!=0:
     transformation[0:0]=(self.settlematrix(transformation)[:,0]*(key[0] if not type(key)==str else -0.1 if key=='R' else 0.1)).reshape(1,3).tolist()
    elif type(key)==str and re.search(r'^[uU]$',key) or not type(key)==str and key[1]!=0:
     transformation[0:0]=(self.settlematrix(transformation)[:,1]*(key[1] if not type(key)==str else -0.1 if key=='U' else 0.1)).reshape(1,3).tolist()
    else:
     transformation[0:0]=(self.settlematrix(transformation)[:,2]*(key[2] if not type(key)==str else -0.1 if key=='N' else 0.1)).reshape(1,3).tolist()
  elif type(key)==str and re.search(r'^[xyzXYZ]$',key) or len(key)==4 and not key[0]=='s':
   transformation[slice(*((1,1) if len(transformation)>0 and len(transformation[0])==3 else (0,0))) if self.mode=='grand' else slice(len(transformation),None)]=[[10*(-1 if key.isupper() else 1),1 if re.search(r'^[xX]$',key) else 0,1 if re.search(r'^[yY]$',key) else 0,1 if re.search(r'^[zZ]$',key) else 0] if type(key)==str else list(key)]
   '''
   print(f'openglutil old transformation {transformation=} {self.settlematrix(transformation)=}')
   angleindex=[xx for xx in range(len(transformation)) if len(transformation[xx])==4 and not re.search(r'[sS]',str(transformation[xx][0]))][0]
   transformation[angleindex:]=self.settlematrix(transformation)
   print(f'openglutil new transformation {angleindex=} {transformation=}')
   '''
  elif type(key)==str and re.search(r'^[Ss]$',key) or len(key)==4 and key[0]=='s':
#   transformation.insert(([count for count in range(len(transformation)) if transformation[count][0]=='s'] or [0])[0],['s',0.8,0.8,0.8] if key=='s' else ['s',1.2,1.2,1.2])
   transformation.insert(([count for count in range(len(transformation)) if transformation[count][0]=='s'] or [0])[0],['s',0.8,0.8,0.8] if key=='s' else ['s',1.2,1.2,1.2] if key=='S' else key)
  elif re.search(r'^[gG]$',key):
   self.mode='local'
   if re.search(r'^g$',key):
    self.mode='grand'
#  print(f'E openglutil.keyboard TEST {transformation=}')
  i=0
  while i<len(transformation):
   j=i+1
   if len(transformation[i])==3:
    while j<len(transformation) and len(transformation[j])==3:
     transformation[i]=(np.array(transformation[i])+np.array(transformation[j])).tolist()
     transformation[j:j+1]=[]
     j=i+1
   elif j<len(transformation) and len(transformation[i])==4 and not transformation[i][0]=='s':
    while j<len(transformation) and len(transformation[j])==4 and not transformation[j][0]=='s' and [k for k in range(1,4) if transformation[i][k]!=0 and transformation[i][k]==transformation[j][k]]:
     transformation[i][0]+=transformation[j][0]

     if transformation[i][0]<=-360 or transformation[i][0]>=360:
      transformation[i][0]%=360

     transformation[j:j+1]=[]
     j=i+1
   elif transformation[i][0]=='s':
    while j<len(transformation) and transformation[j][0]=='s':
     transformation[i][1:]=(np.array(transformation[i][1:])*np.array(transformation[j][1:])).tolist()
     transformation[j:j+1]=[]
     j=i+1
   i+=1
#  print(f'O openglutil.keyboard TEST2 {transformation=}')

 def pprint(self,**kwarg):
  print(f'{"":#>40}')
  for i in kwarg:
   print(f'{i+str(kwarg[i]):>40}')
  print(f'{"":#>40}')
 
 def transformanddrawaxis(self,transformation,lenattrib=None):
  [glTranslate(*x) for x in transformation if len(x)==3]
  [glScale(*x[1:]) for x in transformation if len(x)==4 and x[0]=='s']
  [glRotate(*x) for x in transformation if len(x)==4 and not x[0]=='s']
  Utilc.drawaxis(*lenattrib) if lenattrib else None

 def compileshader(self,*shaderfile):
  shaderprogram=[]
  if not type(shaderfile[0])==tuple and not type(shaderfile[0])==list:
   shaderfile=(shaderfile,)
  for counti,i in enumerate(shaderfile):
   shaderprogram.append(glCreateProgram())
   for count,j in enumerate(i):
    vertshader=glCreateShader((GL_VERTEX_SHADER,GL_FRAGMENT_SHADER)[count])
    glShaderSource(vertshader,open(j).read() if not re.search(r'^\s*void\s+main\s*\(.*?\)',j,flags=re.M) else j)
    glCompileShader(vertshader)
    if not glGetShaderiv(vertshader,GL_COMPILE_STATUS):
     print(f"ERROR {counti=} {('VERT','FRAG')[count]=} {glGetShaderInfoLog(vertshader)=}")
    else:
     print(f"SUCCESS {counti=} {('VERT','FRAG')[count]=}")
     glAttachShader(shaderprogram[-1],vertshader)
   glLinkProgram(shaderprogram[-1])
   if not glGetProgramiv(shaderprogram[-1], GL_LINK_STATUS):
    print(f'ERROR SHADER {counti=} {glGetShaderInfoLog(shaderprogram[-1])=}')
   else:
    print(f'SUCCESS SHADER {counti=}')
   if not hasattr(self,'opengl'):
    self.opengl={}
   if not shaderprogram[-1] in self.opengl:
    self.opengl[shaderprogram[-1]]={}
  print(f'><Utilc.compileshader {shaderprogram=}')
  print(f'TEST Utilc.compileshader {shaderprogram=} {self.opengl=}')
  return shaderprogram[0] if len(shaderprogram)==1 else tuple(shaderprogram)
 
 def getuniloc(self,uniformname,shaderprogram=None):
  print(f'><Utilc.getuniloc {shaderprogram=} {uniformname=} {self.opengl=}')
  if not shaderprogram:
   shaderprogram=glGetInteger(GL_CURRENT_PROGRAM)
#   print(f'TEST Utilc.getuniloc {shaderprogram=}')
  if not uniformname in self.opengl[shaderprogram]:
   self.opengl[shaderprogram][uniformname]=glGetUniformLocation(shaderprogram,uniformname)
#   print(f'TEST Utilc.getuniformloc {shaderprogram=} {uniformname=} {self.opengl=}')
  return self.opengl[shaderprogram][uniformname]

 def getattribloc(self,shaderprogram,attributename):
  print(f'><Utilc.getattribloc {shaderprogram=} {attributename=}')
  if not attributename in self.opengl[shaderprogram]:
   self.opengl[shaderprogram][attributename]=glGetAttribLocation(shaderprogram,attributename)
   print(f'TEST Utilc.getattribloc {shaderprogram=} {attributename=} {self.opengl=}')
  return self.opengl[shaderprogram][attributename]

 def createvao(self,*vao):
  '''createvao(init.shaderprogram,matt,8('coord',0,3),('normal',3,3),('texcoord',6,2))
  createvao((init.shaderprogram,matt,8,('coord',0,3),('normal',3,3),('texcoord',6,2)),(matt2,('coord',0,3)))'''
#  print(f'TEST Utilc.createvao {vao=}')
  if not type(vao[0])==tuple and not type(vao[0])==list:
   vao=(vao,)
  vaobj=glGenVertexArrays(len(vao))
  for count,i in enumerate(vao):
   glBindVertexArray(vaobj if not type(vaobj)==numpy.ndarray else vaobj[count])
   for j in i[3:]:
    glBindBuffer(GL_ARRAY_BUFFER, glGenBuffers(1))
    glBufferData(GL_ARRAY_BUFFER, np.array(self.getbuffer(i[1],j[1],j[2],i[2]),dtype=np.float32), GL_STATIC_DRAW)
    glEnableVertexAttribArray(self.getattribloc(i[0],j[0]))
    glVertexAttribPointer(self.getattribloc(i[0],j[0]),j[2],GL_FLOAT,GL_FALSE,0,None)
  return vaobj

 def createtextureobject(self,*,imagename,textureid=None):
  '''createtextureobject(imagename=('one.png','two.png'))
  createtextureobject(imagename='one.png',textureid=(1,)
  textureid - tuple -> pre created textureid'''
  imagename=(imagename,) if type(imagename)==str else imagename
  if textureid==None:
   textureid=glGenTextures(len(imagename))
   textureid=(textureid,) if not type(textureid)==np.ndarray else textureid
  else:
   textureid=(textureid,) if type(textureid)!=tuple and type(textureid)!=list else textureid
  print(f'TEST createtextureobject {imagename=} {textureid=}')
  for count,i in enumerate(textureid):
   img=Image.open(imagename[count]).convert('RGBA')
   img=img.transpose(Image.FLIP_TOP_BOTTOM)
   glBindTexture(GL_TEXTURE_2D,i)
   glTexImage2D(GL_TEXTURE_2D,0,GL_RGBA,img.width,img.height,0,GL_RGBA,GL_UNSIGNED_BYTE,img.tobytes())
   glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_WRAP_S,GL_REPEAT)
   glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_WRAP_T,GL_REPEAT)
   glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_NEAREST)
   glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_NEAREST)
#   glGenerateMipmap(GL_TEXTURE_2D)
   '''
   glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_LINEAR)
   glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_LINEAR_MIPMAP_LINEAR)
   glGenerateMipmap(GL_TEXTURE_2D)
   '''
  return textureid[0] if len(textureid)==1 else textureid

 def pushuniattribtoshader(self,*uniattrib):
  '''pushuniattribtoshader(('material.position',0,0,5),('light.shininess',40),..)'''
#  print(f'TEST Utilc.pushuniattribtoshader {uniattrib=}')
  if uniattrib and type(uniattrib[0])!=tuple and type(uniattrib[0])!=list and type(uniattrib[0])!=np.ndarray:
   uniattrib=(uniattrib,)
  elif uniattrib and (type(uniattrib[0][0])==tuple or type(uniattrib[0][0])==list or type(uniattrib[0])==np.ndarray):
   uniattrib=uniattrib[0]
  for i in uniattrib:
   if len(i[1:])>1:
    glUniform2f(self.getuniloc(i[0]),*i[1:]) if len(i[1:])==2 else glUniform3f(self.getuniloc(i[0]),*i[1:]) if len(i[1:])==3 else glUniform4f(self.getuniloc(i[0]),*i[1:])
   elif type(i[1])==int:
    glUniform1i(self.getuniloc(i[0]),i[1])
   elif type(i[1])==float:
    glUniform1f(self.getuniloc(i[0]),i[1])
   elif type(i[1])==tuple or type(i[1])==list:
    glUniform2f(self.getuniloc(i[0]),*i[1]) if len(i[1])==2 else glUniform3f(self.getuniloc(i[0]),*i[1]) if len(i[1])==3 else glUniform4f(self.getuniloc(i[0]),*i[1])




 def getcoord(self,*,begintime=None,duration=None,attribtuple=None):
  if not hasattr(getcoord,'timespan'):
   setattr(getcoord,'timespan',0)
   setattr(getcoord,'equation',equation())
   setattr(getcoord,'file',open('record.txt','w'))
   setattr(getcoord,'fps',15)
  if begintime==None:#for initialization
   return
  attribtuple=(attribtuple,) if not type(attribtuple)==tuple and not type(attribtuple)==list else attribtuple
 
  print(f'TEST {attribtuple=} {begintime=} {duration=}')
  for i in attribtuple[:]:
   if type(i['id'])==tuple or type(i['id'])==list:
    print(f'TEST1 {attribtuple=}\n{i=}')
    for j in i['id'][1:]:
     attribtuple.append(i.copy())
     attribtuple[-1]['id']=j
    i['id']=i['id'][0]
  print(f'TEST2 {attribtuple=}')
 
 # precision=0.1
 # precision=getcoord.precision
  lastkey=None
  begintime=getcoord.timespan+float(re.sub('^[+]','',begintime)) if type(begintime)==str else begintime
  getcoord.timespan=begintime+duration
  for i in attribtuple:
   if not 'begintime' in i and begintime:
    i['begintime']=begintime
   elif type(i['begintime'])==str:
    i['begintime']=begintime+float(re.sub('^[+]','',i['begintime']))
   if not 'duration' in i and duration:
 #   i['duration']=duration
    i['duration']=duration-((i['begintime']-begintime) if not type(i['begintime'])==str else float(re.sub('^[+]','',i['begintime'])))
 #  if 'equation' in i and 'angle' in i:
   if len([xx for xx in i if re.search('equation',xx,flags=re.I)]) and 'angle' in i:
    i['duration']=(i['duration'] if 'duration' in i else duration)*(360/i['angle'])
  begintime=min(x['begintime'] for x in attribtuple)
  duration=max(x['begintime']+x['duration'] for x in attribtuple)-begintime
   
 # for i in range(int(duration/precision)):
  for i in range(int(duration*getcoord.fps)):
 #  currenttime=begintime+i*precision
   currenttime=begintime+round(i/getcoord.fps,3)
 #  print(f"{i=} {begintime=} {getcoord.fps=} {currenttime=}")
   for j in attribtuple:
    if j['begintime']<=currenttime<j['begintime']+j['duration']:
 #    file.write(f"\n{round(begintime+i*precision,5)} {j['id']} {j['key'][0]}") if lastkey!=j['key'][0] and j['key'][0]!='s' else None
 #    file.write(f"\n{round(begintime+i*precision,5)} {j['id']} {j['key'][0] if j['key'][0] != 's' else 'g'}") if lastkey!=j['key'][0] else None
     if not re.search(r'^[cC]$',j['key'][0]):
 #     getcoord.file.write(f"\n{round(begintime+i*precision,5)} {j['id']} {j['key'][0] if not re.search(r'^[sS]$',j['key'][0]) else 'g' if j['key'][0]=='s' else 'G'}") if lastkey!=j['key'][0] else None
      getcoord.file.write(f"\n{round(begintime+i/getcoord.fps,3)} {j['id']} {j['key'][0] if not re.search(r'^[sS]$',j['key'][0]) else 'g' if j['key'][0]=='s' else 'G'}") if lastkey!=j['key'][0] else None
     elif j['begintime']==currenttime:
 #     getcoord.file.write(f"\n{round(begintime+i*precision,5)} {j['id']} {j['key'][0]}")
      getcoord.file.write(f"\n{round(begintime+i/getcoord.fps,3)} {j['id']} {j['key'][0]}")
      
     lastkey=j['key'][0] if not re.search(r'^[cCsS]$',j['key'][0]) else 'g' if j['key'][0]=='s' else 'G' if j['key'][0]=='S' else lastkey
 #    if not 'equation' in j and 'angle' in j:
     if not len([xx for xx in j if re.search('equation',xx,flags=re.I)]) and 'angle' in j:
 #     getcoord.file.write(f"\n{round(begintime+i*precision,5)} {j['id']} {list(((j['angle']*precision)/j['duration'],*j['key'][1]))}")
      getcoord.file.write(f"\n{round(begintime+i/getcoord.fps,3)} {j['id']} {list(((j['angle']/getcoord.fps)/j['duration'],*j['key'][1]))}")
 #    elif 'equation' in j:
 #     if currenttime==j['begintime']:
 #      j['data']=getcoord.equation.ellipse(*j['equation'])
 #      j['count']=0
 #     else:
 #      j['count']+=1
 #     getcoord.file.write(f"\n{round(begintime+i*precision,5)} {j['id']} [f,{j['data'][j['count']][0]},0,{j['data'][j['count']][1]}]") if j['count']<len(j['data']) else None
     elif len([xx for xx in j if re.search('equation',xx,flags=re.I)]):
 #     print(f"equation {currenttime=} {j['begintime']}=")
      if currenttime==j['begintime']:
       equationfunc=[xx for xx in j if re.search('equation',xx,flags=re.I)][0]
       j['data']=eval('getcoord.equation.'+re.sub(r'^.*?_(.*)',r'\1',equationfunc)+"(*j['"+equationfunc+"'])")
       j['count']=0
      elif currenttime>j['begintime']:
       j['count']+=1
 #     getcoord.file.write(f"\n{round(begintime+(i*precision if j['data'][j['count']][0]==precision else (i-1)*precision+j['data'][j['count']][0] if i!=0 else 0),3)} {j['id']} {j['data'][j['count']][1:]}") if j['count']<len(j['data']) else None
      getcoord.file.write(f"\n{round(begintime+(i/getcoord.fps if j['data'][j['count']][0]==round(1/getcoord.fps,3) else (i-1)/getcoord.fps+j['data'][j['count']][0] if i!=0 else 0),3)} {j['id']} {j['data'][j['count']][1:]}") if j['count']<len(j['data']) else None
     elif len(j['key'])==2:
 #     print(f'{j=}')
 #     fraction=round(math.pow(j['key'][1],precision/j['duration']),5)
      fraction=round(math.pow(j['key'][1],round(1/getcoord.fps,3)/j['duration']),3)
 #     getcoord.file.write(f"\n{round(begintime+i*precision,5)} {j['id']} [s,{fraction},{fraction},{fraction}]")
      getcoord.file.write(f"\n{round(begintime+i/getcoord.fps,3)} {j['id']} [s,{fraction},{fraction},{fraction}]")
     elif not re.search(r'^[cC]$',j['key'][0]):
 #     getcoord.file.write(f"\n{round(begintime+i*precision,5)} {j['id']} {[(j['key'][2][count]-j['key'][1][count])/(j['duration']/precision) for count in range(3)]}")
      getcoord.file.write(f"\n{round(begintime+i/getcoord.fps,3)} {j['id']} {[(j['key'][2][count]-j['key'][1][count])/(j['duration']*getcoord.fps) for count in range(3)]}")
 #    if 'image' in j and j['begintime']+j['image'][0][0]<=currenttime:
     if 'image' in j and j['begintime']==currenttime:
 #     getcoord.file.write(f"\n{round(begintime+i*precision,5)} {j['id']} texture_{j['image']}")
      getcoord.file.write(f"\n{round(begintime+i/getcoord.fps,3)} {j['id']} texture_{j['image']}")
  
  getcoord.file.close()
  '''
  tmparray=sorted([x for x in re.split('\n',open('record.txt').read()) if not re.search('^\s*$',x)],key=lambda m:float(re.split(r'\s+',m)[0]))
  getcoord.file=open('record.txt','w')
  [getcoord.file.write(f'\n{x}') for x in tmparray]
  getcoord.file.close()
  '''
class equation:
 def ellipse(self,angle,duration,rx,ry,offset=0,precision=0.1):
  data=[(math.cos(i*math.pi/180),-math.sin(i*math.pi/180)) for i in np.arange(angle[0],angle[1],(precision*(angle[1]-angle[0]))/duration)]
  data=[(round(rx*i[0],3)+offset,round(ry*i[1],3)) for i in data]
  print(f'equation.ellipse {len(data)=} {data=}')
  return data

 def locallate(self,data):
  for i in range(len(data)-1,0,-1):
    data[i]=[round(data[i][0],3),*[round(data[i][x]-data[i-1][x],9) for x in range(1,4)]]
  return data
 def mgh(self,height,precision,gravity,offset=None,audiofile=None,reboundpercentage=0.8):
  print(f'E mgh {(height,precision,gravity,offset)=}')
  def getdata(height,precision,maxheight,acceleration,offset):
   count=0
   data=[]
   totaltime=math.sqrt(height*2/acceleration)
   while True:
    distance=0.5*acceleration*math.pow(count*precision,2)
#    print(f'--> {(count,precision,count*precision,totaltime,distance,offset)=}')
    if count*precision>=totaltime or distance>=height:
     data.append([totaltime-(count-1)*precision,0,height*-1,0])
     break
    data.append([precision,0,distance*-1,0])
    count+=1
#   data=[[round(x[0],3),str(round(x[1],3)),f'f{round(round(x[2]-(maxheight-abs(data[-1][2])),3)+offset[1],3)}',str(round(x[3],3))] for x in data]
   data=[[x[0],x[1],x[2]-(maxheight-abs(data[-1][2]))+offset[1],x[3]] for x in data]
   return data
 
  data=[]
  reverse=False
  heightl=height
  countl=0
  while height>0.0001 and countl<100:
   countl+=1
#   print(f'mgh {countl=}')
   datal=getdata(height,precision,heightl,gravity,offset if offset else (0,0,0))
   if reverse:
#    print(f'm1 mgh{height=} {data=}\n')
    for ii in range(len(datal)-1):
     datal[ii][0]=datal[ii+1][0]
#    data.extend(list(reversed(datal[:-1])))
    data.extend(xx.copy() for xx in reversed(datal[:-1]))
#    print(f'm2 mgh{height=} {data=}\n')
   data.extend(datal if not reverse else datal[1:])
   if int(12*height/heightl):
    data+=[[precision,audiofile+'_'+str(int(12*height/heightl))]]
#   print(f'm mgh{height=} {data=}\n')
   height=round(height*reboundpercentage,5)
   reverse=True
  print(f'1 MM {data=}')
  mimeindex=[(xx,data[xx]) for xx in range(len(data)) if re.search('[.]mp3',str(data[xx][1]),flags=re.I)]
  data=self.locallate([x for x in data if not re.search(r'[.]mp3',str(x[1]),flags=re.I)])
  for count,ii in enumerate(mimeindex):
   print(f'mimeindex {(count,ii)=}')
   data[ii[0]:ii[0]]=[mimeindex[count][1]]
   count+=1
  print(f'2 MM {data=}')
  return data+[[precision,0,0,0] for x in range(int(1//precision*4))]

class Shape:
 def __init__(self,*arg,**kwarg):
  '''kwarg['obj'] - objectfile
  kwarg['diffuse'] - diffuse'''
  print(f'<=>Shape.__init__ arg={arg} kwarg={kwarg}')
  filedata=None
  self.texture=None
  if 'texture' in kwarg:
   self.texture=glGenTextures(type(kwarg['texture'])==str and 1 or len(kwarg['texture']))
   self.texture=(self.texture,) if not type(self.texture)==numpy.ndarray else tuple(self.texture)
   kwarg['texture']=type(kwarg['texture'])==str and (kwarg['texture'],) or kwarg['texture']
   print(f"<=>Shape.__init__ {self.texture=} {kwarg['texture']=}")
   for count,i in enumerate(kwarg['texture']):
    img=Image.open(i[0] if type(i)==tuple else i).convert('RGBA')
    img=img.transpose(Image.FLIP_TOP_BOTTOM)
    img.putalpha(i[1]) if type(i)==tuple else None
    glBindTexture(GL_TEXTURE_2D,self.texture[count])
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
# glTexParameterfv(GL_TEXTURE_2D, GL_TEXTURE_BORDER_COLOR, (1.0,1,0,1.0))
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, img.width, img.height, 1, GL_RGBA, GL_UNSIGNED_BYTE, img.tobytes())

  self.m=list(ObjFile(kwarg['obj']).objects.values())[0]
  with open(kwarg['obj']) as file:
   filedata=file.read()
  self.vertices=Utilc.getbuffer(self.m.vertices,0,3,8,maketuple=True if 'mode' in kwarg else False)
  self.normal=Utilc.getbuffer(self.m.vertices,3,3,8,maketuple=True if 'mode' in kwarg else False)
  self.texcoord=Utilc.getbuffer(self.m.vertices,6,2,8,maketuple=True if 'mode' in kwarg else False)
  self.indices=self.m.indices
  self.kwarg=kwarg

 def display(self,**kwarg):
  '''\
  kwarg['normalize'] - vertices/normalize size would change
  kwarg['color'] - (normalvector,color) side of model would change\
  '''
  print(f'><Shape.display')
#  Utilc.display(vertices=[tuple([y/('normalize' in kwarg and kwarg['normalize'] or 1) for y in x]) for x in self.vertices],normal=self.normal,indices=self.indices,**kwarg)
#  self.kwarg.update({x:y for x,y in dict(vertices=self.vertices,normal=self.normal,texcoord=self.texcoord,texture=self.texture,indices=self.indices).items() if y})
#  self.kwarg.update(kwarg)
  Utilc.display(**dict(list(self.kwarg.items())+list(dict(vertices=self.vertices,normal=self.normal,texcoord=self.texcoord,texture=self.texture,indices=self.indices).items())+list(kwarg.items())))

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
  super(Pyramid,self).display(mode='triangle',**kwarg)
import MISC.utillib.util;MISC.utillib.util.cmc(__name__,MISC.utillib.util.mce(__name__,openglutilc) or openglutilc())
