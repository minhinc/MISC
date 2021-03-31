#ffmpeg version 4.2.4-1ubuntu0.1
import datetime, os, re
import libm
class gifc:
 '''1.image,gif,video,audio overlay on source video
  2. pushes video to social media'''
 def __init__(self,debug=False,inputfile='input.mp4'):
  '''Enable debug True/False'''
  self.libi=libm.libc(debug,inputfile)
  self.beginstring="ffmpeg -i "+inputfile+" "
  self.returnstring=''
  self.audiostrip=[]
  self.inputfile=inputfile

 def overlay(self,imagename,begintime,duration=None,position='(W-w)/2,(H-h)/2'):
  '''overlay png/gif/mov/mp4 over video
     imagename - name of image (png/gif/mov/mp4), audiofile, weights to be mixed(*.mp3)
           (imagename,audiofile,weights) - pass as tuple
           imagename or audiofile - if only one is available
     begintime - when overlay starts hh:mm:ss.ms/ss.ms
     position - x,y of overlay W/2,H/2 or W*2 H*5'''
  audiofile=None
  volumeweights=None
  if type(imagename) == tuple: # imagename and audio file
   if re.search(r'audio',self.libi.exiftool(imagename[0],'MIME Type'),re.I):
    audiofile=imagename[0]
    volumeweights=imagename[1] if len(imagename)>1 else None
    imagename=None
   else:
    audiofile=imagename[1] if len(imagename)>1 else None
    volumeweights=imagename[2] if len(imagename)>2 else None
    imagename=imagename[0]
  elif re.search(r'audio',self.libi.exiftool(imagename,'MIME Type'),re.I):
   audiofile=imagename
   imagename=None
  self.beginstring+=(("-t "+str(duration)+" " if duration and float(self.libi.exiftool(audiofile,'Duration'))>duration else "")+"-i "+audiofile+" " if audiofile else "")+((("-loop 1 " if not re.search(r'[.](gif|mov|mp4)$',imagename,re.I) else "-ignore_loop 0 " if re.search(r'[.]gif$',imagename,re.I) else "")+"-t "+str(duration)+" " if duration else "")+"-i "+imagename+" " if imagename else "")
  count=int(re.sub(r'.*io(\d+)\];.*',r'\1',self.returnstring))+1 if self.returnstring else 0

  self.returnstring+="["+str(len(re.findall(r' -i ',self.beginstring))-1)+":v]setpts=PTS+"+self.libi.getsecond(begintime)+"/TB[bio"+str(count)+"];" +("[0:v]" if not count else "[io"+str(count-1)+"]") + "[bio"+str(count)+"]" + self.libi.convertfilter(position,begintime)+":eof_action=pass[io"+str(count)+"];" if imagename else ""

  if audiofile:
   #(('<index>',begintime,weights),<begintime>,<endtime>)
   self.audiostrip.append(((str(len(re.findall(r' -i',self.beginstring))-(2 if imagename else 1)),float(self.libi.getsecond(begintime)),volumeweights),float(self.libi.getsecond(begintime)),float(self.libi.getsecond(begintime))+(duration if duration and float(self.libi.exiftool(audiofile,'Duration'))>duration else float(self.libi.exiftool(audiofile,'Duration')))))

 def stroke(self,outimagename=None):
  '''Render the filtergraphs on video=input.mp4'''
  audiostring="";count=0
  if len(self.audiostrip):
   self.audiostrip.insert(0,(('0',0.0,None),0.0,float(self.libi.exiftool(self.inputfile,'Duration'))))
  print('audiostrip',self.audiostrip)
#  self.audiostrip=sorted(self.audiostrip,key=lambda x: float(x[1]))
  tarr=sorted([*[[i[0],i[1],'b'] for i in sorted(self.audiostrip,key=lambda x: x[1])],*[[i[0],i[2],'e'] for i in sorted(self.audiostrip,key=lambda x:x[2])]],key=lambda x:x[1])
  print('tarr',tarr)
  rarr=[]
  while len(tarr):
   result=[[tarr[0][0]],tarr[0][1],None]
   i=1
   while tarr[i][1]==result[1]:
    result[0].append(tarr[i][0])
    i+=1
   if tarr[i][2]=='b':
    result[2]=tarr[i][1]
    for j in range(i):
     tarr[j][1]=tarr[i][1]
    rarr.append(result)
   elif tarr[i][2]=='e':
    result[2]=tarr[i][1]
    for j in range(i):
     tarr[j][1]=tarr[i][1]
    tarr=[j for j in tarr if j[0]!=tarr[i][0]]
    rarr.append(result)
  print('rarr',rarr)
  for i in rarr:
   if len(i[0])>1:
#    for j in i[0]:
#     audiostring+='['+j[0]+':a]atrim='+str(i[1]-j[1])+':'+str(i[2]-j[1])+',asetpts=PTS-STARTPTS[aio'+j[0]+'];'
#    for j in i[0]:
#     audiostring+='[aio'+j[0]+']'
    audiostring+=''.join(['['+j[0]+':a]atrim='+str(round(i[1]-j[1],3))+':'+str(round(i[2]-j[1],3))+',asetpts=PTS-STARTPTS[aio'+j[0]+'];' for j in i[0]])+''.join(['[aio'+j[0]+']' for j in i[0]])+'amix=inputs='+str(len(i[0]))+(':weights='+re.sub(r'\s+$','',''.join([str(j[2] if j[2] else 1)+' ' for j in i[0]])) if len([j[2] for j in i[0] if j[2]]) else '')+'[aout'+str(count)+'];'
   else:
    audiostring+='['+i[0][0][0]+':a]atrim='+str(round(i[1]-i[0][0][1],3))+':'+str(round(i[2]-i[0][0][1],3))+',asetpts=PTS-STARTPTS[aout'+str(count)+'];'
   count+=1
#  self.audiostring+='[0:a]atrim=start='+re.sub(r'.*atrim=\s*\d+(?:[.]\d+)?:\s*(\d+(?:[.]\d+)?).*',r'\1',self.audiostring)+r',asetpts=PTS-STARTPTS[aud'+str(int(re.sub(r'.*aud(\d+)\];.*',r'\1',self.audiostring))+1)+'];' if self.audiostring else ''
  for i in range(count):
   audiostring+='[aout'+str(i)+']'
  audiostring+='concat=n='+str(count)+':v=0:a=1[aout]' if count else ''
#  for i in range(0,int(re.sub(r'.*aud(\d+)\];.*',r'\1',self.audiostring) if self.audiostring else 0)):
#   self.audiostring+='[aud'+str(i+1)+']'
#  self.audiostring+='concat=n='+str(i+1)+':v=0:a=1[aout]' if self.audiostring else ''
  self.libi.ffmpeg(self.beginstring+"-filter_complex \""+re.sub(r';$','',self.returnstring+audiostring)+"\" -map \""+re.sub(r'.*(\[io\d+\]);.*',r'\1',self.returnstring)+"\" -map "+("\"[aout]\"" if re.search(r'\d+',audiostring) else '0:a -c:a copy')+" -y "+("output.mp4" if not outimagename else outimagename))
#  for key in self.socialmedia:
#   if re.search(r'y',input("wanna push \""+self.outputfile+"\" to "+key+" ?(y/n)..."),re.I):
#    self.libi.system(self.socialmedia[key])

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
