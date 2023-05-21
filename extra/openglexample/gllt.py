from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import re
from openglutil import Pyramid,Utilc,Shape
import openglcylinder

#shapes=('lightcube','pyramid','sphere','chair')
shapes=('lightcube','pyramid')
trasformation={x:[] for x in shapes}
shape='lightcube'
pyramid=cube=chair=coffeemug=plate=None
globalrotateangle_g=0
lighttype_g='directional'
cubescale_g=(0,0,0)

def init():
 global pyramid,cube,chair,tree,plate
 glClearColor(0,0,0,0)
 glShadeModel(GL_SMOOTH)
# glLightModelfv(GL_LIGHT_MODEL_AMBIENT, (0.2,0.2,0.2,1.0))
# glLightModelf(GL_LIGHT_MODEL_LOCAL_VIEWER, 1)
# glLightModelf(GL_LIGHT_MODEL_TWO_SIDE, 1)
# glLightf(GL_LIGHT0,GL_LINEAR_ATTENUATION,1)
 glLightfv(GL_LIGHT0,GL_SPOT_DIRECTION,(0,0,-1))
 glLightf(GL_LIGHT0,GL_SPOT_CUTOFF,20)
 glLightf(GL_LIGHT0,GL_SPOT_EXPONENT,8)
 glEnable(GL_LIGHTING)
 glEnable(GL_LIGHT0)
 glEnable(GL_DEPTH_TEST)
 pyramid=Pyramid()
 cube=Shape(obj='cube211.obj')
 chair=Shape(obj='chair.obj')
 tree=Shape(obj='tree.obj')
 plate=Shape(obj='plate.obj')

def display():
 glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
 glPushMatrix()
 glTranslatef(0,0,-5)
 glRotatef(globalrotateangle_g,0,1,0)
 for lshape in shapes:
  glPushMatrix()
  [glTranslatef(*x) if len(x)==3 else glRotatef(*x) for x in transformation[lshape]]
  if lshape=='lightcube':
#   glLightfv(GL_LIGHT0,GL_AMBIENT, (0.2,0.2,0.2,1.0))
   glLightfv(GL_LIGHT0,GL_SPECULAR,(1,1,1,1.0))
   glLightfv(GL_LIGHT0,GL_DIFFUSE,(1,1,1,1.0))
   glLightfv(GL_LIGHT0,GL_POSITION,(0,0,1.5, 0 if lighttype_g=='directional' else 1.0))
   glTranslatef(0,0,1.5)
   glDisable(GL_LIGHTING)
   glScalef(*cubescale_g)
   cube.display(color=(1.0,1.0,1.0),sidecolor=(((0,0,-1),(1,0.2,0.2)),((0,0,1),(1,1,0.6))))
   glEnable(GL_LIGHTING)
  elif lshape=='pyramid':
   pyramid.display()
  elif lshape=='sphere':
   glMaterialfv(GL_FRONT,GL_AMBIENT,(0,0,0.1,1.0))
   glMaterialfv(GL_FRONT,GL_DIFFUSE,(0,1,0,1.0))
   glMaterialfv(GL_FRONT,GL_SPECULAR,(1,1,1,1.0))
   glMaterialfv(GL_FRONT,GL_SHININESS,10)
   glutSolidSphere(0.5,40,32)
  elif lshape=='cone':
   glMaterialfv(GL_FRONT,GL_AMBIENT,(0,0.1,0,1.0))
   glMaterialfv(GL_FRONT,GL_DIFFUSE,(1,0,1,1.0))
   glMaterialfv(GL_FRONT,GL_SPECULAR,(1,1,1,1.0))
   glMaterialfv(GL_FRONT,GL_SHININESS,40)
   glutSolidCone(0.5,0.8,40,32)
  elif lshape=='chair':
   chair.display(ambient=(0,0.5,0,1.0),diffuse=(1,0,1,1.0),specular=(1,1,1,1.0),shininess=40)
  elif lshape=='cylinder':
   glMaterialfv(GL_FRONT,GL_AMBIENT,(0,0,1,1.0))
   glMaterialfv(GL_FRONT,GL_EMISSION,(0,0,0,1.0))
   glMaterialfv(GL_FRONT,GL_DIFFUSE,(1,0,1,1.0))
   glMaterialfv(GL_BACK,GL_DIFFUSE,(1,1,0,1.0))
   glMaterialfv(GL_FRONT,GL_SPECULAR,(1,1,1,1.0))
   glMaterialfv(GL_BACK,GL_SPECULAR,(0,0,0,1.0))
   glMaterialfv(GL_FRONT,GL_SHININESS,40)
   openglcylinder.cylinder()
  elif lshape=='tree':
   glScalef(0.4,0.4,0.4)
   glMaterialfv(GL_FRONT,GL_EMISSION,(0,0,0,1.0))
   tree.display(ambient=(0,0,0.5,1.0),diffuse=(0,1,0,1.0),specular=(0,0.5,0,1.0),shininess=0)
  elif lshape=='plate':
   glScalef(0.3,0.3,0.3)
   glMaterialfv(GL_FRONT,GL_EMISSION,(0,0,0,1.0))
   plate.display(ambient=(0,0,0.5,1.0),diffuse=(1,0,1,1.0),specular=(0,0,0,1.0),shininess=0)
  glPopMatrix()
 glPopMatrix()
 glFlush()

def reshape(w,h):
 global transformation
 glViewport(0,0,w,h)
 glMatrixMode(GL_PROJECTION)
 glLoadIdentity()
 gluPerspective(40.0,w/h if w>=h else h/w,1.0,10.0)
# glOrtho(-1.5,1.5,-1.5*h/w,1.5*h/w,1,10) if (w<=h) else glOrtho(-1.5,1.5,-1.5*w/h,1.5*w/h,1,10)
 glMatrixMode(GL_MODELVIEW)
 glLoadIdentity()
 transformation={x:[] for x in shapes}

def keyboard(key,x,y):
 global transformation,shapes,shape
 global globalrotateangle_g,lighttype_g,cubescale_g
 key=bytes(key)
 if key==b'\t':
  shape=shapes[(shapes.index(shape)+1)%len(shapes)]
 Utilc.keyboard(key,transformation[shape])
 if key==b'p':
  lighttype_g='positional'
 elif key==b'P':
  lighttype_g='directional'
 if key==b'v':
  Utilc.pprint(**{'shape=':shape,'transformation=':transformation,'lighttype=':lighttype_g,'globalrotateangle_g=':globalrotateangle_g})
 if shape=='lightcube' and re.search(r'^[cC]$',key.decode()):
  cubescale_g=[x+0.05 if key==b'C' else max(0,x-0.05) for x in cubescale_g]
 globalrotateangle_g+=10 if key==b'g' else -10 if key==b'G' else 0
 glutPostRedisplay()

if __name__=="__main__":
 glutInit()
 glutInitDisplayMode(GLUT_SINGLE|GLUT_RGB|GLUT_DEPTH)
 glutInitWindowSize(500,500)
 glutInitWindowPosition(100,100)
 glutCreateWindow("My Light Code")
 init()
 glutDisplayFunc(display)
 glutReshapeFunc(reshape)
 glutKeyboardFunc(keyboard)
 glutMainLoop()
