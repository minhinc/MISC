import re,os
def focusout(self,begintime=0,duration_p=1,backcolor_p='0x004000ff',squareoverlay=True):
 if squareoverlay:
  self.g.libi.prune2(self.g.utili.image2gif(self.g.utili.image2gif(None,re.sub(r':d=\d+',':d='+str(duration_p),self.g.libi.filter['013_a']),backcolor=backcolor_p,duration=duration_p),re.sub(r'T/\d+',r'T/'+str(duration_p),self.g.libi.filter['011_s']),backcolor='0xffffffff',duration=duration_p)+'(20,5),'+str(begintime)+'-'+str(begintime+duration_p),stroketuple=self.stroketuple)
 else:
  self.g.libi.prune2(self.g.utili.image2gif((self.g.libi.videowidth//2,self.g.libi.videoheight//2),re.sub(r':d=\d+',':d='+str(duration_p),self.g.libi.filter['013_a']),backcolor=backcolor_p,duration=duration_p)+'(20,5),'+str(begintime)+'-'+str(begintime+duration_p),stroketuple=self.stroketuple)
 self.g.libi.prune2(self.g.utili.addalpha(os.path.expanduser('~')+r'/tmp/imageglobe/resource/'+('minhincfront.png' if re.search(r'^minh',self.profile,flags=re.I) else 'techawalfront.png' if re.search(r'^tech',self.profile,flags=re.I) else 'missmandovifront.png'),re.sub(r':d=\d+',':d='+str(duration_p),self.g.libi.filter['013_a']))+',(20,5),'+str(begintime==None and float(self.g.libi.duration)-duration_p or begintime),stroketuple=self.stroketuple)

def focusin(self,begintime=None,duration_p=4):
 self.g.libi.prune2(self.g.utili.image2gif((self.g.libi.videowidth//2,self.g.libi.videoheight//2),re.sub(r':d=\d+',':d='+str(duration_p),self.g.libi.filter['012_a']),backcolor='0xffffffff',duration=duration_p)+',(20,5),'+str(begintime==None and float(self.g.libi.duration)-duration_p or begintime),stroketuple=self.stroketuple)
 self.g.libi.prune2(self.g.utili.addalpha(os.path.expanduser('~')+r'/tmp/imageglobe/resource/'+('minhincfront.png' if re.search(r'^minh',self.profile,flags=re.I) else 'techawalfront.png' if re.search(r'^tech',self.profile,flags=re.I) else 'missmandovifront.png'),re.sub(r':d=\d+',':d='+str(duration_p),self.g.libi.filter['012_a']))+',(20,5),'+str(begintime==None and float(self.g.libi.duration)-duration_p or begintime),stroketuple=self.stroketuple)

def advertise(self,AD=4): #advertisementduration
 tempduration=self.g.libi.getslotstamp('advertisement',25*60)
 print(f'<=>ffmpeg_advertisement.fixed {self.g.libi.duration=} {tempduration=}')
 self.g.libi.setduration(self.g.libi.duration+len(tempduration)*AD)
 for count,i in enumerate(tempduration):
  i+=AD*count
  tduration=0
  for count,x in [(count,x) for count,x in enumerate(self.stroketuple) if len(x)==2]:
   print(f'********TEST***********\n {count=} {x=} {i=} {tduration=} {self.stroketuple=}  \n**********************************')
   if x[1]==None:
    x[1]='0-'+str(float(self.g.libi.exiftool(x[0][0],'Duration')))
   tduration+=float(self.g.libi.getsecond(x[1]))
   if i<tduration:
    self.stroketuple[count]=list(self.stroketuple[count])
    self.stroketuple[count][1]=re.split(r'-',x[1])[0]+'-'+str(float(self.g.libi.getsecond(re.split('-',x[1])[0]))+float(self.g.libi.getsecond(x[1]))-(tduration-i))
    self.stroketuple[count+1:count+1]=[self.g.libi.prune2(r'/home/minhinc/tmp/imageglobe/resource/black.mp4,0-'+str(AD))[0]]
    self.stroketuple.insert(count+2,list(self.stroketuple[count]))
    self.stroketuple[count+2][1]=str(float(self.g.libi.getsecond(re.split('-',x[1])[0]))+float(self.g.libi.getsecond(x[1]))-(tduration-i))+'-'+re.split(r'-',x[1])[1]
    self.stroketuple[count]=tuple(self.stroketuple[count])
    self.stroketuple[count+2]=tuple(self.stroketuple[count+2])
    break
   elif i==tduration:
    self.stroketuple[count+1:count+1]=[self.g.libi.prune2(r'/home/minhinc/tmp/imageglobe/resource/black.mp4,0-'+str(AD))[0]]
    break
  focusin(self,i,AD-1)
  focusout(self,i+AD-1,1,backcolor_p='0xffffffff',squareoverlay=False)
