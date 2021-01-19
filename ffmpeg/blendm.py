import re
class blendc:
 '''##Blend##'''
 def __init__(self,libip):
  self.libi=libip
 def blendimage(self,args_p,filter_p,beginstring_p,returnstring_p,count_p):
  '''index[10]:<image>:<imagesize[20,30]>:<filterpos[S]>:<duration[6,3]>:<filternbr[I]>:<split[B]>:<multiply[F]>:<alpha[0-255]>:transitiontime[0-4]'''
  index,image,imagesize,filterpos,duration,filternum,split,multiply,alpha,transitiontime=self.libi.split(args_p[0],(None,'',None,'(W-w)/2,(H-h)/2','6,0',filter_p,False,0.0,255,0.0))
  if imagesize:imagesize=tuple((int(i) for i in re.findall(r'\d+',imagesize)))
  duration=tuple((int(i) for i in (re.findall(r'\d+',duration) if len(re.findall(r'\d+',duration))==2 else re.findall(r'\d+',duration)+['0'])))
  self.libi.debug("blendc::blendimage><",index,image,imagesize,filterpos,duration,filternum,split,multiply)
  if not image:
   for j in range(1,len(args_p)):
    self.libi.ffmpeg('ffmpeg -ss '+args_p[j]+' -t '+str(duration[0])+' -i input.mp4 -y tmp'+str(count_p)+'.mp4')
    beginstring_p,returnstring_p,count_p=self.libi.blendimage([args_p[0],str(float(self.libi.getsecond(args_p[j]))-duration[0])],filternum,beginstring_p,returnstring_p,count_p,'tmp'+str(count_p)+'.mp4',(int(self.libi.videowidth/2),int(self.libi.videoheight/2)),(duration[0],1),filterpos,split_p=True,multiply_p=2.0)
   return beginstring_p,returnstring_p,count_p
  else:
   return self.libi.blendimage(args_p,filternum,beginstring_p,returnstring_p,count_p,image,imagesize,duration,filterpos,split_p=split,multiply_p=multiply,transitiontime_p=transitiontime,alpha_p=alpha)
