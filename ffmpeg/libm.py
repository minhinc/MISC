import os,sys;sys.path.append(os.path.expanduser('~')+r'/tmp')
import math
from PIL import Image,ImageDraw,ImageFont
import re
import shlex
import subprocess
from decimal import Decimal
import copy
import configparser
#from MISC.extra.debugwrite import print
import MISC.ffmpeg.filterm as filterm
class libc:
 '''library class to provide basic functions'''
 counti=-1
 def __init__(self,inputfile=None,destdir='logdir',gifp=None):
  self.filter=filterm.filter
  '''
  self.filter={
   'blend':{'blend':"blend=all_expr='A*(1-min(T/1,1))+B*(min(T/1,1))':eof_action=pass",
     'up': "blend=all_expr='if(lte(Y,(H-T/1*H)),A,B)':eof_action=pass", #Curtain up \
     'right':"blend=all_expr='if(gte(X,(T/1*W)),A,B)':eof_action=pass", #Curtain right \
     'down':"blend=all_expr='if(gte(Y,(T/1*H)),A,B)':eof_action=pass", #curtain down \
     'left':"blend=all_expr='if(lte(X,(W-T/1*W)),A,B)':eof_action=pass", #curtain left \
     'verticalopen':"blend=all_expr='if(between(X,(W/2-T/1*W/2),(W/2+T/1*W/2)),B,A)':eof_action=pass",
     'horizontalopen':"blend=all_expr='if(between(Y,(H/2-T/1*H/2),(H/2+T/1*H/2)),B,A)':eof_action=pass",
     'verticalclose':"",
     'horizontalclose':"",
     'circleopen':"blend=all_expr='if(gte(sqrt((X-W/2)*(X-W/2)+(H/2-Y)*(H/2-Y)),(T/3*max(W,H))),A,B)':eof_action=pass",
     'circleclose':"blend=all_expr='if(lte(sqrt((X-W/2)*(X-W/2)+(H/2-Y)*(H/2-Y)),(max(W,H)-(T/1*max(W,H)))),A,B)':eof_action=pass",
     'expandingwindow':"blend=all_expr='if(between(X,(W/2-T/1*W/2),(W/2+T/1*W/2))*between(Y,(H/2-T/1*H/2),(H/2+T/1*H/2)),B,A)':eof_action=pass",
     'fadein': "fade=in:st=0:d=3:alpha=1",
     'fadeinout': "fade=in:st=0:d=1:alpha=1,fade=out:st=0:d=1:alpha=1",
   },
   'overlay':{ 'normal':"overlay=x='(W-w)/2':y='(H-h)/2':eof_action=pass",
     'up' :"overlay=x='(W-w)/2':y='max((H-h)/2,H-t/1*H)':eof_action=pass",
     'right' : "overlay=x='min((W-w)/2,-w+t/1*W)':y='(H-h)/2':eof_action=pass",
     'bottom': "overlay=x='(W-w)/2':y='min((H-h)/2,-h+t/1*H)':eof_action=pass",
     'left' : "overlay=x='max((W-w)/2,W-t/1*W)':y='(H-h)/2':eof_action=pass",
   },
   '41':r"crop=w=2*floor(iw/2):h=2*floor(ih/2)",
   '00t':((255,0,0,255),(128,128,128,128),0.25,False,'m',10),
   '01t':((255,255,255,255),(128,0,0,128),0.25,False,'m',10),
   '02t':((0,85,255,255),(255,255,255,255),0.25,False,'m',5),
   '03t':((255,255,255,255),(0,85,255,255),0.25,False,'m',5),
  }
  '''
  '''
  self.filter={
   #0-> blend 1-> overlay 2-> text to image 3-> image(gif,.mp4,.png) to .mov
   '00':r"blend=all_expr='A*(1-min(T/1,1))+B*(min(T/1,1))'", #All
   '01':r"blend=all_expr='if(lte(Y,(H-T/1*H)),A,B)'", #Curtain up \
   '02':r"blend=all_expr='if(gte(X,(T/1*W)),A,B)'", #Curtain right \
   '03':r"blend=all_expr='if(gte(Y,(T/1*H)),A,B)'", #curtain down \
   '04':r"blend=all_expr='if(lte(X,(W-T/1*W)),A,B)'", #curtain left \
   '05':r"blend=all_expr='if(between(X,(W/2-T/1*W/2),(W/2+T/1*W/2)),B,A)'",#Vertical open
   '06':r"blend=all_expr='if(between(Y,(H/2-T/1*H/2),(H/2+T/1*H/2)),B,A)'",#horizontal open
   '07':r"",#verticalclose
   '08':r"",#horizontalclose
   '09':r"blend=all_expr='if(gte(sqrt((X-W/2)*(X-W/2)+(H/2-Y)*(H/2-Y)),(T/2*max(W,H))),A,B)'",#circleopen
   '010':r"blend=all_expr='if(lte(sqrt((X-W/2)*(X-W/2)+(H/2-Y)*(H/2-Y)),(max(W,H)-(T/1*max(W,H)))),A,B)'",#circleclose
   '011':r"blend=all_expr='if(between(X,(W/2-T/1*W/2),(W/2+T/1*W/2))*between(Y,(H/2-T/1*H/2),(H/2+T/1*H/2)),B,A)':eof_action=pass",#expandingwindow
    '011_s':r"blend=all_expr='if(between(X,(W*0.34-T/1*W*0.34),(W*0.66+T/1*W*0.34))*between(Y,(H*0.34-T/1*H*0.34),(H*0.66+T/1*H*0.34)),B,A)':eof_action=pass",#expandingwindow
   '012':r"fade=in:st=0:d=1:alpha=0",#fadein
    '012_a':r"fade=in:st=0:d=1:alpha=1",#fadein
   '013':r"fade=out:st=0:d=1:alpha=0",#fadeout
    '013_white':r"fade=out:st=0:d=1:color=0xFFFFFFFF:alpha=0",#fadeout alpha 1
    '013_a':r"fade=out:st=0:d=1:alpha=1",#fadeout alpha 1
   '10':r"overlay=x='(W-w)/2':y='(H-h)/2'",#normal
   '11':r"overlay=x='(W-w)/2':y='max((H-h)/2,H-t/1*H)'",#up
   '12':r"overlay=x='min((W-w)/2,-w+t/1*W)':y='(H-h)/2'",#right
   '13':r"overlay=x='(W-w)/2':y='min((H-h)/2,-h+t/1*H)'",#bottom
   '14':r"overlay=x='max((W-w)/2,W-t/1*W)':y='(H-h)/2'",#left

   '20':('self.gifi.overlay',{'imagename':'$[0][0]','begintime':"re.split('-',$[2])[0]",'duration':"float(self.getsecond(re.split('-',$[2])[1]))-float(self.getsecond(re.split('-',$[2])[0]))",'position':'$[1][1]'}),
    '202':("self.filter['20']",("[1]['begintime']",'$[2]'),("[1]['duration']",None)),
    '203':("self.filter['20']",),

   '21':('self.gifi.overlay',{'imagename':('self.gifi.utili.image2gif',{'imagename':'$[0][0]','duration':"float(self.getsecond(re.split('-',$[2])[1]))-float(self.getsecond(re.split('-',$[2])[0]))",'filtername':"self.filter['01']"}),'begintime':"re.split('-',$[2])[0]",'duration':"float(self.getsecond(re.split('-',$[2])[1]))-float(self.getsecond(re.split('-',$[2])[0]))",'position':'$[1][1]'}),
    '212':("self.filter['21']",("[1]['begintime']",'$[2]'),("[1]['imagename'][1]['duration']",None),("[1]['duration']",None)),
    '213':("self.filter['21']",),

   '22':('self.gifi.overlay',{'imagename':('self.gifi.utili.image2gif',{'imagename':('self.gifi.utili.text2image',{'text':"$[0][0]+':yellow:black:0.5:::'",'richtext':True}),'duration':"float(self.getsecond(re.split('-',$[2])[1]))-float(self.getsecond(re.split('-',$[2])[0]))",'filtername':"self.filter['01']"}),'begintime':"re.split('-',$[2])[0]",'duration':"float(self.getsecond(re.split('-',$[2])[1]))-float(self.getsecond(re.split('-',$[2])[0]))",'position':'$[1][1]'}),
    '222':("self.filter['22']",("[1]['begintime']",'$[2]'),("[1]['imagename'][1]['duration']",None),("[1]['duration']",None)),
    '223':("self.filter['22']",),
    '223_whiteonblack':("self.filter['22']",("[1]['imagename'][1]['imagename'][1]['text']","$[0][0]"),("[1]['imagename'][1]['imagename'][1]['textcolor']","\'white\'"),("[1]['imagename'][1]['imagename'][1]['backcolor']","\'black\'"),("[1]['imagename'][1]['imagename'][1]['size']",0.7),("[1]['imagename'][1]['imagename'][1]['richtext']",False),("[1]['imagename'][1]['filtername']","self.filter['03']")),
    '223_redonyellow':("self.filter['22']",("[1]['imagename'][1]['imagename'][1]['text']","$[0][0]"),("[1]['imagename'][1]['imagename'][1]['backcolor']","\'yellow\'"),("[1]['imagename'][1]['imagename'][1]['richtext']",False)),

   '40':r"zoompan=z='min(zoom+0.0015,1.5)':x='if(gte(zoom,1.5),x-1/a,iw/2-iw/zoom/2)':y='if(gte(zoom,1.5),y,ih/2-ih/zoom/2)'",
    '40_82_pan':r"zoompan=z='if(lte(on,1),zoom+0.4,zoom)':x=(iw/2-iw/zoom/2):y='if(lte(on,2),ih-ih/zoom,y-(ih-ih/zoom)/(25*))'",
    '40_82_zoompan':r"zoompan=z='min(zoom+0.0015,1.5)':x='iw/2-iw/zoom/2':y='if(lt(zoom,1.5),ih-ih/zoom,y-(ih-ih/zoom)/(25*))'",
    '40_82_antizoompan':r"zoompan=z='if(lte(on,1),zoom+1,max(zoom-0.02,1.2))':x='iw/2-iw/zoom/2':y='if(gt(zoom,1.2),ih-ih/zoom,y-(ih-ih/zoom)/(25*))'",
    '40_28_pan':r"zoompan=z='if(lte(on,1),zoom+0.4,zoom)':x='iw/2-iw/zoom/2':y='if(lte(on,2),0,y+(ih-ih/zoom)/(25*))'",
    '40_28_zoompan':r"zoompan=z='min(zoom+0.0015,1.5)':x='iw/2-iw/zoom/2':y='if(lt(zoom,1.5),0,y+(ih-ih/zoom)/(25*))'",
    '40_64_pan':r"zoompan=z='if(lte(on,1),zoom+0.4,zoom)':x='if(lte(on,2),iw-iw/zoom,x-(iw-iw/zoom)/(25*))':y='(ih/2-ih/zoom/2)'",
    '40_64_zoompan':r"zoompan=z='min(zoom+0.0015,1.5)':x='if(lt(zoom,1.5),iw-iw/zoom,x-(iw-iw/zoom)/(25*))':y='(ih/2-ih/zoom/2)'",
    '40_46_pan':r"zoompan=z='if(lte(on,1),zoom+0.4,zoom)':x='if(lte(on,2),0,x+(iw-iw/zoom)/(25*))':y='(ih/2-ih/zoom/2)'",
    '40_46_zoompan':r"zoompan=z='min(zoom+0.008,1.5)':x='if(lt(zoom,1.5),0,x+(iw-iw/zoom)/(25*10))':y='(ih/2-ih/zoom/2)'",
    '40_46_antizoompan':r"zoompan=z='if(lte(on,1),zoom+1,max(zoom-0.02,1.1))':x='if(gt(zoom,1.1),0,x+(iw-iw/zoom)/(25*-(2-1.1)/0.02))':y='ih/2-ih/zoom/2'",
    '40_56_antizoompan':r"zoompan=z='if(lte(on,1),zoom+1,max(zoom-0.02,1.1))':x='if(gt(zoom,1.1)0,iw/2-iw/zoom/2,x+(iw/2-iw/zoom/2)/(25*-(2-1.1)/0.02))':y='ih/2-ih/zoom/2'",
    '40_54_antizoompan':r"zoompan=z='if(lte(on,1),zoom+1,max(zoom-0.02,1.1))':x='if(gt(zoom,1.1),iw/2-iw/zoom/2,x-(iw/2-iw/zoom/2)/(25*-(2-1.1)/0.02))':y='ih/2-ih/zoom/2'",
    '40_64_antizoompan':r"zoompan=z='if(lte(on,1),zoom+1,max(zoom-0.02,1.1))':x='if(gt(zoom,1.1),iw-iw/zoom,x-(iw-iw/zoom)/(25*-(2-1.1)/0.02))':y='ih/2-ih/zoom/2'",
    '40_antizoom':r"zoompan=z='if(lte(on,1),zoom+1,zoom-0.02)':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2'",
    '40_antizoomv':r"zoompan=z='if(lte(on,1),pzoom+1,pzoom-0.02)':x='iw/2-iw/pzoom/2':y='ih/2-ih/pzoom/2'",
#   '40_1.3_28_pan
   '41':r"crop=w=2*floor(iw/2):h=2*floor(ih/2)",
  }
  '''

  self.gifi=gifp
  if not os.path.isdir(destdir):
   os.mkdir(destdir)
  self.destdir=destdir
  if re.search(r'/'+self.destdir,os.getcwd()):
   print(f' ----- cannot run from '+self.destdir+' ------------')
   exit(-1)
#  self.inputfile=self.adddestdir(inputfile) if inputfile else None
#  self.videowidth,self.videoheight=[int(x) for x in os.popen('ffmpeg -i '+self.inputfile+' 2>&1|grep -oP \'Stream .*, \K[0-9]+x[0-9]+\'').read().split('x')] if self.inputfile else None,None
  config=configparser.ConfigParser()
  config.read(os.path.expanduser('~')+r'/minh.ini')
  self.debugf=int(config['debug']['level'])
  self.duration=self.videowidth=self.videoheight=0
  if inputfile:
   self.setvideo(inputfile)
  self.palettecolor={
   'red':(255,0,0,255),
   'yellow':(248,242,0,255),
   'blue':(0,0,255,255),
   'green':(0,255,0,255),
   'gi':(0,64,0,255),
   'white':(255,255,255,255),
   'black':(0,0,0,255),
   'bb':(0,0,2,255),
   'transparent':(0,0,0,0),
   'shade1':(0,0,0,32), 'shade2':(0,0,0,64), 'shade3':(0,0,0,96), 'shade4':(0,0,0,128), 'shade5':(0,0,0,160), 'shade6':(0,0,0,192), 'shade7':(0,0,0,224),
   'shade8':(255,255,255,32), 'shade9':(255,255,255,64), 'shade10':(255,255,255,96), 'shade11':(255,255,255,128), 'shade12':(255,255,255,160), 'shade13':(255,255,255,192), 'shade14':(255,255,255,224)
  }
#  print(f'<>libc::_init__ {self.videowidth=} {self.videoheight=}')

# def setvideo(self,inputfile,dimension=None):
 def setduration(self,durationP):
  print(f'><libc.setduration durationP={durationP}')
#  try:
#   type(float(durationP))
#  except Exception as ec:
#   self.duration+=sum(float(self.getsecond(re.split('-',y)[1]))-float(self.getsecond(re.split('-',y)[0])) for x in durationP if len(x)==2 for y in (x[1] if type(x[1])==tuple else [x[1]]))+sum(float(self.exiftool(re.sub(r'^=','',x[0]),'Duration')) for x in durationP if len(x)==1)
#   self.setvideo([re.sub(r'^=','',x[0]) for x in durationP if len(x)==1 and re.search(r'^=',x[0])][0])
#  else:
  self.duration=float(self.getsecond(durationP))

 def setvideo(self,inputfile):
  '''---------
    inputfile - [<videowidth>[-:x,]<videoheight>] or videofilename'''
  print(f'><libc.setvideo {inputfile=}')
  if type(inputfile)==tuple:
   self.videowidth,self.videoheight=tuple([int(x) for x in inputfile])
  elif re.search(r'^\s*[\d]+\s*[-:x,]\s*[\d]+\s*$',inputfile):
   self.videowidth,self.videoheight=[int(x) for x in re.split('[-:,x]',inputfile)]
  else:
#   self.videowidth,self.videoheight=([int(x) for x in os.popen('ffmpeg -i '+inputfile+' 2>&1|grep -oP \'Stream .*, \K[0-9]+x[0-9]+\'').read().split('x')]) if inputfile else (None,None)
   self.videowidth,self.videoheight=[int(x) for x in self.videoattribute(inputfile)[0]]
  print(f'<>libc.setvideo {self.videowidth=} {self.videoheight=}')

 def videoattribute(self,videofile_p):
  '''---INPUT---
    videofile_p=.mp4/.mov/.mp3 or any media file
   ---OUTPUT---
   ((videowidth,videoheight),fps,samplerate,channeltype)'''
  print(f'><libc.videoattribute videofile_p={videofile_p}')
#  videodata=os.popen('ffprobe -i '+videofile_p+' 2>&1').read()
  videodata=self.system('ffprobe -i '+videofile_p+' 2>&1',popen=True)
#  self.debug(f'><libc.videoattribute videofile_p={videofile_p} (videowidth,videoheight)={(videowidth,videoheight)} fps={fps} samplerate={samplerate} channel={channel}')
  if re.search(r'[.](mp4|mkv)$',videofile_p,flags=re.I):
   return (tuple(re.sub(r'.*,\s*?(\d+x\d+)\s*.*',r'\1',videodata,flags=re.I|re.DOTALL).split('x')),re.sub(r'.*?(\d+)\s*fps\s*,.*',r'\1',videodata,flags=re.I|re.DOTALL),re.sub(r'.*?(\d+)\s*Hz\s*,.*',r'\1',videodata,flags=re.I|re.DOTALL),re.sub(r'.*\d+\s*Hz\s*,\s*([^ ]*)\s*,.*',r'\1',videodata,flags=re.I|re.DOTALL),re.sub(r'.*Duration\s*:\s+(\S+),.*',r'\1',videodata,flags=re.I|re.DOTALL))
  elif re.search(r'[.]mov$',videofile_p,flags=re.I):
   return (tuple(re.sub(r'.*,\s*?(\d+x\d+)\s*.*',r'\1',videodata,flags=re.I|re.DOTALL).split('x')),re.sub(r'.*?(\d+)\s*fps\s*,.*',r'\1',videodata,flags=re.I|re.DOTALL))
  elif re.search(r'[.](mp3|webm)$',videofile_p,flags=re.I):
   return (re.sub(r'.*?(\d+)\s*Hz\s*,.*',r'\1',videodata,flags=re.I|re.DOTALL),re.sub(r'.*\d+\s*Hz\s*,\s*([^ ]*)\s*,.*',r'\1',videodata,flags=re.I|re.DOTALL),re.sub(r'.*Duration\s*:\s+(\S+),.*',r'\1',videodata,flags=re.I|re.DOTALL))

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
  print(f'><libc.dimension {file_p=}')
  if re.search(r'[.](mp4|mov|webm|mkv)$',file_p,flags=re.I):
#   return [int(x) for x in os.popen('ffmpeg -i "+self.inputfile+" 2>&1|grep -oP \'Stream .*, \K[0-9]+x[0-9]+\'').read().split('x')]
   retval= tuple([str(int(x)) for x in os.popen('ffprobe -i '+file_p+' 2>&1|grep -oP \'Stream .*, \K[0-9]+x[0-9]+\'').read().split('x')])
#   print(f'libc.dimension {retval=} {file_p=}')
   return retval
  else:
   return Image.open(file_p).size

 def drawtextstroke(self,draw_p,x_p,y_p,text_p,textfont_p,textcolor_p,strokecolor_p='black',adj_p=2):
  strokelist=[(x_p-adj_p,y_p),(x_p+adj_p,y_p),(x_p,y_p-adj_p),(x_p,y_p+adj_p),(x_p-adj_p,y_p-adj_p),(x_p+adj_p,y_p-adj_p),(x_p-adj_p,y_p+adj_p),(x_p+adj_p,y_p+adj_p)]
  for i in range(len(strokelist)):
   draw_p.text((strokelist[i][0],strokelist[i][1]),text_p,font=textfont_p,fill=strokecolor_p)
  draw_p.text((x_p,y_p),text_p,font=textfont_p,fill=textcolor_p)

 def getfontsize(self,stringlist_p,screenratio_p=0.8,fontfamily_p=os.path.expanduser('~')+r'/.fonts/ufonts.com_tw-cen-mt.ttf',lineheight=0):
  print(f'><libc.getfontsize stringlist_p={stringlist_p} screenratio_p={screenratio_p} fontfamily_p={fontfamily_p} lineheight={lineheight}')
  size=[]
  font=self.getfont(stringlist_p,screenratio_p,fontfamily_p)
  for i in re.split(r'(?:\n|\\n)',stringlist_p):
   size.append(font.getsize(i))
  print(f'<>libc.getfontsize size={size}')
  return (max(x[0] for x in size),sum(x[1] for x in size)+(len(size)-1)*lineheight)

 def getfont(self,stringlist_p,screenratio_p=0.8,fontfamily_p=os.path.expanduser('~')+r'/.fonts/ufonts.com_tw-cen-mt.ttf',widthheight=False,setvideo=None):
  '''\
  stringlist_p - tuple/list of string
  screenratio_p - screen ratio, i.e 0.4 width,height=40% of (screenwidthheight)
  widthheight - consider both width and height of screen
  setvideo - screen width and height, defaults to already set through libi.setvideo
  -----
  multiline string would get converted to stringlist
  -----
  libc.getfont('Hello World',0.5,widthheight=True,setvideo=(300,200))
  libc.getfont('Hello World\nWelcome',0.4)
  libc.getfont(('Hello world','Welcome\nTo the World'))'''
  print(f'><libc.getfont {stringlist_p=} {screenratio_p=} {fontfamily_p=} {widthheight=} {setvideo=} {(self.videowidth,self.videoheight)=}')
  width,height=(0,0)
  maxindex=None
  if setvideo:
   self.setvideo(setvideo)
  i=10
  stringlist_p=[y for x in (stringlist_p if type(stringlist_p)==tuple or type(stringlist_p)==list else (stringlist_p,)) for y in re.split(r'(?:\n|\\n)',x)]
  if widthheight:
   while width<=float(self.videowidth)*screenratio_p and height<=float(self.videoheight)*screenratio_p:
    width,height=(0,0)
    for j in stringlist_p:
     width=max(width,ImageFont.truetype(fontfamily_p,i).getbbox(j,anchor="lt")[2])
#     height+=ImageFont.truetype(fontfamily_p,i).getsize(j)[1]+(widthheight if type(widthheight)==int else 0)
#     height+=ImageFont.truetype(fontfamily_p,i).getmask(j).getbbox()[3]+(widthheight if type(widthheight)==int else 0)
     height+=ImageFont.truetype(fontfamily_p,i).getbbox(j,anchor="lt")[3]+(widthheight if type(widthheight)==int else 0)
    height-=widthheight if type(widthheight)==int else 0
    i+=1
   i-=1
  else:
   stringlist_p.append('Q'*10) # in order to force calculation for 20 characters minimum
   maxindex=[len(j) for j in stringlist_p].index(max(len(j) for j in stringlist_p))
#   while ImageFont.truetype(fontfamily_p,i).getsize(stringlist_p[maxindex])[0] < float(self.videowidth)*screenratio_p: i=i+1
   while ImageFont.truetype(fontfamily_p,i).getbbox(stringlist_p[maxindex],anchor="lt")[2] <= float(self.videowidth)*screenratio_p: i=i+1
   i-=1
  print(f'<>libc.getfont {maxindex=} {i=}')
  return ImageFont.truetype(fontfamily_p,i)
 
 '''
 def ffmpeg(self,commandstring_p):
  print('><libc.ffmpeg *****************')
  print(re.sub(r' -y ([^ ]+[.].*)$',r' -preset ultrafast -y \1',commandstring_p) if self.debugf else commandstring_p)
  print('><libc.ffmpeg *****************')
#  os.system(re.sub(r' -y ([^ ]+[.].*)$',r' -preset ultrafast -y \1',commandstring_p) if self.debugf else commandstring_p)
  subprocess.call(shlex.split(re.sub(r' -y ([^ ]+[.].*)$',r' -preset ultrafast -y \1',commandstring_p) if self.debugf else commandstring_p))
 '''

 def getsecond(self,time_p,demark_p=False):
  '''demark - float to colon format'''
  print(f'><libc.getsecond {time_p=}')
  def _getsecond(time_p):
#   if type(time_p) == int or type(time_p) == float:
   if not re.search(':',str(time_p)):
    return str(time_p)
   elif re.search(r':',time_p):
    return re.sub(r'(?P<id1>\d+):(?P<id2>\d+):(?P<id3>\d+)(?P<id4>.*)$',lambda m: str(int(m.group('id1'))*3600+int(m.group('id2'))*60+int(m.group('id3')))+m.group('id4'),time_p)
  if not demark_p:
   if re.search('-',str(time_p)):
    return str(float(_getsecond(re.split(r'-',time_p)[1]))-float(_getsecond(re.split('-',time_p)[0])))
   else:
    return _getsecond(time_p)
  else:
   hour=int(float(time_p)/3600)
   minute=int((float(time_p)-hour*3600)/60)
   second=round(float(time_p)-hour*3600-minute*60,3)
   return f'{str(hour):0>2}:{str(minute):0>2}:{str(second):0>2}'
  return time_p

 def system(self,commandstring_p,popen=False):
  '''--- ARGUMENTS---
commandstring_p - command in single string ,i.e. "ffmpeg -i abc.mp4 -af \"....
popen - command to be executed through (shell - /bin/bash) subprocess.check_output otherwise subprocess.call
--- RETURN ---
command executed shell('/bin/bash') output if popen=True else None'''
  print(f'********************************')
  print(f'><libc.system {commandstring_p=}')
  print(f'================================')
#  os.system(commandstring_p)
  if not popen:
   subprocess.call(shlex.split(commandstring_p)) if not re.search(r'^s*ffmpeg ',commandstring_p) else subprocess.call(shlex.split(re.sub(r' -y ([^ ]+[.].*)$',r' -preset ultrafast -y \1',commandstring_p) if self.debugf else commandstring_p))
  else:
   return subprocess.check_output(commandstring_p,shell=True,executable=r'/bin/bash').decode()

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
#  print(f'><libc.exiftool imagename={imagename} query={query}')
  if re.search(r'Duration$',query,re.I):
   return re.sub(r'\n$','',os.popen('ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 '+imagename).read())
  else:
#   return re.sub(r'\n?$','',os.popen("exiftool \""+imagename+"\" |egrep '^\s*"+query+"\s+:'|awk -F ':\\\s+' '{print $2}'").read(),re.I)
   return re.sub(r'\n?$','',os.popen("exiftool \""+imagename+"\" |egrep '^\s*"+query+"\s+:'|awk -F ':[ \t]+' '{print $2}'").read(),re.I)

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
#  if not re.search(r'/\w+',filename,flags=re.I) and not re.search(self.destdir+r'/*$',os.getcwd(),flags=re.I):
  filename=re.sub(r'/+$','',filename)
  if not re.search(self.destdir+r'/',filename,flags=re.I) and not re.search(self.destdir+r'/*$',os.getcwd(),flags=re.I):
   print('filename in search',filename)
#   return self.destdir+r'/'+filename
   return re.sub(r'^.*/+(.*)$',r'./'+self.destdir+r'/'+r'\1',filename) if re.search(r'/',filename) else self.destdir+r'/'+filename
  return filename

 def outimagename(self,imagename,outimagename=None,extension=None):
  '''new imagename as imagename<self.count()>.<extension>'''
  print(f'><libc.outimagename imagename={imagename} outimagename={outimagename} extension={extension}')
  if not outimagename:
#   outimagename=self.adddestdir(re.sub('^(?P<id>[^.]*)(?P<id1>.*?)$',lambda m: m.group('id')+'_'+str(self.count())+('.'+re.sub(r'^[.]*','',extension) if extension else m.group('id1') if m.group('id1') else '.'),imagename,re.I))
   outimagename=self.adddestdir(re.sub(r'^(?P<id>.*?)(?P<id1>[.][^.]*)?$',lambda m: m.group('id')+'_'+str(self.count())+('.'+re.sub(r'^[.]*','',extension) if extension else m.group('id1') if m.group('id1') else '.'),imagename,re.I))
   while os.path.isfile(outimagename):
#    outimagename=re.sub('^(?P<id>[^.]*)(?P<id1>.*?)$',lambda m: m.group('id')+'_'+str(self.count())+m.group('id1'),outimagename,re.I)
    outimagename=re.sub('^(?P<id>.*)(?P<id1>[.][^.]*)$',lambda m: m.group('id')+'_'+str(self.count())+m.group('id1'),outimagename,re.I)
   return outimagename
  return outimagename

 def co(self,c,dimension=None):
  '''\
  get coordinate in W,H, c->should be int or converted to int otherwise returned unchanged
  dimension is input and output -> ((600,400),(800,400))
    -------
    |1|2|3|
    |4|5|6|
    |7|8|9|
    -------
  '''
  print(f'><libc.co c={c} dimension={dimension}')
  if not re.search(r'^\d+$',str(c)):
   return c
  print(f'c={c} dimension={dimension}')
  if type(dimension)==str and os.path.exists(dimension):
   dimension=(tuple([int(x) for x in self.dimension(dimension)]),(self.videowidth,self.videoheight))
   print(f'libc.co new dimension={dimension}')
  c=int(c)
  def wh(c=5,W=1,H=1):
   offsetx,offsety=0,0
   if len(str(c))>1:
    offsetx,offsety=wh(str(c)[1:],W/3,H/3)
   return (int(Decimal(int(str(c)[0])-1)%3)-1)*W/3+offsetx,(int(int(int(str(c)[0])-1)/3)-1)*H/3+offsety
#  a,b=wh(c)
  a,b=[round(x,3) for x in wh(c)]
#  return r'(W-w)/2'+('+' if a>=0 else '')+str(a)+r'*W,(H-h)/2'+('+' if b>=0 else '')+str(b)+r'*H'
  '''
  if dimension:
   print(f'dimension -> a={a} b={b}')
   if (int(dimension[1][0])-int(dimension[0][0]))/2+a*int(dimension[1][0])<0:
    a=(int(dimension[0][0])-int(dimension[1][0]))/(2*int(dimension[1][0]))
   elif (int(dimension[1][0])-int(dimension[0][0]))/2+a*int(dimension[1][0])+int(dimension[0][0])>int(dimension[1][0]):
    a=(int(dimension[1][0])-int(dimension[0][0]))/(2*int(dimension[1][0]))
   if (int(dimension[1][1])-int(dimension[0][1]))/2+b*int(dimension[1][1])<0:
    b=(int(dimension[0][1])-int(dimension[1][1]))/(2*int(dimension[1][1]))
   elif (int(dimension[1][1])-int(dimension[0][1]))/2+b*int(dimension[1][1])+int(dimension[0][1])>int(dimension[1][1]):
    b=(int(dimension[1][1])-int(dimension[0][1]))/(2*int(dimension[1][1]))
  '''
  print(f'<>libc.co ...')
  return (r'(W-w)/2'+('+' if a>=0 else '')+str(a)+'*W' if not dimension else r'0' if (int(dimension[1][0])-int(dimension[0][0]))/2+a*int(dimension[1][0])<0 else r'(W-w)' if (int(dimension[1][0])-int(dimension[0][0]))/2+a*int(dimension[1][0])+int(dimension[0][0])>int(dimension[1][0]) else r'(W-w)/2'+('+' if a>=0 else '')+str(a)+'*W')+','+(r'(H-h)/2'+('+' if b>=0 else '')+str(b)+r'*H' if not dimension else '0' if (int(dimension[1][1])-int(dimension[0][1]))/2+b*int(dimension[1][1])<0 else 'H-h' if (int(dimension[1][1])-int(dimension[0][1]))/2+b*int(dimension[1][1])+int(dimension[0][1])>int(dimension[1][1]) else r'(H-h)/2'+('+' if b>=0 else '')+str(b)+r'*H')

 #00:06:45/345 or (3,00:00:05/05,00:40:00/2400)
 def getslotstamp(self,slotname,gaptime,requestcount=None,begintime=None,endtime=None):
  '''\
    slotname - name of the slot i.e 'bigbanner'
    gaptime - duration betweeen two slots,i.e. 30*60 =30 minutes
    requestcount - how many slot times, i.e 4, None=len(slots)
    begintime - begintime for calculations
    endtime - endtime for calculation\
  '''
  print(f'><libc.getslotstamp {slotname=} {gaptime=} {requestcount=} {begintime=} {endtime=}')
  filledslot=None
  timestamp=[]
  if not hasattr(libc.getslotstamp,'slots'):
   libc.getslotstamp.slots=[[] for x in range(min(10,int(self.duration//(5*60))))]
  durationgap=self.duration//min(10,self.duration//(5*60))
  requestcount=len(libc.getslotstamp.slots)-1 if requestcount==None else requestcount
  slotjumpcount=max(1,len(libc.getslotstamp.slots)//(requestcount+1))
  print(f'<=>libc.getslotstamp {slotjumpcount=}')
  for j in range(slotjumpcount,len(libc.getslotstamp.slots)+slotjumpcount,slotjumpcount):
   if j>=len(libc.getslotstamp.slots):
    j=len(libc.getslotstamp.slots)-1
   for i in range(j,-1,-1):
    print(f'{j=} {i=}')
    if (i*durationgap-([count for count in range(i,-1,-1) if libc.getslotstamp.slots[count] and libc.getslotstamp.slots[count][0]==slotname] or [0])[0]*durationgap)>=gaptime and (([count for count in range(i,len(libc.getslotstamp.slots)) if libc.getslotstamp.slots[count] and libc.getslotstamp.slots[count][0]==slotname] or [len(libc.getslotstamp.slots)-1])[0]*durationgap-i*durationgap)>=gaptime and not libc.getslotstamp.slots[i]:
     libc.getslotstamp.slots[i]=(slotname,gaptime)
     timestamp.append(i*durationgap)
     break
    elif libc.getslotstamp.slots[i] and libc.getslotstamp.slots[i][0]==slotname:
     requestcount-=1
     break
   if len(timestamp)==requestcount:
    break
  return timestamp
 """
 def getslotstamp(self,requestcount,begintime=None,endtime=None):
  '''\
  requestcount - number of slots (within begintime - endtime) else timestamp (slot at this timestamp)
  begintime - begintime when requestcount is number else None
  endtime - endtime when requestcount is number of slots else None
  getslotstamp(00:06:45) or getslotstamp(345)
  getslotstamp(3,00:00:05,0:40:00) or getslotstamp(3,5,2400)'''
  if not hasattr(libc.getslotstamp,'slotcount'):
   setattr(libc.getslotstamp,'slotcount',min(int(self.duration/180)+(1 if (self.duration%180)>20 else 0),10)+1)
   setattr(libc.getslotstamp,'slotarray',[None if i!=0 and i!=(libc.getslotstamp.slotcount-1) else True for i in range(libc.getslotstamp.slotcount)])
  print(f'><getslotstamp self.duration={self.duration} slotcount={libc.getslotstamp.slotcount} slotarray={libc.getslotstamp.slotarray}')
  if endtime==None:
   endtime=self.duration
  if not begintime==None:
   begintime,endtime=float(self.getsecond(begintime)),float(self.getsecond(endtime))
  requestcount=int(self.getsecond(requestcount))
  retarray=[]
  def adjust(timestamp):
   tickslot=int((timestamp*(libc.getslotstamp.slotcount-1))/self.duration) if (timestamp*(libc.getslotstamp.slotcount-1))/self.duration==int((timestamp*(libc.getslotstamp.slotcount-1))/self.duration) else int((timestamp*(libc.getslotstamp.slotcount-1))/self.duration)
   if libc.getslotstamp.slotarray[tickslot]:
    if not libc.getslotstamp.slotcount<=2 and (tickslot-1)!=0 and not libc.getslotstamp.slotarray[tickslot-1]:
     libc.getslotstamp.slotarray[tickslot-1]=True
     return int(((tickslot-1)*self.duration)/(libc.getslotstamp.slotcount-1))
    elif not libc.getslotstamp.slotcount<=2 and (tickslot+1)!=(libc.getslotstamp.slotcount-1) and not libc.getslotstamp.slotarray[tickslot+1]:
     libc.getslotstamp.slotarray[tickslot+1]=True
     return int(((tickslot+1)*self.duration)/(libc.getslotstamp.slotcount-1))
    return None
   else:
    libc.getslotstamp.slotarray[tickslot]=True
    return int((tickslot*self.duration)/(libc.getslotstamp.slotcount-1))
  if begintime==None:
   return adjust(requestcount)
  for i in range(requestcount):
   retarray.append(adjust(begintime+((endtime-begintime)*(i+1))/(requestcount+1)))
  print(f'<>getslotstamp slotarray={libc.getslotstamp.slotarray} retarray={retarray}')
  return [x for x in retarray if not x==None]
 """

 def tuple2funccal(self, a, b):
  '''a->tuple b->list'''
#  print(f'><libc.tuple2funccal a={a} b={b}')
  function=None
  def get_tuple2funccal_str(self,a):
   tmpfilter=None
#   print(f'><libc.tuple2funccal.get_tuple2funccal_str a={a} tmpfilter={tmpfilter} self.filter["21"]={self.filter["21"]}')
   for i in a:
    if type(i)==str and re.search(r'^self.filter\[',i):
     tmpfilter=get_tuple2funccal_str(self,eval(i))
    elif type(i)!=tuple:
     return copy.deepcopy(a)
    elif type(i)==tuple:
     exec("tmpfilter"+i[0]+'='+('"'+i[1]+'"' if type(i[1])==str else str(i[1])))
#   print(f'<>libc.tuple2funccal.get_tuple2funccal_str tmpfilter={tmpfilter}')
   return tmpfilter
  if type(a)==tuple and type(a[0])==str and re.search(r'^self.filter\[',a[0]):
   a=get_tuple2funccal_str(self,a)
#  print(f'<=>libc.tuple2funccal a={a}')
  if type(a)==tuple:
   for i in a:
    if type(i)==str:
#     function=getattr(self.utili,i)
     function=eval(i)
    elif type(i)==dict:
     return function(**self.tuple2funccal(i,b))
  elif type(a)==dict:
   for i in a:
#    print(f'i a i={i} a[i]={a[i]}')
    a[i]=(eval(re.sub(r'\$(\[\d+\])','b'+r'\1',a[i])) if type(a[i])==str else a[i]) if not type(a[i])==tuple else self.tuple2funccal(a[i],b)
#   print(f'<>libc.tuple2funccal parameter={a} b={b}')
   return a

 def str2tuple(self,a,resultformat='tuple'):
#  print(f'><libc.str2tuple a={a}')
  aa=[] #result string
  dd=[] #list of '(' indexes
  ii=0 #last ')' brace index
  for count,i in enumerate(a):
   if i==r'(' and (a[count-1]!='\\' if count else True):
    dd.append(count)
   elif i==r')' and a[count-1]!='\\':
    if len(dd)==1:
     aa.extend([re.sub(r'\\([(,)])',r'\1',x) for x in re.split(r'(?<!\\),',a[ii:dd[0]]) if x])
     aa.extend(self.str2tuple(a[dd[0]+1:count],resultformat)) if dd[0]==0 and count==(len(a)-1) else aa.append(self.str2tuple(a[dd[0]+1:count],resultformat))
     ii=count+1
    dd.pop()
  aa.extend([re.sub(r'\\([(,)])',r'\1',x) for x in re.split(r'(?<!\\),',a[ii:len(a)]) if x])
#  print(f'<>libc.str2tuple ii={ii} aa={aa} a[ii:len(a)]={a[ii:len(a)]}')
  return tuple(aa) if resultformat=='tuple' else aa

 def getvideo(self,i):
#  print(f'><libc.getvideo i={i}')
#  return len(i)==2 and type(i[0])==tuple and type(i[0][0])==str and re.search('video',self.exiftool(re.sub(r'^=','',i[0][0]),'MIME Type'),flags=re.I) and i[0][0] or len(i)==1 and type(i[0])==tuple and i[0][0] or len(i)==1 and type(i[0])==str and i[0]
#  ret=len(i)==2 and type(i[0])==tuple and type(i[0][0])==str and re.search('video',self.exiftool(re.sub(r'^=','',i[0][0]),'MIME Type'),flags=re.I) and i[0][0] or len(i)==2 and type(i[0])==str and re.search('video',self.exiftool(re.sub(r'^=','',i[0]),'MIME Type'),flags=re.I) and i[0] or len(i)==1 and type(i[0])==tuple and i[0][0] or len(i)==1 and type(i[0])==str and i[0]
  ret=len(i)==2 and (i[1]==None or type(i[1])==str) and i[0][0] or False
#  print(f'<>libc.getvideo ret={ret}')
  return ret

 def prune2(self,a,setvideo=False,stroketuple=None):
#  print(f'><libc.prune2 {a=}')
  tmp=None
  rettmp=[]
  a=self.str2tuple(a)
#  print(f'<=>libc.prune {a=} {type(a[0])=}')
  for i in [None if len(a)==1 else len(a)==2 and type(a[0])==str and a[1] or len(a)==2 and type(a[0][0])==str and re.search('video',self.exiftool(re.sub(r'^=','',a[0][0]),'MIME Type'),flags=re.I) and a[1] or len(a)==2 and a[1][1] or len(a)==3 and a[2]]:
   for j in (i if type(i)==tuple else [i]):
    if len(a)==1:
     tmp=[(a[0],re.sub('^=?(.*)[.].*',r'\1'+'.mp3',a[0]),None),j]
    elif len(a)==2:
     tmp=[(type(a[0])==str and a[0] or type(a[0][0])==str and re.search(r'video',self.exiftool(re.sub(r'^=','',a[0][0]),'MIME Type'),flags=re.I) and a[0][0] or self.gifi.utili.image2gif(a[0][0],a[1][0],duration=float(self.getsecond(j))),type(a[0])==str and re.sub('^=?(.*)[.].*',r'\1'+'.mp3',a[0]) or a[0][1],None if type(a[0])==str or len(a[0])<3 else a[0][2]),j]
    elif len(a)==3:
     tmp=[(None if re.search('audio',self.exiftool(type(a[0])==str and a[0] or a[0][0],'MIME Type'),flags=re.I) else type(a[0])==str and a[0] or a[0][0],re.search('audio',self.exiftool(type(a[0])==str and a[0] or a[0][0],'MIME Type'),flags=re.I) and (type(a[0])==str and a[0] or a[0][0]) or (None if type(a[0])==str else a[0][1]),None if type(a[0])==str else len(a[0])==2 and re.search('audio',self.exiftool(a[0][0],'MIME Type'),flags=re.I) and a[0][1] or (None if len(a[0])<3 else a[0][2])),None if a[1]=='None' else a[1],j]
    if len(tmp)==3 and type(tmp[1])==tuple:#
     tmp[1]=list(tmp[1])
     tmp[1][0]=re.sub(r'^(?P<id>.*?)(?P<id2>_.*)$',lambda m:m.group('id')+(re.search('-',tmp[2]) and '3' or '2')+m.group('id2'),tmp[1][0]) if re.search(r'_',tmp[1][0]) else tmp[1][0]+(re.search('-',tmp[2]) and '3' or '2')
     tmp[1]=tuple(tmp[1])
    rettmp.append(tuple(tmp))
  if setvideo and len(tmp)==2 and re.search(r'^=',tmp[0][0]):
   for count,tmp in enumerate(rettmp):
    tmp=list(tmp)
    tmp[0]=list(tmp[0])
    tmp[0][0]=re.sub(r'^=(.*)',r'\1',tmp[0][0])
    tmp[0]=tuple(tmp[0])
    rettmp[count]=tuple(tmp)
   self.setvideo(tmp[0][0])
  print(f'<>libc.prune2 {rettmp=}')
  if stroketuple!=None:
   stroketuple.extend(rettmp)
  return rettmp if not stroketuple else None
 def vformat(self,type):
#  return ' -pix_fmt yuv420p -c:v libx264 ' if type=='mp4' and not self.debugf else ' -pix_fmt rgba -c:v png ' if type=='mov' else ' '
  return ' ' if type=='mp4' and not self.debugf else ' -pix_fmt rgba -c:v png ' if type=='mov' else ' '
