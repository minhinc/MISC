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
  filterpos1=self.libi.convertfilter(str(round(self.libi.getposition(filterpos,zoomimagesize)[0][2]+((self.libi.getposition(filterpos,(zoomimagesize[0]/3,zoomimagesize[1]/3))[0][2]+(zoomimagesize[0]/6)/self.libi.videowidth)-(self.libi.getposition(filterpos,zoomimagesize)[0][2]+(zoomimagesize[0]/2)/self.libi.videowidth)),3))+'*W,'+str(round(self.libi.getposition(filterpos,zoomimagesize)[1][2]+((self.libi.getposition(filterpos,(zoomimagesize[0]/3,zoomimagesize[1]/3))[1][2]+(zoomimagesize[1]/6)/self.libi.videoheight)-(self.libi.getposition(filterpos,zoomimagesize)[1][2]+(zoomimagesize[1]/2)/self.libi.videoheight)),3))+'*H',False)

  filterpos2=self.libi.convertfilter(str(self.libi.getposition(filterpos,zoomimagesize)[0][2])+'*W,'+str(self.libi.getposition(filterpos,zoomimagesize)[1][2])+'*H',False)
  alpha=re.sub(r'.*w\)?(.*),.*',r'\1',filterpos) if re.search(r'w',filterpos) else '*'+str(min(1.0,round((self.libi.videowidth*float(re.findall(r'\d+(?:[.]\d+)?',filterpos)[0])/(self.libi.videowidth-zoomimagesize[0]/3)),3)))
  beta=re.sub(r'.*h\)?(.*)',r'\1',filterpos) if re.search(r'h',filterpos) else '*'+str(min(1.0,round((self.libi.videoheight*float(re.findall(r'\d+(?:[.]\d+)?',filterpos)[1])/(self.libi.videoheight-zoomimagesize[1]/3)),3)))

#  glassscaleblendzoom2="["+str(1)+"]scale="+(str(int(2.0*self.videowidth)) if self.videowidth>=self.videoheight else '-1')+":"+(str(int(2.0*self.videoheight)) if self.videoheight>self.videowidth else '-1')+",format=yuva422p,pad="+str(multiplyfactor)+"*iw:"+str(multiplyfactor)+"*ih:(ow-iw)"+alpha+":(oh-ih)"+beta+":color=black@0,zoompan=z='min(zoom+0.01,"+str(multiplyfactor)+")':x=iw"+alpha+"-(iw/zoom)"+alpha+":y=ih"+beta+"-(ih/zoom)"+beta+":d="+str(duration_p[1]*25)+":s="+str(int(imagesize[0]*multiplyfactor))+"x"+str(int(imagesize[1]*multiplyfactor))+",setpts=PTS+"+str(duration_p[0])+"/TB[i];[bg][i]overlay=(W-w)"+alpha+":(H-h)"+beta+":shortest=1:enable='lte(t,"+str(duration_p[0]+duration_p[1])+")'"  if multiply_p and duration_p[1] else ""

  for j in range(1,len(args_p)):
   self.libi.ffmpeg('ffmpeg -ss '+args_p[j]+' -t '+str(duration)+' -i input.mp4 -loop 1 -i '+image+' -i '+image+' -filter_complex "'+re.sub(r'^',r'[1]',re.sub(r'XX1',str(int(zoomimagesize[0]/3))+':-1',re.sub(r'XX2',str(int(zoomimagesize[0]))+':-1',re.sub(r'ALPHA',alpha,re.sub(r'BETA',beta,re.sub(r'YY',str(zoomimagesize[0])+'x'+str(zoomimagesize[1]),re.sub(r'FF1',filterpos1,re.sub(r'FF2','overlay=(W-w)'+alpha+":(H-h)"+beta,self.libi.filterlist[filter_p][0]))))))))+'" -y input'+str(count_p)+'.mp4')
   beginstring_p+="-i input"+str(count_p)+".mp4 "
   returnstring_p+="["+str(len(re.findall(r' -i ',beginstring_p))-1)+":v]setpts=PTS+"+self.libi.getsecond(args_p[j])+"/TB[bio"+str(count_p)+"];"+("[0:v]" if not count_p else "[io"+str(count_p-1)+"]")+"[bio"+str(count_p)+"]overlay=eof_action=pass[io"+str(count_p)+"];"
   count_p=count_p+1
  return (beginstring_p,returnstring_p,count_p)
