from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from PIL import Image
from openglutil import Shape,Utilc
from objloader import ObjFile
shapes=['global','airplane','earth']
shape='global'
transformation={x:[] for x in shapes}
utili=Utilc()
drawaxis=False
#img,texName,texName2,m=None,None,None,None
airplane=earth=None
#cubevertices=[-1,-1,1,0,0, -1,1,1,0,1, 1,1,1,0.5,1, 1,-1,1,0.5,0,    1,-1,1,0.5,0, 1,1,1,0.5,1,  1,1,-1,1,1, 1,-1,-1,1,0,    1,-1,-1,0,0, 1,1,-1,0,1, -1,1,-1,0.5,1, -1,-1,-1,0.5,0,   -1,-1,-1,0.5,0, -1,1,-1,0.5,1, -1,1,1,1,1, -1,-1,1,1,0]

def init():
# global texName,texName2,img,m
 global airplane,earth
 glClearColor(0,0,0,0)
 glShadeModel(GL_FLAT)
 glEnable(GL_DEPTH_TEST)
 '''
# texName=glGenTextures(1)
 texName,texName2=glGenTextures(2)
 img=Image.open('satelite_5000_2500.jpg').convert('RGBA')
 img.putalpha(255)
 img=img.transpose(Image.FLIP_TOP_BOTTOM)
 glBindTexture(GL_TEXTURE_2D,texName)
 glTexImage2D(GL_TEXTURE_2D,0,GL_RGBA,img.width,img.height,0,GL_RGBA,GL_UNSIGNED_BYTE,img.tobytes())
 glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_WRAP_S,GL_REPEAT)
 glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_WRAP_T,GL_REPEAT)
 glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_NEAREST)
 glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_NEAREST)
# glGenerateMipmap(GL_TEXTURE_2D)
# glTexParameterfv(GL_TEXTURE_2D,GL_TEXTURE_BORDER_COLOR,(1,1,0,1))
 m=list(ObjFile('sphere.obj').objects.values())[0]
 img.close()

 img=Image.open('copyright.png').convert('RGBA')
 img.putalpha(40)
 img=img.transpose(Image.FLIP_TOP_BOTTOM)
 glBindTexture(GL_TEXTURE_2D,texName2)
 glTexImage2D(GL_TEXTURE_2D,0,GL_RGBA,img.width,img.height,0,GL_RGBA,GL_UNSIGNED_BYTE,img.tobytes())
 glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_WRAP_S,GL_REPEAT)
 glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_WRAP_T,GL_REPEAT)
 glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_NEAREST)
 glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_NEAREST)
 '''
 glEnable(GL_LIGHTING)
 glEnable(GL_LIGHT0)
 glEnable(GL_NORMALIZE)
 glLightModeli(GL_LIGHT_MODEL_COLOR_CONTROL,GL_SEPARATE_SPECULAR_COLOR)
 airplane=Shape(obj='airplane.obj',texture=('airplane.png',('copyright.png',40)),specular=(0.4,0.4,0.4,1),shininess=20)
 earth=Shape(obj='sphere.obj',texture=('yellowworldmap.png',('copyright.png',40)),specular=(0.4,0.4,0.4,1),shininess=20)

def display():
 glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
 glPushMatrix()
 glTranslate(0,0,-3.6)
 Utilc.transformanddrawaxis(transformation['global'],(2,) if drawaxis else None)

 for lshape in [lshape for lshape in shapes if lshape!='global']:
  glPushMatrix()
  glLightfv(GL_LIGHT0,GL_POSITION,(0,0,1,0.0))
  glLightfv(GL_LIGHT0,GL_SPECULAR,(1,1,1,1))
  Utilc.transformanddrawaxis(transformation[lshape],(2,1) if drawaxis else None)
  if lshape=='airplane':
   airplane.display()
  elif lshape=='earth':
   earth.display()
  glPopMatrix()
 
 '''
 glActiveTexture(GL_TEXTURE0)
 glClientActiveTexture(GL_TEXTURE0)
 glMaterialfv(GL_FRONT,GL_SPECULAR,(0.4,0.4,0.4,1.0))
 glMaterialfv(GL_FRONT,GL_SHININESS,20)
 glEnable(GL_TEXTURE_2D)
 glBindTexture(GL_TEXTURE_2D,texName)
 glTexEnvf(GL_TEXTURE_ENV,GL_TEXTURE_ENV_MODE,GL_REPLACE)
 glEnableClientState(GL_VERTEX_ARRAY)
 glVertexPointer(3,GL_FLOAT,0,[y for count in range(len(m.vertices)) if not count%8 for y in m.vertices[count:count+3]])
 glEnableClientState(GL_NORMAL_ARRAY)
 glNormalPointer(GL_FLOAT,0,[y for count in range(len(m.vertices)) if not count%8 for y in m.vertices[count+3:count+6]])
 glEnableClientState(GL_TEXTURE_COORD_ARRAY)
 glTexCoordPointer(2,GL_FLOAT,0,[y for count in range(len(m.vertices)) if not count%8 for y in m.vertices[count+6:count+8]])

 glActiveTexture(GL_TEXTURE1)
 glClientActiveTexture(GL_TEXTURE1)
 glMaterialfv(GL_FRONT,GL_SPECULAR,(0.4,0.4,0.4,1.0))
 glMaterialfv(GL_FRONT,GL_SHININESS,20)
 glEnable(GL_TEXTURE_2D)
 glBindTexture(GL_TEXTURE_2D,texName2)
 glTexEnvf(GL_TEXTURE_ENV,GL_TEXTURE_ENV_MODE,GL_DECAL)
 glEnableClientState(GL_VERTEX_ARRAY)
 glVertexPointer(3,GL_FLOAT,0,[y for count in range(len(m.vertices)) if not count%8 for y in m.vertices[count:count+3]])
 glEnableClientState(GL_NORMAL_ARRAY)
 glNormalPointer(GL_FLOAT,0,[y for count in range(len(m.vertices)) if not count%8 for y in m.vertices[count+3:count+6]])
 glEnableClientState(GL_TEXTURE_COORD_ARRAY)
 glTexCoordPointer(2,GL_FLOAT,0,[y for count in range(len(m.vertices)) if not count%8 for y in m.vertices[count+6:count+8]])

 glDrawArrays(GL_TRIANGLES,0,int(len(m.indices)))

 glDisableClientState(GL_TEXTURE_COORD_ARRAY)
 glDisableClientState(GL_NORMAL_ARRAY)
 glDisableClientState(GL_VERTEX_ARRAY)
 glDisable(GL_TEXTURE_2D)

 glActiveTexture(GL_TEXTURE0)
 glClientActiveTexture(GL_TEXTURE0)
 glDisableClientState(GL_TEXTURE_COORD_ARRAY)
 glDisableClientState(GL_NORMAL_ARRAY)
 glDisableClientState(GL_VERTEX_ARRAY)
 glDisable(GL_TEXTURE_2D)
 '''

 '''
 glMatrixMode(GL_TEXTURE)
 glLoadIdentity()
 glRotate(20,0,0,1)
 glMatrixMode(GL_MODELVIEW)

 glActiveTexture(GL_TEXTURE1)
 glEnable(GL_TEXTURE_2D)
 glBindTexture(GL_TEXTURE_2D,texName2)
 glTexEnvf(GL_TEXTURE_ENV,GL_TEXTURE_ENV_MODE,GL_DECAL)
 


 glBegin(GL_QUADS)
# glTexCoord2f(0,0);glColor3f(0,1,0);glVertex3f(-2,-1,0)
 glMultiTexCoord2f(GL_TEXTURE0,0,0);glMultiTexCoord2f(GL_TEXTURE1,0,0);glVertex3f(-2,-1,0)
 glMultiTexCoord2f(GL_TEXTURE0,0,1);glMultiTexCoord2f(GL_TEXTURE1,0,1);glVertex3f(-2,1,0)
 glMultiTexCoord2f(GL_TEXTURE0,1,1);glMultiTexCoord2f(GL_TEXTURE1,1,1);glVertex3f(-2+2*img.width/img.height,1,0)
 glMultiTexCoord2f(GL_TEXTURE0,1,0);glMultiTexCoord2f(GL_TEXTURE1,1,0);glVertex3f(-2+2*img.width/img.height,-1,0)
 glTexCoord2f(0,0);glVertex3f(1,-1,0)
 glTexCoord2f(0,1);glVertex3f(1,1,0)
 glTexCoord2f(1,1);glVertex3f(2.41,1,-1.4)
 glTexCoord2f(1,0);glVertex3f(2.41,-1,-1.4)
 glEnd()
 glDisable(GL_TEXTURE_2D)
 glActiveTexture(GL_TEXTURE0)
 glDisable(GL_TEXTURE_2D)
 '''
# glPopMatrix()
 glPopMatrix()
 glFlush()

def keyboard(key,x,y):
 global transformation,shapes,shape
 global utili
 global drawaxis
 key=bytes(key)
 if key==b'\t':
  shape=shapes[(shapes.index(shape)+1)%len(shapes)]
 utili.keyboard(key,transformation[shape])
 if key==b'v':
  Utilc.pprint(**{'shape=':shape,'transformation=':transformation})
 if key==b'a':
  drawaxis=True
 elif key==b'A':
  drawaxis=False
 glutPostRedisplay()

def reshape(w,h):
 glViewport(0,0,w,h)
 glMatrixMode(GL_PROJECTION)
 glLoadIdentity()
 gluPerspective(60,w/h if w>=h else h/w,1,30)
# glOrtho(-2.5,2.5,-2.5*h/w,2.5*h/w,1,30) if w<=h else glOrtho(-2.5*w/h,2.5*w/h,-2.5,2.5,1,30)
 glMatrixMode(GL_MODELVIEW)
 glLoadIdentity()
# glTranslate(0,0,-3.8)

if __name__=='__main__':
 glutInit()
 glutInitDisplayMode(GLUT_SINGLE|GLUT_RGB|GLUT_DEPTH)
 glutInitWindowSize(500,500)
 glutCreateWindow("My OpenGL Code")
 init()
 glutDisplayFunc(display)
 glutKeyboardFunc(keyboard)
 glutReshapeFunc(reshape)
 glutMainLoop()
