from PIL import Image,ImageDraw,ImageFont
import re
class overlayc:
 '''##Overlay##'''
 def __init__(self,libip):
  self.libi=libip

 def overlay(self,args_p,filter_p,beginstring_p,returnstring_p,count_p):
  '''"<index>:<imagename>:<duration>:<filter>:<alpha 0-255>:<b|r|t|l>" <timestamp> <timestamp>'''
  index,imagename,duration,filter,alphablend,side=self.libi.split(args_p[0],(None,"./",None,self.libi.filterlist[filter_p][0],255,'l'))
  filter=re.sub(r'\\:',r':',filter)
  if 60<=filter_p<=63:
   filter_p=60+('t','r','b','l').index(side)
   filter=re.sub(r'\\:',r':',self.libi.filterlist[filter_p][0])
  imagesize=self.libi.dimension(imagename)
  if not re.search(r'[.]gif$',imagename,flags=re.I) and (self.libi.videowidth < imagesize[0] or self.libi.videoheight < imagesize[1]):
   self.libi.ffmpeg('ffmpeg -i input.mp4 -i '+imagename+' -filter_complex "[1][0]scale2ref='+('iw:(main_h/main_w)*ow' if imagesize[0]>imagesize[1] else 'oh*mdar:ih')+'[11][00];[00]nullsink" -map [11] -y '+'image'+str(count_p)+re.sub(r'.*([.].*)$',r'\1',imagename))
  else:
   self.libi.system('cp '+imagename+' image'+str(count_p)+re.sub(r'.*([.].*)$',r'\1',imagename))
  imagename='image'+str(count_p)+re.sub(r'.*([.].*)$',r'\1',imagename)
  if alphablend!=255:
   img=Image.open(imagename).convert('RGBA')
   img.putalpha(Image.new('L',self.libi.dimension(imagename),color=alphablend))
   img.save(imagename)
  beginstring_p+="-i "+imagename+" "
  for j in range(1,len(args_p)):
   returnstring_p+=("["+str(len(re.findall(r' -i ',beginstring_p))-1)+":v]setpts=PTS+"+self.libi.getsecond(args_p[j])+"/TB[bio"+str(count_p)+"];" if re.search(r'[.](gif|mp4)$',imagename,flags=re.I) else '') +("[0:v]" if not count_p else "[io"+str(count_p-1)+"]") + ("[bio"+str(count_p)+"]" if re.search(r'[.](gif|mp4)$',imagename,flags=re.I) else "["+str(len(re.findall(r' -i ',beginstring_p))-1)+":v]") + (re.sub(r'\bt\b',r'(t-'+self.libi.getsecond(args_p[j])+')',filter)+":" if filter else "overlay=") + ("eof_action=pass" if re.search(r'[.](gif|mp4)$',imagename,flags=re.I) else "enable='"+("between(t,"+self.libi.getsecond(args_p[j])+","+str(float(self.libi.getsecond(args_p[j]))+float(duration))+")'" if duration else "gte(t,"+self.libi.getsecond(args_p[j])+")'"))+"[io"+str(count_p)+"];"
   count_p=count_p+1
  return (beginstring_p,returnstring_p,count_p)

 def sidebyside(self,args_p,filter_p,beginstring_p,returnstring_p,count_p):
  '''<index>:<imagename>:<duration>:<filter>:<alpha 0-255>:<b|r|t|l>:<expand T|F>'''
  index,imagename,duration,filter,alphablend,side,expand=self.libi.split(args_p[0],(None,"./",5,'0.5,0.5',255,'l',False))
#  if expand:filter_p=
  filter=re.sub(r'\\:',r':',filter)
  return self.libi.blendoverglass(args_p,filter,beginstring_p,returnstring_p,count_p,imagename,duration_p=(duration,1,side))
