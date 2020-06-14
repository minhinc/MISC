import re
class blendc:
 '''##Blend##'''
 def __init__(self,libip):
  self.libi=libip
 def blendimage(self,args_p,filter_p,beginstring_p,returnstring_p,count_p):
  """index transitiontimestamp """
  for j in range(1,len(args_p)):
   duration=re.sub(r'.*T\/(\d+).*',r'\1',filter_p)
   self.libi.ffmpeg('ffmpeg -ss '+str(float(self.libi.getsecond(args_p[j]))-0.25)+' -i input.mp4 -vframes 1 -q:v 2 -y tmp.png')
   self.libi.ffmpeg('ffmpeg -ss '+str(float(self.libi.getsecond(args_p[j]))-0.25)+' -t '+duration+' -i input.mp4 -y tmp.mp4')
   self.libi.ffmpeg('ffmpeg -i tmp.png -i tmp.mp4 -filter_complex "'+re.sub(r'^',r'[0][1:v]',filter_p)+'" -y input'+str(count_p)+'.mp4')
   beginstring_p+="-i input"+str(count_p)+".mp4 "
   returnstring_p+="["+str(len(re.findall(r' -i ',beginstring_p))-1)+":v]setpts=PTS+"+str(float(self.libi.getsecond(args_p[j]))-0.25)+"/TB[bio"+str(count_p)+"];"+("[0:v]" if not count_p else "[io"+str(count_p-1)+"]")+"[bio"+str(count_p)+"]overlay=eof_action=pass[io"+str(count_p)+"];"
   count_p=count_p+1
  return (beginstring_p,returnstring_p,count_p)

 def sidebyside(self,args_p,filter_p,beginstring_p,returnstring_p,count_p):
  """index transitiontimestamp """
  for j in range(1,len(args_p)):
   self.libi.ffmpeg('ffmpeg -ss '+args_p[j]+' -t 4.5 -i input.mp4 -c copy -y tmp1.mp4')
   self.libi.ffmpeg('ffmpeg -ss '+str(float(self.libi.getsecond(args_p[j]))-5)+' -t 6 -i input.mp4 -c copy -y tmp.mp4')
   self.libi.ffmpeg('ffmpeg -i tmp.mp4 -i tmp1.mp4 -filter_complex "'+re.sub(r'^',r'[0]',filter_p)+'" -y input'+str(count_p)+'.mp4')
   beginstring_p+="-i input"+str(count_p)+".mp4 "
   returnstring_p+="["+str(len(re.findall(r' -i ',beginstring_p))-1)+":v]setpts=PTS+"+str(float(lib.getsecond(args_p[j]))-5)+"/TB[bio"+str(count_p)+"];"+("[0:v]" if not count_p else "[io"+str(count_p-1)+"]")+"[bio"+str(count_p)+"]overlay=eof_action=pass[io"+str(count_p)+"];"
   count_p=count_p+1
  return (beginstring_p,returnstring_p,count_p)
