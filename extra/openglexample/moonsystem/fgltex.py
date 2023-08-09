from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import math,random
import sys;sys.path.append('/home/minhinc/tmp')
import math
import re
import time

from MISC.extra.openglutil import Utilc
from MISC.extra.shader import shader
from global2 import global2
from loco import loco
from earth import earth
from moon import moon
from wheel import wheel
utili=shader.utili

shaderi=None
def init():
 global shaderi
 shader.record=sys.argv[1]
# shaderi=shader(objfile=None)
 shaderi=global2(objfile=None)
 shaderi.children.append(shader(objfile='axis.obj',material_shininess=-2))
 sun2=shader(objfile='sphere.obj',material_diffuse={'__UNKNOWN__':'sun.png'},material_ambient=(2,2,2),light_position=(0,0,0,1),light_specular=(0.2,0.2,0.2),light_diffuse=(1.0,1.0,1.0),light_ambient=(0.2,0.2,0.2))
 sun2.children.append(shader(objfile='ring2.obj',material_shininess=-2,fixtransformation=[['s',3,3,3]]))
 shaderi.children.append(sun2)
 shaderi.children.append(shader(objfile=None,light_position=(0,0,1,1),light_specular=(0.2,0.2,0.2),light_diffuse=(1.0,1.0,1.0),light_ambient=(0.1,0.1,0.1)))
 shaderi.children.append(shader(objfile=None,light_position=(0,0,-1,1),light_specular=(0.2,0.2,0.2),light_diffuse=(1.0,1.0,1.0),light_ambient=(0.1,0.1,0.1)))
 shaderi.children.append(shader(objfile=None,light_position=(1,0,0,1),light_specular=(0.2,0.2,0.2),light_diffuse=(1.0,1.0,1.0),light_ambient=(0.1,0.1,0.1)))
 shaderi.children.append(shader(objfile=None,light_position=(-1,0,0,1),light_specular=(0.2,0.2,0.2),light_diffuse=(1.0,1.0,1.0),light_ambient=(0.1,0.1,0.1)))
 shaderi.children.append(shader(objfile=None,light_position=(0,-1,0,1),light_specular=(0.2,0.2,0.2),light_diffuse=(1.0,1.0,1.0),light_ambient=(0.1,0.1,0.1)))
 shaderi.children.append(shader(objfile=None,light_position=(0,1,0,1),light_specular=(0.2,0.2,0.2),light_diffuse=(1.0,1.0,1.0),light_ambient=(0.1,0.1,0.1)))
 earth2=earth(material_diffuse={'__UNKNOWN__':'earth.png'},fixtransformation=[[12,0,0],['s',0.6,0.6,0.6]],extratransformation=[[23,0,0,1]],material_ambient=(0.3,0.3,0.3))
 earth2.innerchildren.append(shader(objfile='sphere.obj',material_diffuse={'__UNKNOWN__':(1,0,0)},fixtransformation=[[0,0,1.18],['s',0.2,0.2,0.2]],material_ambient=(0.2,0.2,0.2),material_shininess=-1))
 earth2.innerchildren.append(shader(objfile='cubestick.obj',material_emission=(1,1,1),material_diffuse={'Material':(1,1,1)},material_ambient=(0.2,0.2,0.2)))
 earth2.children.append(moon(objfile='sphere.obj',material_diffuse={'__UNKNOWN__':'moon.png'},fixtransformation=[[180,0,1,0],[3,0,0],['s',0.64,0.64,0.64]]))
 earth2.children.append(moon(objfile='ring.obj',material_shininess=-2,fixtransformation=[['s',3,3,3]]))
 '''
 earth2.children.append(moon(objfile='sphere.obj',material_diffuse={'__UNKNOWN__':'moon.png'},transformation=[[20,1,0,0]],fixtransformation=[[3,0,0],['s',0.5,0.5,0.5]]))
 earth2.children.append(moon(objfile='ring.obj',material_shininess=-1,fixtransformation=[[20,1,0,0],['s',3,3,3]]))
 '''
 shaderi.children.append(earth2)

 glClearColor(0,0,0,0)
 glShadeModel(GL_SMOOTH)
 glEnable(GL_DEPTH_TEST)

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
 gluPerspective(40,w/h if w>=h else h/w, 1, 100)
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
