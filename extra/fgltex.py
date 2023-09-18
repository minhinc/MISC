from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import sys;sys.path.append('/home/minhinc/tmp')
from MISC.extra.shader import shader
#from MISC.extra.openglexample.loco.global2 import global2
from MISC.extra.openglexample.solarsystemsizecomparison.global2 import global2
#from MISC.extra.openglexample.earthseason.global2 import global2
utili=shader.utili

shaderi=None
def init():
 global shaderi
 shader.record=sys.argv[1]
 shaderi=global2()
 glClearColor(0,0,0,0)
 glShadeModel(GL_SMOOTH)
 glEnable(GL_BLEND)
 glEnable(GL_DEPTH_TEST)
 glBlendFunc(GL_SRC_ALPHA,GL_ONE_MINUS_SRC_ALPHA)
# glBlendFunc(GL_ONE,GL_ONE_MINUS_SRC_ALPHA)
 glutFullScreen()

def display():
 glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
 glPushMatrix()
 glTranslate(0,0,-15)
 shaderi.display(active=False)
 glPopMatrix()

 glutSwapBuffers()
# glutTimerFunc(100,timerfunc,None)

def reshape(w,h):
 glViewport(0,0,w,h)
 glMatrixMode(GL_PROJECTION)
 glLoadIdentity()
# gluPerspective(40,w/h if w>=h else h/w, 1, 100)
 gluPerspective(20,w/h if w>=h else h/w, 1, 100)
# glOrtho(-4.0,4.0,-4.0*h/w,4.0*h/w,1,20) if (w<=h) else glOrtho(-4.0*w/h,4.0*w/h,-4.0,4.0,1,20)
 glMatrixMode(GL_MODELVIEW)
 glLoadIdentity()

def keyboard(key,x,y):
# print(f'keyboard {shader.focusobject=}')
 glutPostRedisplay() if shaderi.keyboard2(key=key,x=x,y=y) else None

if __name__=='__main__':
 glutInit()
 glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
 glutInitWindowSize(500,500)
 glutInitWindowPosition(0,0)
 glutCreateWindow('GLSL Texture')
 init()
 glutDisplayFunc(display)
 glutReshapeFunc(reshape)
 glutKeyboardFunc(keyboard)
 glutMainLoop()
