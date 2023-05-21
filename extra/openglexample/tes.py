from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
concave=[[-1,1.4,0],[0,0,0],[1,1.4,0,0,1,0],[0,1,0]]
hole=[[-1,1.4,0],[-1,0,0,1,1,0],[1,0,0],[1,1.4,0,0,0,1],[-0.5,1,0,0,1,0],[-0.5,0.5,0],[0.5,0.5,0],[0.5,1,0]]
star=[[0,1.5,0,1,0,1],[-1,0,0,1,1,0],[1,1,0,0,1,1],[-1,1,0,1,0,0],[1,0,0,0,1,0]]
listid=0
hextoprimitive={
   0x0000:"GL_POINTS",
   0x0001:"GL_LINES",
   0x0002:"GL_LINE_LOOP",
   0x0003:"GL_LINE_STRIP",
   0x0004:"GL_TRIANGLES",
   0x0005:"GL_TRIANGLE_STRIP",
   0x0006:"GL_TRIANGLE_FAN",
   0x0007:"GL_QUADS"}

def beginCallback(which):
 print(f'><beginCallback {which=} {hextoprimitive[which]=}')
 glBegin(which)

def endCallback():
 print(f'><endCallback')
 glEnd()

def errorCallback(errorCode):
 print(f'Error - {errorCode=} {gluErrorString(errorCode)=}')

def vertexCallback(vertex_data):
 print(f'><vertexCallback {vertex_data=}')
 glColor3f(*vertex_data[3:]) if len(vertex_data)>3 else None
 glVertex3f(*vertex_data[:3])

def combineCallback(coords,vertex_data,weight):
 print(f'><combineCallback {(type(coords),type(vertex_data),type(weight))=} {(*coords,vertex_data,*weight)=}')
 vertex=[]
 vertex.extend(coords)
# for i in range(3,6):
 for i in range(3):
  vertex.append(weight[0]*vertex_data[0][i]+weight[1]*vertex_data[1][i]+weight[2]*vertex_data[2][i]+weight[3]*vertex_data[3][i])
 print(f'<>combinCallback {vertex=}')
 return vertex


def tessellate():
 startlist=glGenLists(1)
 tobj=gluNewTess()
 gluTessCallback(tobj,GLU_TESS_VERTEX,vertexCallback)
 gluTessCallback(tobj,GLU_TESS_BEGIN,beginCallback)
 gluTessCallback(tobj,GLU_TESS_END,endCallback)
 gluTessCallback(tobj,GLU_TESS_ERROR,errorCallback)
 gluTessCallback(tobj,GLU_TESS_COMBINE,combineCallback)
 glNewList(startlist,GL_COMPILE)
 gluTessBeginPolygon(tobj,0)
 gluTessProperty(tobj,GLU_TESS_WINDING_RULE, GLU_TESS_WINDING_ODD)
 '''
 gluTessBeginContour(tobj)
 for i in range(len(concave)):
  gluTessVertex(tobj,concave[i][:3],concave[i])
 gluTessEndContour(tobj)
 gluTessBeginContour(tobj)
 for i in range(len(star)):
  gluTessVertex(tobj,star[i][:3],star[i])
 gluTessEndContour(tobj)
 '''
 gluTessBeginContour(tobj)
 for i in range(len(hole)//2):
  gluTessVertex(tobj,hole[i][:3],hole[i])
 gluTessEndContour(tobj)
 gluTessBeginContour(tobj)
 for i in range(len(hole)//2,len(hole)):
  gluTessVertex(tobj,hole[i][:3],hole[i])
 gluTessEndContour(tobj)
 gluTessEndPolygon(tobj)
 glEndList()
 gluDeleteTess(tobj)
 return startlist
 
def init():
 global listid
 glClearColor(0,0,0,0)
 glShadeModel(GL_SMOOTH)
 glEnable(GL_DEPTH_TEST)
 listid=tessellate()

 

def display():
 glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
 glPushMatrix()
 glTranslate(0,0,-5)
 glCallList(listid)
 glPopMatrix()
 glFlush()

def reshape(w,h):
 glViewport(0,0,w,h)
 glMatrixMode(GL_PROJECTION)
 glLoadIdentity()
 glOrtho(-1.5,1.5,-1.5*h/w,1.5*h/w,1,10) if(w<=h) else glOrtho(-1.5*w/h,1.5*w/h,-1.5,1.5,1,10)
 glMatrixMode(GL_MODELVIEW)
 glLoadIdentity()

if __name__=="__main__":
 glutInit()
 glutInitDisplayMode(GLUT_SINGLE|GLUT_DEPTH)
 glutInitWindowSize(500,500)
 glutInitWindowPosition(100,100)
 glutCreateWindow("Tessellator")
 init()
 glutDisplayFunc(display)
 glutReshapeFunc(reshape)
 glutMainLoop()
