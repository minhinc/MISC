#ffmpeg version 4.2.4-1ubuntu0.1
import datetime, os, re
import MISC.ffmpeg.libm as libm
import MISC.ffmpeg.utilm as utilm
class gifc:
 '''1.image,gif,video,audio overlay on source video
  2. pushes video to social media'''
 def __init__(self,debug=False,inputfile=None):
  '''Enable debug True/False'''
  self.libi=libm.libc(debug,inputfile,gifp=self)
  self.utili=utilm.utilc(debug,inputfile,libp=self.libi)
  self.returnstring=''
  self.beginstring="ffmpeg -i "+inputfile+" " if inputfile else "ffmpeg "

 def replaceaudiobreakjoin(self,*videoproperty):
  """videoproperty - (<videoname>,<timebreak>)
     *(('=one.mp4',('00:00:01-00:10:01,00:10:00-00:12:33')),('two.mp4',))"""
  print(f'gifc.replaceaudiobreakjoin videoproperty={videoproperty} (self.libi.videowidth,self.libi.videoheight)={(self.libi.videowidth,self.libi.videoheight)}')
  concatstring='';count=0;
  for i in videoproperty:
   print(f'replaceaudiobreakjoin i={i}')
#   self.beginstring+=''.join([' -ss '+(' -to '.join(re.split('-',x)))+' -i '+re.sub(r'^=','',i[0])+' ' for x in re.findall(r'([^,\s]+\s*-\s*[^,\s]+)',i[1])]) if len(i)>1 else ' -i '+re.sub(r'^=','',i[0])+' '
   self.beginstring+=''.join([' -ss '+(' -to '.join(re.split('-',x)))+' -i '+re.sub(r'^=','',i[0])+' ' for x in (i[1] if type(i[1])==tuple else [i[1]])]) if len(i)>1 else ' -i '+re.sub(r'^=','',i[0])+' '
#   concatstring+=''.join([('[io' if (str(self.libi.videowidth),str(self.libi.videoheight))!=self.libi.dimension(re.sub(r'^=','',i[0])) else '[')+str(x+count)+('' if (str(self.libi.videowidth),str(self.libi.videoheight))!=self.libi.dimension(re.sub(r'^=','',i[0])) else ':v')+']['+str(x+count)+':a]' for x in range(len(re.findall('-',i[1] if len(i)>1 else '')) or 1)])
   concatstring+=''.join([('[io' if (str(self.libi.videowidth),str(self.libi.videoheight))!=self.libi.dimension(re.sub(r'^=','',i[0])) else '[')+str(x+count)+('' if (str(self.libi.videowidth),str(self.libi.videoheight))!=self.libi.dimension(re.sub(r'^=','',i[0])) else ':v')+']['+str(x+count)+':a]' for x in range(len(i[1] if type(i[1])==tuple else [i[1]]) if len(i)>1 else 1)])
#   self.returnstring+=''.join(['['+str(x+count)+':v]'+('scale='+self.dimension if int(re.split('x',self.dimension)[0])<=int(self.libi.dimension(re.sub(r'^=','',i[0]))[0]) or int(re.split('x',self.dimension)[1])<=int(self.libi.dimension(re.sub(r'^=','',i[0]))[1]) else 'pad='+re.sub('x',':',self.dimension)+r':(ow-iw)/2:(oh-ih)/2')+',setsar=sar=1'+'[io'+str(x+count)+'];' for x in range(len(re.findall('-',i[1] if len(i)>1 else '')) or 1)]) if re.search(r'^=',i[0]) else ''
#   self.returnstring+=''.join(['['+str(x+count)+':v]'+('scale='+(str(self.libi.videowidth)+":-1" if int(self.libi.dimension(re.sub(r'^=','',i[0]))[0])/self.libi.videowidth > int(self.libi.dimension(re.sub(r'^=','',i[0]))[1])/self.libi.videoheight else "-1:"+str(self.libi.videoheight))+',pad='+str(self.libi.videowidth)+':'+str(self.libi.videoheight)+r':(ow-iw)/2:(oh-ih)/2' if self.libi.videowidth<=int(self.libi.dimension(re.sub(r'^=','',i[0]))[0]) or self.libi.videoheight<=int(self.libi.dimension(re.sub(r'^=','',i[0]))[1]) else 'pad='+str(self.libi.videowidth)+':'+str(self.libi.videoheight)+r':(ow-iw)/2:(oh-ih)/2')+',setsar=sar=1'+'[io'+str(x+count)+'];' for x in range(len(re.findall('-',i[1] if len(i)>1 else '')) or 1)]) if not re.search(r'^=',i[0]) and (str(self.libi.videowidth),str(self.libi.videoheight))!=self.libi.dimension(i[0]) else ''
#   self.returnstring+=''.join(['['+str(x+count)+':v]'+('scale='+(str(self.libi.videowidth)+":-1" if int(self.libi.dimension(re.sub(r'^=','',i[0]))[0])/self.libi.videowidth > int(self.libi.dimension(re.sub(r'^=','',i[0]))[1])/self.libi.videoheight else "-1:"+str(self.libi.videoheight))+',pad='+str(self.libi.videowidth)+':'+str(self.libi.videoheight)+r':(ow-iw)/2:(oh-ih)/2' if self.libi.videowidth<=int(self.libi.dimension(re.sub(r'^=','',i[0]))[0]) or self.libi.videoheight<=int(self.libi.dimension(re.sub(r'^=','',i[0]))[1]) else 'pad='+str(self.libi.videowidth)+':'+str(self.libi.videoheight)+r':(ow-iw)/2:(oh-ih)/2')+',setsar=sar=1'+'[io'+str(x+count)+'];' for x in range(len(i[1] if type(i[1])==tuple else [i[1]]) if len(i)>1 else 1)]) if not re.search(r'^=',i[0]) and (str(self.libi.videowidth),str(self.libi.videoheight))!=self.libi.dimension(i[0]) else ''
   self.returnstring+=''.join(['['+str(x+count)+':v]'+self.utili.scalepad(i[0],targetdimension=(self.libi.videowidth,self.libi.videoheight),getscalestr=True)+'[io'+str(x+count)+'];' for x in range(len(i[1] if type(i[1])==tuple else [i[1]]) if len(i)>1 else 1)]) if not re.search(r'^=',i[0]) and (str(self.libi.videowidth),str(self.libi.videoheight))!=self.libi.dimension(i[0]) else ''
#   count+=len(re.findall('-',i[1] if len(i)>1 else '')) or 1
   count+=len(i[1] if type(i[1])==tuple else [i[1]]) if len(i)>1 else 1
  self.returnstring+=concatstring+'concat=n='+str(len(re.findall(' -i ',self.beginstring)))+':v=1:a=1[io'+str(len(re.findall(' -i ',self.beginstring))-1)+'][aout];' if len(re.findall(' -i ',self.beginstring))>1 else ''
  print(f'<>gifm.replaceaudiobreakjoin self.beginstring={self.beginstring} self.returnstring={self.returnstring} concatstring={concatstring} self.libi.duration={self.libi.duration}')

 def overlay(self,imagename,begintime,duration=None,position='(W-w)/2,(H-h)/2'):
  '''overlay png/gif/mov/mp4 over video
     imagename - name of image (png/gif/mov/mp4)
     begintime - when overlay starts hh:mm:ss.ms/ss.ms
     position - x,y of overlay W/2,H/2 or W*2 H*5'''
  print(f'><gifc.overlay imagename={imagename} begintime={begintime} duration={duration} position={position}')
#  self.beginstring+=(("-t "+str(duration)+" " if duration and float(self.libi.exiftool(audiofile,'Duration'))>duration else "")+"-i "+audiofile+" " if audiofile else "")+((("-loop 1 " if not re.search(r'[.](gif|mov|mp4)$',imagename,re.I) else "-ignore_loop 0 " if re.search(r'[.]gif$',imagename,re.I) else "")+"-t "+str(duration)+" " if duration else "")+"-i "+imagename+" " if imagename else "")
  self.beginstring+=(("-loop 1 " if not re.search(r'[.](gif|mov|mp4)$',imagename,re.I) else "-ignore_loop 0 " if re.search(r'[.]gif$',imagename,re.I) else "")+"-t "+str(duration)+" " if duration else "")+"-i "+imagename+" "
  count=int(re.sub(r'.*io(\d+)\];?.*',r'\1',self.returnstring))+1 if self.returnstring else 0
  self.returnstring+="["+str(len(re.findall(r' -i ',self.beginstring))-1)+":v]setpts=PTS+"+self.libi.getsecond(begintime)+"/TB[bio"+str(count)+"];" +("[0:v]" if not count else "[io"+str(count-1)+"]") + "[bio"+str(count)+"]" + self.libi.convertfilter(self.libi.co(position,imagename),begintime)+":eof_action=pass:format=auto[io"+str(count)+"];"

 def stroke2(self,*arg,outputfile=None):
  '''*arg - (<[=referent]videoname>,<timestamps>),(<videoname>,<timestamps>),((<video>,[audio],[volume]),[<filtermode>,<position>],<timestamps,[timestamp_duration]>)
  *arg - ('=VID.mp4','(00:01:00-00:02:00,00:03:00-00:04:20)'),('VID2.mp4','00:00:00-00:40:00'),(('longway.gif','longo.mp3',0.2),(25,55),(00:00:30-00:00:40,00:00:50))')'''
  print(f'><gifc.stroke2 arg={arg} outputfile={outputfile}')
  audiolist=[]
  result=[]
  audiostring='';audiocount=0;maxvolume=0
  filename=None
  lastoffset=0
  def audio(filename):
   return re.search('audio',self.libi.exiftool(filename,'MIME Type'),re.I) if not type(filename)==tuple and os.path.exists(filename) else False
  def monotostereo(reffilename,filename,duration=None):#files can be both audio or video
   '''copy channelcount and sampling frequency of reffilename -> filename'''
   print(f'monotostereo reffilename={reffilename} filename={filename} duration={duration}')
   refdimension=self.libi.videoattribute(reffilename)
   dimension=self.libi.videoattribute(filename)
   if (not refdimension[-2]==dimension[-2] or not refdimension[-1]==dimension[-1]) and not os.path.exists(re.sub(r'[.]mp3$','_stereo'+('_'+str(duration) if duration else '')+'.mp3',self.libi.adddestdir(filename))):
    self.libi.system('ffmpeg '+('-ss 0 -to '+str(duration) if duration else '')+' -i '+filename+(' -ar '+refdimension[-2] if not refdimension[-2]==dimension[-2] else '')+(' -ac '+str(2 if re.search(r'stereo',refdimension[-1],flags=re.I) else 1) if not refdimension[-1] == dimension[-1] else '')+' -y '+self.libi.adddestdir(re.sub(r'[.]mp3$','_stereo'+('_'+str(duration) if duration else '')+'.mp3',filename)))
   return self.libi.adddestdir(re.sub(r'[.]mp3$','_stereo'+('_'+str(duration) if duration else '')+'.mp3',filename))

  self.replaceaudiobreakjoin(*[i for i in arg if len(i)<=2])
  audiolist.append((('aout',1),(0,self.libi.duration)))
  for i in [i for i in arg if len(i)==3]: #overlapping and audio processing
   print(f'<=>gifc.stroke2 calling libi.tuple2funccal i={i}')
   self.libi.tuple2funccal(self.libi.filter[i[1][0]],i) if i[1] and type(i[1])==tuple else None
   audiolist.append((([x for x in (i[0] if type(i[0])==tuple else [i[0]]) if audio(x)][0],(i[0][-1] if type(i[0])==tuple and type(i[0][-1])==float else 1)),*[[float(self.libi.getsecond(y)) for y in re.split('-',x)] if re.search('-',x) else (float(x),'') for x in (i[2] if type(i[2])==tuple else [i[2]])])) if [x for x in (i[0] if type(i[0])==tuple else [i[0]]) if audio(x)] else None
  self.beginstring+=' '+' '.join(('-ss '+re.split('-',y)[0]+' -to '+re.split('-',y)[1] if y else '')+' -i '+re.sub(r'^=','',re.sub('[.]mp4$',r'.mp3',x[0])) for x in arg if len(x)<=2 for y in ((x[1] if type(x[1])==tuple else [x[1]]) if len(x)==2 else [None]))
  self.returnstring=re.sub(r'\[(?P<id>\d+):a\]',lambda m:r'['+str(int(m.group('id'))+[count for count,i in enumerate(re.findall(r'-i\s+(\S+)',self.beginstring,flags=re.I)) if i in [re.sub(r'=','',re.sub(r'[.]mp4$',r'.mp3',x[0])) for x in arg if len(x)<=2]][0])+r':a]',self.returnstring,flags=re.I)
  print(f'audiolist={audiolist} \n self.beginstring={self.beginstring} \n self.returnstring={self.returnstring}')
  self.libi.ffmpeg(self.beginstring+" -filter_complex \""+re.sub(r';$','',self.returnstring+audiostring)+"\" -map \""+re.sub(r'.*(\[[^\]]+\]);$',r'\1',self.returnstring)+"\" -ac 2 -q:a 4 -map "+("\"[aout]\"" if re.search(r'\[aout\];',self.returnstring) else str(len(re.findall(r'-i\s+\S+',self.beginstring))-1)+":a")+" -y "+self.libi.adddestdir("output.mp4" if not outputfile else outputfile))
 
  if len(audiolist)>1:
   self.libi.system('ffmpeg -i '+self.libi.adddestdir(outputfile)+' -y '+re.sub(r'(.*)[.]mp4$',r'\1'+'.mp3',self.libi.adddestdir(outputfile)))
   self.libi.system('sox -m -v 1 '+re.sub(r'(.*)[.]mp4$',r'\1'+'.mp3',self.libi.adddestdir(outputfile))+' '+' '.join('"|sox -v '+str(x[0][1])+' '+monotostereo(self.libi.adddestdir(outputfile),x[0][0],y[1]-y[0] if y[1] else None)+' -p pad '+str(y[0])+'"' for x in audiolist if not x[0][0]=='aout' for y in x[1:])+' '+self.libi.adddestdir(re.sub(r'[.]mp4$','_sox.mp3',outputfile)))
   self.libi.system('ffmpeg -i '+self.libi.adddestdir(outputfile)+' -i '+self.libi.adddestdir(re.sub(r'[.]mp4$','_sox.mp3',outputfile))+' -map 0:v -map 1:a -c copy -y '+self.libi.adddestdir(re.sub(r'[.]mp4$','_sox.mp4',outputfile)))
   os.rename(self.libi.adddestdir(re.sub(r'[.]mp4$','_sox.mp4',outputfile)),self.libi.adddestdir(outputfile))

 def push2socialmedia(self,socialmedia,jsondata=None):
  '''send data to socialmedia
   socialmedia - name of socialmedia,i.e youtube,facebook,linkedin,instagram,twitter
   data - json data i.e.
   youtube - file,title,description,keywords (,),category,privacyStatus,jsonfile'''
  self.libi.debug('><gifc.push2socialmedia jsondata',jsondata)
  if socialmedia=='youtube':
   socialmediastring="python3 upload_video.py "
   for key in jsondata:
    socialmediastring+="--"+key+"=\""+jsondata[key]+"\" "
   if re.search(r'y',input("******* youtube ********\n"+socialmediastring+"\n   ******************"+"\nwanna continue?(y/n)..."),re.I):
    self.libi.system(socialmediastring)
  if socialmedia=='facebook':
   pass
  if socialmedia=='linkedin':
   pass
  if socialmedia=='instagram':
   pass
  if socialmedia=='twitter':
   pass
