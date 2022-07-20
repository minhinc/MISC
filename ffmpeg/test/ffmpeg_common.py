import os,datetime,random,re,sys
sys.path.append(os.path.expanduser('~')+r'/tmp')
from MISC.ffmpeg.gifm import gifc
class ffmpeg_common:
 def __init__(self):
  if len(sys.argv)<=1 or not [x for x in sys.argv if re.search(r'--profile',x)]:
   if not [x for x in sys.argv if re.search(r'--profile',x)]:
    print(f'---------- --profile missing -----------')
   print('''\
--- usage ---
-all arguments in tuple format-
Arguments in 2 categories
(1)Videos to be concatenated. Tuple len=2. Video,(t1_begin-t1_end,t2_begin...)/((i1.png,i2.png..),audio),(filter,t_begin-t_end)
 filters - 'gif' -> images to gif, 'gif01' -> images to gif and gif to mov with filter='01'
(2)Annotations(visual+audio) over video. Tuple len=3. ((files..),(audio,volume)),(filter,position),(t1_begin-t1_end,t2_begin-t2_end..)
   filter - stroke()-20, image2gif()->stroke()-21, text2image()->image2gif()->stroke()-22
python3 ffmpeg_common.py --profile <minh|tech> [--offset <number>] "<title>" "(=<referencevideo.mp4>,(<timestamp1,timestamp2>)" "(<nonreferencevideo.mp4>,(<timestamp1,timestamp2>))" "((panzoomimage.png,panzoomimage2.png),audio.mp3),(<filtername>,<duration>)" .... "<[gif|.mp4|.mov|.png|text]:<audio>:<volume> <filter:position>,(<timestamp1,timestamp2>)" ....
python3 ffmpeg_common.py --profile minh --offset 10 "Syntax Highlighting Pyside6 QML Chain-Of-Responsibility" "=VID_20210910_180110.mp4,00:00:51-00:07:37" "syntax.mp4,(00:00:00-00:27:05,00:28:05-00:57:30)" syntax2.mp4 "((bluegermanypanzoom.pngred.png,pink.png),t10.mp3),(gif01,0-20>)" "xyz.gif,(21,5),(00:20:00,00:30:00)" "(logo.png,ting.mp3,0.1),(20,5),00:04:00-00:04:30" "(Have a cup of Coffee...,cork.mp3,10),(22,52),00:31:47-00:34:20"\
''')
   sys.exit(-1)
  self.offset=0
  if [x for x in sys.argv if re.search(r'--offset',x)]:
   self.offset=int(sys.argv[sys.argv.index(r'--offset')+1])
   sys.argv[sys.argv.index(r'--offset'):sys.argv.index(r'--offset')+2]=''
  if [x for x in sys.argv if re.search(r'--noomni',x)]:
   self.noomni=True
   sys.argv[sys.argv.index(r'--noomni'):sys.argv.index(r'--noomni')+1]=''
  self.profile=sys.argv[sys.argv.index(r'--profile')+1]
  sys.argv[sys.argv.index(r'--profile'):sys.argv.index(r'--profile')+2]=''
  self.title=sys.argv[1]
  self.g=gifc()
  self.stroketuple=[self.g.libi.str2tuple(x) for x in sys.argv[2:]]
  print(f'<=>ffmpeg_common.__init__ stroketuple={self.stroketuple}')
  self.g.libi.setduration(sum(float(self.g.libi.getsecond(re.split('-',y)[1]))-float(self.g.libi.getsecond(re.split('-',y)[0])) for x in self.stroketuple if len(x)==2 for y in ((x[1] if not type(x[0])==tuple else [x[1][1]]) if type(x[1])==tuple else [x[1]]))+sum(float(self.g.libi.exiftool(re.sub(r'^=','',x[0]),'Duration')) for x in self.stroketuple if len(x)==1))
  self.g.libi.setvideo([re.sub(r'^=','',x[0]) for x in self.stroketuple if len(x)<=2 and type(x[0])==str and re.search(r'^=',x[0])][0])
#  self.g.libi.setduration(self.stroketuple)
  print(f'sys.argv={sys.argv} offset={self.offset} title={self.title} duration={self.g.libi.duration} stroketuple={self.stroketuple}')

 def prepareannotationfile(self):
  duration=0
  afpstr='['
  for i in [i for i in self.stroketuple if len(i)<=2]:
   print(f'ffmpeg_common.prepareannotationfile i={i} len(i)={len(i)}')
   afpstr+='\n{"source":"'+(self.g.utili.image2gif(re.sub(r'^=','',i[0]),filtername='gif',duration=10) if type(i[0])==str and re.search(r'[.]mp4$',i[0],flags=re.I) else self.g.utili.image2gif(i[0][0],filtername='gif',duration=min(10,float(re.split(r'-',i[1][1])[1])-float(re.split(r'-',i[1][1])[0])) if type(i[0])==tuple and type(i[0][0])==tuple else 10))+'","timestamp":"'+str(duration)+r'"},'
   duration+= sum(float(self.g.libi.getsecond(re.split('-',y)[1]))-float(self.g.libi.getsecond(re.split('-',y)[0])) for y in ((i[1] if not type(i[0])==tuple else [i[1][1]]) if type(i[1])==tuple else [i[1]])) if len(i)==2 else float(self.g.libi.exiftool(re.sub(r'^=','',i[0]),'Duration'))
  with open('annotation.jsa','w') as afp:
   afp.write(re.sub(r',$','',afpstr,flags=re.DOTALL)+'\n]\n')

 def fixed(self):
  tempduration=None
  self.stroketuple.append(self.g.libi.str2tuple(('videologo_s.png' if re.search(r'^m',self.profile,flags=re.I) else 'techlogotext_t.png')+',(20,W-w\,h),'+str(self.offset+2)+'-'+str(self.g.libi.duration-2)))
  self.stroketuple.append(self.g.libi.str2tuple(self.g.utili.image2gif(self.g.utili.image2gif(None,'013_a',backcolor='0x004000ff',duration=1),'011_s',backcolor='0xffffffff',duration=1)+'(20,5),0-1'))
  self.stroketuple.append(self.g.libi.str2tuple('frontlogo_minhinc.png'+',(20,5),0-4'))
#  self.stroketuple.append(self.g.libi.str2tuple((self.g.utili.logotext(size=0.3) if re.search(r'^[Mm]',self.profile) else self.g.utili.logotext(size=0.3,textdata=('Tech ','Awal','A Tech Research Firm'),textcolor=((255,85,0,255),(0,0,255,255),(200,200,200,255))))+',(20,5),'+str(self.offset)))
#  self.stroketuple.append(self.g.libi.str2tuple(self.g.utili.scalepad('waterripple.mov',targetdimension=self.g.libi.dimension(self.stroketuple[-1][0]),upscale=True,padcolor='0x00000000')+r',(20,5),'+str(self.offset+0.2)+'-'+str(self.offset+float(self.g.libi.exiftool(self.stroketuple[-1][0],'Duration'))-0.2)))
  #omni
  if not hasattr(self,'noomni'):
   tempduration=self.g.libi.getslotstamp(min(int(self.g.libi.duration/1800),2),begintime=self.offset)
   self.stroketuple.append(self.g.libi.str2tuple(self.g.utili.omnitext(re.sub(r'\s',r'\\n',self.title),size=max(0.6,1.0-len(re.split(r'\s',self.title))*0.1),duration=6)+',(20,'+str(566)+'),('+','.join(str(x) for x in ([6+self.offset] if self.g.libi.duration>300 else [])+tempduration if x)+')'))
   self.stroketuple.append(self.g.libi.str2tuple('cork.mp3'+',None,('+','.join(str(x+1.0) for x in ([6+self.offset] if self.g.libi.duration>300 else [])+tempduration if x)+')'))

   #cracker
   tempduration=self.g.libi.getslotstamp(min(int(self.g.libi.duration/400),3),begintime=self.offset)
   self.stroketuple.append(self.g.libi.str2tuple(self.g.utili.image2gif('contact.gif',filtername=re.sub(r'T/\d+',r'T/24',self.g.libi.filter['09']),duration=10)+'(20,\(W-w\)/2\,\(H-h\)/2),('+','.join(str(x)+'-'+str(x+12) for x in tempduration)+')'))
   self.stroketuple.append(self.g.libi.str2tuple("(cracker.gif,cracker.mp3,0.1),(20,\(W-w-w/10\)/2\,\(H-h\)/2),("+','.join(str(x) for x in tempduration if x)+')'))
 
  #title
  self.stroketuple.append(self.g.libi.str2tuple(self.title+',(22_f,822),('+','.join(str(x)+'-'+str(x+10) for x in self.g.libi.getslotstamp(int(self.g.libi.duration/180),begintime=0) if x)+')'))


 def prune(self):
  tmp=None
  self.stroketuple=[x for x in self.stroketuple if x[-1] or x[-1]==0]
  print(f'ffmpeg_common.prune self.stroketuple={self.stroketuple}')
  for x in self.stroketuple[:]:
   if len(x)>2 and type(x[-1])==tuple:
    self.stroketuple[self.stroketuple.index(x):self.stroketuple.index(x)+1]=[tuple(list(x[:-1])+[y]) for y in x[-1]]
  for count,x in enumerate(self.stroketuple[:]):
   if len(x)>2 and type(x[1])==tuple:
    tmp=list(x[1])
    if type(x[0])==tuple:
     if re.search('-',x[-1]):
      tmp[0]=re.sub(r'^(.*?)(_.*)$',r'\1'+'3'+r'\2',x[1][0]) if re.search(r'_',x[1][0]) else x[1][0]+'3'
     else:
      tmp[0]=re.sub(r'^(.*?)(_.*)$',r'\1'+'2'+r'\2',x[1][0]) if re.search(r'_',x[1][0]) else x[1][0]+'2'
    else:
     if re.search('-',x[-1]):
      tmp[0]=re.sub(r'^(?P<id>.*?)(?P<id2>_.*)$',lambda m:m.group('id')+'1'+m.group('id2'),x[1][0]) if re.search(r'_',x[1][0]) else x[1][0]+'1'
     else:
      tmp[0]=re.sub(r'^(.*?)(_.*)$',r'\1'+'0'+r'\2',x[1][0]) if re.search(r'_',x[1][0]) else x[1][0]+'0'
    x=list(x)
    x[1]=tuple(tmp)
    self.stroketuple[count]=tuple(x)
fc=ffmpeg_common()
fc.prepareannotationfile()
fc.fixed()
fc.prune()
print(f'######stroke tuple##### stroketuple={fc.stroketuple}')
outputfile=re.sub(r'\s+','_',re.sub(r'[.]mp4','{0:%Y-%m-%d}'.format(datetime.datetime.now())+'.mp4',fc.title+'_'+re.sub(r'(.*)[.]py$',r'\1',sys.argv[0])+'_'+fc.profile+'_'+'.mp4',re.I))
#fc.g.stroke2(*[x for x in fc.stroketuple if x[-1] or x[-1]==0],outputfile=outputfile)# final mp4 creation 
fc.g.stroke2(*fc.stroketuple,outputfile=outputfile)# final mp4 creation 
#fc.g.libi.system('python3 ffmpeg_screenshot.py '+fc.g.libi.adddestdir(outputfile)+' ><'+str(fc.offset))
print(f'###################\n##############\n######  outputfile={outputfile}  ########\n################\n##############')
