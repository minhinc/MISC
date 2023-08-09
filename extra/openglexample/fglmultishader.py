from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import sys;sys.path.append('/home/minhinc/tmp')
import math
import re
import time

from MISC.extra.openglutil import Utilc
from MISC.extra.shader import shader
from loco import loco
#from earth import earth
from wheel import wheel
utili=shader.utili

shaderi=None
def init():
 global shaderi
 shaderi=shader(objfile=None)
 loco2=loco(transformation=[[0,0,-40]],fixtransformation=[[90,0,1,0]])
 shaderi.children.append(loco2)
 loco3=loco(transformation=[[0,0,-40]],fixtransformation=[[-3.0,0,0],[90,0,1,0]])
 shaderi.children.append(loco3)
 shaderi.children.append(shader(objfile='birch_tree.obj',fixtransformation=[[-6,0,0]],material_diffuse=[(0,2,0),'Tree.Birch.Leaf.Summer.Mat']))
 shaderi.children.append(shader(objfile='birch_tree.obj',fixtransformation=[[6,0,1],['s',0.5,0.5,0.5]],material_diffuse=[(0,2,0),'Tree.Birch.Leaf.Summer.Mat']))
 shaderi.children.append(shader(objfile='birch_tree.obj',fixtransformation=[[-4,0,-5],['s',0.5,0.5,0.5]],material_diffuse=[(0,2,0),'Tree.Birch.Leaf.Summer.Mat']))
 shaderi.children.append(shader(objfile='birch_tree.obj',fixtransformation=[[4,0,-5],['s',0.7,0.7,0.7]],material_diffuse=[(2,2,1),'Tree.Birch.Leaf.Summer.Mat']))
 shaderi.children.append(shader(objfile='birch_tree.obj',fixtransformation=[[-3,0,-14],['s',0.5,0.5,0.5]],material_diffuse=[(0,2,2),'Tree.Birch.Leaf.Summer.Mat']))
 shaderi.children.append(shader(objfile='birch_tree.obj',fixtransformation=[[-7,0,-14],['s',0.5,0.5,0.5]],material_diffuse=[(2,0,2),'Tree.Birch.Leaf.Summer.Mat']))
 shaderi.children.append(shader(objfile='birch_tree.obj',fixtransformation=[[6,0,-20],['s',0.5,0.5,0.5]],material_diffuse=[(0,2,0),'Tree.Birch.Leaf.Summer.Mat']))
 shaderi.children.append(shader(objfile=None,light_position=(0,0,1,0),light_diffuse=(0.2,0.2,0.2)))#light_spotangle'=40,light_spotexponent'=0}))
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
 gluPerspective(30,w/h if w>=h else h/w, 1, 70)
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
