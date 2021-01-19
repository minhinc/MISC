import os
import math
from PIL import Image,ImageDraw,ImageFont
import re
class libc:
 filterlist={
     10:["blend=all_expr='A*(1-min(T/2,1))+B*(min(T/2,1))'","#Blending"],\
     11:["blend=all_expr='if(lte(Y,(H-T/2*H)),A,B)'","#Curtain up"],\
     12:["blend=all_expr='if(gte(X,(T/2*W)),A,B)'","#Curtain right"],\
     13:["blend=all_expr='if(gte(Y,(T/2*H)),A,B)'","#curtain down"],\
     14:["blend=all_expr='if(lte(X,(W-T/2*W)),A,B)'","#curtain left"],\
     20:["blend=all_expr='if(between(X,(W/2-T/2*W/2),(W/2+T/2*W/2)),B,A)'","#Vertical open"],\
     21:["blend=all_expr='if(between(Y,(H/2-T/2*H/2),(H/2+T/2*H/2)),B,A)'","#Horizontal open"],\
     22:["","#veritcal close"],\
     23:["","#horizontal close"],\
     24:["blend=all_expr='if(gte(sqrt((X-W/2)*(X-W/2)+(H/2-Y)*(H/2-Y)),(T/2*max(W,H))),A,B)'","circle open"],\
     25:["blend=all_expr='if(lte(sqrt((X-W/2)*(X-W/2)+(H/2-Y)*(H/2-Y)),(max(W,H)-(T/2*max(W,H)))),A,B)'","circle close"],\
     26:["blend=all_expr='if(between(X,(W/2-T/1*W/2),(W/2+T/1*W/2))*between(Y,(H/2-T/1*H/2),(H/2+T/1*H/2)),B,A)'","expanding window"],\
     27:["","#collapsing window"],\
#     30:["split=2[bg][v];[bg]drawbox=t=fill[bg];[v]crop=iw/2:ih[v];[1][v]scale2ref=oh*mdar:ih/2[ic][vc];[ic]split=2[ic1][ic2];[ic1]format=yuva422p,pad=2*iw:2*ih:(ow-iw):(oh-ih)/2:color=black@0[ic1];[bg][vc]overlay='max(0,W/4-t/0.5*W/4)'[bg];[bg][ic1]blend=all_expr='if(gt(X,W/2+2)*between(Y,(H/2-(T-0.5)/1.5*H/2),(H/2+(T-0.5)/1.5*H/2)),B,A)':enable='gt(t,0.5)*lt(t,4)'[bg];[ic2]pad=iw+4:ih+4:(ow-iw)-2:(oh-ih)-2:color=#004000[ic2];[bg][ic2]overlay='max((W-w)/2,W/2-(t-4)/1*W/2)':(H-h)/2:enable='gte(t,4)'[bg];[bg][0]blend=all_expr='if(between(X,(W/4-(T-5)/1*W/4),(3*W/4+(T-5)/1*W/4))*between(Y,(H/4-(T-5)/1*H/4),(3*H/4+(T-5)/1*H/4)),B,A)':enable='gt(t,5)'","#blend sidebyside"],\
     30:["[1]split=2[bg][v];[bg]drawbox=t=fill:color=#200000[bg];[v]crop=7*iw/10[v];[0]format=yuva422p,pad=X:Y:(ow-iw):(oh-ih)/2:color=black@0[ic];[bg][v]overlay='max(0,3*W/20-t/0.25*3*W/20)'[bg];[bg][ic]blend=all_expr='if(gt(X,W/2)*between(Y,max(H/4,(H/2-T/0.5*H/4)),min(3*H/4,H/2+T/0.5*H/4)),B,A)'[bg];[bg][1]blend=all_expr='if(gte(X,(W/2-(T-Z)/1*W/2))*between(Y,(H/4-(T-Z)/1*H/4),(3*H/4+(T-Z)/1*H/4)),B,A)':enable='gt(t,Z)'","#blend sidebyside"],\
     #40:["scale=XX,format=yuva444p,pad=3*iw:3*ih:(ow-iw)/2:(oh-ih)/2:color=black@0,rotate=a='if(lte(t,1),PI*4*t,2*PI)':c=none[rotate1];[0][rotate1]overlay=(W-w)/2:(H-h)/2:shortest=1[out];[2][out]scale2ref=w=oh*mdar:h=ih*2[11][00];[11]format=yuva444p,pad=3*iw:3*ih:(ow-iw)/2:(oh-ih)/2:color=black@0,zoompan=z='min(zoom+0.04,3)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=50:s=YY[img];[img]setpts=PTS+1/TB[img];[00][img]overlay='(W-w)/2':'(H-h)/2'","#rotateandzoom"],\
     40:["scale=XX1,format=yuva444p,pad=W1*iw:H1*ih:(ow-iw)/2:(oh-ih)/2:color=black@0,rotate=a='if(lte(t,1),PI*4*t,2*PI)':c=none[rotate1];[0][rotate1]FF1:shortest=1:enable='lte(t,1)'[out];[2]scale=XX2,format=yuva444p,pad=3*iw:3*ih:(ow-iw)ALPHA:(oh-ih)BETA:color=black@0,zoompan=z='min(zoom+0.04,3)':x='iwALPHA-(iw/zoom)ALPHA':y='ihBETA-(ih/zoom)BETA':d=50:s=YY[img];[img]setpts=PTS+1/TB[img];[out][img]FF2","#rotateandzoom"],\
     50:["overlay","#overlay"],\
     51:["overlay=eof_action=pass","#overlay"],\
     52:["overlay=x=(W-w)/2:y=(H-h)/2","#overlay gif/image/video center"],\
     60:["overlay=x='(W-w)/2':y='max((H-h)/2,H-t/2*H)'","#overlay up"],\
     61:["overlay=x='min((W-w)/2,-w+t/2*W)':y='(H-h)/2'","#overlay right"],\
     62:["overlay=x='(W-w)/2':y='min((H-h)/2,-h+t/2*H)'","#overlay bottom"],\
     63:["overlay=x='max((W-w)/2,W-t/1*W)':y='(H-h)/2'","#overlay left"],\
     70:["overlay=x=W-w:y=(H-h)/4","#overlay logo"],\
     #80:["scale2ref=oh*mdar:ih[11][00];[00]split=2[bg][v];[bg]drawbox=t=fill[bg];[v]crop=iw/2:ih[vc];[11]crop=iw/2:ih[ic];[ic]format=yuva422p,pad=2*iw:ih:(ow-iw):(oh-ih)/2:color=black@0[ic];[bg][vc]overlay='max(0,W/4-t/0.25*W/4)'[bg];[bg][ic]blend=all_expr='if(gt(X,W/2+2)*between(Y,(H/2-(T-0.25)/1*H/2),(H/2+(T-0.25)/1*H/2)),B,A)':enable='gt(t,0.25)'[bg];[0][bg]overlay","#overlay sidebyside"],\
     #80:["[1]split=2[bg][v];[bg]drawbox=t=fill:color=#200000[bg];[v]crop=9*iw/10[v];[0]format=yuva422p,pad=X:Y:(ow-iw):(oh-ih)/2:color=black@0[ic];[bg][v]overlay='max(0,W/20-t/0.25*W/20)'[bg];[bg][ic]blend=all_expr='if(gt(X,2*W/3)*between(Y,max(H/3,(H/2-T/0.5*H/6)),min(2*H/3,H/2+T/0.5*H/6)),B,A)'","#blend sidebyside"],\
     80:["[1]split=2[bg][v];[bg]drawbox=t=fill:color=#200000[bg];[v]crop=7*iw/10[v];[0]format=yuva422p,pad=X:Y:(ow-iw):(oh-ih)/2:color=black@0[ic];[bg][v]overlay='max(0,3*W/20-t/0.25*3*W/20)'[bg];[bg][ic]blend=all_expr='if(gt(X,W/2)*between(Y,max(H/4,(H/2-T/0.5*H/4)),min(3*H/4,H/2+T/0.5*H/4)),B,A)'","#blend sidebyside"],\
     90:["select='gte(scene,0.8)',metadata=print:file=time.txt\" -vsync vfr img%03d.png","#scene transition"],\
#Extra, Miscllaneous
     1000:["blend=all_expr='if(lte(T,5),if(gte(Y,(T/2*H)),A,B),if(gte(Y,((T-5)/2*H)),B,A))'","#curtain down back clean 7 sec"],\
     1001:["blend=all_expr='if(lte(T,5),if(gte(X,(T/2*W)),A,B),if(gte(X,((T-5)/2*W)),B,A))'","#Curtain right back clean 7 sec"],\
     1002:["blend=all_expr='if(lte(T,5),if(lte(Y,(H-T/2*H)),A,B),if(lte(Y,(H-(T-5)/2*H)),B,A))'","#Curtain up and back"],\
     1003:["blend=all_expr='if(lte(T,5),if(lte(X,(W-T/2*W)),A,B),if(lte(X,(W-(T-5)/2*W)),B,A))'","#curtain left and back"],\
     1004:["blend=all_expr='if(between(X,(W/2-T/2*W/2),(W/2+T/2*W/2)),B,A)'","#Vertical open"],\
     1005:["blend=all_expr='if(between(Y,(H/2-T/2*H/2),(H/2+T/2*H/2)),B,A)'","#Horizontal open"],\
#     1006:["blend=all_expr='if(between(X,max(0*W,X1*W-(T-Z)/2*X1*W),min(1.0*W,X2*W+(T-Z)/2*X3*W))*between(Y,max(0*H,Y1*H-(T-Z)/2*Y1*H),min(1.0*H,Y2*H+(T-Z)/2*Y3*H)),B,A)'","expanding window"]
     1006:["blend=all_expr='if(between(X,max(0*W,X1*W-T/1*X1*W),min(1.0*W,X2*W+T/1*X3*W))*between(Y,max(0*H,Y1*H-T/1*Y1*H),min(1.0*H,Y2*H+T/1*Y3*H)),B,A)'","expanding window"]
    }
 debugb=False
# videowidth=videoheight=0
 def __init__(self):
  self.videowidth,self.videoheight=[int(x) for x in os.popen('ffmpeg -i input.mp4 2>&1|grep -oP \'Stream .*, \K[0-9]+x[0-9]+\'').read().split('x')]
  print("libc::_init__<> video widthxheight {}x{}".format(self.videowidth,self.videoheight))

 def videoattribute(self,videofile_p):
  print("videofile_p {}".format(videofile_p))
#  videowidth,videoheight=[int(x) for x in os.popen('ffmpeg -i input.mp4 2>&1|grep -oP \'Stream .*, \K[0-9]+x[0-9]+\'').read().split('x')]
  videodata=os.popen('ffmpeg -i '+videofile_p+' 2>&1').read()
  videowidth,videoheight=re.sub(r'.*,\s*?(\d+x\d+)\s*.*',r'\1',videodata,flags=re.I|re.DOTALL).split('x')
  fps=re.sub(r'.*?(\d+)\s*fps\s*,.*',r'\1',videodata,flags=re.I|re.DOTALL)
  samplerate=re.sub(r'.*?(\d+)\s*Hz\s*,.*',r'\1',videodata,flags=re.I|re.DOTALL)
  channel=re.sub(r'.*\d+\s*Hz\s*,\s*([^ ]*)\s*,.*',r'\1',videodata,flags=re.I|re.DOTALL)
  self.debug("libc::videoattribute><",videofile_p,(videowidth,videoheight),fps,samplerate,channel)
  return ((videowidth,videoheight),fps,samplerate,channel)

 def split(self,string_p,default_p=None,delim_p=':'):
  self.debug("libc::split><",string_p,delim_p)
  DBL_ESC="!double escape!"
  if default_p:
   arglist=list(default_p)
   for (count,x) in enumerate(re.split(r'(?<!\\):',string_p.replace(r'\\',DBL_ESC))):
    if x:
#     arglist[count]=x.replace(DBL_ESC,'\\')
     if arglist[count]!=None: 
      arglist[count]=type(arglist[count])(x.replace(DBL_ESC,'\\'))
     else:
      arglist[count]=x.replace(DBL_ESC,'\\')
   return arglist
  return [x.replace(DBL_ESC,'\\') for x in re.split(r'(?<!\\):',string_p.replace(r'\\',DBL_ESC))]

 def dimension(self,file_p):
  if re.search(r'[.]mp4',file_p,flags=re.I):
   return [int(x) for x in os.popen('ffmpeg -i input.mp4 2>&1|grep -oP \'Stream .*, \K[0-9]+x[0-9]+\'').read().split('x')]
  else:
   return Image.open(file_p).size

 def drawtextstroke(self,draw_p,x_p,y_p,text_p,textfont_p,textcolor_p,strokecolor_p='black',adj_p=2):
  strokelist=[(x_p-adj_p,y_p),(x_p+adj_p,y_p),(x_p,y_p-adj_p),(x_p,y_p+adj_p),(x_p-adj_p,y_p-adj_p),(x_p+adj_p,y_p-adj_p),(x_p-adj_p,y_p+adj_p),(x_p+adj_p,y_p+adj_p)]
  for i in range(len(strokelist)):
   draw_p.text((strokelist[i][0],strokelist[i][1]),text_p,font=textfont_p,fill=strokecolor_p)
  draw_p.text((x_p,y_p),text_p,font=textfont_p,fill=textcolor_p)

 def getfont(self,stringlist_p,screenratio_p=0.8,fontfamily_p='../../../.fonts/tw-cen-mt.ttf'):
  self.debug("libc::getfont><",stringlist_p,screenratio_p)
  i=10
  maxindex=[len(j) for j in stringlist_p].index(max(len(j) for j in stringlist_p))
  #while (ImageFont.truetype(fontfamily_p,i).getsize('a')[0]*(max([len(j) for j in stringlist_p]) if max([len(j) for j in stringlist_p])>10 else 10))<(self.videowidth*screenratio_p): i=i+1
  while ImageFont.truetype(fontfamily_p,i).getsize(stringlist_p[maxindex])[0] < float(self.videowidth)*screenratio_p: i=i+1
  self.debug("net ii")
  self.debug("libm::getfont<>")
  return ImageFont.truetype(fontfamily_p,i)
 
 def ffmpeg(self,commandstring_p):
  print('              *****************')
  print("              "+re.sub(r' -y ([^ ]+[.]mp4)',r' -preset ultrafast -y \1',commandstring_p) if self.debugb else commandstring_p)
  print('              *****************')
  os.system(re.sub(r' -y ([^ ]+[.]mp4)',r' -preset ultrafast -y \1',commandstring_p) if self.debugb else commandstring_p)

 def getsecond(self,time_p,demark_p=False):
  '''demark is time non colon to colon format'''
#  print('libc::getsecond<> '+time_p)
  if re.search(r':',time_p):
   return re.sub(r'(?P<id1>\d+):(?P<id2>\d+):(?P<id3>\d+)(?P<id4>.*)$',lambda m: str(int(m.group('id1'))*3600+int(m.group('id2'))*60+int(m.group('id3')))+m.group('id4'),time_p)
  elif demark_p:
   hour=int(float(time_p)/3600)
   minute=int((float(time_p)-hour*3600)/60)
   second=round(float(time_p)-hour*3600-minute*60,2)
   return str(hour)+":"+str(minute)+":"+str(second)
  return time_p

 def system(self,commandstring_p):
  self.debug("libm::system<>",commandstring_p)
  os.system(commandstring_p)

 def stepvalue(self,initial_p,last_p,step_p=2):
  '''min step_p=2. that is 0 and 1. For step_p=1 initial_p would return'''
  stepsize=0
  if step_p>1:
   stepsize=(last_p-initial_p)/(step_p-1)
  for i in range(step_p):
   yield round(initial_p+i*stepsize,3)

 def getrectpoint(self,xy_p,rect_p,angle_p,offset_p=None):
  '''angle_p in degrees
  ----------------- <---- 1
  |^              |
  | \----- 0      | 
  |               |
  -----------------'''
  self.debug("libm::getrectpoint><",xy_p,rect_p,angle_p,offset_p)
  funclist=(lambda x:(xy_p[0]+(rect_p[1]-xy_p[1])/math.tan(x),rect_p[1]),lambda x:(rect_p[2],xy_p[1]+(rect_p[2]-xy_p[0])*math.tan(x)),lambda x:(xy_p[0]+(rect_p[3]-xy_p[1])/math.tan(x),rect_p[3]),lambda x:(rect_p[0],xy_p[1]+(rect_p[0]-xy_p[0])*math.tan(x)))
  anglelist=(math.pi+math.atan((xy_p[1]-rect_p[1])/(xy_p[0]-rect_p[0])),math.atan((xy_p[1]-rect_p[1])/(xy_p[0]-rect_p[2])),math.atan((xy_p[1]-rect_p[3])/(xy_p[0]-rect_p[2])),math.pi+math.atan((xy_p[1]-rect_p[3])/(xy_p[0]-rect_p[0])))
  [print(math.degrees(i)) for i in anglelist]
  for i in range(len(anglelist)):
   if i==0:
    if angle_p>=math.degrees(anglelist[0]) or angle_p<=math.degrees(anglelist[1]):
     return ((round(funclist[0](math.radians(angle_p))[0],3),round(funclist[0](math.radians(angle_p))[1],3)-(offset_p[1] if offset_p else 0)))
   elif math.degrees(anglelist[i])<=angle_p<=math.degrees(anglelist[(i+1)%len(anglelist)]):
    return ((round(funclist[i](math.radians(angle_p))[0],3)-(offset_p[0] if i==3 and offset_p else 0),round(funclist[i](math.radians(angle_p))[1],3)))

 def debug(self,*arg_p):
  if self.debugb:print(*arg_p)

 def altervideo(self,videofile_p,outputfile_p=None,size_p=1):
  if not outputfile_p:
   outputfile_p=re.sub(r'(.*)[.](.*)$',r'\1'+'_mod.'+r'\2',videofile_p)
  self.ffmpeg('ffmpeg -i '+videofile_p+' -vf scale='+str(int(self.videowidth*float(size_p)))+':'+str(int(self.videoheight*float(size_p)))+' -y '+outputfile_p)
  if re.search(r'_mod[.]',outputfile_p):
   self.system('mv '+outputfile_p+' '+videofile_p)

 def convertfilter(self,filter_p,eof_action_p=False):
  self.debug("libc::convertfilter><",filter,eof_action_p)
  if not re.search(r'(overlay|blend)',filter_p):
   first,second=re.split(r',',filter_p)
   return 'overlay=x='+('W*' if not re.search(r'W',first,flags=re.I) else '')+first+':y='+('H*' if not re.search(r'H',second,flags=re.I) else '')+second+(':eof_action=pass' if eof_action_p else '')
  elif eof_action_p and not re.search(r'eof_action',filter_p,re.I):
   filter_p+='=eof_action=pass' if re.search(r'overlay$',filter_p,re.I) else ':eof_action=pass'
  return filter_p

 def blendoverglass(self,args_p,filter_p,beginstring_p,returnstring_p,count_p,image_p,duration_p=(5,0.15,'r'),shade_p=(0,0,0,0)):
  '''filter_p is positon filter. duration_p[2] decides for filter'''
  img=Image.new('RGBA',self.dimension(image_p),shade_p)
  img.save('back_'+str(count_p)+'.png')
  beginstring_p+='-i back_'+str(count_p)+'.png '
  imagecount=str(len(re.findall(r' -i ',beginstring_p))-1)
  self.system('mv '+image_p+' image_'+str(count_p)+re.sub(r'.*([.].*)',r'\1',image_p))
  image_p='image_'+str(count_p)+re.sub(r'.*([.].*)',r'\1',image_p)
  beginstring_p+=('' if re.search(r'[.](gif|mp4)$',image_p,re.I) else '-loop 1 -t '+str(duration_p[0]))+' -i '+image_p+' '
  filter=1000+('b','r','t','l').index(duration_p[2])
  for j in range(1,len(args_p)):
   returnstring_p+="["+imagecount+"]["+str(len(re.findall(r' -i ',beginstring_p))-1)+"]"+(self.filterlist[50][0] if re.search(r'[.](gif|mp4)$',image_p,re.I) else re.sub(r'(?P<id>lte\(T,|\(T-)\d+',lambda m:m.group('id')+str(duration_p[0]-duration_p[1]),re.sub(r'(?P<id>T/|\(T-\d+\)/)\d?[.]?\d+',lambda m:m.group('id')+str(duration_p[1]),self.filterlist[filter][0])))+",setpts=PTS+"+self.getsecond(args_p[j])+"/TB[bio"+str(count_p)+"];"+("[0:v]" if not count_p else "[io"+str(count_p-1)+"]")+"[bio"+str(count_p)+"]"+self.convertfilter(filter_p,eof_action_p=True)+"[io"+str(count_p)+"];"
   count_p=count_p+1
  return (beginstring_p,returnstring_p,count_p)

 def scale(self,image_p,size_p,bound=None):
  if bound==None: bound=(self.videowidth,self.videoheight)
  imagesize=image_p if type(image_p)==tuple else self.dimension(image_p)
  if imagesize[0]>imagesize[1]:
   newwidth,newheight=size_p[0],int(size_p[0]*imagesize[1]/imagesize[0])
  else:
   newwidth,newheight=int(size_p[1]*imagesize[0]/imagesize[1]),size_p[1]
  if bound:
   if newwidth>self.videowidth:
    newheight=(self.videowidth*newheight)/newwidth
    newwidth=self.videowidth
   elif newheight>self.videoheight:
    newwidth=(self.videoheight*newwidth)/newheight
    newheight=self.videoheight
  return newwidth,newheight

 def getposition(self,filterpos_p,size_p,videosize_p=None,multiply_p=1.5):
  if not videosize_p: videosize_p=(self.videowidth,self.videoheight)
  self.debug("libc::getposition><",filterpos_p,size_p,videosize_p,multiply_p)
  first,second=re.split(r',',filterpos_p)
  first+='*W' if not re.search(r'W',first,re.I) else ''
  second+='*H' if not re.search(r'H',second,re.I) else ''
  oldx=eval(re.sub(r'W',str(videosize_p[0]),re.sub(r'w',str(size_p[0]),first)))
  oldy=eval(re.sub(r'H',str(videosize_p[1]),re.sub(r'h',str(size_p[1]),second)))
  oldx=oldx-(oldx+size_p[0]-videosize_p[0] if oldx+size_p[0] > videosize_p[0] else 0)
  oldy=oldy-(oldy+size_p[1]-videosize_p[1] if oldy+size_p[1] > videosize_p[1] else 0)
  if oldx<0: oldx=0
  if oldy<0: oldy=0
  newx=eval(re.sub(r'W',str(videosize_p[0]),re.sub(r'w',str(size_p[0]),first)))-(size_p[0]*(multiply_p-1))/2
  newy=eval(re.sub(r'H',str(videosize_p[1]),re.sub(r'h',str(size_p[1]),second)))-(size_p[1]*(multiply_p-1))/2
  newx=newx-(newx+size_p[0]*multiply_p-videosize_p[0] if newx+size_p[0]*multiply_p > videosize_p[0] else 0)
  newy=newy-(newy+size_p[1]*multiply_p-videosize_p[1] if newy+size_p[1]*multiply_p > videosize_p[1] else 0)
  if newx<0: newx=0
  if newy<0: newy=0
  return ([round(i,3) for i in (newx/videosize_p[0],min(1.0,(newx+size_p[0]*multiply_p)/videosize_p[0]),oldx/videosize_p[0],min(1.0,(oldx+size_p[0])/videosize_p[0]))],[round(i,3) for i in (newy/videosize_p[1],min(1.0,(newy+size_p[1]*multiply_p)/videosize_p[1]),oldy/videosize_p[1],min(1.0,(oldy+size_p[1])/videosize_p[1]))])

 def blendimage(self,args_p,filter_p,beginstring_p,returnstring_p,count_p,image_p,imagesize_p=None,duration_p=(3,0),filterpos_p='(W-w),(H-h)/2',transitiontime_p=2,split_p=False,multiply_p=None,glasscolor_p=(0,0,0,0),alpha_p=255):
  self.debug("libc::blendimage><",args_p,filter_p,beginstring_p,returnstring_p,count_p,image_p,imagesize_p,duration_p,filterpos_p,transitiontime_p,split_p,multiply_p,glasscolor_p,alpha_p)
  if alpha_p!=255:
   img=Image.open(image_p).convert('RGBA')
   img.putalpha(Image.new('L',self.dimension(image_p),color=alpha_p))
   img.save(image_p)
  imagesize=self.scale(image_p,self.dimension(image_p) if not imagesize_p else imagesize_p)
  filter_p=re.sub(r'(?P<id>T,|\(T-)\d',lambda m:m.group('id')+str(duration_p[0]-transitiontime_p),re.sub(r'(?P<id>[Tt]/|\([Tt]-\d+\)/)\d+',lambda m:m.group('id')+str(transitiontime_p),self.filterlist[filter_p][0] if type(filter_p)==int else filter_p))
  print("filter {}".format(filter_p))
  singleton=False
  if not split_p and not multiply_p and not duration_p[1]:
   print("##################SINGLETON##################")
   singleton=True
   beginstring_p+=('-ignore_loop 0 ' if re.search(r'[.]gif$',image_p) else '-t '+str(duration_p[0])+' -loop 1 ' if re.search(r'[.](png|jpeg|jpg)$',image_p) and transitiontime_p else '')+'-i '+image_p+' '
  for j in range(1,len(args_p)):
   beginstring=('-ignore_loop 0 ' if re.search(r'[.]gif$',image_p) else '-t '+str(duration_p[0])+' -loop 1 ' if re.search(r'[.](png|jpeg|jpg)$',image_p) and transitiontime_p else '')+'-i '+image_p+' '
   beginstring+='-i '+image_p+' ' if re.search(r'[.](png|jpeg|jpg)$',image_p) and multiply_p and duration_p[1] else ''
   beginstring+='-ss '+self.getsecond(args_p[j])+' -t '+str(duration_p[0]+(duration_p[1] if multiply_p else 0))+' -i input.mp4 '
   #glassscaleblend1='color=0x000000@0:s='+'x'.join([str(imagesize[0]),str(imagesize[1])])+'[i];['+str(len(re.findall(r' -i ',beginstring_p))-1 if singleton else 0)+']scale='+':'.join([str(imagesize[0]-imagesize[0]%2),str(imagesize[1]-imagesize[1]%2)])+'[11];[i][11]'+(filter_p if transitiontime_p else 'overlay')+("[int];"+'color=0x'+''.join(re.sub(r'^0x','0',hex(int(i)))[-2:] for i in glasscolor_p[:3])+'@'+str(round(glasscolor_p[3]/255,3) if glasscolor_p[3] else 0)+':s='+'x'.join([str(imagesize[0]),str(imagesize[1])])+"[i];[i][int]overlay" if glasscolor_p!=(0,0,0,0) else "")+(",setpts=PTS+"+self.getsecond(args_p[j])+"/TB" if singleton else "")+"[i];"+(("[0:v]" if not count_p else "[io"+str(count_p-1)+"]") if singleton else '[bg]' if split_p else '['+str(len(re.findall(r' -i ',beginstring))-1)+"]")+'[i]'+self.convertfilter(str(self.getposition(filterpos_p,imagesize)[0][2])+'*W,'+str(self.getposition(filterpos_p,imagesize)[1][2])+'*H',False)+":eof_action=pass:enable='lte(t,"+str(float(self.getsecond(args_p[j]))+duration_p[0] if singleton else duration_p[0])+")'"+("[io"+str(count_p)+"];" if singleton else "[bg];" if multiply_p and duration_p[1] else "")
#   glassscaleblend1=('color=0x000000@0:s='+'x'.join([str(imagesize[0]),str(imagesize[1])])+'[i];' if transitiontime_p else "")+'['+str(len(re.findall(r' -i ',beginstring_p))-1 if singleton else 0)+']scale='+':'.join([str(imagesize[0]-imagesize[0]%2),str(imagesize[1]-imagesize[1]%2)])+'[11];'+('[i][11]'+filter_p+'[11];' if transitiontime_p else '')+('color=0x'+''.join(re.sub(r'^0x','0',hex(int(i)))[-2:] for i in glasscolor_p[:3])+'@'+str(round(glasscolor_p[3]/255,3) if glasscolor_p[3] else 0)+':s='+'x'.join([str(imagesize[0]),str(imagesize[1])])+"[i];[i][11]overlay[11];" if glasscolor_p!=(0,0,0,0) else "")+("[11]setpts=PTS+"+self.getsecond(args_p[j])+"/TB[11];" if singleton and (transitiontime_p or glasscolor_p!=(0,0,0,0)) else "")+(("[0:v]" if not count_p else "[io"+str(count_p-1)+"]") if singleton else '[bg]' if split_p else '['+str(len(re.findall(r' -i ',beginstring))-1)+"]")+'[11]'+self.convertfilter(str(self.getposition(filterpos_p,imagesize)[0][2])+'*W,'+str(self.getposition(filterpos_p,imagesize)[1][2])+'*H',False)+(":eof_action=pass" if transitiontime_p else '')+":enable='"+("lte(t," if singleton and (transitiontime_p or glasscolor_p!=(0,0,0,0)) else "between(t,"+self.getsecond(args_p[j])+",")+str(float(self.getsecond(args_p[j]))+duration_p[0] if singleton else duration_p[0])+")'"+("[io"+str(count_p)+"];" if singleton else "[bg];" if multiply_p and duration_p[1] else "")
   glassscaleblend1=('color=0x000000@0:s='+'x'.join([str(imagesize[0]),str(imagesize[1])])+'[i];' if transitiontime_p else "")+'['+str(len(re.findall(r' -i ',beginstring_p))-1 if singleton else 0)+']scale='+':'.join([str(imagesize[0]-imagesize[0]%2),str(imagesize[1]-imagesize[1]%2)])+'[11];'+('[i][11]'+filter_p+(":enable='lte(t,"+str(duration_p[0])+")'" if singleton else '')+'[11];' if transitiontime_p else '')+('color=0x'+''.join(re.sub(r'^0x','0',hex(int(i)))[-2:] for i in glasscolor_p[:3])+'@'+str(round(glasscolor_p[3]/255,3) if glasscolor_p[3] else 0)+':s='+'x'.join([str(imagesize[0]),str(imagesize[1])])+"[i];[i][11]overlay=0:0"+(":enable='lte(t,"+str(duration_p[0])+")'" if singleton else '')+"[11];" if glasscolor_p!=(0,0,0,0) else "")+("[11]setpts=PTS+"+self.getsecond(args_p[j])+"/TB[11];" if singleton and (transitiontime_p or glasscolor_p!=(0,0,0,0)) else "")+(("[0:v]" if not count_p else "[io"+str(count_p-1)+"]") if singleton else '[bg]' if split_p else '['+str(len(re.findall(r' -i ',beginstring))-1)+"]")+'[11]'+self.convertfilter(str(self.getposition(filterpos_p,imagesize)[0][2])+'*W,'+str(self.getposition(filterpos_p,imagesize)[1][2])+'*H',False)+(":eof_action=pass" if transitiontime_p or re.search(r'[.](gif|mp4)$',image_p) else '')+(":enable='lte(t,"+str(float(self.getsecond(args_p[j]))+duration_p[0])+")'" if singleton and (transitiontime_p or glasscolor_p!=(0,0,0,0)) else ":enable='between(t,"+self.getsecond(args_p[j])+","+str(float(self.getsecond(args_p[j]))+duration_p[0])+")'" if singleton and not transitiontime_p else "")+("[io"+str(count_p)+"];" if singleton else "[bg];" if multiply_p and duration_p[1] else "")
   multiplyfactor=round(min(multiply_p,self.videowidth/imagesize[0]) if imagesize[1]*self.videowidth/imagesize[0]<=self.videoheight else min(multiply_p,self.videoheight/imagesize[1]),3) if multiply_p else 0
   glassscaleblend2='color=0x000000@0:s='+'x'.join([str(int(imagesize[0]*multiplyfactor)),str(int(imagesize[1]*multiplyfactor))])+'[i];['+str(0)+']scale='+':'.join([str(int(int(imagesize[0]*multiplyfactor)/2)*2),str(int(int(imagesize[1]*multiplyfactor)/2)*2)])+'[11];[i][11]'+re.sub(r'X1',str(self.getposition(filterpos_p,imagesize,(imagesize[0]*multiplyfactor,imagesize[1]*multiplyfactor))[0][2]),re.sub(r'X2',str(self.getposition(filterpos_p,imagesize,(imagesize[0]*multiplyfactor,imagesize[1]*multiplyfactor))[0][3]),re.sub(r'X3',str(1-self.getposition(filterpos_p,imagesize,(imagesize[0]*multiplyfactor,imagesize[1]*multiplyfactor))[0][3]),re.sub(r'Y1',str(self.getposition(filterpos_p,imagesize,(imagesize[0]*multiplyfactor,imagesize[1]*multiplyfactor))[1][2]),re.sub(r'Y2',str(self.getposition(filterpos_p,imagesize,(imagesize[0]*multiplyfactor,imagesize[1]*multiplyfactor))[1][3]),re.sub(r'Y3',str(round(1-self.getposition(filterpos_p,imagesize,(imagesize[0]*multiplyfactor,imagesize[1]*multiplyfactor))[1][3],3)),self.filterlist[1006][0]))))))+("[int];"+'color=0x'+''.join(re.sub(r'^0x','0',hex(int(i)))[-2:] for i in glasscolor_p[:3])+'@'+str(round(glasscolor_p[3]/255,3) if glasscolor_p[3] else 0)+':s='+'x'.join([str(int(imagesize[0]*multiplyfactor)),str(int(imagesize[1]*multiplyfactor))])+"[i];[i][int]overlay=0:0" if glasscolor_p!=(0,0,0,0) else "")+",setpts=PTS+"+str(duration_p[0])+"/TB[i];"+'[bg][i]'+self.convertfilter(str(self.getposition(filterpos_p,(imagesize[0]*multiplyfactor,imagesize[1]*multiplyfactor))[0][2])+'*W,'+str(self.getposition(filterpos_p,(imagesize[0]*multiplyfactor,imagesize[1]*multiplyfactor))[1][2])+'*H',False)+":enable='lte(t,"+str(duration_p[0]+duration_p[1])+")':shortest=1" if multiply_p and duration_p[1] else ""
   alpha=re.sub(r'.*w\)?(.*),.*',r'\1',filterpos_p) if re.search(r'w',filterpos_p) else '*'+str(min(1.0,round((self.videowidth*float(re.findall(r'\d+(?:[.]\d+)?',filterpos_p)[0])/(self.videowidth-imagesize[0])),3)))
   beta=re.sub(r'.*h\)?(.*)',r'\1',filterpos_p) if re.search(r'h',filterpos_p) else '*'+str(min(1.0,round((self.videoheight*float(re.findall(r',(\d+(?:[.]\d+)?)',filterpos_p)[0])/(self.videoheight-imagesize[1])),3)))
   glassscaleblendzoom2="["+str(1)+"]scale="+(str(int(2.0*self.videowidth)) if self.videowidth>=self.videoheight else '-1')+":"+(str(int(2.0*self.videoheight)) if self.videoheight>self.videowidth else '-1')+",format=yuva422p,pad="+str(multiplyfactor)+"*iw:"+str(multiplyfactor)+"*ih:(ow-iw)"+alpha+":(oh-ih)"+beta+":color=black@0,zoompan=z='min(zoom+0.01,"+str(multiplyfactor)+")':x=iw"+alpha+"-(iw/zoom)"+alpha+":y=ih"+beta+"-(ih/zoom)"+beta+":d="+str(duration_p[1]*25)+":s="+str(int(imagesize[0]*multiplyfactor))+"x"+str(int(imagesize[1]*multiplyfactor))+",setpts=PTS+"+str(duration_p[0])+"/TB[i];[bg][i]overlay=(W-w)"+alpha+":(H-h)"+beta+":shortest=1:enable='lte(t,"+str(duration_p[0]+duration_p[1])+")'"  if multiply_p and duration_p[1] else ""
#   overlay2=(",setpts=PTS+"+str(self.getsecond(args_p[j]))+"/TB[bg];"+("[0:v]" if not count_p else "[io"+str(count_p-1)+"]")+"[bg]overlay=eof_action=pass[io"+str(count_p)+"];" if split_p else "[io"+str(count_p)+"];")
   background=('['+str(len(re.findall(r'-i ',beginstring))-1)+"]split=2[bg][v];[bg]drawbox=t=fill:color=#000000[bg];[v]crop=7*iw/10[v];[bg][v]overlay='max(0,3*W/20-t/0.1*3*W/20)'[bg];") if split_p else ""
   if singleton:
    returnstring_p+=glassscaleblend1
   else:
    self.ffmpeg('ffmpeg '+beginstring+' -filter_complex "'+background+glassscaleblend1+(glassscaleblendzoom2 if re.search(r'[.](png|jpg|jpeg)$',image_p,re.I) else glassscaleblend2)+'" -y input'+str(count_p)+'.mp4')
    beginstring_p+="-i input"+str(count_p)+".mp4 "
    returnstring_p+="["+str(len(re.findall(r' -i ',beginstring_p))-1)+":v]setpts=PTS+"+self.getsecond(args_p[j])+"/TB[bio"+str(count_p)+"];"+("[0:v]" if not count_p else "[io"+str(count_p-1)+"]")+"[bio"+str(count_p)+"]overlay=eof_action=pass[io"+str(count_p)+"];"
   count_p=count_p+1
  return (beginstring_p,returnstring_p,count_p)
