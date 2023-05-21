from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
vertices=((1,0,0),(0,0,-1),(-1,0,0),(0,0,1),(0,1,0))
color=((0,1,0),(0,0,1),(0,1,0),(0,0,1),(1,0,0))
indices=((0,1,2),(2,3,0),(0,1,4),(1,2,4),(2,3,4),(3,0,4))

def init():
 glClearColor(0.0,0.0,0.0,0.0)
 glShadeModel(GL_SMOOTH)
 glEnable(GL_DEPTH_TEST)

def display():
 glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
 for i in indices:
  glBegin(GL_TRIANGLES)
  for j in i:
   glColor3fv(color[j])
   glVertex3iv(vertices[j])
  glEnd()
 glFlush()

def reshape(w,h):
 glViewport(0,0,w,h)
 glMatrixMode(GL_PROJECTION)
 glLoadIdentity()
 glOrtho(-1.5*w/h,1.5*w/h,-1.5,1.5,3,7)
 glMatrixMode(GL_MODELVIEW)
 glLoadIdentity()
 glTranslate(0,0,-5)

def keyboard(key,x,y):
 key=bytes(key)
 glTranslate(key==b'l' and -0.2 or key==b'r' and 0.2,key==b'd' and -0.2 or key==b'u' and 0.2,key==b'n' and 0.2 or key==b'f' and -0.2)
 glRotate(10,0,1,0) if key==b'y' else glRotate(10,1,0,0) if key==b'x' else glRotate(10,0,0,1) if key==b'z' else None
 glutPostRedisplay()

if __name__=='__main__':
 glutInit()
 glutInitDisplayMode(GLUT_SINGLE|GLUT_RGB|GLUT_DEPTH)
 glutInitWindowSize(500,500)
 glutInitWindowPosition(100,100)
 glutCreateWindow('Fixed Function Pipeline')
 init()
 glutDisplayFunc(display)
 glutReshapeFunc(reshape)
 glutKeyboardFunc(keyboard)
 glutMainLoop()
