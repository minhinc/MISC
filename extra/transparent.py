import sys
from PIL import Image
fuzz=20
if len(sys.argv)==1:
 print(f'{"usage":-^40}')
 print(f'transparent.py abc.png 000000ff')
 print(f'transparent.py <file> <color>')
 sys.exit(-1)
img=Image.open(sys.argv[1]).convert('RGBA')
bytedata=img.tobytes()
color=(int(sys.argv[2][0:2],16),int(sys.argv[2][2:4],16),int(sys.argv[2][4:6],16),int(sys.argv[2][6:8],16))
print(f'{bytedata[:48]=} {color=}')
bytedata=[(0,0,0,0) if (color[0]-fuzz)<bytedata[count]<(color[0]+fuzz) and (color[1]-fuzz)<bytedata[count+1]<(color[1]+fuzz) and (color[2]-fuzz)<bytedata[count+2]<(color[2]+fuzz) else bytedata[count:count+4] for count in range(len(bytedata)) if not count%4]
print(f'{bytedata[:48]=}')
bytedata=[y for x in bytedata for y in x]
Image.frombytes('RGBA',img.size,bytes(bytedata),'raw').save('dong.png')
