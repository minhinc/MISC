import os
import math
from PIL import Image,ImageDraw,ImageFont
import re
import shlex
import subprocess
class libc:
 '''library class to provide basic functions'''
 counti=-1
 def __init__(self,debug=False,inputfile=None,destdir='logdir'):
  self.filter={
   'blend':{'blend':"blend=all_expr='A*(1-min(T/1,1))+B*(min(T/1,1))'",
     'up': "blend=all_expr='if(lte(Y,(H-T/1*H)),A,B)'", #Curtain up \
     'right':"blend=all_expr='if(gte(X,(T/1*W)),A,B)'", #Curtain right \
     'down':"blend=all_expr='if(gte(Y,(T/1*H)),A,B)'", #curtain down \
     'left':"blend=all_expr='if(lte(X,(W-T/1*W)),A,B)'", #curtain left \
     'verticalopen':"blend=all_expr='if(between(X,(W/2-T/1*W/2),(W/2+T/1*W/2)),B,A)'",
     'horizontalclose':"blend=all_expr='if(between(Y,(H/2-T/1*H/2),(H/2+T/1*H/2)),B,A)'",
     'verticalclose':"",
     'horizontalclose':"",
     'circleopen':"blend=all_expr='if(gte(sqrt((X-W/2)*(X-W/2)+(H/2-Y)*(H/2-Y)),(T/2*max(W,H))),A,B)'",
     'circleclose':"blend=all_expr='if(lte(sqrt((X-W/2)*(X-W/2)+(H/2-Y)*(H/2-Y)),(max(W,H)-(T/1*max(W,H)))),A,B)'",
     'expandingwindow':"blend=all_expr='if(between(X,(W/2-T/1*W/2),(W/2+T/1*W/2))*between(Y,(H/2-T/1*H/2),(H/2+T/1*H/2)),B,A)'",
     'fadein': "[1]fade=in:st=0:d=3:alpha=1"
   },
   'overlay':{ 'normal':"overlay=x='(W-w)/2':y='(H-h)/2'",
     'up' :"overlay=x='(W-w)/2':y='max((H-h)/2,H-t/1*H)'",
     'right' : "overlay=x='min((W-w)/2,-w+t/1*W)':y='(H-h)/2'",
     'bottom': "overlay=x='(W-w)/2':y='min((H-h)/2,-h+t/1*H)'",
     'left' : "overlay=x='max((W-w)/2,W-t/1*W)':y='(H-h)/2'"
   }
  }
  self.debugf=debug
  if not os.path.isdir(destdir):
   os.mkdir(destdir)
  self.destdir=destdir
#  self.inputfile=self.adddestdir(inputfile) if inputfile else None
#  self.videowidth,self.videoheight=[int(x) for x in os.popen('ffmpeg -i '+self.inputfile+' 2>&1|grep -oP \'Stream .*, \K[0-9]+x[0-9]+\'').read().split('x')] if self.inputfile else None,None
  self.videowidth=self.videoheight=0
  if inputfile:
   self.setvideo(inputfile)
  self.palettecolor={
   'red':(255,0,0,255),
   'blue':(0,0,255,255),
   'green':(0,255,0,255),
   'gi':(0,64,0,255),
   'white':(255,255,255,255),
   'black':(0,0,0,255),
   'transparent':(0,0,0,0),
   'shade1':(0,0,0,32), 'shade2':(0,0,0,64), 'shade3':(0,0,0,96), 'shade4':(0,0,0,128), 'shade5':(0,0,0,160), 'shade6':(0,0,0,192), 'shade7':(0,0,0,224),
   'shade8':(255,255,255,32), 'shade9':(255,255,255,64), 'shade10':(255,255,255,96), 'shade11':(255,255,255,128), 'shade12':(255,255,255,160), 'shade13':(255,255,255,192), 'shade14':(255,255,255,224)
  }
  print(f'<>libc::_init__ {self.videowidth=} {self.videoheight=}')

# def setvideo(self,inputfile,dimension=None):
 def setvideo(self,inputfile):
  print(f'><libc.setvideo {inputfile=}')
  if re.search(r'^\s*[\d]+\s*[-:x,]\s*[\d]+\s*$',inputfile):
   self.videowidth,self.videoheight=[int(x) for x in re.split('[-:,x]',inputfile)]
  else:
#   self.inputfile=self.adddestdir(inputfile) if inputfile else None
   self.videowidth,self.videoheight=([int(x) for x in os.popen('ffmpeg -i '+inputfile+' 2>&1|grep -oP \'Stream .*, \K[0-9]+x[0-9]+\'').read().split('x')]) if self.inputfile else (None,None)
  print(f'<>libc.setvideo {self.videowidth=} {self.videoheight=}')

 def videoattribute(self,videofile_p):
  print("videofile_p {}".format(videofile_p))
#  videowidth,videoheight=[int(x) for x in os.popen('ffmpeg -i input.mp4 2>&1|grep -oP \'Stream .*, \K[0-9]+x[0-9]+\'').read().split('x')]
#  videodata=os.popen('ffmpeg -i '+videofile_p+' 2>&1').read()
  videodata=os.popen('ffprobe -i '+videofile_p+' 2>&1').read()
#  videowidth,videoheight=re.findall(r'\d+',os.popen('ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of default=nw=1'+inputfile).read(),re.I)
#  fps=re.split(r'/',ffprobe -v error -select_streams v -of default=noprint_wrappers=1:nokey=1 -show_entries stream=r_frame_rate'+inputfile)[0]
  videowidth,videoheight=re.sub(r'.*,\s*?(\d+x\d+)\s*.*',r'\1',videodata,flags=re.I|re.DOTALL).split('x')
  fps=re.sub(r'.*?(\d+)\s*fps\s*,.*',r'\1',videodata,flags=re.I|re.DOTALL)
  samplerate=re.sub(r'.*?(\d+)\s*Hz\s*,.*',r'\1',videodata,flags=re.I|re.DOTALL)
  channel=re.sub(r'.*\d+\s*Hz\s*,\s*([^ ]*)\s*,.*',r'\1',videodata,flags=re.I|re.DOTALL)
  self.debug("libc::videoattribute><",videofile_p,(videowidth,videoheight),fps,samplerate,channel)
  return ((videowidth,videoheight),fps,samplerate,channel)

 def split(self,string_p,default_p=None,delim_p=':'):
  self.debug("libc::split><",string_p,delim_p)
  DBL_ESC="!double escape!"
  if default_p:
   arglist=list(default_p)
   for (count,x) in enumerate(re.split(r'(?<!\\):',string_p.replace(r'\\',DBL_ESC))):
    if x:
#     arglist[count]=x.replace(DBL_ESC,'\\')
     if arglist[count]!=None: 
      arglist[count]=type(arglist[count])(x.replace('\\:',':').replace(DBL_ESC,'\\'))
     else:
      arglist[count]=x.replace('\\:',':').replace(DBL_ESC,'\\')
   return arglist
  return [x.replace('\\:',':').replace(DBL_ESC,'\\') for x in re.split(r'(?<!\\):',string_p.replace(r'\\',DBL_ESC))]

 def dimension(self,file_p):
  if re.search(r'[.]mp4$',file_p,flags=re.I):
#   return [int(x) for x in os.popen('ffmpeg -i "+self.inputfile+" 2>&1|grep -oP \'Stream .*, \K[0-9]+x[0-9]+\'').read().split('x')]
   retval= [str(int(x)) for x in os.popen('ffmpeg -i '+file_p+' 2>&1|grep -oP \'Stream .*, \K[0-9]+x[0-9]+\'').read().split('x')]
   print(f'libc.dimension {retval=} {file_p=}')
   return retval
  else:
   return Image.open(file_p).size

 def drawtextstroke(self,draw_p,x_p,y_p,text_p,textfont_p,textcolor_p,strokecolor_p='black',adj_p=2):
  strokelist=[(x_p-adj_p,y_p),(x_p+adj_p,y_p),(x_p,y_p-adj_p),(x_p,y_p+adj_p),(x_p-adj_p,y_p-adj_p),(x_p+adj_p,y_p-adj_p),(x_p-adj_p,y_p+adj_p),(x_p+adj_p,y_p+adj_p)]
  for i in range(len(strokelist)):
   draw_p.text((strokelist[i][0],strokelist[i][1]),text_p,font=textfont_p,fill=strokecolor_p)
  draw_p.text((x_p,y_p),text_p,font=textfont_p,fill=textcolor_p)

 def getfont(self,stringlist_p,screenratio_p=0.8,fontfamily_p='/home/minhinc/.fonts/ufonts.com_tw-cen-mt.ttf'):
  print(f'><libc.getfont {self.videowidth=} {self.videoheight=} {stringlist_p} {screenratio_p} {fontfamily_p}')
  self.debug("libc::getfont><",stringlist_p,screenratio_p)
  i=10
  maxindex=[len(j) for j in stringlist_p].index(max(len(j) for j in stringlist_p))
  #while (ImageFont.truetype(fontfamily_p,i).getsize('a')[0]*(max([len(j) for j in stringlist_p]) if max([len(j) for j in stringlist_p])>10 else 10))<(self.videowidth*screenratio_p): i=i+1
  while ImageFont.truetype(fontfamily_p,i).getsize(stringlist_p[maxindex])[0] < float(self.videowidth)*screenratio_p: i=i+1
  return ImageFont.truetype(fontfamily_p,i)
 
 def ffmpeg(self,commandstring_p):
  print('*****************')
  print(re.sub(r' -y ([^ ]+[.].*)$',r' -preset ultrafast -y \1',commandstring_p) if self.debugf else commandstring_p)
  print('*****************')
  if self.debugf:
   input("Press key to continue...")
#  os.system(re.sub(r' -y ([^ ]+[.].*)$',r' -preset ultrafast -y \1',commandstring_p) if self.debugf else commandstring_p)
  subprocess.call(shlex.split(re.sub(r' -y ([^ ]+[.].*)$',r' -preset ultrafast -y \1',commandstring_p) if self.debugf else commandstring_p))

 def getsecond(self,time_p,demark_p=False):
  '''demark is time non colon to colon format'''
#  print('libc::getsecond<> '+time_p)
  if type(time_p) == int or type(time_p) == float: time_p=str(time_p)
  if re.search(r':',time_p):
   return re.sub(r'(?P<id1>\d+):(?P<id2>\d+):(?P<id3>\d+)(?P<id4>.*)$',lambda m: str(int(m.group('id1'))*3600+int(m.group('id2'))*60+int(m.group('id3')))+m.group('id4'),time_p)
  elif demark_p:
   hour=int(float(time_p)/3600)
   minute=int((float(time_p)-hour*3600)/60)
   second=round(float(time_p)-hour*3600-minute*60,2)
   return str(hour)+":"+str(minute)+":"+str(second)
  return time_p

 def system(self,commandstring_p):
  print(f'libc.system {commandstring_p=}')
  if self.debugf:
   input("Press key to continue...")
#  os.system(commandstring_p)
  subprocess.call(shlex.split(commandstring_p))

 def stepvalue(self,initial_p,last_p,step_p=2):
  '''min step_p=2. that is 0 and 1. For step_p=1 initial_p would return'''
  stepsize=0
  if step_p>1:
   stepsize=(last_p-initial_p)/(step_p-1)
  for i in range(step_p):
   yield round(initial_p+i*stepsize,3)

 def getrectpoint(self,xy_p,rect_p,angle_p,offset_p=None):
  '''angle_p in degrees
  ----------------- <---- 1
  |^              |
  | \----- 0      | 
  |               |
  -----------------'''
  self.debug("libm::getrectpoint><",xy_p,rect_p,angle_p,offset_p)
  funclist=(lambda x:(xy_p[0]+(rect_p[1]-xy_p[1])/math.tan(x),rect_p[1]),lambda x:(rect_p[2],xy_p[1]+(rect_p[2]-xy_p[0])*math.tan(x)),lambda x:(xy_p[0]+(rect_p[3]-xy_p[1])/math.tan(x),rect_p[3]),lambda x:(rect_p[0],xy_p[1]+(rect_p[0]-xy_p[0])*math.tan(x)))
  anglelist=(math.pi+math.atan((xy_p[1]-rect_p[1])/(xy_p[0]-rect_p[0])),math.atan((xy_p[1]-rect_p[1])/(xy_p[0]-rect_p[2])),math.atan((xy_p[1]-rect_p[3])/(xy_p[0]-rect_p[2])),math.pi+math.atan((xy_p[1]-rect_p[3])/(xy_p[0]-rect_p[0])))
  [print(math.degrees(i)) for i in anglelist]
  for i in range(len(anglelist)):
   if i==0:
    if angle_p>=math.degrees(anglelist[0]) or angle_p<=math.degrees(anglelist[1]):
     return ((round(funclist[0](math.radians(angle_p))[0],3),round(funclist[0](math.radians(angle_p))[1],3)-(offset_p[1] if offset_p else 0)))
   elif math.degrees(anglelist[i])<=angle_p<=math.degrees(anglelist[(i+1)%len(anglelist)]):
    return ((round(funclist[i](math.radians(angle_p))[0],3)-(offset_p[0] if i==3 and offset_p else 0),round(funclist[i](math.radians(angle_p))[1],3)))

 def debug(self,*arg_p):
  if self.debugf:print(*arg_p)

# def altervideo(self,videofile_p,outputfile_p=None,size_p=1):
#  if not outputfile_p:
#   outputfile_p=re.sub(r'(.*)[.](.*)$',r'\1'+'_mod.'+r'\2',videofile_p)
#  self.ffmpeg('ffmpeg -i '+videofile_p+' -vf scale='+str(int(self.videowidth*float(size_p)))+':'+str(int(self.videoheight*float(size_p)))+' -y '+outputfile_p)
#  if re.search(r'_mod[.]',outputfile_p):
#   self.system('mv '+outputfile_p+' '+videofile_p)

# def convertfilter(self,filter,mode=None,imagename=None,begintime=None,duration=None,eof_action=False):
# def convertfilter(self,imagename,filter,begintime,duration=None):
 def convertfilter(self,filter,begintime):
#  self.debug("libc::convertfilter><",filter,mode,imagename,begintime,duration,eof_action)
  if not re.search(r'^\s*(overlay|blend)',filter):
   first,second=re.split(r',',filter)
   return 'overlay=x='+('W*' if not re.search(r'W',first,flags=re.I) else '')+first+':y='+('H*' if not re.search(r'H',second,flags=re.I) else '')+second
#   return 'overlay=x='+('W*' if not re.search(r'W',first,flags=re.I) else '')+first+':y='+('H*' if not re.search(r'H',second,flags=re.I) else '')+second+(':eof_action=pass' if re.search(r'[.](gif|mov|mp4)$',imagename,re.I) else ":enable='between(t,"+self.getsecond(begintime)+","+str(float(self.getsecond(begintime))+duration)+")'")
  else:
#   filter=self.filter[filter][mode]
#   if re.search(r'[.](mp4|gif|mov)$',imagename):
   filter=re.sub(r'(\b[tT]\b)',r'(\1-{})'.format(self.getsecond(begintime)),filter)
#   if duration:
#    filter=re.sub(r'/D',r'/'+str(duration),filter)
#   if eof_action and not re.search(r'eof_action',filter,re.I):
#    filter+='=eof_action=pass' if re.search(r'overlay$',filter,re.I) else ':eof_action=pass'
#   filter+=(':eof_action=pass' if re.search(r'[.](gif|mov|mp4)$',imagename,re.I) else ":enable='between(t,"+self.getsecond(begintime)+","+str(float(self.getsecond(begintime))+duration)+")'")
  return filter

 def exiftool(self,imagename,query):
  self.debug('><libc::exiftool - '+imagename+' '+query)
  if re.search(r'Duration$',query,re.I):
   return re.sub(r'\n$','',os.popen('ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 '+imagename).read())
  else:
   return re.sub(r'\n?$','',os.popen("exiftool "+imagename+" |egrep '^\s*"+query+"\s+:'|awk -F ':\\\s+' '{print $2}'").read(),re.I)

# def insertsilence(self,beginaudio,silenceduration=0.0,endaudio=None,outimagename=None):
#  outimagename=re.sub(r'(.*)[.].*',r'\1',beginaudio[0])+'_'+str(beginaudio[1])+str(silenceduration)+r'_'+(re.sub(r'(.*)[.].*',r'\1',endaudio[0])+str(endaudio[1]) if endaudio else '')+re.sub(r'.*([.].*)$',r'\1',beginaudio[0]) if not outimagename else outimagename
#  if not os.path.isfile(outimagename):
#   self.system("ffmpeg -t "+self.getsecond(beginaudio[1])+" -i "+beginaudio[0]+(" -t "+self.getsecond(endaudio[1])+" -i "+endaudio[0] if endaudio else "")+" -filter_complex \"[0:a]apad=pad_dur="+str(silenceduration)+"[aout]"+(";[aout][1:a]concat=n=2:v=0:a=1[aout]" if endaudio else "")+"\" -map \"[aout]\""+" -y "+outimagename)
#  return outimagename
#

 @classmethod
 def count(cls):
  cls.counti+=1
  return cls.counti

 def palette(self,color):
  if type(color) == tuple:
   return color
  elif re.search(r'^\s*\(.*\)',color,re.I):
   return tuple([int(i) for i in re.findall(r'\d+',color)])
  else:
   for key in self.palettecolor:
    if key.startswith(color):
     return self.palettecolor[key]
  return None

 def adddestdir(self,filename):
  if not re.search(r'/\w+',filename,flags=re.I) and not re.search(self.destdir+r'/*$',os.getcwd(),flags=re.I):
   print('filename in search',filename)
   return self.destdir+r'/'+filename
  return filename
 def outimagename(self,imagename,outimagename=None,extension=None):
  '''new imagename as imagename<self.count()>.<extension>'''
  if not outimagename:
   outimagename=re.sub('^(?P<id>[^.]*)(?P<id1>.*?)$',lambda m: m.group('id')+'_'+str(self.count())+m.group('id1'),imagename,re.I)
   while os.path.isfile(outimagename):
    outimagename=re.sub('^(?P<id>[^.]*)(?P<id1>.*?)$',lambda m: m.group('id')+'_'+str(self.count())+m.group('id1'),imagename,re.I)
  return self.adddestdir(outimagename if not extension else re.sub(r'[.].*$',r'.{}'.format(extension),outimagename))
