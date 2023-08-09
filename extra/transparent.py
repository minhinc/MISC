import sys,os;sys.path.append(os.path.expanduser('~')+'/tmp')
from PIL import Image
import re
from MISC.utillib.util import Util
if len(sys.argv)<=2:
 print(f'{"usage":-^40}')
 print(f'transparent.py <file> <color> [--fuzz] [--mode]')
 print(f'transparent.py abc.png 000000ff')
 print(f'transparent.py abc.png 000000ff --fuzz 10 --mode full')
 sys.exit(-1)
fuzz=int(Util.getarg('--fuzz',count=2)) or 10
mode=Util.getarg('--mode',count=2) or 'outer'
img=Image.open(sys.argv[1]).convert('RGBA')
bytedata=img.tobytes()
bytedata=list(bytedata)
color=(int(sys.argv[2][0:2],16),int(sys.argv[2][2:4],16),int(sys.argv[2][4:6],16),int(sys.argv[2][6:8],16))
print(f'{bytedata[:48]=} {color=} {img.size=} {fuzz=} {mode=}')
if mode=='full':
 bytedata=[(0,0,0,0) if (color[0]-fuzz)<bytedata[count]<(color[0]+fuzz) and (color[1]-fuzz)<bytedata[count+1]<(color[1]+fuzz) and (color[2]-fuzz)<bytedata[count+2]<(color[2]+fuzz) else bytedata[count:count+4] for count in range(len(bytedata)) if not count%4]
 bytedata=[y for x in bytedata for y in x]
else:
 for i in range(img.height):
  for j in range(img.width):
   if (color[0]-fuzz)<bytedata[i*img.width*4+j*4]<(color[0]+fuzz) and (color[1]-fuzz)<bytedata[i*img.width*4+j*4+1]<(color[1]+fuzz) and (color[2]-fuzz)<bytedata[i*img.width*4+j*4+2]<(color[2]+fuzz):
    bytedata[i*img.width*4+j*4:i*img.width*4+j*4+4]=[0,0,0,0]
   else:
    print(f'broke1 {i=} {j=}')
    for k in range(img.width-1,j-1,-1):
     print(f'11 {i=} {j=} {k=}')
     if (color[0]-fuzz)<bytedata[i*img.width*4+k*4]<(color[0]+fuzz) and (color[1]-fuzz)<bytedata[i*img.width*4+k*4+1]<(color[1]+fuzz) and (color[2]-fuzz)<bytedata[i*img.width*4+k*4+2]<(color[2]+fuzz):
      bytedata[i*img.width*4+k*4:i*img.width*4+k*4+4]=[0,0,0,0]
     else:
      break
    break
 print(f'BREAK {bytedata[42*img.width*4:42*img.width*4+4]=}')
 for i in range(img.width):
  for j in range(img.height):
   print(f'{i=} {j=}')
   if ((color[0]-fuzz)<bytedata[j*img.width*4+i*4]<(color[0]+fuzz) and (color[1]-fuzz)<bytedata[j*img.width*4+i*4+1]<(color[1]+fuzz) and (color[2]-fuzz)<bytedata[j*img.width*4+i*4+2]<(color[2]+fuzz)) or bytedata[j*img.width*4+i*4:j*img.width*4+i*4+4]==[0,0,0,0]:
    bytedata[j*img.width*4+i*4:j*img.width*4+i*4+4]=[0,0,0,0]
   else:
    print(f'broke2 {i=} {j=} {bytedata[j*img.width*4+i*4:j*img.width*4+i*4+4]=}')
    for k in range(img.height-1,j-1,-1):
     print(f'22 {i=} {j=} {k=} {bytedata[k*img.width*4+i*4:k*img.width*4+i*4+4]=}')
     if ((color[0]-fuzz)<bytedata[k*img.width*4+i*4]<(color[0]+fuzz) and (color[1]-fuzz)<bytedata[k*img.width*4+i*4+1]<(color[1]+fuzz) and (color[2]-fuzz)<bytedata[k*img.width*4+i*4+2]<(color[2]+fuzz)) or bytedata[k*img.width*4+i*4:k*img.width*4+i*4+4]==[0,0,0,0]:
      bytedata[k*img.width*4+i*4:k*img.width*4+i*4+4]=[0,0,0,0]
     else:
      break
    break
print(f'{bytedata[:48]=}')
Image.frombytes('RGBA',img.size,bytes(bytedata),'raw').save(re.sub(r'^(.*)[.](.*)$',r'\1_t.\2',re.split("/",sys.argv[1])[-1]))
print(f'{"":-^40}')
print(re.sub(r'^(.*)[.](.*)$',r'\1_t.\2',re.split("/",sys.argv[1])[-1]))
print(f'{"":-^40}')
