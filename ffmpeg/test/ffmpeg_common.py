import os,datetime,random,re,sys
sys.path.append(os.path.expanduser('~')+r'/tmp')
from MISC.ffmpeg.gifm import gifc
from MISC.ffmpeg.test.ffmpeg_advertisement import focusin,focusout,advertise

class ffmpeg_common:
 def __init__(self):
  if len(sys.argv)<=1 or not [x for x in sys.argv if re.search(r'--profile',x)]:
   if not [x for x in sys.argv if re.search(r'--profile',x)]:
    print(f'---------- --profile missing -----------')
   print('''\
--- usage ---
-all arguments in tuple format-
Arguments in 2 categories
(1)Videos to be concatenated. Tuple len=2. (Video,[audio,volume])(t1_begin-t1_end,t2_begin...)/((i1.png,i2.png..),audio,[volume]),(filter,t_begin-t_end)
 filters - 'gif' -> images to gif, 'gif01' -> images to gif and gif to mov with filter='01' (on intermediate gif)
            more on utilc.image2gif doc
(2)Annotations(visual+audio) over video. Tuple len=3. ((files..),(audio,volume)),(filter,position),(t1_begin-t1_end,t2_begin-t2_end..)
   filter - stroke()-20, image2gif()->stroke()-21, text2image()->image2gif()->stroke()-22
python3 ffmpeg_common.py --profile <minh|tech|miss> [--offset <number>] "<title>" "(=<referencevideo.mp4>,(<timestamp1,timestamp2>)" "(<nonreferencevideo.mp4>,audio.mp3,0.8)>,(<timestamp1,timestamp2>))" "((panzoomimage.png,panzoomimage2.png),audio.mp3),(<filtername>,<duration>)" .... "<[gif|.mp4|.mov|.png|text]:<audio>:<volume> <filter:position>,(<timestamp1,timestamp2>)" ....
python3 ffmpeg_common.py --profile minh --offset 10 "Syntax Highlighting Pyside6 QML Chain-Of-Responsibility" "=VID_20210910_180110.mp4,00:00:51-00:07:37" "(syntax.mp4,audio.mp3,0.8),(00:00:00-00:27:05,00:28:05-00:57:30)" syntax2.mp4 "((bluegermanypanzoom.png,red.png,pink.png),t10.mp3),(40,0-20)" "xyz.gif,(21,5),(00:20:00,00:30:00)" "(logo.png,ting.mp3,0.1),(20,5),00:04:00-00:04:30" "(Have a cup of Coffee...,cork.mp3,10),(22,52),00:31:47-00:34:20"\
''')
   sys.exit(-1)
  self.offset=0
  self.omni=False
  if [x for x in sys.argv if re.search(r'--offset',x)]:
   self.offset=int(sys.argv[sys.argv.index(r'--offset')+1])
   sys.argv[sys.argv.index(r'--offset'):sys.argv.index(r'--offset')+2]=''
  if [x for x in sys.argv if re.search(r'--omni',x)]:
   self.omni=True
   sys.argv[sys.argv.index(r'--omni'):sys.argv.index(r'--omni')+1]=''
  self.profile=sys.argv[sys.argv.index(r'--profile')+1]
  sys.argv[sys.argv.index(r'--profile'):sys.argv.index(r'--profile')+2]=''
  self.title=sys.argv[1]
  self.g=gifc()
  self.stroketuple=[]
  [self.g.libi.prune2(x,setvideo=True,stroketuple=self.stroketuple) for x in sys.argv[2:]]
  self.g.libi.setduration(sum(float(self.g.libi.getsecond(x[1])) if not x[1]==None else float(self.g.libi.exiftool(x[0][0],'Duration')) for x in self.stroketuple if len(x)==2))
  if self.omni:
   advertise(self)
  self.g.libi.setduration(sum(float(self.g.libi.getsecond(x[1])) if not x[1]==None else float(self.g.libi.exiftool(x[0][0],'Duration')) for x in self.stroketuple if len(x)==2))
  #settle three tuple overlappings
  duration=durationt=0
  stroketuplet=[]
  for count,x in enumerate(self.stroketuple):
   if len(x)==2:
    if len(self.stroketuple[count and count-1 or 0])==3 or self.stroketuple[count][0][0]!=self.stroketuple[count and count-1 or 0][0][0]:
     print(f' --- resetting duration {duration=} {durationt=}')
     duration+=durationt
     durationt=0
    durationt+=float(self.g.libi.getsecond(x[1])) if not x[1]==None else float(self.g.libi.exiftool(x[0][0],'Duration'))
   elif len(x)==3 and [y for y in self.stroketuple[count+1:] if len(y)==2]:
    print(f'{x=}')
    stroketuplet=list(self.stroketuple[count])
    stroketuplet[2]=re.sub(r'(?P<id>([\d+.:]+))',lambda m:str(float(self.g.libi.getsecond(m.group('id')))+duration),x[2])
    self.stroketuple[count]=tuple(stroketuplet)
    print(f'{x[2]=} {duration=} {stroketuplet=} {self.stroketuple=}')
  print(f'<>ffmpeg_common.__init__ sys.argv={sys.argv} {self.profile=} offset={self.offset} title={self.title} duration={self.g.libi.duration} stroketuple={self.stroketuple}')

 def prepareannotationfile(self):
  duration=0
  afpstr='['
  for i in [i for i in self.stroketuple if len(i)==2]:
   print(f'<=>ffmpeg_common.prepareannotationfile i={i}')
   afpstr+='\n{"source":"'+self.g.utili.image2gif(i[0][0],filtername='gif',duration=i[1])+'","timestamp":"'+str(duration)+r'"},'
   duration+= i[1]!=None and float(self.g.libi.getsecond(i[1])) or float(self.g.libi.exiftool(i[0][0],'Duration'))
  with open('annotation.jsa','w') as afp:
   afp.write(re.sub(r',$','',afpstr,flags=re.DOTALL)+'\n]\n')

 def fixed(self):
  print(f'><ffmpeg_common.fixed {self.stroketuple=}')
  tempduration=None
  tduration=0
  focusout(self)
  focusin(self)
  self.g.libi.prune2((os.path.expanduser('~')+r'/tmp/imageglobe/resource/'+('minhinctoprightlogo.png' if re.search(r'^minh',self.profile,flags=re.I) else 'techawaltoprightlogo.png' if re.search(r'^tech',self.profile,flags=re.I) else 'missmandovitoprightlogo.png'))+',(20,W-w\,h),'+str(self.offset+2)+'-'+str(self.g.libi.duration-2),stroketuple=self.stroketuple)
  if self.omni:
   #omni
#   self.g.libi.prune2(self.g.utili.omnitext(re.sub(r'\s',r'\\n',self.title),size=max(0.6,1.0-len(re.split(r'\s',self.title))*0.1),duration=6)+',(20,'+str(566)+'),('+','.join(str(x) for x in ([6+self.offset] if self.g.libi.duration>300 else [])+tempduration if x)+')',stroketuple=self.stroketuple)
   self.g.libi.prune2(self.g.utili.omnitext(re.sub(r'\s',r'\\n',self.title),size=max(0.6,1.0-len(re.split(r'\s',self.title))*0.1),duration=6)+',(20,'+str(566)+'),'+str(6+self.offset),stroketuple=self.stroketuple) if self.g.libi.duration>300 else None
#   self.g.libi.prune2(os.path.expanduser('~')+r'/tmp/imageglobe/resource/'+'cork.mp3'+',None,('+','.join(str(x+1.0) for x in ([6+self.offset] if self.g.libi.duration>300 else [])+tempduration if x)+')',stroketuple=self.stroketuple)
   self.g.libi.prune2(os.path.expanduser('~')+r'/tmp/imageglobe/resource/'+'cork.mp3'+',None,'+str(1+6+self.offset),stroketuple=self.stroketuple) if self.g.libi.duration>300 else None
   #cracker
#   tempduration=self.g.libi.getslotstamp(min(int(self.g.libi.duration/400),3),begintime=self.offset)
   tempduration=self.g.libi.getslotstamp('cracker',int(self.g.libi.duration/400),3)
   self.g.libi.prune2(self.g.utili.image2gif(os.path.expanduser('~')+r'/tmp/imageglobe/resource/'+'contact.gif',filtername=re.sub(r'T/\d+',r'T/24',self.g.libi.filter['09']),duration=10)+'(20,\(W-1.05*w\)\,h*1.5),('+','.join(str(x)+'-'+str(x+12) for x in tempduration)+')',stroketuple=self.stroketuple)
   self.g.libi.prune2("("+os.path.expanduser('~')+r'/tmp/imageglobe/resource/'+"cracker.gif,"+os.path.expanduser('~')+r'/tmp/imageglobe/resource/'+"cracker.mp3,0.1),(20,\(W-w*1.16\)\,h*0.39),("+','.join(str(x) for x in tempduration if x)+')',stroketuple=self.stroketuple)
 
   #title
#   self.g.libi.prune2(self.title+',(22,8),('+','.join(str(x)+'-'+str(x+8) for x in self.g.libi.getslotstamp(int(self.g.libi.duration/180),begintime=0) if x)+')',stroketuple=self.stroketuple)
   self.g.libi.prune2(self.title+',(22,8),('+','.join(str(x)+'-'+str(x+8) for x in self.g.libi.getslotstamp('title',int(self.g.libi.duration/180)) if x)+')',stroketuple=self.stroketuple)


fc=ffmpeg_common()
fc.prepareannotationfile()
fc.fixed()
print(f'######stroke tuple##### stroketuple={fc.stroketuple}')
outputfile=re.sub(r'\s+','_',re.sub(r'[.]mp4','{0:%Y-%m-%d}'.format(datetime.datetime.now())+'.mp4',fc.title+'_'+re.sub(r'.*/?(.*)[.]py$',r'\1',sys.argv[0])+'_'+fc.profile+'_'+'.mp4',re.I))
fc.g.stroke2(*fc.stroketuple,outputfile=outputfile)# final mp4 creation 
print(f'###################\n##############\n######  outputfile={outputfile}  ########\n################\n##############')
