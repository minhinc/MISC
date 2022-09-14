import sys,re
from PIL import Image
def getfile(filep):
 return re.sub(r'^(.*)[.].*$',r'\1',filep)
if len(sys.argv)<2:
 print(r'---usage python3 alignimage.py <image1> <eyecoord> <image2> <eyecoord>')
 print(r'---usage python3 alignimage.py --crop <image1> <x1,y1,w,h> <x2,y2,w,h> ....')
 sys.exit(-1)
if sys.argv[1]=='--crop':
 for count,i in enumerate([tuple([int(x) for x in re.split(',',i)]) for i in sys.argv[3:]]):
  img=Image.open(sys.argv[2]).convert('RGBA')
  img=img.crop((*i[:2],i[0]+i[2],i[1]+i[3]))
  img.save(getfile(sys.argv[2])+'_'+str(count)+'_crop.png')
  print(f'saved to {getfile(sys.argv[2])+"_"+str(count)+"_crop.png"}')
else:
 img1=Image.open(sys.argv[1]).convert('RGBA')
 imagesize=img1.size
 print(f'{imagesize=}')
 i1ec=[int(x) for x in re.split(',',sys.argv[2])]
 img2=Image.open(sys.argv[3]).convert('RGBA')
 i2ec=[int(x) for x in re.split(',',sys.argv[4])]
 img1=img1.crop((i1ec[0]>i2ec[0] and i1ec[0]-i2ec[0] or 0,i1ec[1]>i2ec[1] and i1ec[1]-i2ec[1] or 0,*img1.size))
 img2=img2.crop((i2ec[0]>i1ec[0] and i2ec[0]-i1ec[0] or 0,i2ec[1]>i1ec[1] and i2ec[1]-i1ec[1] or 0,*img2.size))
 print(f'size after crop {img1.size=} {img2.size=}')
 for i in [(count,i) for count,i in enumerate((img1,img2)) if i.size != imagesize]:
  img=Image.new('RGBA',imagesize,color=(0,0,0,255))
  img.paste(i[1],(0,0),i[1])
  img.save(getfile(sys.argv[i[0]*2+1])+'_new.png')
  print(f'saved to {getfile(sys.argv[i[0]*2+1])+"_new.png"}')
