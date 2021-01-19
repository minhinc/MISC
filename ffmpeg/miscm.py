import re
class miscc:
 '''##misc##'''
 def __init__(self,libip):
  self.libi=libip

 def scenetransition(self,args_p,filter_p,beginstring_p,returnstring_p,count_p):
  '''<index[50]>'''
  self.libi.ffmpeg('ffmpeg -i input.mp4 -filter_complex "'+filter_p)
  print([(self.libi.getsecond(x[1]),'img0'+str(x[0]+1)+'.png') for x in enumerate(re.findall('pts_time:([\d.]+)',open('time.txt').read()))])
  return (beginstring_p,returnstring_p,count_p)

 def breakvideo(self,args_p,filter_p,beginstring_p,returnstring_p,count_p):
  '''<index[51]:videofile:slice[0-40,40-00:01:30,00:02:00-140]'''
  index,videofile,slice=self.libi.split(args_p[0],(None,'',''))
  print("slice {}".format(slice))
  slice=re.sub(r'\\:',':',slice)
  self.libi.debug("miscc::breakvideo><",index,videofile,slice)
  print("Make sure Audacity improved audio is replaced")
  for count,i in enumerate(re.split(r',',slice)):
   self.libi.ffmpeg("ffmpeg -ss "+re.split(r'-',i)[0]+" -t "+str(float(self.libi.getsecond(re.split(r'-',i)[1]))-float(self.libi.getsecond(re.split(r'-',i)[0])))+" -i "+videofile+" -c copy -y input"+str(count)+".mp4")
  return (beginstring_p,returnstring_p,count_p)

 def addvideo(self,args_p,filter_p,beginstring_p,returnstring_p,count_p):
  '''<index[52]:videofilelist[videofile1,><videofile2,videofile3...]'''
  index,videofilelist=self.libi.split(args_p[0],(None,''))
  videofilelist=re.split(r',',videofilelist)
  dimension,fps,samplerate,channel=self.libi.videoattribute(re.sub(r'><(.*)',r'\1',[i for i in videofilelist if re.search(r'^><',i)][0]))
  self.libi.debug("miscc::addvideo><",index,videofilelist,dimension,fps,samplerate,channel)
  print("Make sure Audacity improved audio is replaced")
  concatstring=''
  videofilelist=[re.sub(r'^><',r'',i) for i in videofilelist]
  for j in range(len(videofilelist)):
   if self.libi.videoattribute(videofilelist[j])!=(dimension,fps,samplerate,channel):
    self.libi.ffmpeg("ffmpeg -i "+videofilelist[j]+" -vf \"pad=w="+dimension[0]+":h="+dimension[1]+":x=(ow-iw)/2:y=(oh-ih)/2:color=black@0\" -r "+fps+" -ar "+samplerate+" -ac "+str(['mono','stereo'].index(channel)+1)+" -y "+re.sub(r'(.*)[.].*',r'\1',videofilelist[j])+"_tmp.mp4")
    videofilelist[j]=re.sub(r'(.*)[.].*',r'\1',videofilelist[j])+"_tmp.mp4"
   self.libi.ffmpeg("ffmpeg -i "+videofilelist[j]+" -c copy -bsf:v h264_mp4toannexb -f mpegts temp"+str(j)+".ts")
   concatstring+="temp"+str(j)+".ts|"
  self.libi.ffmpeg("ffmpeg -i \"concat:"+re.sub(r'\|$','',concatstring)+"\" -y output.mp4")
  return (beginstring_p,returnstring_p,count_p)

 def replaceaudio(self,args_p,filter_p,beginstring_p,returnstring_p,count_p):
  '''index[53]:videofile[mp4]:audiofile[mp3]'''
  print("**********************")
  print("audiofile must be from audocity")
  print("**********************")
  self.libi.ffmpeg("ffmpeg -i "+videofile+" -i "+audiofile+" -map 0:v -map 1:a -c copy -y output.mp4")
  return (beginstring_p,returnstring_p,count_p)
