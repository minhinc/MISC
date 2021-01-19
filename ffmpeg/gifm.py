import os
import sys
from PIL import Image,ImageDraw,ImageFont
import re
import libm
import blendm, zoomm, overlaym, textm, miscm
class gifc:
 arg=list()
 classobject=[
              ('blend','blendimage'), #0
              ('zoom','rotateandzoom'), #1
              ('overlay','overlay'), #2
              ('text','dialogtext','swipetext','logotext','omnitext'), #2
              ('misc','scenetransition','breakvideo','addvideo') #3
             ]

 filter={
         1:("",-1,"#Blend"),\
          10:(10,(0,0),"#Blending(0,0)"),\
#          11:(12,(0,0),"#Curtain 0(u) 1(r) 2(d) 3(l) (0,0)"),\
#          12:(20,(0,0),"#OpenClose 0(vo) 1(ho) 2(co) 3(cc) 4(ew) (0,0)"),\
#          14:(30,(0,1),"#SidebySide"),\
         2:("",-1,"#Zoom"),\
          20:(40,(1,0),"#rotateandzoom(1,0)"),\
#         3:("",-1,"#Overlay"),\
#          30:(70,(2,0),"#logo(2,0)"),\
#          31:(63,(2,0),"#Curtain 0(u) 1(r) 2(d) 3(l) (2,0)"),\
#          32:(80,(0,1),"#SidebySide(2,2)"),\
         4:("",-1,"#Text"),\
          40:(52,(3,0),"#dialogtext"),\
          41:(52,(3,1),"#swipetext"),\
          42:(52,(3,2),"#logotext"),\
          43:(52,(3,3),"#omnitext"),\
          44:(52,(3,4),"#alphaimage"),\
         5:("",-1,"Misc"),\
          50:(90,(4,0),"#scenetransition(4,0)"),\
          51:(50,(4,1),"#breakvideo(4,1)"),\
          52:(50,(4,2),"#addvideo(4,2)")
        }
 def __init__(self):
  if len(sys.argv)<2 or sys.argv[1]=='-f' or re.search(r'^\(\d+',sys.argv[1]):
   print("usage------")
   print("python3 gifm.py [-f] [\"(2,4)\"] [-d] <filternumber:[...]> [args]")
   print("python3 gifm.py -d \"310:<imagename>:<duration>:<filter>\" 00:20:30.200 \"20:<imagename>\" 00:40:10")
   print("python3 gifm.py -f")
   print("python3 gifm.py \"(2,4)\"")
   if len(sys.argv)==2 and sys.argv[1]=='-f':
    print("######### FILTERS #########")
    for key,value in libm.libc.filterlist.items():
     print("{} {}".format(key,value))
    exit(-1)
   for item in self.filter.items():
    if len(sys.argv)==1 and item[1][2]!='':
     print("{}:{}:{}:{}".format(' '*(len(str(item[0]))-1)+str(item[0]),item[1][0],item[1][1],item[1][2]))
#     if item[1][1]!=-1:print(eval(self.classobject[item[1][1][0]][0]+'m.'+self.classobject[item[1][1][0]][0]+'c.'+self.classobject[item[1][1][0]][item[1][1][1]+1]+'.__doc__'))
  #  elif len(sys.argv)==2 and sys.argv[1]=='-f':
  #   print("{}:{} {}".format(' '*(len(str(item[0]))-1)+str(item[0]),item[1][2],item[1][0]))
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
  if sys.argv[1]=='-d': # debug mode
   print('######## DEBUG MODE ########')
   libm.libc.debugb=True
   sys.argv.pop(1)
  self.libi=libm.libc()
  i=1
  while i<len(sys.argv):
   filterarg=list()
   filterarg.append(sys.argv[i])
   i=i+1
   while i<len(sys.argv) and re.search(r'^\d+(:\d+:\d+|[.]\d+)',sys.argv[i]):
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
   index=int(re.sub(r'^\D?(\d+).*',r'\1',self.arg[i][0]))
   beginstring,returnstring,count=getattr(eval("self."+self.classobject[self.filter[index][1][0]][0]+"i"),self.classobject[self.filter[index][1][0]][self.filter[index][1][1]+1],None)(self.arg[i],self.filter[index][0],beginstring,returnstring,count)
  return beginstring+"-filter_complex \""+re.sub(r';$','',returnstring)+"\" -map \"[io"+str(count-1)+"]\" -map 0:a -c:a copy "+("-preset ultrafast " if self.libi.debugb else '')+"-y output.mp4"

print(gifc().process())
