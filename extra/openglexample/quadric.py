import sys
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from PIL import Image
from openglutil import Utilc
startlist=0
texname=None
utili=Utilc()
shapes=('lightsource','sphere','cylinder','disk','partialdisk')
shape='lightsource'
transformation={x:[] for x in shapes}

def init():
 global startlist,texname
 glClearColor(0,0,0,0)
 glMaterialfv(GL_FRONT,GL_AMBIENT,(0.5,0.5,0.5,1))
 glMaterialfv(GL_FRONT,GL_SPECULAR,(1,1,1,1))
 glMaterialfv(GL_FRONT,GL_SHININESS,[50])
 glLightModelfv(GL_LIGHT_MODEL_AMBIENT,(0.5,0.5,0.5,1))
 glLightModelfv(GL_LIGHT_MODEL_COLOR_CONTROL,GL_SEPARATE_SPECULAR_COLOR)

 texname=glGenTextures(2)
 image=['earth.png','pyramid.png']
 for i in range(2):
  glBindTexture(GL_TEXTURE_2D,texname[i])
  glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
  glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
  glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
  glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
  img=Image.open(image[i]).convert('RGBA').transpose(Image.FLIP_TOP_BOTTOM)
  glTexImage2D(GL_TEXTURE_2D,0,GL_RGBA,img.width,img.height,0,GL_RGBA,GL_UNSIGNED_BYTE,img.tobytes())

 startlist=glGenLists(4)
 qobj=gluNewQuadric()

 gluQuadricDrawStyle(qobj,GLU_FILL) 
 gluQuadricNormals(qobj,GLU_SMOOTH)
 gluQuadricTexture(qobj,GL_TRUE)
 glNewList(startlist,GL_COMPILE)
 gluSphere(qobj,0.75,25,20)
 glEndList()

 gluQuadricDrawStyle(qobj,GLU_FILL) 
 gluQuadricNormals(qobj,GLU_SMOOTH)
 gluQuadricTexture(qobj,GL_TRUE)
 glNewList(startlist+1,GL_COMPILE)
 gluCylinder(qobj,0.5,0.3,1.0,15,5)
 glEndList()

 gluQuadricDrawStyle(qobj,GLU_LINE) 
 gluQuadricNormals(qobj,GLU_NONE)
 gluQuadricTexture(qobj,GL_FALSE)
 glNewList(startlist+2,GL_COMPILE)
 gluDisk(qobj,0.25,1,20,5)
 glEndList()

 gluQuadricDrawStyle(qobj,GLU_LINE) 
 gluQuadricNormals(qobj,GLU_NONE)
 gluQuadricTexture(qobj,GL_FALSE)
 glNewList(startlist+3,GL_COMPILE)
 gluPartialDisk(qobj,0,1,20,4,0,225)
 glEndList()


 glShadeModel(GL_SMOOTH)
 glEnable(GL_LIGHTING)
 glEnable(GL_NORMALIZE)
 glEnable(GL_LIGHT0)
 glEnable(GL_DEPTH_TEST)

def display():
 glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
 glPushMatrix()
 glTranslate(0,0,-5)
 for lshape in shapes:
  glPushMatrix()
  [glTranslate(*x) if len(x)==3 else glRotatef(*x) for x in transformation[lshape]]
  if lshape=='lightsource':
   glEnable(GL_LIGHTING)
   glLightfv(GL_LIGHT0,GL_POSITION,(0,0,4,1))
  elif lshape=='sphere':
   glEnable(GL_TEXTURE_2D)
   glTexEnvf(GL_TEXTURE_ENV,GL_TEXTURE_ENV_MODE,GL_REPLACE)
   glBindTexture(GL_TEXTURE_2D,texname[0])
   glCallList(startlist)
   glDisable(GL_TEXTURE_2D)
  elif lshape=='cylinder':
   glEnable(GL_TEXTURE_2D)
   glTexEnvf(GL_TEXTURE_ENV,GL_TEXTURE_ENV_MODE,GL_REPLACE)
   glBindTexture(GL_TEXTURE_2D,texname[1])
   glCallList(startlist+1)
   glDisable(GL_TEXTURE_2D)
  elif lshape=='disk':
   glDisable(GL_LIGHTING)
   glCallList(startlist+2)
   glEnable(GL_LIGHTING)
  elif lshape=='partialdisk':
   glDisable(GL_LIGHTING)
   glCallList(startlist+3)
   glEnable(GL_LIGHTING)
  glPopMatrix()

 glPopMatrix()
 glFlush()

def reshape(w,h):
 glViewport(0,0,w,h)
 glMatrixMode(GL_PROJECTION)
 glLoadIdentity()
 gluPerspective(40,w/h if w>=h else h/w, 0.5, 10)
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
 glutPostRedisplay()

if __name__=='__main__':
 glutInit()
 glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB | GLUT_DEPTH)
 glutInitWindowSize(500,500)
 glutInitWindowPosition(100,100)
 glutCreateWindow('Quadrics')
 init()
 glutDisplayFunc(display)
 glutReshapeFunc(reshape)
 glutKeyboardFunc(keyboard)
 glutMainLoop()
