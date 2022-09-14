#ffmpeg version 4.2.4-1ubuntu0.1
import datetime, os, re
import MISC.ffmpeg.libm as libm
import MISC.ffmpeg.utilm as utilm
class gifc:
 '''1.image,gif,video,audio overlay on source video
  2. pushes video to social media'''
 def __init__(self,inputfile=None):
  '''Enable debug True/False'''
  self.libi=libm.libc(inputfile,gifp=self)
  self.utili=utilm.utilc(inputfile,libp=self.libi)
  self.returnstring=''
  self.beginstring="ffmpeg -i "+inputfile+" " if inputfile else "ffmpeg "

 def videoaudioadd(self,*videoproperty):
  """videoproperty - ((<videoname>|<imagelist>)[<audioname>,<volume>],[filter,0-<length>],<timebreak>)
     *(('=one.mp4',('00:00:01-00:10:01,00:10:00-00:12:33')),('two.mp4',)),(('one.jpg','two.jpg'),('gifmp4','0-10'))"""
  print(f'gifc.videoaudioadd videoproperty={videoproperty} (self.libi.videowidth,self.libi.videoheight)={(self.libi.videowidth,self.libi.videoheight)}')
  concatstring='';count=0;
  for count,i in enumerate(videoproperty):
   print(f'<=>gifc.videoaudioadd i={i}')
   self.beginstring+=' '+' '.join(''.join([(' -ss '+(' -to '.join(re.split('-',i[1]))) if i[1]!=None else '')+' -i '+x]) for x in i[0][:2])+' '
   concatstring+=('[io'+str(2*count) if (str(self.libi.videowidth),str(self.libi.videoheight))!=self.libi.dimension(i[0][0]) else '['+str(2*count)+':v')+']['+(i[0][2]!=None and 'io'+str(2*count+1) or str(2*count+1)+':a')+']'
   self.returnstring+=('['+str(2*count)+':v]'+self.utili.scalepad(i[0][0],targetdimension=(self.libi.videowidth,self.libi.videoheight),getscalestr=True,upscale=True)+'[io'+str(2*count)+'];' if (str(self.libi.videowidth),str(self.libi.videoheight))!=self.libi.dimension(i[0][0]) else '')+('['+str(2*count+1)+':a]volume='+i[0][2]+'[io'+str(2*count+1)+'];' if i[0][2]!=None else '')
  self.returnstring+=concatstring+'concat=n='+str(int(len(re.findall(' -i ',self.beginstring))/2))+':v=1:a=1[io'+str(len(re.findall(' -i ',self.beginstring))-1)+'][aout];' if len(re.findall(' -i ',self.beginstring))>1 else ''
  print(f'<>gifm.videoaudioadd self.beginstring={self.beginstring} self.returnstring={self.returnstring} concatstring={concatstring} self.libi.duration={self.libi.duration}')

 def overlay(self,imagename,begintime,duration=None,position='(W-w)/2,(H-h)/2'):
  '''overlay png/gif/mov/mp4 over video
     imagename - name of image (png/gif/mov/mp4)
     begintime - when overlay starts hh:mm:ss.ms/ss.ms
     position - x,y of overlay W/2,H/2 or W*2 H*5'''
  print(f'><gifc.overlay imagename={imagename} begintime={begintime} duration={duration} position={position}')
  self.beginstring+=(("-loop 1 " if not re.search(r'[.](gif|mov|mp4|webm)$',imagename,re.I) else "-ignore_loop 0 " if re.search(r'[.]gif$',imagename,re.I) else "")+" -t "+str(duration)+" " if duration else "")+"-i "+imagename+" "
  count=int(re.sub(r'.*io(\d+)\];?.*',r'\1',self.returnstring))+1 if self.returnstring else 0
  self.returnstring+="["+str(len(re.findall(r' -i ',self.beginstring))-1)+":v]setpts=PTS+"+self.libi.getsecond(begintime)+"/TB[bio"+str(count)+"];" +("[0:v]" if not count else "[io"+str(count-1)+"]") + "[bio"+str(count)+"]" + self.libi.convertfilter(self.libi.co(position,imagename),begintime)+":eof_action=pass:format=auto[io"+str(count)+"];"
  print(f'<>gifm.overlay')

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
   return re.search('audio',self.libi.exiftool(filename,'MIME Type'),flags=re.I) if not type(filename)==tuple and os.path.exists(filename) else False
  def monotostereo(reffilename,filename,duration=None):#files can be both audio or video
   '''copy channelcount and sampling frequency of reffilename -> filename'''
   print(f'><gifc.stroke2.monotostereo reffilename={reffilename} filename={filename} duration={duration}')
   refdimension=self.libi.videoattribute(reffilename)
   dimension=self.libi.videoattribute(filename)
   print(f'<=>gifc.stroke2.monostereo refdimension={refdimension} dimension={dimension}')
   if (not refdimension[-3]==dimension[-3] or not refdimension[-2]==dimension[-2]) and not os.path.exists(re.sub(r'[.]mp3$','_stereo'+('_'+str(duration) if duration else '')+'.mp3',self.libi.adddestdir(filename))):
    self.libi.system('ffmpeg '+('-ss 0 -to '+str(duration) if duration else '')+' -i '+filename+(' -ar '+refdimension[-3] if not refdimension[-3]==dimension[-3] else '')+(' -ac '+str(2 if re.search(r'stereo',refdimension[-2],flags=re.I) else 1) if not refdimension[-2] == dimension[-2] else '')+' -y '+self.libi.adddestdir(re.sub(r'[.]mp3$','_stereo'+('_'+str(duration) if duration else '')+'.mp3',filename)))
   return re.sub(r'[.]mp3$',('_'+str(duration) if duration else '')+'.mp3',filename) if refdimension[-3]==dimension[-3] and refdimension[-2]==dimension[-2] else self.libi.adddestdir(re.sub(r'[.]mp3$','_stereo'+('_'+str(duration) if duration else '')+'.mp3',filename))

  self.videoaudioadd(*[i for i in arg if len(i)<=2])
  audiolist.append((('aout',1),(0,self.libi.duration)))
  for i in [i for i in arg if len(i)==3]: #overlapping and audio processing
   print(f'<=>gifc.stroke2 calling libi.tuple2funccal i={i}')
   self.libi.tuple2funccal(self.libi.filter[i[1][0]],i) if i[1] and type(i[1])==tuple else None
   audiolist.append(((i[0][1],i[0][2]==None and 1 or float(i[0][2])),tuple(round(float(self.libi.getsecond(x)),3) for x in re.split('-',(i[2] if re.search('-',i[2]) else i[2]+'-'+str(float(self.libi.getsecond(i[2]))+float(self.libi.getsecond(self.libi.exiftool(i[0][1],'Duration'))))))))) if not i[0][1]==None and re.search('audio',self.libi.exiftool(i[0][1],'MIME Type'),flags=re.I) else None
  print(f'<=>gifc.stroke2 audiolist={audiolist} \n self.beginstring={self.beginstring} \n self.returnstring={self.returnstring}')
 
  lastoffset=maxvolume=audiocount=0
  recordedaudiooffset="float(re.sub('_dot_','.',re.sub(r'^.*__(.*?_dot_.*?)_[.].*',r'\\1',x[0][0])))"
#  recordedaudiooffset="float(re.sub('_dot_','.',re.sub(r'^.*__(.*?_dot_.*?)_[.].*',r'\\1',j[0][0])))"
  for x in audiolist[1:]:
   if not re.search(r'\s+-i\s+'+x[0][0],self.beginstring):
    self.beginstring+=' -i  '+x[0][0]
  for i in sorted(set([y for i in audiolist for x in i[1:] for y in x]))[1:]:
   for j in audiolist:
#     result.append((j[0],lastoffset-j[1][0],i-j[1][0])) if j[1][0]<i<=j[1][1] else None
     result.append((j[0],(lastoffset if re.search('_dot_',j[0][0]) else lastoffset-j[1][0]),(i if re.search('_dot_',j[0][0]) else i-j[1][0]))) if j[1][0]<i<=j[1][1] else None
#     result.append((j[0],(lastoffset+eval(recordedaudiooffset) if re.search('_dot_',j[0][0]) else lastoffset-j[1][0]),(i+eval(recordedaudiooffset) if re.search('_dot_',j[0][0]) else i-j[1][0]))) if j[1][0]<i<=j[1][1] else None
   lastoffset=i
   print(f'<=>gifc.stroke2 {result=} {lastoffset=} {audiocount=}')
   maxvolume=max([x[0][1] for x in result])
   print(f'<=>gifc.stroke2 {maxvolume=}')
   if len(result)>1:
#    audiostring+=''.join([(r'['+str(re.findall(r'-i\s+(\S+)',self.beginstring).index(x[0][0]))+r':a]' if x[0][0]!='aout' else '[aout]')+'atrim='+str(round(x[1],3))+':'+str(round(x[2],3))+',volume='+str((x[0][1]/maxvolume)*len(result))+r',asetpts=PTS-STARTPTS[aio'+(str(re.findall(r'-i\s+(\S+)',self.beginstring).index(x[0][0]))+r'];' if x[0][0]!='aout' else r'aout];') for x in result])+''.join([r'[aio'+(str(re.findall(r'-i\s+(\S+)',self.beginstring).index(x[0][0]))+r']' if x[0][0]!='aout' else r'aout]') for x in result])+'amerge=inputs='+str(len(result))+'[aout'+str(audiocount)+r'];'
    audiostring+=''.join([(r'['+str(re.findall(r'-i\s+(\S+)',self.beginstring).index(x[0][0]))+r':a]' if x[0][0]!='aout' else '[aout]')+'atrim='+str(round((re.search(r'_dot_',x[0][0]) and eval(recordedaudiooffset) or 0)+x[1],3))+':'+str(round((re.search(r'_dot_',x[0][0]) and eval(recordedaudiooffset) or 0)+x[2],3))+',volume='+str((x[0][1]/maxvolume)*len(result))+r',asetpts=PTS-STARTPTS[aio'+(str(re.findall(r'-i\s+(\S+)',self.beginstring).index(x[0][0]))+r'];' if x[0][0]!='aout' else r'aout];') for x in result])+''.join([r'[aio'+(str(re.findall(r'-i\s+(\S+)',self.beginstring).index(x[0][0]))+r']' if x[0][0]!='aout' else r'aout]') for x in result])+'amerge=inputs='+str(len(result))+'[aout'+str(audiocount)+r'];'
   elif len(result)==1:
    audiostring+=(r'['+str(re.findall(r'-i\s+(\S+)',self.beginstring).index(result[0][0][0]))+r':a]' if result[0][0][0]!='aout' else '[aout]')+'atrim='+str(round(result[0][1],3))+':'+str(round(result[0][2],3))+r',asetpts=PTS-STARTPTS[aout'+str(audiocount)+'];'
   audiocount+=1
   result=[]
   print(f'TEST len(result)={len(result)} audiostring={audiostring}')
  audiostring=re.sub(r'^(.*):.*?(,asetpts.*)$',r'\1\2',audiostring)
  audiostring=re.sub(r'.*?(\[[^\]]+\])(?:\[[^\]]+\])?;$',r'\1',self.returnstring)+r'split='+str(audiocount)+'[vout]'*(audiocount)+';'+''.join(re.sub('aout','vout',re.sub('atrim','trim',re.sub('asetpts','setpts',re.sub(r'volume=[^,]+,','',re.sub('\[\w+\];',r'[vout'+str(count)+r'];',x))))) for count,x in enumerate(re.findall(r'\[aout\]atrim.*?;',audiostring)))+('[aout]' if re.search(r'\[aout\]',self.returnstring) else r'['+str(re.findall(r'-i\s+\S+',self.beginstring).index(re.sub(r'[.]mp4',r'.mp3',re.findall(r'-i\s+\S+',self.beginstring)[0])))+r':a]')+r'asplit='+str(audiocount)+'[aout]'*(audiocount)+';'+audiostring if audiocount else ''
  for i in range(audiocount):
   audiostring+='[vout'+str(i)+'][aout'+str(i)+']'
  audiostring+='concat=n='+str(audiocount)+':v=1:a=1[vout][aout]' if audiocount else ''
  print(f'<=>gifc.stroke2 {audiostring=}')
  self.libi.system(self.beginstring+" -filter_complex \""+re.sub(r';$','',self.returnstring+audiostring)+"\""+self.libi.vformat('mp4')+" -map \"[vout]\" -ac 2 -map \"[aout]\" -y "+self.libi.adddestdir("output.mp4" if not outputfile else outputfile))

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
