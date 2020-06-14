from PIL import Image,ImageDraw,ImageFont
import re
class overlayc:
 '''##Overlay##'''
 def __init__(self,libip):
  self.libi=libip

 def logo(self,args_p,filter_p,beginstring_p,returnstring_p,count_p):
  beginstring_p+="-i "+self.libi.split(args_p[0])[1]+" "
  returnstring_p+="["+str(len(re.findall(r' -i ',beginstring_p))-1)+":v]setpts=PTS+0/TB[bio"+str(count_p)+"];"+("[0:v]" if not count_p else "[io"+str(count_p-1)+"]")+"[bio"+str(count_p)+"]"+filter_p+"[io"+str(count_p)+"];"
  count_p=count_p+1
  return (beginstring_p,returnstring_p,count_p)

 def overlay(self,args_p,filter_p,beginstring_p,returnstring_p,count_p):
  '''"<index>:<imagepath>:<duration>:<filter>" <timestamp> <timestamp>
  "101:logo.png:10:overlay=x=(W-w)/2" 00:00:02
  "101:logo.gif::overlay=x=W*0.2\:y=H*0.4\" 00:20:00'''
  duration=None
  imagename=self.libi.split(args_p[0])[1]
  imagesize=self.libi.dimension(self.libi.split(args_p[0])[1])
  if not re.search(r'[.]gif$',imagename,flags=re.I) and (self.libi.videowidth < imagesize[0] or self.libi.videoheight < imagesize[1]):
   self.libi.ffmpeg('ffmpeg -i input.mp4 -i '+self.libi.split(args_p[0])[1]+' -filter_complex "[1][0]scale2ref='+('iw:(main_h/main_w)*ow' if imagesize[0]>imagesize[1] else 'oh*mdar:ih')+'[11][00];[00]nullsink" -map [11] -y '+'image'+str(count_p)+re.sub(r'.*([.].*)$',r'\1',imagename))
   imagename='image'+str(count_p)+re.sub(r'.*([.].*)$',r'\1',imagename)
  if len(self.libi.split(args_p[0]))>=3: duration=self.libi.split(args_p[0])[2]
  if len(self.libi.split(args_p[0]))>=4: filter_p=re.sub(r'\\:',r':',self.libi.split(args_p[0])[3])
  beginstring_p+="-i "+imagename+" "
  for j in range(1,len(args_p)):
   returnstring_p+=("["+str(len(re.findall(r' -i ',beginstring_p))-1)+":v]setpts=PTS+"+self.libi.getsecond(args_p[j])+"/TB[bio"+str(count_p)+"];" if re.search(r'[.](gif|mp4)$',imagename,flags=re.I) else '') +("[0:v]" if not count_p else "[io"+str(count_p-1)+"]") + ("[bio"+str(count_p)+"]" if re.search(r'[.](gif|mp4)$',imagename,flags=re.I) else "["+str(len(re.findall(r' -i ',beginstring_p))-1)+":v]") + (re.sub(r'\bt\b',r'(t-'+self.libi.getsecond(args_p[j])+')',filter_p)+":" if filter_p else "overlay=") + ("eof_action=pass" if re.search(r'[.](gif|mp4)$',imagename,flags=re.I) else "enable='"+("between(t,"+self.libi.getsecond(args_p[j])+","+str(float(self.libi.getsecond(args_p[j]))+float(duration))+")'" if duration else "gte(t,"+self.libi.getsecond(args_p[j])+")'"))+"[io"+str(count_p)+"];"
   count_p=count_p+1
  return (beginstring_p,returnstring_p,count_p)

 def textoverlay(self,args_p,filter_p,beginstring_p,returnstring_p,count_p):
  ''' "index:image:duration" scenetransition scenetransition '''
  index=int(re.sub(r'^(\d+).*',r'\1',args_p[0]))
  if index==20:#logo
   beginstring_p+="-i logo.png "
   returnstring_p+="["+str(len(re.findall(r' -i ',beginstring_p))-1)+":v]setpts=PTS+0/TB[bio"+str(count_p)+"];"+("[0:v]" if not count_p else "[io"+str(count_p-1)+"]")+"[bio"+str(count_p)+"]"+filter_p+"[io"+str(count_p)+"];"
   count_p=count_p+1
  elif index==21: 
   beginstring_p+="-i title.gif "
#   os.system(self.titletext(re.sub(r'.*,(.*)$',r'\1',args_p[0]).split(r'\n')))
#   os.system(self.titletext(self.split(args_p[0])[1].split(r'\n')))
   os.system(self.messagebox(self.split(args_p[0])[1].split(r'\n')))
   for j in range(1,len(args_p)):
    returnstring_p+="["+str(len(re.findall(r' -i ',beginstring_p))-1)+":v]setpts=PTS+"+self.getsecond(args_p[j])+"/TB[bio"+str(count_p)+"];"+("[0:v]" if not count_p else "[io"+str(count_p-1)+"]")+"[bio"+str(count_p)+"]"+re.sub(r'\(t\)',r'(t-'+self.getsecond(args_p[j])+")",filter_p)+"[io"+str(count_p)+"];"
    count_p=count_p+1
  elif index==22:
   os.system(self.wipelr(re.sub(r'.*,(.*)',r'\1',args_p[0])))
   beginstring_p+="-i annotation.gif "
   for j in range(1,len(args_p)):
    returnstring_p+="["+str(len(re.findall(r' -i ',beginstring_p))-1)+":v]setpts=PTS+"+self.getsecond(args_p[j])+"/TB[bio"+str(count_p)+"];"+("[0:v]" if not count_p else "[io"+str(count_p-1)+"]")+"[bio"+str(count_p)+"]"+filter_p+"[io"+str(count_p)+"];"
    count_p=count_p+1
  elif index>=23 and index<=26:
   duration=10
   imagesize=Image.open(self.split(args_p[0])[1]).size
   self.ffmpeg('ffmpeg -i input.mp4 -i '+self.split(args_p[0])[1]+' -filter_complex "[1][0]scale2ref='+('iw:(main_h/main_w)*ow' if imagesize[0]>imagesize[1] else 'oh*mdar:ih')+'[11][00];[00]nullsink" -map [11] -y tmp.png')
   if self.split(args_p[0])[2]: duration=self.split(args_p[0])[2]
   for j in range(1,len(args_p)):
    self.ffmpeg('ffmpeg -ss '+args_p[j]+' -t '+duration+' -i input.mp4 -i tmp.png -filter_complex "'+re.sub(r'^',r'[0][1]',filter_p)+'" -y input'+str(count_p)+'.mp4')
    beginstring_p+="-i input"+str(count_p)+".mp4 "
    returnstring_p+="["+str(len(re.findall(r' -i ',beginstring_p))-1)+":v]setpts=PTS+"+self.getsecond(args_p[j])+"/TB[bio"+str(count_p)+"];"+("[0:v]" if not count_p else "[io"+str(count_p-1)+"]")+"[bio"+str(count_p)+"]overlay=eof_action=pass[io"+str(count_p)+"];"
    count_p=count_p+1
  elif index==27:
   duration=10
   videoimage=self.split(args_p[0])[1]
   if self.split(args_p[0])[2]: duration=self.split(args_p[0])[2]
   for j in range(1,len(args_p)):
    self.ffmpeg('ffmpeg -ss '+args_p[j]+' -t '+duration+' -i input.mp4 -ss 00:00:00 -t '+duration+' -i '+videoimage+' -filter_complex "'+re.sub(r'^',r'[1][0]',filter_p)+'" -y input'+str(count_p)+'.mp4')
    beginstring_p+="-i input"+str(count_p)+".mp4 "
    returnstring_p+="["+str(len(re.findall(r' -i ',beginstring_p))-1)+":v]setpts=PTS+"+self.getsecond(args_p[j])+"/TB[bio"+str(count_p)+"];"+("[0:v]" if not count_p else "[io"+str(count_p-1)+"]")+"[bio"+str(count_p)+"]overlay=eof_action=pass[io"+str(count_p)+"];"
    count_p=count_p+1
  return (beginstring_p,returnstring_p,count_p)
 def scenetransition(self,args_p,filter_p,beginstring_p,returnstring_p,count_p):
  ''' index '''
  self.ffmpeg('ffmpeg -i input.mp4 -filter_complex "'+filter_p)
  print([(x[1],'img0'+str(x[0]+1)+'.png') for x in enumerate(re.findall('pts_time:([\d.]+)',open('time.txt').read()))])
  return (beginstring_p,returnstring_p,count_p)
 
 def sidebyside(self,args_p,filter_p,beginstring_p,returnstring_p,count_p):
  pass

