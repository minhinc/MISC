import re,os,sys;sys.path.append(os.path.expanduser('~')+r'/tmp/')
from PIL import Image,ImageDraw,ImageFont
import sys;sys.path.append(r'/home/minhinc/tmp')
import MISC.ffmpeg.libm
from MISC.extra.debugwrite import print

def getimage(topic,subtopiclab=(),keysubtopicindex=(),outimagename='ding.png'):
 '''
 def multiline_text(**kwarg):
  print(f'{kwarg=}')
  draw.multiline_text(**kwarg)
 '''
 def drawarc(xy,xb,yb,text,color,keysubtopic=False):#xb-xboundary,yb-yboundary
  nonlocal draw,linewidth,unitsizehalf,rectsizehalf,xoffset,dimension,img,libi
  print(f'><drawarc {xy=} {xb=} {yb=} {text=} {color=} {keysubtopic=} {draw=} {xoffset=} {dimension=}')
  xpipe=rectsizehalf[0]
  xb=xb-xpipe if xb>xy[0] else xb+xpipe
  draw.arc(((xb-(xy[0]-xb) if xy[0]>xb else xy[0],yb if yb<xy[1] else xy[1]-(yb-xy[1])),(xb+xb-xy[0] if xb>xy[0] else xy[0],xy[1]+xy[1]-yb if yb<xy[1] else yb)),180 if xy[0]<xb and yb<xy[1] else 90 if xy[0]<xb and yb>xy[1] else -90 if xb<xy[0] and yb<xy[1] else 0, -90 if xb>xy[0] and yb<xy[1] else 180 if xb>xy[0] and yb>xy[1] else 0 if xb<xy[0] and yb<xy[1] else 90,color,width=linewidth)
  draw.line(((xb,yb+linewidth//2 if yb<xy[1] else yb-linewidth//2),(xb>xy[0] and not keysubtopic and xb+xpipe or xb>xy[0] and keysubtopic and img.width or xb<xy[0] and not keysubtopic and xb-xpipe or xb<xy[0] and keysubtopic and 0,yb+linewidth//2 if yb<xy[1] else yb-linewidth//2)),fill=color if not keysubtopic else (255,255,0,255),width=linewidth)
#  draw.multiline_text(xy=(xb>xy[0] and not keysubtopic and xb+xpipe//2 or xb>xy[0] and keysubtopic and (img.width-xpipe//2 if max(len(x) for x in re.split(r'(?:\n|\\n)',text))<unitsizehalf//4 else img.width-(xpipe+(img.width-dimension[0])//2)//2) or xb<xy[0] and not keysubtopic and xb-xpipe//2 or xb<xy[0] and keysubtopic and (xpipe//2 if max(len(x) for x in re.split(r'(?:\n|\\n)',text))<unitsizehalf//4 else xpipe//2+(img.width-dimension[0])//4),yb-unitsizehalf//2+linewidth//2),text=text,align='center',anchor='mm',fill=(255,255,255,255),font=libi.getfont((text,),fontfamily_p=r'/home/minhinc/.fonts/NimbusSanL-Reg.otf',screenratio_p=0.8,widthheight=abs(xy[1]-yb)//10,setvideo=str(xpipe+(img.width-dimension[0])//2 if keysubtopic and max(len(x) for x in re.split(r'(?:\n|\\n)',text))>=unitsizehalf//4 else xpipe)+'x'+str(unitsizehalf-linewidth)))
  draw.multiline_text(xy=(xb>xy[0] and not keysubtopic and xb+xpipe//2 or xb>xy[0] and keysubtopic and (img.width-xpipe//2 if max(len(x) for x in re.split(r'(?:\n|\\n)',text))<unitsizehalf//4 else img.width-(xpipe+(img.width-dimension[0])//2)//2) or xb<xy[0] and not keysubtopic and xb-xpipe//2 or xb<xy[0] and keysubtopic and (xpipe//2 if max(len(x) for x in re.split(r'(?:\n|\\n)',text))<unitsizehalf//4 else xpipe//2+(img.width-dimension[0])//4),yb-unitsizehalf//2+linewidth//2),text=text,align='center',spacing=unitsizehalf//10,anchor='mm',fill=(255,255,255,255),font=libi.getfont((text,),fontfamily_p=r'/home/minhinc/.fonts/NimbusSanL-Reg.otf',screenratio_p=0.8,widthheight=unitsizehalf//10,setvideo=str(xpipe+(img.width-dimension[0])//2 if keysubtopic and max(len(x) for x in re.split(r'(?:\n|\\n)',text))>=unitsizehalf//4 else xpipe)+'x'+str(unitsizehalf-linewidth)))

# unitsizehalf=100
 unitsizehalf=400
 linewidth=unitsizehalf//10
 subtopic=subtopiclab[0:subtopiclab.index('><') if subtopiclab.count('><') else None]
 lab=subtopiclab[subtopiclab.index('><')+1:None] if subtopiclab.count('><') else []
 print(f'><getimage {subtopic=} {lab=} {keysubtopicindex=} {outimagename=}')
 rectsizehalf=(unitsizehalf*6,int(unitsizehalf*1.2))
 libi=MISC.ffmpeg.libm.libc()
 dimension=(rectsizehalf[0]+rectsizehalf[0]//2+rectsizehalf[0]*2+rectsizehalf[0]//2+rectsizehalf[0],unitsizehalf*2*((max(len(subtopic),len(lab))+5)//2))
 xoffset=int(rectsizehalf[0]//(2*max((len(subtopic)-2)//2,6)))
 img=Image.new('RGBA',(dimension[0]+int(dimension[0]-rectsizehalf[0]*2)//3,dimension[1]),(0,0,0,0))
 draw=ImageDraw.Draw(img)
 print(f'<=>getimage {subtopic=} {lab=} {img.size=} {dimension=} {xoffset=} {rectsizehalf=}')
 draw.rounded_rectangle(((img.width//2-rectsizehalf[0],dimension[1]//2-rectsizehalf[1]),(img.width//2+rectsizehalf[0],dimension[1]//2+rectsizehalf[1])),30,outline=(0,255,0,255),width=linewidth)
# draw.multiline_text((img.width//2,img.height//2),topic,anchor='mm',align='center',spacing=rectsizehalf[1]//6,fill=(255,255,255,255),font=libi.getfont((topic,),fontfamily_p=r'/home/minhinc/.fonts/NimbusSanL-Reg.otf',screenratio_p=0.8,widthheight=rectsizehalf[1]//6,setvideo='x'.join(str(x*2) for x in rectsizehalf)))
 draw.multiline_text((img.width//2,img.height//2+rectsizehalf[1]//20),topic,anchor='mm',align='center',spacing=(rectsizehalf[1]*2)//7,fill=(255,255,255,255),font=libi.getfont((topic,),fontfamily_p=r'/home/minhinc/.fonts/NimbusSanL-Reg.otf',screenratio_p=0.8,widthheight=rectsizehalf[1]//8,setvideo='x'.join(str(x*2) for x in rectsizehalf)))
# color=[(85,170,0,255),(85,70,255,255),(0,85,255,255),(255,170,0,255),(255,0,0,255)]
 color=[(85,170,0,255),(170,85,255,255),(0,85,255,255),(255,170,0,255),(255,0,0,255),(125,205,255)]

 drawarc((img.width//2+rectsizehalf[0],img.height//2-rectsizehalf[1]//2),(img.width+dimension[0])//2,img.height//2-unitsizehalf,subtopic[(len(subtopic)-1)//2],color[((len(subtopic)-1)//2)%len(color)],keysubtopic=True if (len(subtopic)-1)//2 in keysubtopicindex else False) if len(subtopic)>0 else None
 drawarc((img.width//2-rectsizehalf[0],img.height//2-rectsizehalf[1]//2),(img.width-dimension[0])//2,img.height//2-unitsizehalf,lab[(len(lab)-1)//2],color[((len(lab)-1)//2)%len(color)],keysubtopic=True if len(subtopic)+(len(lab)-1)//2 in keysubtopicindex else False) if len(lab)>0 else None
 drawarc((img.width//2+rectsizehalf[0],img.height//2+rectsizehalf[1]//2),(img.width+dimension[0])//2,img.height//2+unitsizehalf,subtopic[(len(subtopic)-1)//2+1],color[((len(subtopic)-1)//2+1)%len(color)],keysubtopic=True if (len(subtopic)-1)//2+1 in keysubtopicindex else False) if len(subtopic)>1 else None
 drawarc((img.width//2-rectsizehalf[0],img.height//2+rectsizehalf[1]//2),(img.width-dimension[0])//2,img.height//2+unitsizehalf,lab[(len(lab)-1)//2+1],color[((len(lab)-1)//2+1)%len(color)],keysubtopic=True if len(subtopic)+(len(lab)-1)//2+1 in keysubtopicindex else False) if len(lab)>1 else None

 for x in range((len(subtopic)-1)//2):
  drawarc((img.width//2+rectsizehalf[0]-((len(subtopic)-1)//2-x)*xoffset,img.height//2-rectsizehalf[1]),(img.width+dimension[0])//2,img.height//2-((len(subtopic)-1)//2+1-x)*unitsizehalf,subtopic[x],color[x%len(color)],keysubtopic=True if x in keysubtopicindex else False)
 for x in range((len(subtopic)-1)//2+2,len(subtopic)):
  drawarc((img.width//2+rectsizehalf[0]-int((x-((len(subtopic)-1)//2+2)+1.5)*xoffset),img.height//2+rectsizehalf[1]),(img.width+dimension[0])//2,img.height//2+(x-((len(subtopic)-1)//2))*unitsizehalf,subtopic[x],color[x%len(color)],keysubtopic=True if x in keysubtopicindex else False)
 for x in range((len(lab)-1)//2):
  drawarc((img.width//2-rectsizehalf[0]+((len(lab)-1)//2-x)*xoffset,img.height//2-rectsizehalf[1]),(img.width-dimension[0])//2,img.height//2-((len(lab)-1)//2+1-x)*unitsizehalf,lab[x],color[x%len(color)],keysubtopic=True if len(subtopic)+x in keysubtopicindex else False)
 for x in range((len(lab)-1)//2+2,len(lab)):
  drawarc((img.width//2-rectsizehalf[0]+int((x-((len(lab)-1)//2+2)+1.5)*xoffset),img.height//2+rectsizehalf[1]),(img.width-dimension[0])//2,img.height//2+(x-((len(lab)-1)//2))*unitsizehalf,lab[x],color[x%len(color)],keysubtopic=True if len(subtopic)+x in keysubtopicindex else False)

 img=img.crop(((img.width-dimension[0])//2,0,img.width,img.height+unitsizehalf//4-unitsizehalf*(max(len(subtopic),len(lab))%2+1))) if [x for x in range(len(subtopic)) if x in keysubtopicindex] and not [x for x in range(len(subtopic),len(subtopic+lab)) if x in keysubtopicindex] else img.crop((0,0,(img.width+dimension[0])//2,img.height+unitsizehalf//4-unitsizehalf*(max(len(subtopic),len(lab))%2+1))) if [x for x in range(len(subtopic),len(subtopic+lab)) if x in keysubtopicindex] and not [x for x in range(len(subtopic)) if x in keysubtopicindex] else img.crop(((img.width-dimension[0])//2,0,(img.width+dimension[0])//2,img.height+unitsizehalf//4-unitsizehalf*(max(len(subtopic),len(lab))%2+1)))
 '''
 if [x for x in range(len(subtopic)) if x in keysubtopicindex] and not [x for x in range(len(subtopic),len(subtopic+lab)) if x in keysubtopicindex]:
  img=img.crop((img.width-dimension[0])//2,0,img.width,img.height+unitsizehalf//4-unitsizehalf*(max(len(subtopic),len(lab))%2+1))
 elif [x for x in range(len(subtopic),len(subtopic+lab)) if x in keysubtopicindex] and not [x for x in range(len(subtopic)) if x in keysubtopicindex]:
  img=(0,0,(img.width+dimension[0])//2,img.height+unitsizehalf//4-unitsizehalf*(max(len(subtopic),len(lab))%2+1))
 '''
 if resizewidth:
  print(f"resizing... {img.size=} '{resizewidth}x...'")
  img=img.resize((resizewidth,int(img.height*resizewidth/img.width)))
 print(f'saving...{outimagename=} {img.size=}')
 img.save(outimagename)
if __name__=='__main__':
 if len(sys.argv)<=2:
  print(f'----- usage -----\n\
python3 {sys.argv[0]} \'topic\' \'subtopic1\' \'subtopic2\' ... \'><\' \'lab1\' \'lab2\' ... [<combined>] [--resize <width=320>]\n\
python3 subtopicgraph.py \'Context Menu\\nin Kivy\' \'Introduction\' \'Issues with\\ncurrent implementation\' \'><\' \'Exercise0\' \'Exercise1\' <2,3>' '--resize 320')
  sys.exit(-1)
 resizewidth=None
 count=None
 if [x for x in sys.argv if re.search(r'--resize',x)]:
  count=[count for count,x in enumerate(sys.argv) if re.search(r'--resize',x)][0]
  if len(sys.argv)>(count+1) and re.search(r'^\d+$',sys.argv[count+1]):
   resizewidth=int(sys.argv[count+1])
   sys.argv[count:count+2]=[]
  else:
   resizewidth=350
   sys.argv[count:count+1]=[]
 sys.argv[1:]=[re.sub(r'\\n','\n',x) for x in sys.argv[1:]]
 if not [x for x in sys.argv[2:] if re.search('^\s*<.*?>\s*$',x)]:
  for i in range(len([x for x in sys.argv[2:] if not re.search(r'^\s*><\s*$',x)])):
   getimage(sys.argv[1],sys.argv[2:],(i,),re.sub(r'\s+','_',sys.argv[1])+'_'+str(i)+'.png')
 else:
  getimage(sys.argv[1],[x for x in sys.argv[2:] if not re.search(r'^\s*<.*?>\s*$',x)],[[int(x) for x in re.split(',',re.sub(r'.*?<(.*?)>.*?$',r'\1',x)) if x] for x in sys.argv[2:] if re.search(r'^\s*<.*?>\s*$',x)][0],re.sub(r'\s+','_',sys.argv[1])+'.png')
