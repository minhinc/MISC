import re,os,sys;sys.path.append(os.path.expanduser('~')+r'/tmp/')
from PIL import Image,ImageDraw,ImageFont
import sys;sys.path.append(r'/home/minhinc/tmp')
import MISC.ffmpeg.libm
from MISC.utillib.util import Util as Utilc
#from MISC.extra.debugwrite import print

def getimage(topic,subtopiclab=(),keysubtopicindex=(),outimagename='ding.png'):
 print(f'><getimage {topic=} {subtopiclab=} {keysubtopicindex=} {outimagename=}')
 '''
 def multiline_text(**kwarg):
  print(f'{kwarg=}')
  draw.multiline_text(**kwarg)
 '''
 def drawarc(xy,xb,yb,text,color,keysubtopic=False,multiplesubtopic=False):#xb-xboundary,yb-yboundary
  nonlocal draw,linewidth,unitsizehalf,rectsizehalf,xoffset,dimension,img,libi
  print(f'><drawarc {xy=} {xb=} {yb=} {text=} {color=} {keysubtopic=} {draw=} {xoffset=} {dimension=} {multiplesubtopic=}')
  text=re.sub(r'\n',' ',text) if multiplesubtopic else re.sub(r'\s+',r'\n',text)
  xpipe=rectsizehalf[0]
  xb=xb-xpipe if xb>xy[0] else xb+xpipe
  draw.arc(((xb-(xy[0]-xb) if xy[0]>xb else xy[0],yb if yb<xy[1] else xy[1]-(yb-xy[1])),(xb+xb-xy[0] if xb>xy[0] else xy[0],xy[1]+xy[1]-yb if yb<xy[1] else yb)),180 if xy[0]<xb and yb<xy[1] else 90 if xy[0]<xb and yb>xy[1] else -90 if xb<xy[0] and yb<xy[1] else 0, -90 if xb>xy[0] and yb<xy[1] else 180 if xb>xy[0] and yb>xy[1] else 0 if xb<xy[0] and yb<xy[1] else 90,color,width=linewidth)
  draw.line(((xb,yb+linewidth//2 if yb<xy[1] else yb-linewidth//2),(xb>xy[0] and not keysubtopic and xb+xpipe or xb>xy[0] and keysubtopic and img.width or xb<xy[0] and not keysubtopic and xb-xpipe or xb<xy[0] and keysubtopic and 0,yb+linewidth//2 if yb<xy[1] else yb-linewidth//2)),fill=color if not keysubtopic else (255,255,0,255),width=linewidth)
  if multiplesubtopic:
   draw.multiline_text(xy=(xb>xy[0] and not keysubtopic and xb+xpipe//2 or xb>xy[0] and keysubtopic and (img.width-xpipe//2 if max(len(x) for x in re.split(r'(?:\n|\\n)',text))<unitsizehalf//4 else img.width-(xpipe+(img.width-dimension[0])//2)//2) or xb<xy[0] and not keysubtopic and xb-xpipe//2 or xb<xy[0] and keysubtopic and (xpipe//2 if max(len(x) for x in re.split(r'(?:\n|\\n)',text))<unitsizehalf//4 else xpipe//2+(img.width-dimension[0])//4),yb-unitsizehalf//2+linewidth//2),text=text,align='center',spacing=unitsizehalf//10,anchor='mm',fill=(255,255,255,255),font=libi.getfont((text,),fontfamily_p=r'/home/minhinc/.fonts/NimbusSanL-Reg.otf',screenratio_p=0.8,widthheight=unitsizehalf//10,setvideo=str(xpipe+(img.width-dimension[0])//2 if keysubtopic and max(len(x) for x in re.split(r'(?:\n|\\n)',text))>=unitsizehalf//4 else xpipe)+'x'+str(unitsizehalf-linewidth)))
  else:
   draw.multiline_text(xy=(xb>xy[0] and not keysubtopic and xb+xpipe or xb>xy[0] and keysubtopic and img.width or xb<xy[0] and not keysubtopic and xb or xb<xy[0] and keysubtopic and xpipe*2,yb),text=text,align='center',spacing=unitsizehalf//7,anchor='rd',fill=(255,255,255,255),font=libi.getfont((text,),fontfamily_p=r'/home/minhinc/.fonts/NimbusSanL-Reg.otf',screenratio_p=0.9,widthheight=unitsizehalf//7,setvideo=str(xpipe if not keysubtopic else xpipe*2)+'x'+str(unitsizehalf-linewidth if not keysubtopic else 4*unitsizehalf)))

# unitsizehalf=100
#                                                                               |
#                                                                               |
#                                                                               v
#                   |                                      +  +   +   +   +  +  +
#          -------->| rectsizehalf |<----------        +                     unitsizehalf
#                   |              |                          +  +  +  +  +  +  +
#                   ---------------|--------------  +      +                    ^
#                   |                            |     +                        |
#                   |                            |+                             |
#                   |                            |
#                   ------------------------------
 unitsizehalf=400
 linewidth=unitsizehalf//10
 subtopic=subtopiclab[0:subtopiclab.index('><') if subtopiclab.count('><') else None]
 lab=subtopiclab[subtopiclab.index('><')+1:None] if subtopiclab.count('><') else []
# print(f'><getimage {subtopic=} {lab=} {keysubtopicindex=} {outimagename=}')
 rectsizehalf=(unitsizehalf*6,int(unitsizehalf*1.2))
 libi=MISC.ffmpeg.libm.libc()
 if len(keysubtopicindex)>1:
  dimension=(rectsizehalf[0]+2*rectsizehalf[0]+2*(rectsizehalf[0]//2+rectsizehalf[0]),unitsizehalf*2*max(len(subtopic),len(lab))+4*unitsizehalf)
 else:
  dimension=(2*rectsizehalf[0]+2*(rectsizehalf[0]//2+rectsizehalf[0]+2*rectsizehalf[0]),unitsizehalf*2*max(len(subtopic),len(lab))+4*unitsizehalf)
 xoffset=int(rectsizehalf[0]//(2*max((len(subtopic)-2)//2,6)))
 img=Image.new('RGBA',dimension,(0,0,0,0))
 draw=ImageDraw.Draw(img)
 print(f'<=>getimage {subtopic=} {lab=} {img.size=} {dimension=} {xoffset=} {rectsizehalf=} {unitsizehalf=}')
 draw.rounded_rectangle(((img.width//2-rectsizehalf[0],dimension[1]//2-rectsizehalf[1]),(img.width//2+rectsizehalf[0],dimension[1]//2+rectsizehalf[1])),30,outline=(0,255,0,255),width=linewidth)
 draw.multiline_text((img.width//2,img.height//2+rectsizehalf[1]//20),topic,anchor='mm',align='center',spacing=(rectsizehalf[1]*2)//7,fill=(255,255,255,255),font=libi.getfont((topic,),fontfamily_p=r'/home/minhinc/.fonts/NimbusSanL-Reg.otf',screenratio_p=0.8,widthheight=(rectsizehalf[1]*2)//7,setvideo='x'.join(str(x*2) for x in rectsizehalf)))
 color=[(85,170,0,255),(170,85,255,255),(0,85,255,255),(255,170,0,255),(255,0,0,255),(125,205,255)]

 drawarc((img.width//2+rectsizehalf[0],img.height//2-rectsizehalf[1]//2),img.width//2+rectsizehalf[0]+(3*rectsizehalf[0])//2,img.height//2-unitsizehalf,subtopic[(len(subtopic)-1)//2],color[((len(subtopic)-1)//2)%len(color)],keysubtopic=True if (len(subtopic)-1)//2 in keysubtopicindex else False,multiplesubtopic=len(keysubtopicindex)>1) if len(subtopic)>0 else None
 drawarc((img.width//2-rectsizehalf[0],img.height//2-rectsizehalf[1]//2),img.width//2-rectsizehalf[0]-(3*rectsizehalf[0])//2,img.height//2-unitsizehalf,lab[(len(lab)-1)//2],color[((len(lab)-1)//2)%len(color)],keysubtopic=True if len(subtopic)+(len(lab)-1)//2 in keysubtopicindex else False,multiplesubtopic=len(keysubtopicindex)>1) if len(lab)>0 else None
 drawarc((img.width//2+rectsizehalf[0],img.height//2+rectsizehalf[1]//2),img.width//2+rectsizehalf[0]+(3*rectsizehalf[0])//2,img.height//2+unitsizehalf,subtopic[(len(subtopic)-1)//2+1],color[((len(subtopic)-1)//2+1)%len(color)],keysubtopic=True if (len(subtopic)-1)//2+1 in keysubtopicindex else False,multiplesubtopic=len(keysubtopicindex)>1) if len(subtopic)>1 else None
 drawarc((img.width//2-rectsizehalf[0],img.height//2+rectsizehalf[1]//2),img.width//2-rectsizehalf[0]-(3*rectsizehalf[0])//2,img.height//2+unitsizehalf,lab[(len(lab)-1)//2+1],color[((len(lab)-1)//2+1)%len(color)],keysubtopic=True if len(subtopic)+(len(lab)-1)//2+1 in keysubtopicindex else False,multiplesubtopic=len(keysubtopicindex)>1) if len(lab)>1 else None
 for x in range((len(subtopic)-1)//2):
  drawarc((img.width//2+rectsizehalf[0]-((len(subtopic)-1)//2-x)*xoffset,img.height//2-rectsizehalf[1]),img.width//2+rectsizehalf[0]+(3*rectsizehalf[0])//2,img.height//2-((len(subtopic)-1)//2+1-x)*unitsizehalf,subtopic[x],color[x%len(color)],keysubtopic=True if x in keysubtopicindex else False,multiplesubtopic=len(keysubtopicindex)>1)
 for x in range((len(subtopic)-1)//2+2,len(subtopic)):
  drawarc((img.width//2+rectsizehalf[0]-int((x-((len(subtopic)-1)//2+2)+1.5)*xoffset),img.height//2+rectsizehalf[1]),img.width//2+rectsizehalf[0]+(3*rectsizehalf[0])//2,img.height//2+(x-((len(subtopic)-1)//2))*unitsizehalf,subtopic[x],color[x%len(color)],keysubtopic=True if x in keysubtopicindex else False,multiplesubtopic=len(keysubtopicindex)>1)
 for x in range((len(lab)-1)//2):
  drawarc((img.width//2-rectsizehalf[0]+((len(lab)-1)//2-x)*xoffset,img.height//2-rectsizehalf[1]),img.width//2-rectsizehalf[0]-(3*rectsizehalf[0])//2,img.height//2-((len(lab)-1)//2+1-x)*unitsizehalf,lab[x],color[x%len(color)],keysubtopic=True if len(subtopic)+x in keysubtopicindex else False,multiplesubtopic=len(keysubtopicindex)>1)
 for x in range((len(lab)-1)//2+2,len(lab)):
  drawarc((img.width//2-rectsizehalf[0]+int((x-((len(lab)-1)//2+2)+1.5)*xoffset),img.height//2+rectsizehalf[1]),img.width//2-rectsizehalf[0]-(3*rectsizehalf[0])//2,img.height//2+(x-((len(lab)-1)//2))*unitsizehalf,lab[x],color[x%len(color)],keysubtopic=True if len(subtopic)+x in keysubtopicindex else False,multiplesubtopic=len(keysubtopicindex)>1)

# img=img.crop(((img.width-dimension[0])//2,0,img.width,img.height+unitsizehalf//4-unitsizehalf*(max(len(subtopic),len(lab))%2+1))) if [x for x in range(len(subtopic)) if x in keysubtopicindex] and not [x for x in range(len(subtopic),len(subtopic+lab)) if x in keysubtopicindex] else img.crop((0,0,(img.width+dimension[0])//2,img.height+unitsizehalf//4-unitsizehalf*(max(len(subtopic),len(lab))%2+1))) if [x for x in range(len(subtopic),len(subtopic+lab)) if x in keysubtopicindex] and not [x for x in range(len(subtopic)) if x in keysubtopicindex] else img.crop(((img.width-dimension[0])//2,0,(img.width+dimension[0])//2,img.height+unitsizehalf//4-unitsizehalf*(max(len(subtopic),len(lab))%2+1)))
 '''
 if [x for x in range(len(subtopic)) if x in keysubtopicindex] and not [x for x in range(len(subtopic),len(subtopic+lab)) if x in keysubtopicindex]:
  img=img.crop((img.width-dimension[0])//2,0,img.width,img.height+unitsizehalf//4-unitsizehalf*(max(len(subtopic),len(lab))%2+1))
 elif [x for x in range(len(subtopic),len(subtopic+lab)) if x in keysubtopicindex] and not [x for x in range(len(subtopic)) if x in keysubtopicindex]:
  img=(0,0,(img.width+dimension[0])//2,img.height+unitsizehalf//4-unitsizehalf*(max(len(subtopic),len(lab))%2+1))
 '''
# if resizewidth:
 print(f"resizing... {img.size=} '{int(resizewidth)}x...'")
 img=img.resize((int(resizewidth),int(img.height*int(resizewidth)/img.width)))
 print(f'saving...{outimagename=} {img.size=}')
 img.save(outimagename)
if __name__=='__main__':
 if len(sys.argv)<=2:
  print(f'''----- usage -----
python3 {sys.argv[0]} 'topic' 'subtopic1' 'subtopic2' ... '><' 'lab1' 'lab2' ... [<combined>] [--resize <width=320>]
python3 subtopicgraph.py 'Context Menu\\nin Kivy' 'Introduction' 'Issues with\\ncurrent implementation' '><' 'Exercise0' 'Exercise1' <0,3> --resize [350]
python3 subtopicgraph.py 'Context Menu\\nin Kivy' 'Introduction' 'Issues with\\ncurrent implementation' '><' 'Exercise0' 'Exercise1' <> --resize [350]''')
  sys.exit(-1)
 count=None
 specialtopics=Utilc.getarg(r'^<.*?>$',0)
 specialtopics=tuple([count for count in range(len([x for x in sys.argv[2:] if not x=='><']))] if specialtopics=='<>' else [int(x) for x in re.split(r'[<>, \t]+',specialtopics) if x]) if specialtopics else specialtopics
 resizewidth=Utilc.getarg(r'--resize',2) or (350 if not specialtopics else 800)
 '''
 if [x for x in sys.argv if re.search(r'--resize',x)]:
  count=[count for count,x in enumerate(sys.argv) if re.search(r'--resize',x)][0]
  if len(sys.argv)>(count+1) and re.search(r'^\d+$',sys.argv[count+1]):
   resizewidth=int(sys.argv[count+1])
   sys.argv[count:count+2]=[]
  else:
   resizewidth=350
   sys.argv[count:count+1]=[]
 '''
 print(f'TEST {specialtopics=} {sys.argv=} {resizewidth=}')
 sys.argv[1:]=[re.sub(r'\\n','\n',x) for x in sys.argv[1:]]
# if not [x for x in sys.argv[2:] if re.search('^\s*<.*?>\s*$',x)]:
 if not specialtopics:
  for i in range(len([x for x in sys.argv[2:] if not re.search(r'^\s*><\s*$',x)])):
   getimage(sys.argv[1],sys.argv[2:],(i,),re.sub(r'\s+','_',sys.argv[1])+'_'+str(i)+'.png')
 else:
  getimage(sys.argv[1],sys.argv[2:],specialtopics,re.sub(r'\s+','_',sys.argv[1])+'.png')
