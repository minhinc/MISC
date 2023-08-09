import os,datetime,random,re,sys
sys.path.append(os.path.expanduser('~')+r'/tmp')
from MISC.ffmpeg.gifm import gifc
from MISC.utillib.util import Util

class ffmpeg_common:
 def usage(self):
  print(f'''{"usage":-^40}
python3 ffmpeg_common.py --profile [minhinc|techawal|..] [--notail] [--title <title>] video1.mp4 '(video2.mp4,00:00:02-00:10:20)' '(=video3.mp4,(00:30:00-00:50:00,01:00:00-01:22:00,01:30:00-01:32:00))' '(audio.mp3,0.5,(01:30:00-01:30:00,01:30:50-01:31:00))' 'Hello World,(5,BUP,00t),00:45:00)' '(abc.gif,(55,OUP),00:44:00)' 'video4_1600x900.mp4,00:20:30-00:30:00' 'example_00:02:10-00:11:40.mp4,(45,oup,60s),00:23:00-00:32:30)' 'toprightlogo.png,362,00:00:02'
basevideo - singlefile or tuple(filename,duration) or tuple(filename,tuple(durations))
 filename - '=<filename>.mp4' referece file or '<filname>_1600x900.mp4' for non reference file particular dimension
overlapping - (audio,volume,timestamp) or (image,position,tuple(timestamps)) or (image,(position,type1,type2),timestamp)
 image - abc.mp4 or abc_00:00:02-00:00:40_00:01:23-00:02:32.mp4 or abc_00:01:54.mp4
         abc.gif or abc.png or (one.png,two.png,three.png)
 type - 
  bfadeinout,00t or bfadeinout,oup,00t,01t,02t    ->   text
  bfadeinout,50s,0.8a or bup100%50%,0.4a or bfadeinout,bup50%100%,50s,0.8a   ->   video or image''')
  sys.exit(-1)
 def __init__(self):
  if len(sys.argv)<=1 or not [x for x in sys.argv if re.search(r'--profile',x)]:
   self.usage()
  self.g=gifc()
  if [x for x in sys.argv if re.search(r'^=',x)]:
   self.g.libi.setvideo(self.g.libi.str2tuple([re.sub(r'^=','',x) for x in sys.argv if re.search('^=',x)][0])[0])
#   print(f'{"VIDEO DIMENSTION SET":-^60}\n{(self.g.libi.videowidth,self.g.libi.videoheight):^60}\n{"":-^60}')
   print(f'{"VIDEO DIMENSTION SET":-^60}\n{self.g.libi.videowidth:^60}\n{"":-^60}')
  else:
   print(f'{"":-^60}\n{"NO VIDEO DIMENSION SET":^60}\n{"":-^60}')
   self.usage()
  self.profile=Util.getarg('--profile',count=2)
  self.notail=Util.getarg('--notail')
  self.title=Util.getarg('--title',2) or ''
  self.nospellcheck=Util.getarg('--nospellcheck')
  for x in [x for x in re.split(r'\s+',self.title) if x and not self.nospellcheck]:
   if os.system('egrep -i -e "^'+x+'$" /usr/share/dict/british-english'):
    print(f'SPELLING MISTAKE IN TITLE {x=} use --nospellcheck')
    self.usage()
  duration=tduration=t2duration=0
  tdurationlist=[]
  if not self.notail:
   sys.argv.extend(['/home/minhinc/tmp/imageglobe/resource/black_'+str(self.g.libi.videowidth)+'_'+str(self.g.libi.videoheight)+'.mp4,00:00:00-00:01:00',self.profile.title()+'\\nPresentation\\nYouTube.com/@minhinc,(5,oup_4s60%100%,02_5t,03_5t,01_5t),00:00:00-00:00:10','Tech Awal,(166,oright,04t_l25),00:00:19-00:01:00','youtube.com/@techawal,(344,oleft,04t_l25),00:00:19-00:01:00','Minh Inc,(199,oright,04t_l25),00:00:19-00:01:00','youtube.com/@minhinc,(377,oleft,04t_l25),00:00:19-00:01:00','Miss Mandovi,(733,oright,04t_l25),00:00:19-00:01:00','youtube.com/@missmandovi,(911,oleft,04t_l25),00:00:19-00:01:00','Mathematics Real,(766,oright,04t_l25),00:00:19-00:01:00','youtube.com/@mathematicsreal,(944,oleft,04t_l25),00:00:19-00:01:00','WhatsApp\\n+91 9483160610,(5,oup_4s50%100%,00_5t,01_5t),00:00:10-00:01:00','/home/minhinc/tmp/imageglobe/image/whatsapp_t.png,(652,oup_4s50%90%,10s),00:00:10-00:01:00','/home/minhinc/tmp/imageglobe/resource/tail.mp3,1,00:00:00-00:01:00'])
  self.profile=re.sub(r'\s+','',self.profile).lower()
  print(f'ffmpeg_common TEST {sys.argv=}')
  for count,i in enumerate(sys.argv[1:]):
   if len(self.g.libi.str2tuple(i))<=2:
    if self.g.libi.str2tuple(i)[0][0]=='=':
     sys.argv[count+1]=i=re.sub('=','',i,count=1)
#     self.g.libi.setvideo(self.g.libi.str2tuple(i)[0])
    tduration=t2duration
    tdurationlist=[]
    if len(self.g.libi.str2tuple(i))==1:
     tdurationlist=[[0,round(float(self.g.libi.exiftool(re.sub(r'_\d+x\d+([.]\w+)$',r'\1',i),'Duration')),3)]]
    else:
#     tdurationlist=[[float(self.g.libi.getsecond(y)) for y in re.split('-',x)] for x in (type(self.g.libi.str2tuple(i)[1])==tuple and self.g.libi.str2tuple(i)[1] or (self.g.libi.str2tuple(i)[1],))]
     tdurationlist=[[float(self.g.libi.getsecond(y)) for y in re.split('-',re.search('-',x) and x or x+'-'+self.g.libi.exiftool(re.sub(r'_\d+x\d+([.]\w+)$',r'\1',self.g.libi.str2tuple(i)[0]),'Duration'))] for x in (type(self.g.libi.str2tuple(i)[1])==tuple and self.g.libi.str2tuple(i)[1] or (self.g.libi.str2tuple(i)[1],))]
    t2duration=tduration+sum(x[1]-x[0] for x in tdurationlist)
   elif tdurationlist:
#    for j in re.findall(r'(\d+:\d+:\d+(?:[.]\d+)?|\b\d+\b(?!:))',re.sub('^.*?,(?:\(.*?\)|.*?),(.*)',r'\1',i)):
    print(f'TEST {tdurationlist=}')
    for j in re.findall(r'(\d+:\d+:\d+(?:[.]\d+)?|\b\d+\b(?!:))',re.sub(r'.*?,(?P<id>(?:\(((?!\().)*\)|((?!,).)*))$',lambda m:m.group('id'),i)):
     duration=tduration
     for k in tdurationlist:
      print(f'TEST {j=} {(tduration,t2duration,duration)=}')
      if k[0]<=float(self.g.libi.getsecond(j))<=k[1]:
       duration+=round(float(self.g.libi.getsecond(j))-k[0],3)
       break
      else:
       duration+=k[1]-k[0]
#     sys.argv[count+1]=re.sub(r'(.*?,(?:\(.*?\)|.*?),).*$',r'\1',sys.argv[count+1])+re.sub(j,str(duration),re.sub('^.*?,(?:\(.*?\)|.*?),(.*)',r'\1',sys.argv[count+1]))
     sys.argv[count+1]=re.sub(r'(?P<id>.*?,)(?:\(((?!\().)*\)|((?!,).)*)$',lambda m:m.group('id'),sys.argv[count+1])+re.sub(j,str(duration),re.sub(r'.*?,(?P<id>(?:\(((?!\().)*\)|((?!,).)*))$',lambda m:m.group('id'),sys.argv[count+1]))

  self.g.libi.setduration(t2duration)
#  self.stroketuple=[self.g.libi.str2tuple(len(self.g.libi.str2tuple(x))>=2 and not type(self.g.libi.str2tuple(x)[-1])==tuple and re.sub('(.*,)(.*)',r'\1'+'('+r'\2'+')',x) or x) for x in sys.argv[1:]]
  self.stroketuple=[self.g.libi.str2tuple(x) for x in sys.argv[1:]]
  if self.profile:
   print(f'TEST {self.stroketuple=}')
#   self.stroketuple[1:1]=(self.g.libi.str2tuple(os.path.expanduser('~')+'/tmp/imageglobe/resource/'+self.profile+'toprightlogo.png,326,'+(len(self.stroketuple[0])==1 and '00:00:00' or re.split('-',type(self.stroketuple[0][1])==tuple and self.stroketuple[0][1][0] or self.stroketuple[0][1])[0])),)
   self.stroketuple[1:1]=(self.g.libi.str2tuple(os.path.expanduser('~')+'/tmp/imageglobe/resource/'+self.profile+'toprightlogo.png,326,00:00:00'),)
  if self.title:
   self.stroketuple[1:1]=((self.g.utili.omnitext(re.sub(r'\s',r'\\n',self.title),size=min(0.6,1.0-len(re.split(r'\s',self.title))*0.1),duration=6),'5','6'),(os.path.expanduser('~')+r'/tmp/imageglobe/resource/cork.mp3','0.2','7'))
  print(f'TEST {sys.argv=} {self.stroketuple=}')
fc=ffmpeg_common()
outputfile=re.sub(r'\s+','_',re.sub(r'[.]mp4','{0:%Y-%m-%d}'.format(datetime.datetime.now())+'.mp4',fc.title+'_'+re.sub(r'.*/?(.*)[.]py$',r'\1',sys.argv[0])+'_'+fc.profile+'_'+'.mp4',re.I))
print(f'TEST {outputfile=}')
fc.g.stroke2(*fc.stroketuple,outputfile=outputfile)
print(f'{"":-^40}\n{outputfile:-^40}\n{"":-^40}')
