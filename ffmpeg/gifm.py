#ffmpeg version 4.2.4-1ubuntu0.1
import datetime, os, re
from PIL import Image
import MISC.ffmpeg.libm as libm
import MISC.ffmpeg.utilm as utilm
from MISC.utillib.util import Util
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
  '''(('minhinc/VID_20230223_173611.mp4', '00:00:10-00:00:20'), ('/home/minhinc/Videos/simplescreenrecorder-2023-01-12_14.35.38.mp4', '00:00:02-00:00:20'), ('/home/minhinc/Videos/simplescreenrecorder-2023-01-12_14.35.38.mp4', '00:10:00-00:13:00'))'''
  print(f'gifc.videoaudioadd {videoproperty=} {(self.libi.videowidth,self.libi.videoheight)=}')
  for i in videoproperty:
   print(f'<=>gifc.videoaudioadd i={i}')
#   self.beginstring+=' '+' '.join(''.join([(' -ss '+(' -to '.join(re.split('-',i[1]))) if i[1]!=None else '')+' -i '+x]) for x in i[0][:2])+' '
   self.beginstring+=len(i)==1 and ' -i '+i[0]+' -i '+re.sub('[.]\w+$','.mp3',i[0]) or ' '.join(re.sub('^(.*?)-(.*?)$',' -ss '+r'\1'+' -to '+r'\2'+' -i '+i[0]+' -ss '+r'\1'+' -to '+r'\2'+' -i '+re.sub('[.]\w+$','.mp3',i[0]),x) for x in (type(i[1])==tuple and i[1] or (i[1],)))
#  self.returnstring+=''.join('['+str(count)+':v]'+self.utili.scalepad(x,targetdimension=(self.libi.videowidth,self.libi.videoheight),getscalestr=True,upscale=True)+'[io'+str(count)+'];' if not count%2 and (str(self.libi.videowidth),str(self.libi.videoheight))!=self.libi.dimension(x) else '' for count,x in enumerate(re.findall('-i\s+(\S+)',self.beginstring)))+''.join((f'[io{count}]' if (str(self.libi.videowidth),str(self.libi.videoheight))!=self.libi.dimension(x) else f'[{count}:v]') if not count%2 else f'[{count}:a]' for count,x in enumerate(re.findall('-i\s+(\S+)',self.beginstring)))+'concat=n='+str(len(re.findall(' -i ',self.beginstring))//2)+':v=1:a=1[io'+str(len(re.findall(' -i ',self.beginstring))-1)+'][aout];'
  print(f'TEST {self.beginstring=}')
  self.returnstring+=''.join('['+str(count)+':v]'+self.utili.scalepad(re.sub(r'_\d+x\d+([.]\w+)$',r'\1',x),scaledimension=re.search('_\d+x\d+[.]\w+$',x) and re.sub(r'^.*_(\d+x\d+)[.]\w+$',r'\1',x) or None,getscalestr=True)+'[io'+str(count)+'];' if not count%2 and (str(self.libi.videowidth),str(self.libi.videoheight))!=self.libi.dimension(re.sub(r'_\d+x\d+([.]\w+)$',r'\1',x)) else '' for count,x in enumerate(re.findall('-i\s+(\S+)',self.beginstring)))+''.join((f'[io{count}]' if (str(self.libi.videowidth),str(self.libi.videoheight))!=self.libi.dimension(re.sub(r'_\d+x\d+([.]\w+)$',r'\1',x)) else f'[{count}:v]') if not count%2 else f'[{count}:a]' for count,x in enumerate(re.findall('-i\s+(\S+)',self.beginstring)))+'concat=n='+str(len(re.findall(' -i ',self.beginstring))//2)+':v=1:a=1[io'+str(len(re.findall(' -i ',self.beginstring))-1)+'][aout];'
  self.beginstring=re.sub('_\d+x\d+([.]\w+)',r'\1',self.beginstring)
  '''
  concatstring+=('[io'+str(count) if (str(self.libi.videowidth),str(self.libi.videoheight))!=self.libi.dimension(i[0]) else '['+str(count)+':v')+']['+(i[0][2]!=None and 'io'+str(2*count+1) or str(2*count+1)+':a')+']'
  self.returnstring+=('['+str(2*count)+':v]'+self.utili.scalepad(i[0][0],targetdimension=(self.libi.videowidth,self.libi.videoheight),getscalestr=True,upscale=True)+'[io'+str(2*count)+'];' if (str(self.libi.videowidth),str(self.libi.videoheight))!=self.libi.dimension(i[0][0]) else '')+('['+str(2*count+1)+':a]volume='+i[0][2]+'[io'+str(2*count+1)+'];' if i[0][2]!=None else '')
  self.returnstring+=concatstring+'concat=n='+str(int(len(re.findall(' -i ',self.beginstring))/2))+':v=1:a=1[io'+str(len(re.findall(' -i ',self.beginstring))-1)+'][aout];' if len(re.findall(' -i ',self.beginstring))>1 else ''
  print(f'<>gifm.videoaudioadd self.beginstring={self.beginstring} self.returnstring={self.returnstring} concatstring={concatstring} self.libi.duration={self.libi.duration}')
  '''
  print(f'<>gifm.videoaudioadd {self.beginstring=} {self.returnstring=}')

# def overlay(self,imagename,begintime,duration=None,position='(W-w)/2,(H-h)/2'):
 def overlay(self,*overlayproperty):
  '''\
  (('  Hello Bang  \\nSing Sang\\nWelcome', ('71', 'bhorizontalopen', '00t', '01t', '00t'), '148.0-158.0'), (('../../../imageglobe/image/fevicon-48x48.png', '../../../imageglobe/image/li-slide-pipefork.png', '../../../imageglobe/image/li-slide-pageentry.png'), ('55', 'bfadeinout', 'oup'), '168.0-178.0'))'''
#  print(f'><gifc.overlay imagename={imagename} begintime={begintime} duration={duration} position={position}')
  print(f'><gifc.overlay {overlayproperty=}')
  imagenamelist=[]
  duration=None
  filter=[]
  text=[]
  tmp=None
  for i in overlayproperty:
   i=list(i)
   text=[]
#   filter=[re.sub(r'^(?P<id>.*?d=)(?P<id2>\d+)(?P<id3>.*?out.*s=)\d+(?P<id4>.*)$',lambda m:m.group('id')+m.group('id2')+m.group('id3')+str(duration-int(m.group('id2')))+m.group('id4'),self.libi.filter[re.search(r'^[oO]',j) and 'overlay' or 'blend'][j[1:].lower()]) for j in (not type(i[1])==str and i[1][1:] or []) if not re.search(r'^\d+',j)]
   filter=[(j,self.libi.filter[re.search(r'^[oO]',j) and 'overlay' or 'blend'][re.sub(r'^(.*?)\d+%\d+%$',r'\1',j[1:]).lower()]) for j in (not type(i[1])==str and i[1][1:] or []) if not re.search(r'^\d+',j)]
   filter.append(('onormal',self.libi.filter['overlay']['normal'])) if [x for x in filter if re.search('fade.*(in|out)',x[1],flags=re.I)] and len(filter)==1 else None
   if type(i[0])==str and re.search('video',self.libi.exiftool(re.sub(r'^(.*?)_\d+:\d+:[.\d]+.*?([.]\w+)$',r'\1\2',i[0]),'MIME Type'),flags=re.I):
    if re.search(r'_\d+:\d+:[.\d]+.*?[.]\w+$',i[0]):
     tmp=re.sub(r'^(.*?)_\d+:\d+:[.\d]+.*?([.]\w+)$',r'\1\2',i[0])
     for j in re.split('_',re.sub(r'^.*?_(\d+:\d+:[.\d]+.*?)[.]\w+$',r'\1',i[0])):
      i[0]=[] if type(i[0])==str else i[0]
      i[0].append(self.libi.outimagename(tmp))
      self.libi.system('ffmpeg -ss '+re.split('-',j)[0]+(' -to '+re.split('-',j)[1] if re.search('-',j) else '')+' -i '+tmp+(self.libi.vformat('mov') if re.search(r'[.]mov$',i[0][-1]) else self.libi.vformat('mp4'))+' -c copy -y '+i[0][-1])
    print(f'overlay TEST {j=} {i[0]=}')
    if not type(i[0])==str:
     for ii in range(len(i[0])):
      tmp=[int(re.sub('^(.*)s$',r'\1',x)) for x in (not type(i[1])==str and i[1][1:] or []) if re.search('^\d+s$',x)]
      if tmp:
       i[0][ii]=self.utili.scalepad(i[0][ii],scaledimension=Util.scaledwidthheight(i[0][ii],((self.libi.videowidth*tmp[0])//100,(self.libi.videoheight*tmp[0])//100),libi=self.libi),padposition=None)
      tmp=[re.sub('^(.*)a$',r'\1',x) for x in (not type(i[1])==str and i[1][1:] or []) if re.search('^[.\d]+a$',x)]
      if tmp:
       i[0][ii]=self.utili.addalpha2(i[0][ii],alpha=tmp[0])
    else:
     tmp=[int(re.sub('^(.*)s$',r'\1',x)) for x in (not type(i[1])==str and i[1][1:] or []) if re.search('^\d+s$',x)]
     if tmp:
      i[0]=self.utili.scalepad(i[0],scaledimension=Util.scaledwidthheight(i[0],((self.libi.videowidth*tmp[0])//100,(self.libi.videoheight*tmp[0])//100),libi=self.libi),padposition=None)
     tmp=[re.sub('^(.*)a$',r'\1',x) for x in (not type(i[1])==str and i[1][1:] or []) if re.search('^[.\d]+a$',x)]
     if tmp:
      i[0]=self.utili.addalpha2(i[0],alpha=tmp[0])
#    else:
#     tmp=re.sub(r'^(.*?)_\d+:\d+:[.\d]+.*?([.]\w+)$',r'\1\2',i[0])
   elif type(i[0])==str and re.search('image',self.libi.exiftool(i[0],'MIME Type'),flags=re.I):
    tmp=[int(re.sub('^(.*)s$',r'\1',x)) for x in (not type(i[1])==str and i[1][1:] or []) if re.search('^\d+s$',x)]
    if tmp:
     print(f'overlay1 {i[0]=}')
     img=Image.open(i[0])
#     img.resize(((self.libi.videowidth*tmp[0])//100,(img.height*self.libi.videowidth*tmp[0])//(100*img.width))).save('logdir/'+re.sub(r'.*/(.*)$',r'\1',i[0]))
     img.resize(Util.resizeimagesize((self.libi.videowidth,self.libi.videoheight),img.size,float(tmp[0]))).save('logdir/'+re.sub(r'.*/(.*)$',r'\1',i[0]))
     i[0]='logdir/'+re.sub(r'.*/(.*)$',r'\1',i[0])
     print(f'overlay TEST {tmp=} {i[0]=}')
    tmp=[re.sub('^(.*)a$',r'\1',x) for x in (not type(i[1])==str and i[1][1:] or []) if re.search('^[.\d]+a$',x)]
    if tmp:
     print(f'overlay TEST {tmp=} {i[0]=}')
     i[0]=self.utili.addalpha2(i[0],alpha=tmp[0])
   elif type(i[0])==str and not os.path.exists(i[0]):
    for count,j in enumerate([j for j in (not type(i[1])==str and i[1][1:] or ['00t']) if re.search(r'^\d+',j)]):
     text.append([re.split(r'\\n',i[0])[count]]+list(self.libi.filter[j]))
    i[0]=self.utili.text2image(text=text)
#    imagenamelist.append((self.utili.image2mov(i[0],filtername=re.sub(r'(?P<id>,fade=out:st=)\d+',lambda m:m.group('id')+str(duration-1),self.libi.filter[re.search('^[oO]',i[1][1]) and 'overlay' or 'blend'][i[1][1][1:].lower()],flags=re.I),duration=duration) if type(i[1])==tuple and re.search(r'^[ob]',i[1][1],flags=re.I) else i[0],re.split('-',j)[0],self.libi.getsecond(j) if re.search('-',j) else float(self.libi.getsecond(self.libi.exiftool(i[0],'Duration'))),type(i[1])==tuple and i[1][0] or i[1]))
   for count,j in enumerate((type(i[2])==tuple and i[2] or (i[2],))):
    print(f'TEST {i=} {text=} {filter=} {duration=} {j=} {count=} ')
    tmp=i[0] if type(i[0])==str else i[0][count] if count<len(i[0]) else i[0][-1]#for triple length overlapping .mp4 subsections
#    duration=re.search('-',j) and float(self.libi.getsecond(j)) or float(self.libi.getsecond(self.libi.exiftool(tmp,'Duration')))
    duration=round(re.search('-',j) and float(self.libi.getsecond(j)) or re.search('image',self.libi.exiftool(tmp,'MIME Type')) and type(i[1])==str and not re.search('[.]gif$',tmp,flags=re.I) and self.libi.duration-float(self.libi.getsecond(j)) or float(self.libi.getsecond(self.libi.exiftool(tmp,'Duration'))),3)
    filter=[(x[0],re.sub(r'^(?P<id>fade.*?in.*?d=)(?P<id2>\d+)(?P<id3>.*?out.*?st=)[\d.]+(?P<id4>.*)$',lambda m:m.group('id')+m.group('id2')+m.group('id3')+str(duration-int(m.group('id2')))+m.group('id4'),x[1])) for x in filter]
#    imagenamelist.append((self.utili.image2mov(tmp,filter=filter,duration=duration) if filter else tmp,re.split('-',j)[0],self.libi.getsecond(j) if re.search('-',j) else float(self.libi.getsecond(self.libi.exiftool(tmp,'Duration'))),type(i[1])==tuple and i[1][0] or i[1]))
    imagenamelist.append((self.utili.image2mov(tmp,filter=filter,duration=duration) if filter else tmp,re.split('-',j)[0],duration,type(i[1])==tuple and i[1][0] or i[1]))
  print(f'<=>gif.overlay {imagenamelist=}')
  for imagename,begintime,duration,position in imagenamelist:
   self.beginstring+=((" -loop 1 " if not re.search(r'[.](gif|mov|mp4|webm)$',imagename,re.I) else " -ignore_loop 0 " if re.search(r'[.]gif$',imagename,re.I) else "")+" -t "+str(duration)+" " if duration else "")+" -i "+imagename+" "
   count=int(re.sub(r'.*io(\d+)\];?.*',r'\1',self.returnstring))+1 if self.returnstring else 0
   self.returnstring+="["+str(len(re.findall(r' -i ',self.beginstring))-1)+":v]setpts=PTS+"+self.libi.getsecond(begintime)+"/TB[bio"+str(count)+"];" +("[0:v]" if not count else "[io"+str(count-1)+"]") + "[bio"+str(count)+"]" + self.libi.convertfilter(self.libi.co(position,imagename),begintime)+":eof_action=pass:format=auto[io"+str(count)+"];"
  print(f'<>gifm.overlay')

 def stroke2(self,*arg,outputfile=None):
  '''arg - (('minhinc/VID_20230223_173611.mp4',), ('video2.mp4', '00:00:02-00:10:20'), ('=video3.mp4', ('00:30:00-00:50:00', '01:00:00-01:22:00', '01:30:00-01:32:00')), ('audio.mp3', '0.5', '00:58:20.215'), ('abc.gif', '55', ('ocir', '00:29:20.215')), ('video4.mp4', '00:20:30-00:30:00'), ('example.mp4', '45', ('ou', '01:01:50.215')))'''
  print(f'><gifc.stroke2 arg={arg} outputfile={outputfile}')
  audiolist=[]
  result=[]
  audiostring='';audiocount=0;maxvolume=0
  filename=None
  lastoffset=0
  def isaudiofile(filename):
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
  self.overlay(*[i for i in arg if len(i)==3 if not isaudiofile(i[0])])
  audiolist.append((('aout',1),(0,round(self.libi.duration,3))))
  for i in [i for i in arg if len(i)==3 and isaudiofile(i[0])]: #overlapping and audio processing
#   audiolist.append(((i[0][1],i[0][2]==None and 1 or float(i[0][2])),tuple(round(float(self.libi.getsecond(x)),3) for x in re.split('-',(i[2] if re.search('-',i[2]) else i[2]+'-'+str(float(self.libi.getsecond(i[2]))+float(self.libi.getsecond(self.libi.exiftool(i[0][1],'Duration'))))))))) if not i[0][1]==None and re.search('audio',self.libi.exiftool(i[0][1],'MIME Type'),flags=re.I) else None
   [audiolist.append(((i[0],i[1]==None and 1 or float(i[1])),tuple(round(float(y),3) for y in re.split('-',(x if re.search('-',x) else x+'-'+str(float(x)+float(self.libi.getsecond(self.libi.exiftool(i[0],'Duration'))))))))) for x in (type(i[2])==tuple and i[2] or (i[2],))]
  print(f'<=>gifc.stroke2 audiolist={audiolist} \n self.beginstring={self.beginstring} \n self.returnstring={self.returnstring}')
 
  lastoffset=maxvolume=audiocount=0
#  recordedaudiooffset="float(re.sub('_dot_','.',re.sub(r'^.*__(.*?_dot_.*?)_[.].*',r'\\1',x[0][0])))"
#  recordedaudiooffset="float(re.sub('_dot_','.',re.sub(r'^.*__(.*?_dot_.*?)_[.].*',r'\\1',j[0][0])))"
  for x in audiolist[1:]:
   if not re.search(r'\s+-i\s+'+x[0][0],self.beginstring):
    self.beginstring+=' -i  '+x[0][0]
  for i in sorted(set([y for i in audiolist for x in i[1:] for y in x]))[1:]:
   for j in audiolist:
     result.append((j[0],lastoffset-j[1][0],i-j[1][0])) if j[1][0]<i<=j[1][1] else None
#     result.append((j[0],(lastoffset if re.search('_dot_',j[0][0]) else lastoffset-j[1][0]),(i if re.search('_dot_',j[0][0]) else i-j[1][0]))) if j[1][0]<i<=j[1][1] else None
#     result.append((j[0],(lastoffset+eval(recordedaudiooffset) if re.search('_dot_',j[0][0]) else lastoffset-j[1][0]),(i+eval(recordedaudiooffset) if re.search('_dot_',j[0][0]) else i-j[1][0]))) if j[1][0]<i<=j[1][1] else None
   lastoffset=i
   print(f'<=>gifc.stroke2 {result=} {lastoffset=} {audiocount=}')
   maxvolume=max([x[0][1] for x in result])
   print(f'<=>gifc.stroke2 {maxvolume=}')
   if len(result)>1:
    audiostring+=''.join([(r'['+str(re.findall(r'-i\s+(\S+)',self.beginstring).index(x[0][0]))+r':a]' if x[0][0]!='aout' else '[aout]')+'atrim='+str(round(x[1],3))+':'+str(round(x[2],3))+',volume='+str((x[0][1]/maxvolume)*len(result))+r',asetpts=PTS-STARTPTS[aio'+(str(re.findall(r'-i\s+(\S+)',self.beginstring).index(x[0][0]))+r'];' if x[0][0]!='aout' else r'aout];') for x in result])+''.join([r'[aio'+(str(re.findall(r'-i\s+(\S+)',self.beginstring).index(x[0][0]))+r']' if x[0][0]!='aout' else r'aout]') for x in result])+'amerge=inputs='+str(len(result))+'[aout'+str(audiocount)+r'];'
#    audiostring+=''.join([(r'['+str(re.findall(r'-i\s+(\S+)',self.beginstring).index(x[0][0]))+r':a]' if x[0][0]!='aout' else '[aout]')+'atrim='+str(round((re.search(r'_dot_',x[0][0]) and eval(recordedaudiooffset) or 0)+x[1],3))+':'+str(round((re.search(r'_dot_',x[0][0]) and eval(recordedaudiooffset) or 0)+x[2],3))+',volume='+str((x[0][1]/maxvolume)*len(result))+r',asetpts=PTS-STARTPTS[aio'+(str(re.findall(r'-i\s+(\S+)',self.beginstring).index(x[0][0]))+r'];' if x[0][0]!='aout' else r'aout];') for x in result])+''.join([r'[aio'+(str(re.findall(r'-i\s+(\S+)',self.beginstring).index(x[0][0]))+r']' if x[0][0]!='aout' else r'aout]') for x in result])+'amerge=inputs='+str(len(result))+'[aout'+str(audiocount)+r'];'
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
#  self.libi.system(self.beginstring+" -filter_complex \""+re.sub(r';$','',self.returnstring+audiostring)+"\""+self.libi.vformat('mp4')+" -map \"[vout]\" -ac 2 -map \"[aout]\" -vsync 2 -y "+self.libi.adddestdir("output.mp4" if not outputfile else outputfile))
  self.libi.system(self.beginstring+" -filter_complex \""+re.sub(r';$','',self.returnstring+audiostring)+"\""+self.libi.vformat('mp4')+" -map \"[vout]\" -map \"[aout]\" -vsync 2 -y "+self.libi.adddestdir("output.mp4" if not outputfile else outputfile))

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
