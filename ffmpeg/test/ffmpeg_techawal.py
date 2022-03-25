from decimal import Decimal
import os,datetime,random,re,sys
sys.path.append('/home/minhinc/tmp')
from MISC.ffmpeg.gifm import gifc;from MISC.ffmpeg.utilm import utilc;from MISC.ffmpeg.libm import libc
#inputfile=sys.argv[1]
#title=sys.argv[2]
if len(sys.argv)<=1:
 print('usage ---\npython3 ffmpeg test.py "<title>" "=<videoneedsscaling.mp4>" "<duraton" "<without_=_firstreferencevideo.mp4>" "<duration>" ....')
 print('python3 ffmpeg_test.py "Syntax Highlighting Pyside6 QML Chain-Of-Responsibility" "=VID_20210910_180110.mp4" "00:00:51-00:07:37" syntax.mp4 "00:00:00-00:27:05,00:28:05-00:57:30,00:57:43-01:00:34" syntax2.mp4 "00:00:00-00:21:18,00:21:40-00:22:08,00:22:38-00:24:27"')
 sys.exit(-1)
title=sys.argv[1]
outputfile=re.sub(r'\s+','_',re.sub(r'[.]mp4','{0:%Y-%m-%d}'.format(datetime.datetime.now())+'.mp4',title+'.mp4',re.I))
print(f'ffmpeg_test.py {outputfile=}')

#g=gifc(inputfile=inputfile);u=utilc(inputfile=inputfile);l=libc(inputfile=inputfile)
g=gifc();u=utilc();l=libc()
#duration=float(l.getsecond(l.exiftool(l.adddestdir(inputfile),'Duration')))
videorange=[]
videoname=None
for i in sys.argv[2:]:
 print(f'{i=}')
 if re.search(r'^(\s*[\d:]+\s*[-]\s*[\d:]+\s*,?)+$',i):
  print('111111111111111111')
  videorange.append((videoname,i))
  videoname=None
 elif videoname:
  print('22222222222222222222')
  videorange.append((videoname,))
#  os.system('rm '+u.libi.adddestdir(re.sub(r'^=?(.*)[.]mp4$',r'\1'+'_*.mp4',i)))
  videoname=('=' if re.search(r'^=',i) else '')+u.replaceaudio(re.sub(r'^=','',i),re.sub(r'^=?(.*)?[.]mp4$',r'\1',i,flags=re.I)+'.mp3')
 else:
  print('33333333333333333')
#  os.system('rm '+u.libi.adddestdir(re.sub(r'^=?(.*)[.]mp4$',r'\1'+'_*.mp4',i)))
  videoname=('=' if re.search(r'^=',i) else '')+u.replaceaudio(re.sub(r'^=','',i),re.sub(r'^=?(.*)?[.]mp4$',r'\1',i,flags=re.I)+'.mp3')
else:
 if videoname:
  videorange.append((videoname,))
print(f'ffmpeg_test {videorange=}')
#os.system('rm '+u.libi.adddestdir(r'screenshot*.png'))
#for i in range(10):
# u.screenshot(re.sub(r'^=','',videorange[0][0]),i*4)
#g.replaceaudiobreakjoin(*(('=VID_20210919_115419_0.mp4','00:00:00-00:03:46'),('fileio_1.mp4',)))
g.replaceaudiobreakjoin(*videorange)
u.setvideo(g.dimension)
duration=g.duration
print(f'><test {duration=}')
numberoftick=min(int(duration/180)+(1 if (duration%180)>20 else 0),10)+1
tick=[None if i!=0 and i!=(numberoftick-1) else True for i in range(numberoftick)]

def co(c):
 '''
   -------
   |1|2|3|
   |4|5|6|
   |7|8|9|
   -------
 '''
 def wh(c=5,W=1,H=1):
  offsetx,offsety=0,0
  if len(str(c))>1:
   offsetx,offsety=wh(str(c)[1:],W/3,H/3)
  return (int(Decimal(int(str(c)[0])-1)%3)-1)*W/3+offsetx,(int(int(int(str(c)[0])-1)/3)-1)*H/3+offsety
 a,b=wh(c)
 return r'(W-w)/2'+('+' if a>=0 else '')+str(a)+r'*W,(H-h)/2'+('+' if b>=0 else '')+str(b)+r'*H'

#00:06:45/345 or (3,00:00:05/05,00:40:00/2400)
def getslotstamp(requestcount,begintime=None,endtime=duration):
 global duration,numberoftick,tick
 if begintime:
  begintime,endtime=l.getsecond(begintime),l.getsecond(endtime)
 requestcount=float(l.getsecond(requestcount))
 retarray=[]
# print(f'gettimestamp {requestcount=} {begintime=} {endtime=}')
 def adjust(timestamp):
  global duration
  tickcount=int((timestamp*(numberoftick-1))/duration) if (timestamp*(numberoftick-1))/duration==int((timestamp*(numberoftick-1))/duration) else int((timestamp*(numberoftick-1))/duration)
#  print(f'gettimestamp.adjust {timestamp=} {tickcount=} {tick=} {numberoftick=}')
  if tick[tickcount]:
   if (tickcount-1)!=0 and not tick[tickcount-1]:
    tick[tickcount-1]=True
    return ((tickcount-1)*duration)/(numberoftick-1)
   elif (tickcount+1)!=(numberoftick-1) and not tick[tickcount+1]:
    tick[tickcount+1]=True
    return ((tickcount+1)*duration)/(numberoftick-1)
   return None
  else:
   tick[tickcount]=True
   return (tickcount*duration)/(numberoftick-1)
 if begintime==None:
  return adjust(requestcount)
 for i in range(int(requestcount)):
  retarray.append(adjust(begintime+((endtime-begintime)*(i+1))/(requestcount+1)))
 print(f'<>getslotstamp {retarray=}')
 return retarray


def fixed(omnitime=6,endmargin=20,omniposition='(W-w)/2,(H-h)/2',logotext=False,tailaudio='mizmar.mp3'):
 omnitextgif=contactgif=None
 g.overlay((l.adddestdir('techlogotext_t.png')),position='W-w,h',begintime=2.0,duration=duration-2) #top right logo
 if logotext: # position 5 initial logo
  g.overlay(u.logotext(size=0.3,textdata=('Tech ','Awal','A Tech Research Firm'),textcolor=((255,85,0,255),(0,0,255,255),(200,200,200,255))),0)

 omnitextgif=u.omnitext(re.sub(r'\s',r'\\n',title),size=max(0.6,1.0-len(re.split(r'\s',title))*0.1),duration=6)
 g.overlay(omnitextgif,begintime=omnitime,position=omniposition) #omni text
 g.overlay((l.adddestdir('cork.mp3'),10.0),begintime=omnitime+1.0) # music sync with omni text
 for i in getslotstamp(min(int(duration/1800),2),begintime=0):
  if i:
   g.overlay(omnitextgif,begintime=i,position=omniposition) #omni text
   g.overlay((l.adddestdir('cork.mp3'),10.0),begintime=i+1.0) # music sync with omni text

 for count,i in enumerate(getslotstamp(min(int(duration/400),3),begintime=0)):
  if i:
#   g.overlay(l.adddestdir('contact.gif'),begintime=i,position=(re.sub(r'h\)/2',r'h)*2/3',re.sub(r'\(W-w\)/2',r'\(W-w\)',l.filter['overlay']['up'])),l.filter['blend']['circleopen'])[count%2],duration=10)
#   g.overlay(l.adddestdir('contact.gif'),begintime=i,position=re.sub(r'h\)/2',r'h)*2/3',re.sub(r'\(W-w\)/2',r'\(W-w\)',l.filter['overlay']['up'])),duration=10)
   g.overlay(u.image2gif(l.adddestdir('contact.gif'),filtermode=re.sub(r'T/\d+',r'T/24',l.filter['blend']['circleopen']),duration=10),begintime=i,position='(W-w),(H-h)/2',duration=12)
   g.overlay(l.adddestdir('cracker.gif'),begintime=i,position='(W-w-w/10),(H-h)/2')
   #g.overlay((l.adddestdir('ting.mp3'),00.2),begintime=i+0.44) # music sync with omni text
   g.overlay((l.adddestdir('cracker.mp3'),0.1),begintime=i) # music sync with omni text

 g.overlay(u.text2image(r'ThankYou::w:shade6\n::::40\nvisit:0.2:\nyoutube.com/c/minhinc:0.7:gi:shade10',margin=20,backcolor=(0,0,0,28)),begintime=duration-endmargin,position=re.sub(r't/\d',r't/4',l.filter['overlay']['up']),duration=10) #end tail presentation
 g.overlay(u.text2image(r'Training Contacts:0.5:white\nWhatsApp +91 9483160610:0.7:gi:shade12',margin=20,backcolor=(0,0,0,28)),begintime=duration-endmargin+10,position=re.sub(r't/\d',r't/4',l.filter['overlay']['up']),duration=endmargin-10) #end tail presentation
 g.overlay((l.adddestdir(tailaudio),1.0),begintime=duration-endmargin,duration=endmargin) # music sync with omni text
 

def bannertext(*bannertime):
 """textdata - <time>,<position>,<backgroundcolor>,<text>
   textdata - '00:03:00','(W-w)/2',(255,255,255,255),'hello world'
   textdata - '00:03:00','co(5)',(255,255,255,255),'hello world'"""
 backcolor=None
 for count,t in enumerate(list(zip(*bannertime))[0]):
  backcolor=bannertime[count][2] if len(bannertime[count])>2 and bannertime[count][2] else (255,255,255,128)
  text=bannertime[count][3] if len(bannertime[count])>3 and bannertime[count][3] else title
  print(f'bannertext {bannertime[count]=} {count=} {text=} {type(text)=}')
  g.overlay(u.image2gif(u.image2gif(u.text2image(text,textcolor=(255,16,81,255),size=0.6),(l.filter['blend']['left'],l.filter['blend']['right'])[count%2],duration=6),l.filter['overlay']['normal'],backcolor=backcolor),begintime=t,position=list(zip(*bannertime))[1][count])

def textblackonwhite(text,time,position,size=0.6,duration=6):
  g.overlay(u.image2gif(u.text2image(text,textcolor=(0,0,0,255),size=size),l.filter['overlay']['up'],duration=duration,backcolor=(255,255,255,128)),begintime=time,position=position)
def textwhiteonblack(text,time,position,size=0.6,duration=6):
  g.overlay(u.image2gif(u.text2image(text,textcolor=(255,255,255,255),size=size),l.filter['overlay']['up'],duration=duration,backcolor=(0,0,0,128)),begintime=time,position=position)

fixed(logotext=True,omniposition=co(56),tailaudio='guitar_1.mp3',endmargin=60)
bannerlist=[]
for count,i in enumerate(getslotstamp(int(duration/180),begintime=0)):
 if i:
  bannerlist.append((i,(co(85),co(25))[count%2],(255,255,255,192),title))
print(f'{bannerlist=}')
bannertext(*bannerlist)

#bannertext(('00:08:00',co(82)),('00:11:52',co(282),'','Conventional Queue based BFS'),('00:13:29',co(282),'','Stack based BFS'),('00:15:57',co(6),'','Program'))
#textblackonwhite(r'http\://www.minhinc.com','00:01:05',co(28))
#g.overlay(l.adddestdir('queuebasedbfs_s.gif'),begintime='00:01:11',duration=20,position=co(56))#
#g.overlay(u.image2gif('queuebasedbfs_ss.gif','blend','fadein',duration=120),begintime='00:02:11',position=co(37))#
g.stroke(outputfile)# final mp4 creation 
for i in videorange:
 print('deleting i[0]',i[0])
 os.system('rm '+u.libi.adddestdir(re.sub(r'^=?(.*)_\d+[.]mp4$',r'\1'+'_*.mp4',i[0])))
print(f'###################\n##############\n######  {outputfile=}  ########\n################\n##############')
