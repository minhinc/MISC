from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import re,json,time
from openglutil import Utilc,Shape

shapes=['global']
transformation={x:[] for x in shapes}
shape='global'
coordinatesystem_g='local'
airplane=None
begintime=time.time()
jsonshapedict=json.load(open('ss.json'))

def init():
 global airplane
 glClearColor(0.0,0.0,0.0,0.0)
 glShadeModel(GL_SMOOTH)
 
 glEnable(GL_LIGHTING)
 glEnable(GL_LIGHT0)

 glEnable(GL_DEPTH_TEST)
# airplane=shape(obj='airplane.obj',mode='multidrawelement')

def draw(shapehash):
 def str2tuple(tuplestr):
  return tuple(float(i) for i in re.findall(r'[-\d.]+',tuplestr))
 global begintime
 glPushMatrix()
 if 'rotation' in shapehash:
  glRotatef(((time.time()-begintime)%shapehash['rotation'])/shapehash['rotation']*360,*str2tuple(shapehash['rotationaxis']))
  glTranslatef(*str2tuple(shapehash['distance'])) if 'distance' in shapehash else None
  if 'rotateonaxis' in shapehash:
   glPushMatrix()
   glRotatef(((time.time()-begintime)%shapehash['rotateonaxis'])/shapehash['rotateonaxis']*360,0,1,0)
#   glColor3f(*str2tuple(shapehash['color']))
   glMaterialfv(GL_FRONT,GL_DIFFUSE,(*str2tuple(shapehash['color']),1.0))
   glutSolidSphere(shapehash['radius'],40,32)
   glPopMatrix()
  else:
#   glColor3f(*str2tuple(shapehash['color']))
   glMaterialfv(GL_FRONT,GL_DIFFUSE,(*str2tuple(shapehash['color']),1.0))
   glutSolidSphere(shapehash['radius'],40,32)
 else:
#  glColor3f(*str2tuple(shapehash['color']))
  glMaterialfv(GL_FRONT,GL_DIFFUSE,(0,0,0,1.0))
  glMaterialfv(GL_FRONT,GL_EMISSION,(*str2tuple(shapehash['color']),1.0))
  glutSolidSphere(shapehash['radius'],40,32)
  glMaterialfv(GL_FRONT,GL_EMISSION,(0,0,0,1.0))
 [draw(shapehash['child'][i]) for i in ('child' in shapehash and shapehash['child'] or [])]
 glPopMatrix()

def display(value=None):
 global jsonshapedict
 glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
 glPushMatrix()
 glTranslatef(0.0,0.0,-5.0)
 glLightfv(GL_LIGHT0,GL_DIFFUSE,(2,2,2,1.0))
 glLightfv(GL_LIGHT0,GL_POSITION,(0,0,0,1.0))
 [glTranslate(*x) if len(x)==3 else glRotate(*x) if not x[0]=='s' else None for x in transformation['global']]
 glLineWidth(1)
 for i in zip((((-0.5,0,0),(1.0,0,0)),((0,-0.5,0),(0,1.2,0)),((0,0,-0.5),(0,0,1.0))),((0.5,0,0),(0,0.5,0),(0,0,0.5))):
  glBegin(GL_LINES)
#  glColor3f(*i[1])
  glMaterialfv(GL_FRONT,GL_DIFFUSE,(0,0,0,1.0))
  glMaterialfv(GL_FRONT,GL_EMISSION,(*i[1],1.0))
  glVertex3f(*i[0][0])
  glVertex3f(*i[0][1])
  glEnd()
 glMaterialfv(GL_FRONT,GL_EMISSION,(0,0,0,1.0))
 draw(jsonshapedict['sun'])
 '''
 for lshape in shapes:
  glPushMatrix()
  [glTranslate(*x) if len(x)==3 else glRotate(*x) if not x[0]=='s' else glScalef(*x[1:]) for x in (reversed(transformation[lshape]) if coordinatesystem_g=='grand' else transformation[lshape]) if lshape!='global']
  if lshape=='cone':
   if coordinatesystem_g=='local':
    glLineWidth(2)
    for i in zip((((-0.3,0,0),(0.5,0,0)),((0,-0.3,0),(0,1.0,0)),((0,0,-0.3),(0,0,0.5))),((1,0,0),(0,1,0),(0,0,1))):
     glBegin(GL_LINES)
     glColor3f(*i[1])
     glVertex3f(*i[0][0])
     glVertex3f(*i[0][1])
     glEnd()
   glColor3f(1,0,1)
   glRotatef(-90,1,0,0)
   glutSolidCone(0.2,0.8,40,32)
  elif lshape=='airplane':
   color3f(0,1,0)
   airplane.display(mode='multidrawelement')
  glPopMatrix()
 '''
 glPopMatrix()
 glFlush()
 glutTimerFunc(100,display,10)


def reshape(w,h):
 global transformation
 glViewport(0,0,w,h)
 glMatrixMode(GL_PROJECTION)
 glLoadIdentity()
 gluPerspective(40.0, w/h if w>=h else h/w, 1.0, 10.0)
# glOrtho(-1.5,1.5,-1.5*h/w,1.5*h/w,1,10.0) if (w>=h) else glOrtho(-1.5,1.5,-1.5*w/h,1.5*w/h,1,10.0)
 glMatrixMode(GL_MODELVIEW)
 glLoadIdentity()
 transformation={x:[] for x in shapes}

def keyboard(key,x,y):
 global transformation,shapes,shape
 global coordinatesystem_g
 key=bytes(key)
 if key==b'\t':
  shape=shapes[(shapes.index(shape)+1)%len(shapes)]
  Utilc.pprint(**{'==keyboard New Shape':shape})
 Utilc.keyboard(key,transformation[shape])
 if key==b'v':
  Utilc.pprint(**{'shape=':shape,'transformation=':transformation,'coordinatesystem_g':coordinatesystem_g})
 if re.search(r'^[gG]$',key.decode()):
   coordinatesystem_g='grand' if key.decode()=='g' else 'local'
 glutPostRedisplay()

if __name__=='__main__':
 glutInit()
 glutInitDisplayMode(GLUT_SINGLE|GLUT_RGB|GLUT_DEPTH)
 glutInitWindowSize(500,500)
 glutInitWindowPosition(100,100)
 glutCreateWindow("My OpenGL Code")
 init()
 glutDisplayFunc(display)
 glutReshapeFunc(reshape)
 glutKeyboardFunc(keyboard)
 glutMainLoop()
