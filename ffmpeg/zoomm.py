import re
class zoomc:
 def __init__(self,libip):
  self.libi=libip
 def rotateandzoom(self,args_p,filter_p,beginstring_p,returnstring_p,count_p):
  '''"index:image:duration" timeoffset timeoffset'''
  imagename=self.libi.split(args_p[0])[1]
  imagesize=self.libi.dimension(imagename)
  duration=6
  if len(self.libi.split(args_p[0]))>=3 and self.libi.split(args_p[0])[2]: duration=self.libi.split(args_p[0])[2]
  zoomscalewidth=int(self.libi.videowidth) if imagesize[1]<imagesize[0] else int((imagesize[0]/imagesize[1])*int(self.libi.videoheight))
  zoomscaleheight=int(self.libi.videoheight) if imagesize[1]>imagesize[0] else int((imagesize[1]/imagesize[0])*int(self.libi.videowidth))
  for j in range(1,len(args_p)):
   self.libi.ffmpeg('ffmpeg -ss '+args_p[j]+' -t '+str(duration)+' -i input.mp4 -loop 1 -i '+imagename+' -i '+imagename+' -filter_complex "'+re.sub(r'^',r'[1]',re.sub(r'XX','-1:'+str(int(self.libi.videoheight)/3) if imagesize[1]>imagesize[0] else str(int(self.libi.videowidth)/3)+':-1',re.sub(r'YY',str(zoomscalewidth)+'x'+str(zoomscaleheight),filter_p)))+'" -y input'+str(count_p)+'.mp4')
   beginstring_p+="-i input"+str(count_p)+".mp4 "
   returnstring_p+="["+str(len(re.findall(r' -i ',beginstring_p))-1)+":v]setpts=PTS+"+self.libi.getsecond(args_p[j])+"/TB[bio"+str(count_p)+"];"+("[0:v]" if not count_p else "[io"+str(count_p-1)+"]")+"[bio"+str(count_p)+"]overlay=eof_action=pass[io"+str(count_p)+"];"
   count_p=count_p+1
  return (beginstring_p,returnstring_p,count_p)
