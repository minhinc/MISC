import os
from PIL import Image,ImageDraw,ImageFont
import re
class libc:
 def __init__(self):
  self.videowidth,self.videoheight=[int(x) for x in os.popen('ffmpeg -i input.mp4 2>&1|grep -oP \'Stream .*, \K[0-9]+x[0-9]+\'').read().split('x')]
  print("libc::_init__<> video widthxheight {}x{}".format(self.videowidth,self.videoheight))

 def split(self,string_p,delim_p=':'):
  print("libc::split<> {} {}".format(string_p,delim_p))
  DBL_ESC="!double escape!"
  return [x.replace(DBL_ESC,'\\') for x in re.split(r'(?<!\\):',string_p.replace(r'\\',DBL_ESC))]

 def dimension(self,file_p):
  if re.search(r'[.]mp4',file_p,flags=re.I):
   return [int(x) for x in os.popen('ffmpeg -i input.mp4 2>&1|grep -oP \'Stream .*, \K[0-9]+x[0-9]+\'').read().split('x')]
  else:
   return Image.open(file_p).size

 def getfont(self,stringlist_p,screenratio_n=0.8,fontfamily_p='/home/pi/.fonts/twcenmt.ttf'):
  print("libc::getfont {}".format(stringlist_p))
  i=10
  while (ImageFont.truetype(fontfamily_p,i).getsize('a')[0]*(max([len(j) for j in stringlist_p]) if max([len(j) for j in stringlist_p])>10 else 10))<(self.videowidth*screenratio_n): i=i+1
  print("net i {}".format(i))
  return ImageFont.truetype(fontfamily_p,i)
 
 def ffmpeg(self,commandstring_p):
  print('              *****************')
  print("              "+re.sub(r' -y ([^ ]+[.]mp4)',r' -preset ultrafast -y \1',commandstring_p))
  print('              *****************')
  os.system(re.sub(r' -y ([^ ]+[.]mp4)',r' -preset ultrafast -y \1',commandstring_p))

 def getsecond(self,time_p):
  print('libc::getsecond<> '+time_p)
  if re.search(r':',time_p):
   return re.sub(r'(?P<id1>\d+):(?P<id2>\d+):(?P<id3>\d+)(?P<id4>.*)$',lambda m: str(int(m.group('id1'))*3600+int(m.group('id2'))*60+int(m.group('id3')))+m.group('id4'),time_p)
  return time_p

 def system(self,commandstring_p):
  print(commandstring_p)
  os.system(commandstring_p)
