from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import re
import numpy as np
from objloader import ObjFile
from openglutil import Utilc

utili=Utilc()
shapes=('lightsource','sphere')
shape='lightsource'
transformation={x:[] for x in shapes}

vertcode="""\
#version 140
uniform mat4 projection;
uniform mat4 transposeinversemodelviewlight;
uniform mat4 modelviewlight;
uniform mat4 modelviewsphere;
uniform mat4 transposeinversemodelviewsphere;
uniform bool lit;
attribute vec3 coord;
attribute vec3 normal;
varying vec4 vertex_color;
void main() {
 vec4 diffusecolor=vec4(0,1,0,1);
 vec4 specularcolor=vec4(1,0,0,1);
 const int specularexponent=10;
 float spotfactor=0.0;
 float distanceLV=0.0;
 float attenuation=0.0;
 gl_Position=projection * (modelviewsphere * vec4(coord,1.0));
 if (lit) {
//  vertex_color= vec4(color.rgb*dot(normalize((transposeinversemodelviewsphere*vec4(normal,1.0)).xyz),normalize((transposeinversemodelviewlight*vec4(0,0,10,0)).xyz)),color.a);
//  vertex_color= vec4(color.rgb*dot(normalize((transposeinversemodelviewsphere*vec4(normal,1.0)).xyz),normalize((modelviewlight*vec4(0,0,5,1.0)-modelviewsphere*vec4(coord,1.0)).xyz)),color.a);
  vec3 N,L,R,E,D;
  N=normalize((transposeinversemodelviewsphere*vec4(normal,1.0)).xyz);
  L=normalize((modelviewlight*vec4(0,0,5,1.0)-modelviewsphere*vec4(coord,1.0)).xyz);
  distanceLV=distance((modelviewlight*vec4(0,0,5,1)).xyz,(modelviewsphere*vec4(coord,1.0)).xyz);
  attenuation=clamp(10/(1+distanceLV),0.0,1.0);
  D=normalize((transposeinversemodelviewlight*vec4(0,0,1,1)).xyz);
  R=-reflect(L,N);
  E=normalize(-(modelviewsphere*vec4(coord,1.0)).xyz);
  if (dot(L,N) <= 0.0){
   vertex_color=vec4(0,0,0.2,1);
  }else{
   if (dot(D,L) >= cos((3.14*30)/180)) {
//    spotfactor=pow(max(0,dot(D,L)),40);
    spotfactor=pow(max(0,dot(D,L)),0);
   }
   vec3 color=0.8*dot(L,N)*diffusecolor.rgb;
   if (dot(R,E)>0) {
 //   color+=0.4*pow(dot(R,E),specularexponent)*specularcolor.rgb;
    color+=0.8*pow(dot(R,E),specularexponent)*specularcolor.rgb;
   }
//   vertex_color=vec4(attenuation*spotfactor*color,diffusecolor.a);
   vertex_color=vec4(attenuation*color,diffusecolor.a);
  }
 }else {
  vertex_color=diffusecolor;
 }
};"""

fragcode="""\
#version 140
varying vec4 vertex_color;
void main() {
gl_FragColor=vertex_color;
};
"""

'''
vertcode="""\
#version 330
uniform mat4 projection;
uniform mat4 modelviewsphere;
attribute vec3 coord;
attribute vec3 normal;
varying vec3 vertex_coord;
varying vec3 vertex_normal;
void main() {
 gl_Position=projection * (modelviewsphere * vec4(coord,1.0));
 vertex_coord=coord;
 vertex_normal=normal;
};
"""


fragcode="""\
#version 330
uniform mat4 projection;
uniform mat4 transposeinversemodelviewlight;
uniform mat4 modelviewlight;
uniform mat4 modelviewsphere;
uniform mat4 transposeinversemodelviewsphere;
uniform bool lit;
varying vec3 vertex_coord;
varying vec3 vertex_normal;
void main() {
 vec4 diffusecolor=vec4(0,1,0,1);
 vec4 specularcolor=vec4(1,0,0,1);
 const int specularexponent=10;
 float spotfactor=0.0;
 float distanceLV=0.0;
 float attenuation=0.0;
 if (lit) {
//  vertex_color= vec4(color.rgb*dot(normalize((transposeinversemodelviewsphere*vec4(normal,1.0)).xyz),normalize((transposeinversemodelviewlight*vec4(0,0,10,0)).xyz)),color.a);
//  vertex_color= vec4(color.rgb*dot(normalize((transposeinversemodelviewsphere*vec4(normal,1.0)).xyz),normalize((modelviewlight*vec4(0,0,5,1.0)-modelviewsphere*vec4(coord,1.0)).xyz)),color.a);
  vec3 N,L,R,E,D;
  N=normalize((transposeinversemodelviewsphere*vec4(vertex_normal,1.0)).xyz);
  L=normalize((modelviewlight*vec4(0,0,5,1.0)-modelviewsphere*vec4(vertex_coord,1.0)).xyz);
  distanceLV=distance((modelviewlight*vec4(0,0,5,1)).xyz,(modelviewsphere*vec4(vertex_coord,1.0)).xyz);
  attenuation=clamp(10/(1+distanceLV),0.0,1.0);
  D=normalize((transposeinversemodelviewlight*vec4(0,0,1,1)).xyz);
  R=-reflect(L,N);
  E=normalize(-(modelviewsphere*vec4(vertex_coord,1.0)).xyz);
  if (dot(L,N) <= 0.0){
   gl_FragColor=vec4(0,0,0.2,1);
  }else{
   if (dot(D,L) >= cos((3.14*30)/180)) {
//    spotfactor=pow(max(0,dot(D,L)),40);
    spotfactor=pow(max(0,dot(D,L)),0);
   }
   vec3 color=0.8*dot(L,N)*diffusecolor.rgb;
   if (dot(R,E)>0) {
  //  color+=0.4*pow(dot(R,E),specularexponent)*specularcolor.rgb;
    color+=0.8*pow(dot(R,E),specularexponent)*specularcolor.rgb;
   }
   gl_FragColor=vec4(spotfactor*color,diffusecolor.a);
//   glFragColor=vec4(attenuation*color,diffusecolor.a);
  }
 }else {
  gl_FragColor=diffusecolor;
 }
};"""
'''


vertcode2="""\
#version 140
uniform mat4 projection2;
uniform mat4 modelviewlight2;
attribute vec3 coord2;
varying vec4 vertex_color;
void main() {
 vec4 color=vec4(1,1,1,1);
 gl_Position=projection2 * (modelviewlight2 * vec4(coord2,1.0));
 vertex_color=color;
};"""

fragcode2="""\
#version 140
varying vec4 vertex_color;
void main() {
gl_FragColor=vertex_color;
};
"""

def init():
 glClearColor(0,0,0,0)

 vertshader=glCreateShader(GL_VERTEX_SHADER)
 glShaderSource(vertshader,vertcode)
 glCompileShader(vertshader)
 if not glGetShaderiv(vertshader,GL_COMPILE_STATUS):
  print(f'ERROR {glGetShaderInfoLog(vertshader)=}')

 fragshader=glCreateShader(GL_FRAGMENT_SHADER)
 glShaderSource(fragshader,fragcode)
 glCompileShader(fragshader)
 if not glGetShaderiv(fragshader,GL_COMPILE_STATUS):
  print(f'ERROR {glGetShaderInfoLog(fragshader)=}')

 shaderprogram=glCreateProgram()
 glAttachShader(shaderprogram,vertshader)
 glAttachShader(shaderprogram,fragshader)
 glLinkProgram(shaderprogram)
 if not glGetProgramiv(shaderprogram,GL_LINK_STATUS):
  print(f'ERROR {glGetShaderInfoLog(shaderprogram)=}')


 vertshader=glCreateShader(GL_VERTEX_SHADER)
 glShaderSource(vertshader,vertcode2)
 glCompileShader(vertshader)
 if not glGetShaderiv(vertshader,GL_COMPILE_STATUS):
  print(f'ERROR {glGetShaderInfoLog(vertshader)=}')

 fragshader=glCreateShader(GL_FRAGMENT_SHADER)
 glShaderSource(fragshader,fragcode2)
 glCompileShader(fragshader)
 if not glGetShaderiv(fragshader,GL_COMPILE_STATUS):
  print(f'ERROR {glGetShaderInfoLog(fragshader)=}')

 shaderprogram2=glCreateProgram()
 glAttachShader(shaderprogram2,vertshader)
 glAttachShader(shaderprogram2,fragshader)
 glLinkProgram(shaderprogram2)
 if not glGetProgramiv(shaderprogram2,GL_LINK_STATUS):
  print(f'ERROR {glGetShaderInfoLog(shaderprogram2)=}')
# glUseProgram(shaderprogram)

# for i in ('projection', 'transposeinversemodelviewlight', 'modelviewsphere', 'transposeinversemodelviewsphere', 'lit'):
 for i in ('projection', 'modelviewlight', 'transposeinversemodelviewlight','modelviewsphere', 'transposeinversemodelviewsphere', 'lit'):
  setattr(init,i+'_loc',glGetUniformLocation(shaderprogram,i))
 for i in ('coord','normal'):
  setattr(init,i+'_loc',glGetAttribLocation(shaderprogram,i))

 for i in ('projection2', 'modelviewlight2'):
  setattr(init,i+'_loc',glGetUniformLocation(shaderprogram2,i))
 for i in ('coord2',):
  setattr(init,i+'_loc',glGetAttribLocation(shaderprogram2,i))


 matt=list(ObjFile('cube.obj').objects.values())[0].vertices
 #VBO1
 posbuffer=glGenBuffers(1)
 glBindBuffer(GL_ARRAY_BUFFER,posbuffer)
 glBufferData(GL_ARRAY_BUFFER,np.array(Utilc.getbuffer(matt,0,3,8),dtype=np.float32),GL_STATIC_DRAW)

 #VBO2
 norbuffer=glGenBuffers(1)
 glBindBuffer(GL_ARRAY_BUFFER,norbuffer)
 glBufferData(GL_ARRAY_BUFFER,np.array(Utilc.getbuffer(matt,3,3,8),dtype=np.float32),GL_STATIC_DRAW)

 #VAO -> VBO1, VBO2
 vaobj=glGenVertexArrays(2)
 glBindVertexArray(vaobj[0])
 glEnableVertexAttribArray(init.coord_loc)
 glEnableVertexAttribArray(init.normal_loc)
 glBindBuffer(GL_ARRAY_BUFFER,posbuffer)
 glVertexAttribPointer(init.coord_loc,3,GL_FLOAT,GL_FALSE,0,None)
 glBindBuffer(GL_ARRAY_BUFFER,norbuffer)
 glVertexAttribPointer(init.normal_loc,3,GL_FLOAT,GL_FALSE,0,None)


 matt2=list(ObjFile('cube.obj').objects.values())[0].vertices
 #VBO1
 posbuffer=glGenBuffers(1)
 glBindBuffer(GL_ARRAY_BUFFER,posbuffer)
 glBufferData(GL_ARRAY_BUFFER,np.array(Utilc.getbuffer(matt2,0,3,8),dtype=np.float32),GL_STATIC_DRAW)
 glBindVertexArray(vaobj[1])
 glEnableVertexAttribArray(init.coord2_loc)
 glBindBuffer(GL_ARRAY_BUFFER,posbuffer)
 glVertexAttribPointer(init.coord2_loc,3,GL_FLOAT,GL_FALSE,0,None)


 setattr(init,'matt',matt)
 setattr(init,'matt2',matt2)
 setattr(init,'vaobj',vaobj)
 setattr(init,'shaderprogram',shaderprogram)
 setattr(init,'shaderprogram2',shaderprogram2)
 setattr(init,'cube',0)

 glUseProgram(shaderprogram)
 glUniform1i(init.lit_loc, 1)

 print('init attributes')
 [print(x[0]+' --> '+str(x[1])) for x in init.__dict__.items() if not type(x[1])==list]


 glShadeModel(GL_SMOOTH)
 glEnable(GL_DEPTH_TEST)

def display():
 glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
 glUniformMatrix4fv(init.projection_loc, 1 , GL_FALSE, glGetFloatv(GL_PROJECTION_MATRIX))
 glUniformMatrix4fv(init.projection2_loc, 1 , GL_FALSE, glGetFloatv(GL_PROJECTION_MATRIX))
 glPushMatrix()
 glTranslate(0,0,-10)

 glUseProgram(init.shaderprogram)
 glPushMatrix()
 [glTranslate(*x) if len(x)==3 else glRotate(*x) for x in transformation['lightsource']]
 glUniformMatrix4fv(init.transposeinversemodelviewlight_loc, 1 , GL_FALSE, np.transpose(np.linalg.inv(glGetFloatv(GL_MODELVIEW_MATRIX))))
 glUniformMatrix4fv(init.modelviewlight_loc, 1 , GL_FALSE, glGetFloatv(GL_MODELVIEW_MATRIX))
 glPopMatrix()

 glPushMatrix()
 [glTranslate(*x) if len(x)==3 else glRotate(*x) for x in transformation['sphere']]
 glUniformMatrix4fv(init.modelviewsphere_loc, 1 , GL_FALSE, glGetFloatv(GL_MODELVIEW_MATRIX))
 glUniformMatrix4fv(init.transposeinversemodelviewsphere_loc, 1 , GL_FALSE, np.transpose(np.linalg.inv(glGetFloatv(GL_MODELVIEW_MATRIX))))
 glBindVertexArray(init.vaobj[0])
 glDrawArrays(GL_TRIANGLES,0,len(init.matt)//8)
 glPopMatrix()

 if init.cube:
  glUseProgram(init.shaderprogram2)
  glPushMatrix()
  [glTranslate(*x) if len(x)==3 else glRotate(*x) for x in transformation['lightsource']]
  glTranslate(0,0,5)
  glUniformMatrix4fv(init.modelviewlight2_loc, 1 , GL_FALSE, glGetFloatv(GL_MODELVIEW_MATRIX))
  glBindVertexArray(init.vaobj[1])
  glDrawArrays(GL_TRIANGLES,0,len(init.matt2)//8)
  glPopMatrix()
  

 
 glPopMatrix()
 glutSwapBuffers()

def reshape(w,h):
 glViewport(0,0,w,h)
 glMatrixMode(GL_PROJECTION)
 glLoadIdentity()
 gluPerspective(40,w/h if w>=h else h/w, 1, 20)
# glOrtho(-2.5,2.5,-2.5*h/w,2.5*h/w,1,20) if (w<=h) else glOrtho(-2.5*w/h,2.5*w/h,-2.5,2.5,1,20)
 glMatrixMode(GL_MODELVIEW)
 glLoadIdentity()

def keyboard(key,x,y):
 global transformation,shapes,shape
 key=bytes(key)
 if key==b'\t':
  shape=shapes[(shapes.index(shape)+1)%len(shapes)]
 utili.keyboard(key,transformation[shape])
 if key==b'v':
  print(f'{shape=} {transformation=}')

 if re.search(r'^[tT]$',key.decode()):
  glUniform1i(init.lit_loc, 1 if key==b't' else 0)

 if re.search(r'^[cC]$',key.decode()):
  setattr(init,'cube', 1 if key==b'c' else 0)

 glutPostRedisplay()

if __name__=='__main__':
 glutInit()
 glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
 glutInitWindowSize(500,500)
 glutInitWindowPosition(100,100)
 glutCreateWindow('GLSL')
 init()
 glutDisplayFunc(display)
 glutReshapeFunc(reshape)
 glutKeyboardFunc(keyboard)
 glutMainLoop()
