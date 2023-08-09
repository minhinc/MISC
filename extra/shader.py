#from abc import ABC, abstractmethod
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import re
from PIL import Image
import numpy as np
import time
import sys;sys.path.append('/home/minhinc/tmp')
from MISC.extra import objfileloader
from MISC.extra.openglutil import Utilc
from MISC.utillib.util import Util

vertsource1="""\
#version 330
uniform mat4 projection;
uniform mat4 modelviewsphere;
//uniform mat4 transposeinversemodelviewsphere;
attribute vec3 coord;
attribute vec3 normal;
attribute vec2 texcoord;
varying vec3 vertex_coord;
varying vec3 vertex_normal;
varying vec2 vertex_texcoord;
void main() {
 gl_Position=projection * (modelviewsphere * vec4(coord,1.0));
 vertex_coord=(modelviewsphere*vec4(coord,1.0)).xyz;
// vertex_normal=(transposeinversemodelviewsphere*vec4(normal,1.0)).xyz;
 vertex_normal=mat3(modelviewsphere)*normal;
 vertex_texcoord=texcoord;
};"""

fragsource1="""\
#version 330
#define MAXLIGHTCOUNT 20
struct Material {
 sampler2D diffuse;
 vec3 diffuse2;
 vec3 ambient;
 vec3 specular;
 vec3 emission;
 int shininess; /* -1 -> Lighting disabled*/
};

struct Light {
 vec4 position;/*position.w 0 -> directional 1 -> positional 2 -> not attenuation -1 -> light switched off*/
 vec3 ambient;
 vec3 diffuse;
 vec3 specular;
 vec3 spotdirection;
 int spotangle;
 int spotexponent;
};

uniform Material material;
uniform Light[MAXLIGHTCOUNT] light;
uniform int textureb;
uniform int lightcounti;
varying vec3 vertex_coord;
varying vec3 vertex_normal;
varying vec2 vertex_texcoord;
void main() {
 vec3 N,L,R,E,D;
 vec3 out_color=vec3(0,0,0);
 N=normalize(vertex_normal);
 E=normalize(vec3(0,0,0)-vertex_coord);
 float attenuation=0.0;
 float distanceLV=0.0;
 float spotfactor;
 for (int i=0;i<lightcounti; i++) {
  if (light[i].position.w==-1 || material.shininess <0) {
   continue;
  }
  L=normalize(light[i].position.w>=1.0?light[i].position.xyz-vertex_coord:light[i].position.xyz);
  R=-reflect(L,N);
  D=normalize(light[i].spotdirection);
  float spotfactor=(light[i].spotangle==90 || light[i].position.w==0.0?1.0:0.0);
//  spotfactor=1.0;
  attenuation=1.0;
  if (light[i].position.w==1.0) {
   distanceLV=distance(light[i].position.xyz,vertex_coord);
   attenuation=clamp(10/(1+distanceLV),0.0,1.0);
  }
  if (light[i].spotangle!=90 && light[i].position.w!=0.0 && dot(D,L) >= cos((3.14*light[i].spotangle)/180)) {
   spotfactor=pow(max(0,dot(D,L)),light[i].spotexponent);
  }
  if (textureb==1) {
    out_color+=vec3(attenuation*spotfactor*vec3(material.emission + light[i].ambient*material.ambient * texture(material.diffuse,vertex_texcoord).rgb + light[i].specular * pow(max(0.0,dot(E,R)),material.shininess) * material.specular + light[i].diffuse * max(0.0,dot(L,N)) * texture(material.diffuse,vertex_texcoord).rgb));
  } else {
    out_color+=vec3(attenuation*spotfactor*vec3(material.emission + light[i].ambient*material.ambient + light[i].specular * pow(max(0.0,dot(E,R)),material.shininess) * material.specular + light[i].diffuse * max(0.0,dot(L,N)) * material.diffuse2));
  }
 }
 if (lightcounti==0 || material.shininess<0) {
  if (textureb==1) {
//   gl_FragColor=vec4(texture(material.diffuse,vertex_texcoord).rgb,1.0);
   gl_FragColor=texture(material.diffuse,vertex_texcoord);
  } else {
   gl_FragColor=vec4(material.diffuse2,1.0);
  }
 } else {
//  gl_FragColor=vec4(clamp(out_color,0,1),1.0);
  gl_FragColor=vec4(clamp(out_color,0,1),texture(material.diffuse,vertex_texcoord).a);
 }
};"""

#class shader(ABC):
class shader:
 shaderprogram=None
 texturename={} # {'abc.png':1,..} {<imagename>,<textureid>}
 lightposition={} # {<objectinstance>:{'position':(1,0,10),spotangle:20,spotdirection:(0,0,1,0),spotexponent:23},..}
 utili=Utilc()
 unknowntexture='__UNKNOWN__'
 defaultuniform=dict((('material.diffuse',0),('material.diffuse2',(1,0,0)),('material.specular',(0,0,0)),('material.emission',(0,0,0)),('material.ambient',(0,0,0)),('material.shininess',1)))
 vao={} # {'objfile':[imagecolor,vaomaterialname,vaolength,vaoid],..} # vao can be texture or color vao
 focusobject=None
 def __init__(self,*,objfile,id=None,addaxis=True,**kwarg):
  '''\
  shader(objfile='sphere.obj',material_diffuse={'__UNKNOWN__':'yellowworldmap.png'},fixtransformation=[[0,0,6],['s',0.2,0.2,0.2]],extratransformation=[30,0,0,1] \
  '''
  self.children=[]
  self.innerchildren=[]
  [setattr(self,x[0],x[1]) for x in dict({'transformation':[],'fixtransformation':[]},**kwarg).items() if not hasattr(self,x[0])]
  self.fixtransformation.sort(key=lambda x:len(x)!=3);self.fixtransformation.sort(key=lambda x:len(x)==4 and x[0]=='s')
  if not shader.shaderprogram:
   shader.shaderprogram=self.utili.compileshader(vertsource1,fragsource1)
   glUseProgram(shader.shaderprogram)
  shader.focusobject=self
  self.addlight(**{re.sub('^light_','light.',x):y for x,y in kwarg.items() if re.search(r'^light_',x)}) if 'light_position' in kwarg else None
  self.objfile=objfile
  self.id=shader.getid() if not id else id
  if not objfile or objfile in shader.vao:
   Util.pprint('DID NOT PROCEED',objfile,self,self.id)
   return
  obj=objfileloader.OBJ(objfile)
  #coord and normal is expected in all obj file
  texcoord,usemtl=obj.drawarrayvertices[6]!=-1,obj.drawarrayvertices[8]
  countl=0
  record=False
  self.children.append(shader(objfile='axis.obj',material_shininess=-2,addaxis=False)) if addaxis else None

  def pushtovao(count1,count2,imagecolor,vaomaterialname):
   nonlocal self,texcoord
#   print(f" TEST {imagecolor=} {shader.shaderprogram=}")
   if objfile not in shader.vao:
    shader.vao[objfile]=[]
   shader.vao[objfile].append([imagecolor,vaomaterialname,count2-count1,self.utili.createvao(shader.shaderprogram,obj.drawarrayvertices[count1*9:count2*9],9,*[x for x in [('coord',0,3),('normal',3,3),('texcoord',6,2)] if x!=('texcoord',6,2) or texcoord])])
  for count,i in enumerate([obj.drawarrayvertices[count:count+9] for count in range(len(obj.drawarrayvertices)) if not count%9]):
   if (i[6]!=-1)!=texcoord or usemtl!=i[8]:
    pushtovao(countl,count,texcoord and usemtl!=-1 and 'map_Kd' in obj.mtl[usemtl] and obj.mtl[usemtl]['map_Kd'] or usemtl!=-1 and 'Kd' in obj.mtl[usemtl] and obj.mtl[usemtl]['Kd']  or shader.defaultuniform['material.diffuse2'],usemtl!=-1 and obj.mtl[usemtl]['name'] or texcoord and shader.unknowntexture or None)
    texcoord,usemtl=i[6]!=-1,i[8]
    countl=count
  pushtovao(countl,count+1,texcoord and usemtl!=-1 and 'map_Kd' in obj.mtl[usemtl] and obj.mtl[usemtl]['map_Kd'] or usemtl!=-1 and 'Kd' in obj.mtl[usemtl] and obj.mtl[usemtl]['Kd']  or shader.defaultuniform['material.diffuse2'],usemtl!=-1 and obj.mtl[usemtl]['name'] or texcoord and shader.unknowntexture or None)

 def transformmatrix(self,transformation):
  [glTranslate(*x) if len(x)==3 else glRotate(*x) if not x[0]=='s' else glScalef(*x[1:]) for x in transformation]

 def switchlight(self,on=True):
  print(f'TEST shader.switchlight {shader.lightposition=}')
  if len(shader.lightposition[self]['light.position'])==4:
   shader.lightposition[self]['light.position']=list(shader.lightposition[self]['light.position'])+list(shader.lightposition[self]['light.position'])[3:4]
  shader.lightposition[self]['light.position'][3]=-1 if not on else shader.lightposition[self]['light.position'][4]
  shader.utili.pushuniattribtoshader(('light['+str(list(shader.lightposition).index(self))+'].position',shader.lightposition[self]['light.position'][0:4]))

 def addlight(self,**kwarg):
  if not self in shader.lightposition:
   shader.lightposition[self]=dict({'light.position':(0,0,0,1),'light.ambient':(0,0,0),'light.diffuse':(0,0,0),'light.specular':(0,0,0),'light.spotangle':90,'light.spotexponent':0,'light.spotdirection':(0,0,1)},**kwarg)
   shader.utili.pushuniattribtoshader(('lightcounti',len(shader.lightposition)),*[('light['+str(len(shader.lightposition)-1)+'].'+re.sub(r'^.*[.](.*)$',r'\1',x),y) for x,y in shader.lightposition[self].items()])
  print(f'<>shader.addlight {self=} {kwarg=} {shader.lightposition=}')

 @staticmethod
 def getid():
  if not hasattr(shader.getid,'count'):
   setattr(shader.getid,'count',0)
  shader.getid.count+=1
  return str(shader.getid.count)
 '''
 def drawtexture(self):
  for i in self.texname:
   glActiveTexture(GL_TEXTURE0+count)
   glEnable(GL_TEXTURE_2D)
   glBindTexture(GL_TEXTURE_2D,self.texname[count])
   glBindVertexArray(self.vao)
  glDrawArrays(GL_TRIANGLES,0,len(self.matt)//8)
  glDisable(GL_TEXTURE_2D)
 '''

 def difftranslation(self,transformation):
  difftransformation=[]
  if len(self.transformation)==0 or len(self.transformation[0])!=3:
   difftransformation=(len(transformation)==0 or len(transformation[0])!=3) and [] or transformation[0]
   if transformation and len(transformation[0])==3:
    self.transformation[0:0]=[x for x in transformation[0]]
  else:
   difftransformation=[transformation[0][i]-self.transformation[0][i] for i in range(3)]
   self.transformation[0]=[x for x in transformation[0]]
  return difftransformation

 def diffrotation(self,transformation):
  difftransformation=[]
  diffcount=count=0
  if transformation and len(transformation[0])==3:
   count+=1
  if self.transformation and len(self.transformation[0])==3:
   diffcount+=1
  while count<len(transformation) or diffcount<len(self.transformation):
   if diffcount==len(self.transformation) and count<len(transformation):
    for i in transformation[count:]:
     self.transformation.append([x for x in i])
     difftransformation.append([x for x in i])
     count+=1
   elif diffcount==(len(self.transformation)-1) and count==(len(transformation)-1) and self.transformation[0]==transformation[0]:
    difftransformation=[transformation[count]-self.transformation[diffcount] for x in transformation[count]]
    self.transformation[diffcount]=[x for x in transformation[count]]
    diffcount+=1
    count+=1
   elif self.transformation[diffcount][0] != transformation[count][0]:
    count+=1
   else:
    diffcount+=1
    count+=1
  return difftransformation

# @abstractmethod
 '''
 def getchildrencount(self):
  if not hasattr(self,'childrencount'):
   setattr(self,'childrencount',0)
  else:
   self.childrencount+=1
  return self.childrencount
 '''

 def getfocusobject(**kwarg):
  '''keyboard(key)
  keyboard(key,transformation=[2,0,0])'''
#  print(f'TEST shader.keyboard {kwarg=}')
#  print(f'TEST shader.keyboard {shader.keyboard.key=}') if hasattr(shader.keyboard,'key') else None
#  kwarg['key']=kwarg['key'].decode() if type(kwarg['key'])==bytes else [float(x) for x in re.findall('-?\d+(?:[.]\d+)?',kwarg['key'])] if type(kwarg['key'])==str and re.search(r'^(\[|\()',kwarg['key']) else kwarg['key']
  '''
  if not hasattr(shader.keyboard,'count'):
   setattr(shader.keyboard,'count',0)
  '''
  if not hasattr(shader.getfocusobject,'key'):
   setattr(shader.getfocusobject,'key','')
  if type(kwarg['key'])==str and re.search(r'^(:|\d)$',kwarg['key'],flags=re.I):
   shader.getfocusobject.key='' if not type(shader.getfocusobject.key)==str or not re.search(r'^\d',shader.getfocusobject.key) else shader.getfocusobject.key
   shader.getfocusobject.key+=kwarg['key']
   return False
#  elif kwarg['key']=='\t':
#    shader.keyboard.count=(shader.keyboard.count+1)%(len(kwarg['rootshader'])+1)
#    shader.focusobject=kwarg['rootshader'].children[shader.keyboard.count] if not shader.keyboard.count==len(shader.keyboard.count) else kwarg['rootshader']
#  if type(shader.keyboard.key)==str and re.search(r'^\d',shader.keyboard.key):
##   shader.keyboard.count=int(re.sub(r'^(\d+).*$',r'\1',shader.keyboard.key))
  elif re.search(r'^\d',shader.getfocusobject.key):
   print(f'TEST shader.keyboard {shader.getfocusobject.key=}')
   count=int(re.sub(r'^(\d+).*$',r'\1',shader.getfocusobject.key))
   try:
    if not re.search(r':',shader.getfocusobject.key):
     shader.focusobject=kwarg['rootshader'].children[count] if not count==len(kwarg['rootshader'].children) else kwarg['rootshader']
    else:
     shader.focusobject=kwarg['rootshader']
     while shader.getfocusobject.key:
      shader.focusobject=shader.focusobject.children[int(re.sub(r'^(.*?):.+$',r'\1',shader.getfocusobject.key))]
      shader.getfocusobject.key=re.sub(r'^.*?:(.*)$',r'\1',shader.getfocusobject.key) if ':' in shader.getfocusobject.key else ''
#     shader.focusobject=(kwarg['rootshader'].children[count] if not count==len(kwarg['rootshader'].children) else kwarg['rootshader']).children[int(re.sub(r'^.*?:(\d+).*$',r'\1',shader.getfocusobject.key))]
   except Exception as exc:
    print(f'Exception caught {exc=}')
  shader.getfocusobject.key=kwarg['key']
  return True
#  return False

 def keyboard(self,**kwarg):
#  if type(kwarg['key'])!=str or kwarg['key'] in 'rRuUnNgGxXyYzZsSoOcC':
  if type(kwarg['key'])!=str or kwarg['key'][0]=='[' or kwarg['key'][0]=='(' or kwarg['key'] in 'rRuUnNgGxXyYzZsSoOcC':
#   shader.utili.keyboard(kwarg['key'],shader.focusobject.transformation if not 'transformation' in kwarg else kwarg['transformation']) if type(kwarg['key'])==tuple or type(kwarg['key'])==list or kwarg['key'] in 'rRuUnNgGxXyYzZsS' else None
#   shader.utili.keyboard(kwarg['key'],self.transformation if not 'transformation' in kwarg else kwarg['transformation']) if type(kwarg['key'])==tuple or type(kwarg['key'])==list or kwarg['key'] in 'rRuUnNgGxXyYzZsS' else None
   shader.utili.keyboard(kwarg['key'],self.transformation if not 'transformation' in kwarg else kwarg['transformation']) if type(kwarg['key'])==tuple or type(kwarg['key'])==list or kwarg['key'][0]=='[' or kwarg['key'][0]=='(' or kwarg['key'] in 'rRuUnNgGxXyYzZsS' else None
#   print(f'TEST shader.keyboard after transformaton {shader.focusobject.transformation=}')
   self.switchlight(kwarg['key']=='o') if type(kwarg['key'])==str and kwarg['key'] in 'oO' else None
   if type(kwarg['key'])==str and kwarg['key'] in 'cC':
    if not hasattr(self,'back_material_shininess'):
     self.material_shininess=shader.defaultuniform['material.shininess'] if not hasattr(self,'material_shininess') else self.material_shininess
     self.back_material_shininess=self.material_shininess
    if kwarg['key']=='C':
     self.material_shininess=-2 if self.material_shininess!=-2 else self.back_material_shininess
    else:
     self.material_shininess=-1 if self.material_shininess!=-1 else self.back_material_shininess
     print(f"TEST keyaobrtd2 {kwarg['key']=} {self.material_shininess=}")
#   shader.keyboard.key=kwarg['key']
   if shader.record=='record':
    shader.record=open('record.txt','w') if type(shader.record)==str else shader.record
   if shader.record and not type(shader.record)==str:
    shader.record.write(str(time.time())+' '+self.id+' '+str(kwarg['key'])+'\n')
    shader.record.flush()
   return True
  elif kwarg['key']=='v':
   kwarg['rootshader'].printchildren()
  return False

 def keyboard2(self,*arg,**kwarg):
  '''this function can be called only from opengl glut function through root object.
cannnot be recursed'''
  if not hasattr(self.keyboard2,'index') and shader.record=='play':
   setattr(shader.keyboard2,'index',0)
   setattr(shader.keyboard2,'timeidkey',[re.split('\s+',re.sub(r'\s*#.*$','',x),maxsplit=2) for x in re.split('\n',open('record.txt').read()) if x and not re.search(r'^(#|\s*$)',x)])
#   setattr(shader.keyboard2,'processduration',0.005)
   setattr(shader.keyboard2,'processduration',1/30) #1/fps
   setattr(shader.keyboard2,'begintime',time.time())
   setattr(shader.keyboard2,'idobjmap',{})

#todelete
#   setattr(shader.keyboard2,'previoustime',None)

   self.getidchildren(shader.keyboard2.idobjmap)
   shader.keyboard2.idobjmap[self.id]=self
  currenttime=time.time()
  if shader.record=='play':
#   while shader.keyboard2.index < len(shader.keyboard2.timeidkey) and float(shader.keyboard2.timeidkey[shader.keyboard2.index][0]) < (float(shader.keyboard2.timeidkey[0][0])+currenttime-shader.keyboard2.begintime-shader.keyboard2.processduration):
   while shader.keyboard2.index < len(shader.keyboard2.timeidkey) and float(shader.keyboard2.timeidkey[shader.keyboard2.index][0]) < (float(shader.keyboard2.timeidkey[0][0])+currenttime-shader.keyboard2.begintime+shader.keyboard2.processduration):
#    print(f'TEST shader.keyboard2 {shader.keyboard2.index=} dropping')
#    print(f'{shader.keyboard2.timeidkey[shader.keyboard2.index][2]=}')

#todelete
    '''
    if shader.keyboard2.timeidkey[shader.keyboard2.index][0]!=shader.keyboard2.previoustime:
     shader.keyboard2.idobjmap[shader.keyboard2.timeidkey[shader.keyboard2.index][1]].transformation=[]
     shader.keyboard2.previoustime=shader.keyboard2.timeidkey[shader.keyboard2.index][0]
     print(f'TEST {shader.keyboard2.previoustime=} {shader.keyboard2.timeidkey[shader.keyboard2.index][0]=} {shader.keyboard2.index=} {len(shader.keyboard2.timeidkey)=}')
    '''

    shader.keyboard2.idobjmap[shader.keyboard2.timeidkey[shader.keyboard2.index][1]].keyboard(key=shader.keyboard2.timeidkey[shader.keyboard2.index][2])
    shader.keyboard2.index+=1
   '''
   while shader.keyboard2.index < len(shader.keyboard2.timeidkey) and float(shader.keyboard2.timeidkey[shader.keyboard2.index][0]) <= float(shader.keyboard2.timeidkey[0][0])+currenttime - shader.keyboard2.begintime+shader.keyboard2.processduration:
    shader.keyboard2.idobjmap[shader.keyboard2.timeidkey[shader.keyboard2.index][1]].keyboard(key=shader.keyboard2.timeidkey[shader.keyboard2.index][2])
   '''
   if shader.keyboard2.index < len(shader.keyboard2.timeidkey):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glPushMatrix()
    glTranslate(0,0,-15)
    self.display(active=False)
    glPopMatrix()
    glutSwapBuffers()
#    shader.keyboard2.index+=1
    waittime=float(shader.keyboard2.timeidkey[shader.keyboard2.index][0])-float(shader.keyboard2.timeidkey[0][0]) - (time.time()-shader.keyboard2.begintime)
    if waittime < 0:
     print(f'{waittime=} {shader.keyboard2.index=} LOOSING THE FRAME current ftp = {1/shader.keyboard2.processduration=}')
     shader.keyboard2.processduration=1/(1/shader.keyboard2.processduration-1)
    glutTimerFunc(waittime>0 and int(waittime*1000) or 0,self.keyboard2,ord('p'))
  else:
#   kwarg['key']=kwarg['key'].decode() if type(kwarg['key'])==bytes else [float(x) for x in re.findall('-?\d+(?:[.]\d+)?',kwarg['key'])] if type(kwarg['key'])==str and re.search(r'^(\[|\()',kwarg['key']) else kwarg['key']
   kwarg['key']=kwarg['key'].decode() if type(kwarg['key'])==bytes else kwarg['key']
#   shader.getfocusobject(**dict(kwarg,rootshader=self))
#   return shader.focusobject.keyboard(**dict(kwarg,rootshader=self))
   return shader.focusobject.keyboard(**dict(kwarg,rootshader=self)) if shader.getfocusobject(**dict(kwarg,rootshader=self)) else False

 '''
 def add(self,*,object,**kwarg):
  self.children.append({'object':object,'transformation':[],'fixtransformation':[],**kwarg})
#  print(f'TEST shader.add {object=} {kwarg=} {self.children=}')

 def getlightchildren(self):
  retvalue=[]
  if not self.children:
   return []
  elif self in shader.lightposition:
   return [self]
  for i in self.children:
   [retvalue.extend(self.getlightchildren()) for count in range(len(self.children))]
  return retvalue
 '''

 def getidchildren(self,idhash):
  for i in self.children:
   idhash[i.id]=i
   i.getidchildren(idhash) if i.children else None
 def printchildren(self,count=-1,level=0,getstring=False):
  '''getstring should be io.StringIO object'''
  printstring=f'{str(self.objfile)} {self.id} {self.transformation=} {self.fixtransformation=} {"self.extratransformation=" if hasattr(self,"extratransformation") else ""}{self.extratransformation if hasattr(self,"extratransformation") else ""}'
  if not getstring:
   print(f'{"->" if self==shader.focusobject else "  "}{" "*level*4}{count}',end='') if count!=-1 else print(f'{"->" if self==shader.focusobject else "  "}{" "*level*4}{len(self.children)}',end='');print(printstring)
  else:
   getstring.write(f'{" "*level*4}{count}') if count!=-1 else getstring.write(f'\n:{" "*1*4}{len(self.children)}');getstring.write(printstring)
  for countl,i in enumerate(self.children):
   i.printchildren(count=('' if count==-1 else count+':')+str(countl),level=level+1,getstring=getstring)

 def display(self,**kwarg):
#  print(f'TEST shader.display {self=} {self.children=} {kwarg=} {self.id=} {shader.focusobject.id=} {self.objfile=} {self.transformation=} {self.fixtransformation=} ')
  tmp=None
  glPushMatrix()
  self.transformmatrix(self.transformation) if hasattr(self,'transformation') else None
  self.transformmatrix(self.fixtransformation) if hasattr(self,'fixtransformation') else None
  if hasattr(self,'extratransformation'):
   glPushMatrix()
   self.transformmatrix(self.extratransformation)
  glUniformMatrix4fv(self.utili.getuniloc('projection'),1,GL_FALSE,glGetFloatv(GL_PROJECTION_MATRIX).tolist())
  glUniformMatrix4fv(self.utili.getuniloc('modelviewsphere'),1,GL_FALSE,glGetFloatv(GL_MODELVIEW_MATRIX).tolist())
#  glUniformMatrix4fv(self.utili.getuniloc('transposeinversemodelviewsphere'),1,GL_FALSE,np.transpose(np.linalg.inv(glGetFloatv(GL_MODELVIEW_MATRIX).tolist())))
#  glUniformMatrix3fv(self.utili.getuniloc('transposeinversemodelviewsphere'),1,GL_FALSE,glGetFloatv(GL_MODELVIEW_MATRIX)[:3,:3])
  shader.utili.pushuniattribtoshader('light['+str(list(shader.lightposition).index(self))+'].position',(np.transpose(glGetFloatv(GL_MODELVIEW_MATRIX))@shader.lightposition[self]['light.position'][0:4]).tolist()) if self in shader.lightposition else None
#  shader.utili.pushuniattribtoshader('light['+str(list(shader.lightposition).index(self))+'].position',(np.transpose(glGetFloatv(GL_MODELVIEW_MATRIX))@shader.lightposition[self]['light.position']).tolist()[0:3]+list(shader.lightposition[self]['light.position'])[3:4]) if self in shader.lightposition else None
#  shader.utili.pushuniattribtoshader('light['+str(list(shader.lightposition).index(self))+'].spotdirection',(np.transpose(np.linalg.inv(np.transpose(glGetFloatv(GL_MODELVIEW_MATRIX))))@(list(shader.lightposition[self]['light.spotdirection'])+[1.0])).tolist()[0:3]) if self in shader.lightposition else None
  shader.utili.pushuniattribtoshader('light['+str(list(shader.lightposition).index(self))+'].spotdirection',(np.transpose(glGetFloatv(GL_MODELVIEW_MATRIX))[:3,:3]@shader.lightposition[self]['light.spotdirection']).tolist()) if self in shader.lightposition else None
  for i in (shader.vao[self.objfile] if self.objfile else []):
#   print(f'TEST shader.display {self=} {i=} {self.__dict__=}')
   tmp=hasattr(self,'material_diffuse') and i[1] in self.material_diffuse and self.material_diffuse[i[1]] or i[0]
   shader.utili.pushuniattribtoshader(*[x for x in dict(shader.defaultuniform,**{re.sub('^material_','material.',x[0]):x[1] for x in self.__dict__.items()}).items() if re.search(r'^material[.](?!diffuse)',x[0])])
   if type(tmp)==str:
    if not tmp in shader.texturename:
     shader.texturename[tmp]=self.utili.createtextureobject(imagename=tmp,textureid=1)
    shader.utili.pushuniattribtoshader(('textureb',1),('material.diffuse',shader.defaultuniform['material.diffuse']))
    glActiveTexture(GL_TEXTURE0)
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D,shader.texturename[tmp])
    glBindVertexArray(i[3])
    glDrawArrays(GL_TRIANGLES,0,i[2])
    glDisable(GL_TEXTURE_2D)
   else:
    shader.utili.pushuniattribtoshader(('textureb',0),('material.diffuse2',tmp))
    glBindVertexArray(i[3])
    glDrawArrays(GL_TRIANGLES,0,i[2])
  if hasattr(self,'extratransformation'):
   [x.display(**dict(kwarg,active=kwarg['active'] or x.objfile and x==shader.focusobject)) for x in self.innerchildren]
   glPopMatrix()
  [x.display(**dict(kwarg,active=kwarg['active'] or x.objfile and x==shader.focusobject)) for x in self.children if not hasattr(x,'material_shininess') or not x.material_shininess==-2]
  glPopMatrix()
