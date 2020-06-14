import os
import sys
from PIL import Image,ImageDraw,ImageFont
import re
import libm
import blendm, zoomm, overlaym, textm, miscm
class gifc:
 arg=list()
 classobject=[
              ('blend','blendimage','sidebyside'), #0
              ('zoom','rotateandzoom'), #1
              ('overlay','overlay','logo','sidebyside'), #2
              ('text','titletext','annotation','messagebox','stilltext'), #2
              ('misc','scenetransition') #3
             ]
 filter={
         1:("",-1,"#Blend"),\
          10:("blend=all_expr='A*(1-min(T/2,1))+B*(min(T/2,1))'",(0,0),"#Blending(0,0)"),\
          11:("",-1,"#Curtain 0(u) 1(r) 2(d) 3(l) (0,0)"),\
           110:("blend=all_expr='if(lte(Y,(H-T/2*H)),A,B)'",(0,0),""),\
           111:("blend=all_expr='if(gte(X,(T/2*W)),A,B)'",(0,0),""),\
           112:("blend=all_expr='if(gte(Y,(T/2*H)),A,B)'",(0,0),""),\
           113:("blend=all_expr='if(lte(X,(W-T/2*W)),A,B)'",(0,0),""),\
          13:("",-1,"#OpenClose 0(vo) 1(ho) 2(co) 3(cc) 4(ew) (0,0)"),\
           130:("blend=all_expr='if(between(X,(W/2-T/2*W/2),(W/2+T/2*W/2)),B,A)'",(0,0),""),\
           131:("blend=all_expr='if(between(Y,(H/2-T/2*H/2),(H/2+T/2*H/2)),B,A)'",(0,0),""),\
           132:("blend=all_expr='if(gte(sqrt((X-W/2)*(X-W/2)+(H/2-Y)*(H/2-Y)),(T/2*max(W,H))),A,B)'",(0,0),""),\
           133:("blend=all_expr='if(lte(sqrt((X-W/2)*(X-W/2)+(H/2-Y)*(H/2-Y)),(max(W,H)-(T/2*max(W,H)))),A,B)'",(0,0),""),\
           134:("blend=all_expr='if(between(X,(W/2-T/1*W/2),(W/2+T/1*W/2))*between(Y,(H/2-T/1*H/2),(H/2+T/1*H/2)),B,A)'",(0,0),""),\
          14:("",-1,"#SidebySide"),\
           140:("split=2[bg][v];[bg]drawbox=t=fill[bg];[v]crop=iw/2:ih[v];[1][v]scale2ref=oh*mdar:ih/2[ic][vc];[ic]split=2[ic1][ic2];[ic1]format=yuva422p,pad=2*iw:2*ih:(ow-iw):(oh-ih)/2:color=black@0[ic1];[bg][vc]overlay='max(0,W/4-t/0.5*W/4)'[bg];[bg][ic1]blend=all_expr='if(gt(X,W/2+2)*between(Y,(H/2-(T-0.5)/1.5*H/2),(H/2+(T-0.5)/1.5*H/2)),B,A)':enable='gt(t,0.5)*lt(t,4)'[bg];[ic2]pad=iw+4:ih+4:(ow-iw)-2:(oh-ih)-2:color=#004000[ic2];[bg][ic2]overlay='max((W-w)/2,W/2-(t-4)/1*W/2)':(H-h)/2:enable='gte(t,4)'[bg];[bg][0]blend=all_expr='if(between(X,(W/4-(T-5)/1*W/4),(3*W/4+(T-5)/1*W/4))*between(Y,(H/4-(T-5)/1*H/4),(3*H/4+(T-5)/1*H/4)),B,A)':enable='gt(t,5)'",(0,1),"#sidebysideimage(0,1)"),\
         2:("",-1,"#Zoom"),\
          #20:("scale=-1:XX,format=yuva444p,pad=3*iw:3*ih:(ow-iw)/2:(oh-ih)/2:color=black@0,rotate=a='if(lte(t,1),PI*4*t,2*PI)':c=none[rotate1];[0][rotate1]overlay=(W-w)/2:(H-h)/2:shortest=1[out];[2][out]scale2ref=w=oh*mdar:h=ih*2[11][00];[11]format=yuva444p,pad=3*iw:3*ih:(ow-iw)/2:(oh-ih)/2:color=black@0,zoompan=z='min(zoom+0.04,3)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=50:s=YY[img];[img]setpts=PTS+1/TB[img];[00][img]overlay='(W-w)/2':'(H-h)/2'",(1,0),"#rotateandzoom(1,0)"),\
          20:("scale=XX,format=yuva444p,pad=3*iw:3*ih:(ow-iw)/2:(oh-ih)/2:color=black@0,rotate=a='if(lte(t,1),PI*4*t,2*PI)':c=none[rotate1];[0][rotate1]overlay=(W-w)/2:(H-h)/2:shortest=1[out];[2][out]scale2ref=w=oh*mdar:h=ih*2[11][00];[11]format=yuva444p,pad=3*iw:3*ih:(ow-iw)/2:(oh-ih)/2:color=black@0,zoompan=z='min(zoom+0.04,3)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=50:s=YY[img];[img]setpts=PTS+1/TB[img];[00][img]overlay='(W-w)/2':'(H-h)/2'",(1,0),"#rotateandzoom(1,0)"),\
          #20:("scale=107:-1,format=yuva444p,pad=3*iw:3*ih:(ow-iw)/2:(oh-ih)/2:color=black@0,rotate=a='if(lte(t,1),PI*4*t,2*PI)':c=none[rotate1];[0][rotate1]overlay=(W-w)/2:(H-h)/2:shortest=1[out];[2][out]scale2ref=w=iw*2:h=(main_h/main_w)*ow[11][00];[11]format=yuva444p,pad=3*iw:3*ih:(ow-iw)/2:(oh-ih)/2:color=black@0,zoompan=z='min(zoom+0.04,3)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=50:s=YY[img];[img]setpts=PTS+1/TB[img];[00][img]overlay='(W-w)/2':'(H-h)/2'",(1,0),"#rotateandzoom(1,0)"),\
         3:("",-1,"#Overlay"),\
          30:("overlay=x=W-w:y=(H-h)/4",(2,0),"#logo(2,0)"),\
         #21:("overlay=x=(W-w)/2:y='if(lt(H-exp((t)+4)\,(H-h)/2)\,(H-h)/2\,H-exp((t)+4))':eof_action=pass",3,"#titleBottomUp"),\
          31:("",-1,"#Curtain 0(u) 1(r) 2(d) 3(l) (2,0)"),\
           310:("overlay=x='(W-w)/2':y='max((H-h)/2,H-t/2*H)'",(2,0),""),
           311:("overlay=x='min((W-w)/2,-w+t/2*W)':y='(H-h)/2'",(2,0),""),\
           312:("overlay=x='(W-w)/2':y='min((H-h)/2,-h+t/2*H)'",(2,0),""),\
           313:("overlay=x='max((W-w)/2,W-t/1*W)':y='(H-h)/2'",(2,0),""),\
          32:("",-1,"#SidebySide"),\
           320:("scale2ref=oh*mdar:ih[11][00];[00]split=2[bg][v];[bg]drawbox=t=fill[bg];[v]crop=iw/2:ih[vc];[11]crop=iw/2:ih[ic];[ic]format=yuva422p,pad=2*iw:ih:(ow-iw):(oh-ih)/2:color=black@0[ic];[bg][vc]overlay='max(0,W/4-t/0.25*W/4)'[bg];[bg][ic]blend=all_expr='if(gt(X,W/2+2)*between(Y,(H/2-(T-0.25)/1*H/2),(H/2+(T-0.25)/1*H/2)),B,A)':enable='gt(t,0.25)'[bg];[0][bg]overlay",(2,2),"#overlaysidebyside"),\
         4:("",-1,"#Text"),\
          40:("overlay=eof_action=pass",(3,0),"#titleText"),\
          41:("overlay=x=(W-w)*3/4:y=(H-h)*3/4:eof_action=pass",(3,1),"#annotation"),\
          42:("overlay=eof_action=pass",(3,2),"#messagebox"),\
          43:("overlay=eof_action=pass",(3,3),"#linemessage"),\
          44:("overlay=eof_action=pass",(3,4),"#stilltext"),\
         5:("",-1,"Misc"),\
          50:("select='gte(scene,0.8)',metadata=print:file=time.txt\" -vsync vfr img%03d.png",(4,0),"#scenetransition(4,0)")
        }
 def __init__(self):
  if len(sys.argv)<2 or sys.argv[1]=='-f' or re.search(r'^\(\d+',sys.argv[1]):
   print("usage------")
   print("python3 gifm.py [-f] [\"(2,4)\"] <filternumber:[...]> [args]")
   print("python3 gifm.py \"310:<imagename>:<duration>:<filter>\" 00:20:30.200 \"20:<imagename>\" 00:40:10")
   print("python3 gifm.py -f")
   print("python3 gifm.py \"(2,4)\"")
   if len(sys.argv)<2 or sys.argv[1]=='-f':
    print("######### FILTERS #########")
   for item in self.filter.items():
    if len(sys.argv)==1 and item[1][2]!='':
     print("{}:{}".format(' '*(len(str(item[0]))-1)+str(item[0]),item[1][2]))
    elif len(sys.argv)==2 and sys.argv[1]=='-f':
     print("{}:{} {}".format(' '*(len(str(item[0]))-1)+str(item[0]),item[1][2],item[1][0]))
   for item in range(len(self.classobject)):
    if len(sys.argv)==2 and re.search(r'^\(\d+',sys.argv[1]) and str(item) in re.findall(r'\d+',sys.argv[1]):
     docclassstring=eval(self.classobject[item][0]+'m.'+self.classobject[item][0]+'c.__doc__')
     for i in range(len(self.classobject[item])):
      if i==0 and docclassstring:
       print(str(item)+self.classobject[item][i]+' '+docclassstring)
      elif docclassstring:
       docclassmethodstring=eval(self.classobject[item][0]+'m.'+self.classobject[item][0]+'c.'+self.classobject[item][i]+'.__doc__')
       if docclassmethodstring: print(' '+str(i-1)+self.classobject[item][i]+'\n  '+docclassmethodstring)
   exit(-1)
  self.libi=libm.libc()
  i=1
  while i<len(sys.argv):
   filterarg=list()
   filterarg.append(sys.argv[i])
   i=i+1
   while i<len(sys.argv) and re.search(r'\d+(:\d+:\d+|[.]\d+)',sys.argv[i]):
    filterarg.append(sys.argv[i])
    i=i+1
   self.arg.append(filterarg)
  print("arguments {}".format(self.arg))
  for obj in self.classobject:
   exec("self."+obj[0]+"i="+obj[0]+"m."+obj[0]+"c(self.libi)")
 def process(self):
  beginstring="ffmpeg -i input.mp4 "
  returnstring=""
  count=0
  for i in range(len(self.arg)):
   index=int(re.sub(r'^(\d+).*',r'\1',self.arg[i][0]))
   print("calling index {}".format(index))
#   beginstring,returnstring,count=getattr(self.libi,libm.libc.filterfunction[self.filter[index][1]],None)(self.arg[i],self.filter[index][0],beginstring,returnstring,count)
   beginstring,returnstring,count=getattr(eval("self."+self.classobject[self.filter[index][1][0]][0]+"i"),self.classobject[self.filter[index][1][0]][self.filter[index][1][1]+1],None)(self.arg[i],self.filter[index][0],beginstring,returnstring,count)
  return beginstring+"-filter_complex \""+re.sub(r';$','',returnstring)+"\" -map \"[io"+str(count-1)+"]\" -map 0:a -c:a copy -preset ultrafast -y output.mp4"

print(gifc().process())
