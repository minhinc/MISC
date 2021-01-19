import re
class zoomc:
 '''zoomm::zoomc'''
 def __init__(self,libip):
  self.libi=libip
 def rotateandzoom(self,args_p,filter_p,beginstring_p,returnstring_p,count_p):
  '''index[20]:image:filterpos:duration:zoomimagesize timeoffset'''
  index,image,filterpos,duration,zoomimagesize,alpha=self.libi.split(args_p[0],(None,None,'(W-w)/2,(H-h)/2',4,str(self.libi.videowidth)+','+str(self.libi.videoheight),255))
  zoomimagesize=self.libi.scale(image,self.dimension(image) if not zoomimagesize else tuple(int(i) for i in re.findall(r'\d+',zoomimagesize)))
  self.libi.debug("zoomc::rotateandzoom><",index,image,filterpos,duration,zoomimagesize,alpha)
  alpha=re.sub(r'.*w\)?(.*),.*',r'\1',filterpos) if re.search(r'w',filterpos) else '*'+str(min(1.0,round((self.libi.videowidth*float(re.findall(r'\d+(?:[.]\d+)?',filterpos)[0])/(self.libi.videowidth-zoomimagesize[0]/3)),3)))
  beta=re.sub(r'.*h\)?(.*)',r'\1',filterpos) if re.search(r'h',filterpos) else '*'+str(min(1.0,round((self.libi.videoheight*float(re.findall(r'\d+(?:[.]\d+)?',filterpos)[1])/(self.libi.videoheight-zoomimagesize[1]/3)),3)))
  if zoomimagesize[0]>=zoomimagesize[1]:
   W1=1.2; H1=round(1.2*zoomimagesize[0]/zoomimagesize[1],3)
  else:
   W1=round(1.2*zoomimagesize[1]/zoomimagesize[0],3);H1=1.2
  smallimagex=(self.libi.getposition(filterpos,(zoomimagesize[0]/3,zoomimagesize[1]/3))[0][2]*self.libi.videowidth+zoomimagesize[0]/6-(self.libi.getposition(filterpos,(W1*zoomimagesize[0]/3,H1*zoomimagesize[1]/3))[0][2]*self.libi.videowidth+(W1*zoomimagesize[0]/3)/2))/self.libi.videowidth+self.libi.getposition(filterpos,(W1*zoomimagesize[0]/3,H1*zoomimagesize[1]/3))[0][2]
  smallimagey=(self.libi.getposition(filterpos,(zoomimagesize[0]/3,zoomimagesize[1]/3))[1][2]*self.libi.videoheight+zoomimagesize[1]/6-(self.libi.getposition(filterpos,(W1*zoomimagesize[0]/3,H1*zoomimagesize[1]/3))[1][2]*self.libi.videoheight+(H1*zoomimagesize[1]/3)/2))/self.libi.videoheight+self.libi.getposition(filterpos,(W1*zoomimagesize[0]/3,H1*zoomimagesize[1]/3))[1][2]
#  beginstring_p+=' -loop 1 -i '+image+' -i '+image+' '
  for j in range(1,len(args_p)):
   self.libi.ffmpeg('ffmpeg -ss '+args_p[j]+' -t '+str(duration)+' -i input.mp4 -loop 1 -i '+image+' -i '+image+' -filter_complex "'+re.sub(r'^',r'[1]',re.sub(r'XX1',str(int(zoomimagesize[0]/3))+':-1',re.sub(r'XX2',str(int(zoomimagesize[0]*2))+':-1',re.sub(r'W1',str(W1),re.sub(r'H1',str(H1),re.sub(r'ALPHA',alpha,re.sub(r'BETA',beta,re.sub(r'YY',str(zoomimagesize[0])+'x'+str(zoomimagesize[1]),re.sub(r'FF1',self.libi.convertfilter(str(smallimagex)+','+str(smallimagey),False),re.sub(r'FF2','overlay=(W-w)'+alpha+":(H-h)"+beta,self.libi.filterlist[filter_p][0]))))))))))+'" -y input'+str(count_p)+'.mp4')
   beginstring_p+="-i input"+str(count_p)+".mp4 "
   returnstring_p+="["+str(len(re.findall(r' -i ',beginstring_p))-1)+":v]setpts=PTS+"+self.libi.getsecond(args_p[j])+"/TB[bio"+str(count_p)+"];"+("[0:v]" if not count_p else "[io"+str(count_p-1)+"]")+"[bio"+str(count_p)+"]overlay=eof_action=pass[io"+str(count_p)+"];"
   count_p=count_p+1
#   returnstring_p+=re.sub(r'^',"["+str(len(re.findall(r' -i ',beginstring_p))-2)+":v]",re.sub(r'\[2\]',"["+str(len(re.findall(r' -i ',beginstring_p))-1)+":v]",re.sub(r'\[0\]',"[0:v]" if not count_p else "[io"+str(count_p-1)+"]",re.sub(r'XX1',str(int(zoomimagesize[0]/3))+':-1',re.sub(r'XX2',str(int(zoomimagesize[0]*2))+':-1',re.sub(r'W1',str(W1),re.sub(r'H1',str(H1),re.sub(r'ALPHA',alpha,re.sub(r'BETA',beta,re.sub(r'YY',str(zoomimagesize[0])+'x'+str(zoomimagesize[1]),re.sub(r'FF1',self.libi.convertfilter(str(smallimagex)+','+str(smallimagey),False),re.sub(r'FF2','overlay=(W-w)'+alpha+":(H-h)"+beta,self.libi.filterlist[filter_p][0]))))))))))))+":enable='lte(t,"+str(float(self.libi.getsecond(args_p[j]))+duration)+")'[io"+str(count_p)+"];"
#   count_p=count_p+1
  return (beginstring_p,returnstring_p,count_p)
