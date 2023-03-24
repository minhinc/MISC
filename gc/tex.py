import os,sys;sys.path.append(os.path.expanduser('~')+r'/tmp/')
import random
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import re
import subprocess,shlex
from PIL import Image,ImageFont,ImageDraw;
from MISC.extra.openglutil import Shape,Utilc
from objloader import ObjFile
shapes=['global','earth']
shape='global'
transformation={x:[] for x in shapes}
if sys.argv[2]=='1':
 transformation['earth']=[[10, 1, 0, 0], [-10, 0, 1, 0], ['s', 1.44, 1.44, 1.44]]
else:
 transformation['earth']=[[0.5383093507674839, 0.9301312221547864, -3.0065235622181583], [-30, 0, 1, 0], [10, 1, 0, 0], [-10, 0, 1, 0], ['s', 1.152, 1.152, 1.152], [10, 1, 0, 0]]
utili=Utilc()
drawaxis=False
airplane=earth=None

def init():
 global airplane,earth
 glClearColor(0,0,0,0)
 glShadeModel(GL_FLAT)
 glEnable(GL_DEPTH_TEST)
 def drawtext(draw,text):
  font=ImageFont.truetype(os.path.expanduser('~')+r'/.fonts/timesnewromanbold.ttf',20)
  for count in range(len(text)):
   draw.text((int(font.getsize(r'C++/20 Programming')[0]/font.getsize(text)[0]*font.getsize(text[0:count])[0]),0),text[count],font=font)
 IMGWIDTH,IMGHEIGHT=200,120
 img2=Image.new('RGBA',(IMGWIDTH,IMGHEIGHT),(0,0,0,0));
 draw=ImageDraw.Draw(img2);
 if sys.argv[2]=='1':
#  draw.text((IMGWIDTH//2,0),sys.argv[1],fill=(255,255,255,255),font=ImageFont.truetype(r'/home/minhinc/.fonts/ufonts.com_tw-cen-mt.ttf',int(56*8/len(sys.argv[1]))),anchor='mt')
  draw.text((IMGWIDTH//2,0),sys.argv[1],fill=(255,255,255,255),font=ImageFont.truetype(r'/home/minhinc/.fonts/ufonts.com_tw-cen-mt.ttf',int(48*8/max(8,len(sys.argv[1])))),anchor='mt')
  draw.text((int(IMGWIDTH/2),ImageFont.truetype(r'/home/minhinc/.fonts/ufonts.com_tw-cen-mt.ttf',int(48*8/max(8,len(sys.argv[1])))).getsize(sys.argv[1])[1]-4),'Minh, Inc.',fill=(255,255,255,255),font=ImageFont.truetype(r'/home/minhinc/.fonts/ufonts.com_tw-cen-mt.ttf',int(48*8/(max(8,len(sys.argv[1]))*1.2))),anchor='mt')
  img=Image.new('RGBA',(2000,800),(0,0,0,0))
  for i in range(int(img.width/(img2.width*1.8))):
   for j in range(int(img.height/(img2.height*1.8))+1):
    img.paste(img2,(int(i*img2.width*1.8),int(j*img2.height*1.8)),img2)
 else:
#  draw.text((IMGWIDTH//2,0),sys.argv[1],fill=(255,255,255,255),font=ImageFont.truetype(r'/home/minhinc/.fonts/ufonts.com_tw-cen-mt.ttf',20),anchor='mt')
  drawtext(draw,sys.argv[1])
  img=Image.new('RGBA',(1090,314),(0,0,0,0))
  img.paste(img2,(200,155),img2)
 img.save('logdir/copyright.png')
 glEnable(GL_LIGHTING)
 glEnable(GL_LIGHT0)
 glEnable(GL_NORMALIZE)
 glLightModeli(GL_LIGHT_MODEL_COLOR_CONTROL,GL_SEPARATE_SPECULAR_COLOR)
# airplane=Shape(obj='airplane.obj',texture=('airplane.png',('copyright.png',40)),specular=(0.4,0.4,0.4,1),shininess=20)
# earth=Shape(obj=os.path.expanduser('~')+r'/tmp/imageglobe/'+'airplane.obj',texture=(os.path.expanduser('~')+r'/tmp/MISC/gc/'+'skyblue.png',('copyright.png',100)),specular=(0.4,0.4,0.4,1),shininess=20)
 if sys.argv[2]=='1':
  earth=Shape(obj=os.path.expanduser('~')+r'/tmp/imageglobe/'+'sphere.obj',texture=(os.path.expanduser('~')+r'/tmp/imageglobe/'+('physical-world-map.jpg','satelite_2048_1024_mod.jpg','satelite_5000_2500_mod.jpg','yellowworldmap_mod.png')[random.randint(0,3)],('logdir/copyright.png',80 )),specular=(0.4,0.4,0.4,1),shininess=20)
 else:
  Image.new('RGBA',(200,100),(0,255,0,255)).save('logdir/skyblue.png')
  earth=Shape(obj=os.path.expanduser('~')+r'/tmp/imageglobe/'+'airplane.obj',texture=(r'logdir/skyblue.png',('logdir/copyright.png',127)),specular=(0.4,0.4,0.4,1),shininess=20)

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
  eval(lshape+'.display()')
  glPopMatrix()
 glPopMatrix()
 glFlush()
 glutTimerFunc(1000,keyboard,ord('P'))


def keyboard(key,x=0,y=0):
 global transformation,shapes,shape
 global utili
 global drawaxis
 key=chr(key).encode() if type(key)==int else bytes(key)
 if key==b'\t':
  shape=shapes[(shapes.index(shape)+1)%len(shapes)]
 utili.keyboard(key,transformation[shape])
 if key==b'v':
  Utilc.pprint(**{'shape=':shape,'transformation=':transformation})
 if key==b'a':
  drawaxis=True
 elif key==b'A':
  drawaxis=False
 elif key==b'P':
  glFlush()
  glutTimerFunc(1000,keyboard,ord('p'))
 elif key==b'p':
  glFlush()
#  subprocess.call(shlex.split(r'gnome-screenshot -d 1 -w -f tmp.png'))
  subprocess.call(shlex.split(r'scrot -d 1 -u -F logdir/tmp.png'))
  img=Image.open('logdir/tmp.png').convert('RGBA')
#  img.crop((img.width//3.3,img.height//7.2,img.width-img.width//3.3,img.height-img.height//8.5)).save('tmp2.png')
  if sys.argv[2]=='1':
   img.crop((img.width//3.3,img.height//8.5,img.width-img.width//3.3,img.height-img.height//8.5)).save('logdir/tmp2.png')
  else:
   img.crop((img.width//3.3,img.height//8.5,img.width-img.width//5,img.height-img.height//8.5)).save('logdir/tmp2.png')
  subprocess.call(shlex.split(r'convert logdir/tmp2.png -channel rgba -fill "rgba(0,0,0,0)" -opaque "rgb(0,0,0)" '+r'logdir/tex_'+re.sub(r'[\s/]+','',sys.argv[1]).lower()+'.png'))
  os.remove('logdir/tmp.png')
  os.remove('logdir/tmp2.png')
  glutDestroyWindow(globalwindow)
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
 glutInitWindowSize(1366,780)
 globalwindow=glutCreateWindow("My OpenGL Code")
 init()
 glutDisplayFunc(display)
 glutKeyboardFunc(keyboard)
 glutReshapeFunc(reshape)
 glutMainLoop()
