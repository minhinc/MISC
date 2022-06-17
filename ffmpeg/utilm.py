import datetime
import os
import sys
from PIL import Image,ImageDraw,ImageFont
import textwrap
import re
import math
#import json
import requests
import MISC.ffmpeg.libm as libm
class utilc:
 '''1. Video editing functions
    2. Gif creation functions
    3. Image manipulation functions'''
 def __init__(self,debug=False,inputfile=None,libp=None):
  '''Enable debug True/False'''
  self.libi=libm.libc(debug,inputfile=inputfile) if not libp else libp

 def setvideo(self,inputfile):
  self.libi.setvideo(inputfile)

 def addalpha(self,imagename,alpha,outimagename=None):
  '''Add alpha to image/video (png/jpg/mp4)'''
  self.libi.debug("><addalpha",imagename,alpha,outimagename)
  mask=Image.new(r'L',[int(i) for i in self.libi.videoattribute(imagename)[0]] if re.search(r'[.]mp4$',imagename,re.I) else Image.open(imagename).size,color=alpha)
  if re.search(r'video',self.libi.exiftool(imagename,'MIME Type'),re.I):
   outimagename=self.libi.outimagename(imagename,outimagename,'mov')
   mask.save(self.libi.adddestdir('maskimage.png'))
   mask.close()
   self.libi.ffmpeg("ffmpeg -i "+imagename+" -loop 1 -i "+self.libi.adddestdir('maskimage.png')+" -filter_complex \"[0][1]alphamerge\" -pix_fmt rgba -vcodec png -y "+outimagename)
  else:
   outimagename=self.libi.outimagename(imagename,outimagename)
   img=Image.open(imagename).convert('RGBA')
   img.putalpha(mask)
   img.save(outimagename)
   img.close()
  return outimagename

# def image2gif(self,imagename,filter,mode,duration=None,backcolor=(0,0,0,0),outimagename=None):
 def image2gif(self,imagename,filtermode,duration=None,backcolor=(0,0,0,0),outimagename=None):
  '''Create mov from png/gif/.mp4 image based on filter,mode libc.filter[filter][mode]
   imangename - listof imagename for chimchim else str
   filter - blend/overlay
   mode - up/left/bottom/right.... see libc.filter
   imagename - input png/gif/.mp4 image
   duration - total duration of mov=None
   backcolor - background glass color
   outimagename - output mov name=<imagename>_<count>.mov'''
  print(f'><utilc.image2gif imagename={imagename} type(imagename)={type(imagename)} filtermode={filtermode} duration={duration} backcolor={backcolor}')
  filtermode=self.libi.filter[str(filtermode)] if re.search(r'^\d+$',str(filtermode)) else filtermode
  img=Image.new('RGBA',[int(i) for i in self.libi.videoattribute(imagename)[0]] if re.search('video',self.libi.exiftool(imagename,'MIME Type'),re.I) else Image.open(imagename).size,backcolor) if not type(imagename)==tuple else Image.new('RGBA',Image.open(imagename[0]).size,backcolor)
  img.save(self.libi.adddestdir('transparentpng.png'))
  img.close()
#  os.system('rm out*.png')
#  self.libi.system("ffmpeg -i transparentpng.png"+(" -loop 1 -t "+str(duration) if not re.search(r'.(gif|mp4)$',imagename) else "")+" -i "+imagename+" -filter_complex \""+("[0][1]" if not re.search(r'^\[',self.libi.filter[filter][mode]) else "")+self.libi.filter[filter][mode]+",split=2[b][f];[b]palettegen[b];[f][b]paletteuse,fps=10\" -vsync 0 out%0"+str(int(math.log10(duration*10))+1)+"d.png")
  outimagename=self.libi.outimagename(imagename,outimagename,extension='mov') if not type(imagename)==tuple else self.libi.outimagename(re.sub(r'^(.*)[.].*',r'\1'+r'.gif',imagename[0]))
#  self.libi.system("ffmpeg -i transparentpng.png"+(" -loop 1 -t "+str(duration) if not re.search(r'.(gif|mp4)$',imagename) else "")+" -i "+imagename+" -filter_complex \""+("[0][1]" if not re.search(r'^\[',self.libi.filter[filter][mode]) else "")+self.libi.filter[filter][mode]+"\" -pix_fmt rgba -vcodec png "+outimagename)
  if type(imagename)==tuple:
   self.libi.system('convert -loop 0 -dispose Background -delay 20 '+' '.join(imagename[count%len(imagename)]+' '+self.libi.adddestdir('transparentpng.png') for count in range(len(imagename)))+' '+self.libi.adddestdir(outimagename))
  else:
   self.libi.ffmpeg("ffmpeg -i "+self.libi.adddestdir('transparentpng.png')+" "+(("-loop 1 " if not re.search(r'[.](gif|mov|mp4)$',imagename) else "-ignore_loop 0 " if re.search(r'[.]gif$',imagename,re.I) else "")+"-t "+str(duration)+" " if duration else "")+"-i "+imagename+" -filter_complex \""+("[0][1]" if not re.search(r'^\[',filtermode) else "")+filtermode+"\" -pix_fmt rgba -vcodec png -y "+outimagename)
#  duration=duration if duration else float(self.libi.exiftool(imagename,'Duration')) if re.search(r'[.](gif|mov|mp4)$',imagename,re.I) else duration
#  self.libi.ffmpeg("ffmpeg -loop 1 -t "+str(duration)+" -i transparentpng.png "+(("-ignore_loop 0 " if re.search(r'[.]gif$',imagename,re.I) else "")+"-t "+str(duration)+" " if duration and re.search(r'[.](gif|mov|mp4)$',imagename,re.I) else "")+"-i "+imagename+" -filter_complex \""+("[0][1]" if not re.search(r'^\[',self.libi.filter[filter][mode]) else "")+self.libi.filter[filter][mode]+"\" -pix_fmt rgba -vcodec png -y "+outimagename)
#  self.libi.system("convert -loop 1 -dispose Background -delay 10 out*.png "+outimagename)
  return outimagename

 def text2image(self,text,textcolor='r',backcolor=(0,0,0,0),size=0.3,stroke=False,alignment='m',linemargin=10,richtext=False,outimagename=None):
  '''\
  ------ richtext=True, Rich text properties for each line in Text ------
  text - ='<text>:<textcolor>:<backcolor>:<size>:<stroke>:<alignment>:<linemargin>\n<text>:<textcolor>......\n<text>...'
          'Hello World:r::0.5:::20\nHow are you::::::'
         --------------------
  ----- richtext=False, Common properties of all lines or default properties for separate line text properties (above) -----
  text - multiline text separate by '\n', NO raw text = 'Hello\nWorld'
  textcolor - default color of text = 'red' see lib.palettecolor
  backcolor - background color of text = (0,0,0,192)
  size - width of textline/video width = 0.4
  stroke - Need stroke (True/False) = False
  alignment - m:center l:left = 'm'
  margin - inter line margin
  outimagename - output image file name = To auto generated
  ex. 'Hello World\nHow are Your,textcolor='g',backcolor=(255,0,0,128),size=0.4,stroke=True'
            ----------------'''
  stringlist=[]
  offset=4
  yoffset=4
  print(f'><utilc.text2image text={text}')
  if richtext:
   for i in re.split('\n',text):
    stringlist.append(self.libi.split(i,('',textcolor,str(backcolor),size,stroke,alignment,linemargin)))
  else:
   stringlist.append((text,textcolor,str(backcolor),size,stroke,alignment,linemargin))
#  imagewidth=max([self.libi.getfont([stringlist[i][0]] if len(stringlist[i][0]) >= 20 else ['Q'*20],stringlist[i][3],os.path.expanduser('~')+r'/.fonts/Consolas.ttf').getsize(stringlist[i][0])[0]+offset for i in range(len(stringlist))])
  imagewidth=max([self.libi.getfont(re.split('\n',text[0]) if max([len(x) for x in re.split('\n',text[0])]) >= 20 else ['Q'*20],text[3] if richtext else size,os.path.expanduser('~')+r'/.fonts/Consolas.ttf').getsize(text[0] if richtext else 'Q'*max(len(x) for x in re.split('\n',text[0])))[0]+offset for count,text in enumerate(stringlist)])
#  imageheight=sum([self.libi.getfont([stringlist[i][0]] if len(stringlist[i][0]) >= 20 else ['Q'*20],stringlist[i][3],os.path.expanduser('~')+r'/.fonts/Consolas.ttf').getsize(stringlist[i][0])[1]+stringlist[i][6] for i in range(len(stringlist))])
  imageheight=sum([self.libi.getfont([(text[0] if richtext else text) if len(text[0] if richtext else text) >= 20 else 'Q'*20],text[3] if richtext else size,os.path.expanduser('~')+r'/.fonts/Consolas.ttf').getsize(text[0] if richtext else text)[1]+(text[6]+yoffset if richtext else linemargin) for count,text in enumerate(stringlist if richtext else re.split('\n',text))])-(stringlist[-1][6] if richtext else linemargin-yoffset)
  print(f'stringlist={stringlist} imagewidth={imagewidth} imageheight={imageheight}')
  img=Image.new('RGBA',(imagewidth,imageheight),(0,0,0,0))
  draw=ImageDraw.Draw(img)
  #bottommargin=0
  for count,text in enumerate(stringlist):
   fntl=self.libi.getfont(re.split('\n',text[0]) if max(len(x) for x in re.split('\n',text[0])) >=20 else ['Q'*20],float(text[3] if richtext else size),os.path.expanduser('~')+r'/.fonts/Consolas.ttf')
#   bottommargin+=(fntl.getsize(text[0])[1] if richtext else sum(fntl.getsize(text)[1] for text in re.split('\n',text[0])))+(text[6] if richtext else linemargin)
#   draw.rectangle(((imagewidth-fntl.getsize(text[0] if richtext else 'Q'*max(len(x) for x in re.split('\n',text[0])))[0])/2-offset/2,bottommargin-(fntl.getsize(text[0])[1] if richtext else sum(fntl.getsize(text)[1] for text in re.split('\n',text[0])))-(text[6] if richtext else linemargin),(imagewidth+fntl.getsize(text[0] if richtext else 'Q'*max(len(x) for x in re.split('\n',text[0])))[0])/2+offset/2,bottommargin) if alignment=='m' else (offset/4,bottommargin-fntl.getsize(text[0])[1]-(text[6] if richtext else linemargin),fntl.getsize(text[0] if richtext else 'Q'*max(len(x) for x in re.split('\n',text[0])))[0]+offset,bottommargin),fill=self.libi.palette(text[2] if richtext else backcolor))
   draw.rectangle(((imagewidth-fntl.getsize(text[0] if richtext else 'Q'*max(len(x) for x in re.split('\n',text[0])))[0])/2-offset/2,sum([fntl.getsize(stringlist[i][0])[1]+stringlist[i][6]+yoffset for i in range(count)] or [0]) if richtext else 0,(imagewidth+fntl.getsize(text[0] if richtext else 'Q'*max(len(x) for x in re.split('\n',text[0])))[0])/2+offset/2,sum([fntl.getsize(stringlist[i][0])[1]+stringlist[i][6]+yoffset for i in range(count)] or [0])+fntl.getsize(text[0])[1]+yoffset if richtext else imageheight) if alignment=='m' else (offset/4,sum([fntl.getsize(stringlist[i][0])[1]+stringlist[i][6]+yoffset for i in range(count)] or [0]) if richtext else 0,fntl.getsize(text[0] if richtext else 'Q'*max(len(x) for x in re.split('\n',text[0])))[0]+offset,sum([fntl.getsize(stringlist[i][0])[1]+stringlist[i][6]+yoffset for i in range(count)] or [0])+fntl.getsize(text[0])[1]+yoffset if richtext else imageheight),fill=self.libi.palette(text[2] if richtext else backcolor))
   if stroke:
    self.libi.drawtextstroke(draw,(imagewidth-fntl.getsize(text[0] if richtext else 'Q'*max(len(x) for x in re.split('\n',text[0])))[0])/2 if re.search(r'm',alignment) else offset/2,bottommargin-(fntl.getsize(text[0])[1] if richtext else sum(fntl.getsize(text)[1] for text in re.split('\n',text[0])))-(text[4] if richtext else linemargin),text,fntl,self.libi.palette(text[1] if richtext else textcolor))
   else:
#    draw.text(((imagewidth-fntl.getsize(text[0] if richtext else 'Q'*max(len(x) for x in re.split('\n',text[0])))[0])/2 if re.search(r'm',alignment) else offset/2,sum([fntl.getsize(stringlist[i][0])[1]+stringlist[i][6]+yoffset for i in range(count)] or [yoffset/2]) if richtext else yoffset/2),text[0],font=fntl,fill=self.libi.palette(text[1] if richtext else textcolor))
    [draw.text(((imagewidth-fntl.getsize(text)[0])/2 if re.search(r'm',alignment) else offset/2,sum([fntl.getsize(stringlist[i][0])[1]+stringlist[i][6]+yoffset for i in range(count)] or [yoffset/2]) if richtext else sum([fntl.getsize(re.split('\n',stringlist[count][0])[x])[1]+linemargin for x in range(lcount)] or [0])+yoffset/2),text,font=fntl,fill=self.libi.palette(stringlist[count][1] if richtext else textcolor)) for lcount,text in enumerate(re.split('\n',text[0]))]
   print(f'linemargin+yofset{linemargin+yoffset}')
#   if stroke:
#    self.libi.drawtextstroke(drawmask,(imagewidth-fnt.getsize(stringlist[i])[0])/2 if re.search(r'm',alignment) else offset/2,i*textcellheight+(textcellheight-fnt.getsize(stringlist[i])[1])/2,stringlist[i],fntl,self.libi.palette(stringlist[i][2])[3])
#   else:
#    drawmask.text(((imagewidth-fntl.getsize(stringlist[i])[0])/2 if re.search(r'm',alignment) else offset/2,i*textcellheight+(textcellheight-fntl.getsize(stringlist[i])[1])/2),stringlist[i],font=fntl,fill=self.libi.palette(stringlist[i][2])[3])
 # if re.search(r'm',orientation): img.putalpha(mask)
#  img.putalpha(mask)
  outimagename=self.libi.outimagename('textimage.',extension='png')
  img.save(outimagename)
  img.close()
  return outimagename

 def logotext(self,size=0.4,textdata=('Minh, ','Inc.','A Software Research Firm'),textcolor=((0,64,0,255),(0,64,0,255),(200,200,200,255)),outimagename=None):
  '''Create Logo giff three words two lines (one+two/three)
   size - gif width/video width=0.4
   textdata=tuple of three words=('Minh, ','Inc.','A Software Research Firm')'''
  yoffset=10
  font=self.libi.getfont([textdata[0]+textdata[1]],size,os.path.expanduser('~')+r'/.fonts/ufonts.com_tw-cen-mt.ttf')
  font1=self.libi.getfont([textdata[0]+textdata[1]],size*0.8,os.path.expanduser('~')+r'/.fonts/ufonts.com_tw-cen-mt.ttf')
  font2=self.libi.getfont([textdata[2]],size,os.path.expanduser('~')+r'/.fonts/ufonts.com_tw-cen-mt.ttf')
  imagewidth=max(font.getsize(textdata[0]+textdata[1])[0],font2.getsize(textdata[2])[0])
  imageheight=int(font.getsize(textdata[0]+textdata[1])[1]+4*yoffset+font2.getsize(textdata[2])[1])
  img=Image.new('RGBA',(imagewidth,int(font.getsize(textdata[0]+textdata[1])[1]+4*yoffset+font2.getsize(textdata[2])[1])),(0,0,0,0))
  draw=ImageDraw.Draw(img)
  xoffset=(font2.getsize(textdata[2])[0]-(font.getsize(textdata[0])[0]+font1.getsize(textdata[1])[0]))/2
  if textdata[0]:draw.text((xoffset,-10),textdata[0],font=font,fill=textcolor[0])
#  if textdata[1]:draw.text((xoffset+font.getsize(textdata[0])[0],font.getsize(textdata[0])[1]-font1.getsize(textdata[0])[1]-10),textdata[1],font=font1,fill=textcolor[0])
  if textdata[1]:draw.text((xoffset+font.getsize(textdata[0])[0],font.getsize(textdata[0])[1]-font1.getsize(textdata[0])[1]-10),textdata[1],font=font1,fill=textcolor[1])
#  if textdata[2]:draw.text((int((imagewidth-font2.getsize(textdata[2])[0])/2),font.getsize(textdata[0])[1]+1.5*yoffset-10),textdata[2],font=font2,fill=textcolor[1])
  if textdata[2]:draw.text((int((imagewidth-font2.getsize(textdata[2])[0])/2),font.getsize(textdata[0])[1]+1.5*yoffset-10),textdata[2],font=font2,fill=textcolor[2])
  img.save(self.libi.adddestdir('frnt.png'))
  convertstring='convert -loop 0 -dispose Background -delay 4 '
  for j in range(2):
   for count,i in enumerate(self.libi.stepvalue(0,imagewidth+int(font.getsize(textdata[0]+textdata[1])[1]+4*yoffset+font2.getsize(textdata[2])[1]),22)):
    img=Image.open(self.libi.adddestdir('frnt.png')).convert('RGBA')
    mask=Image.new(r'L',img.size,color=0)
    draw=ImageDraw.Draw(mask)
    if textdata[0]:draw.text((xoffset,-10),textdata[0],font=font,fill=255)
    if textdata[1]:draw.text((xoffset+font.getsize(textdata[0])[0],font.getsize(textdata[0])[1]-font1.getsize(textdata[0])[1]-10),textdata[1],font=font1,fill=255)
    if textdata[2]:draw.text((int((imagewidth-font2.getsize(textdata[2])[0])/2),font.getsize(textdata[0])[1]+1.5*yoffset-10),textdata[2],font=font2,fill=255)
    if j==0:
     draw.polygon([(i,0),(0,i),(0,imagewidth*2),(imagewidth*2,0)],fill=0)
    else:
     draw.polygon([(0,0),(i,0),(0,i)],fill=0)
    img.putalpha(mask)
    convertstring+=self.libi.adddestdir('out'+str(j)+str(count)+'.png')+' '
    img.save(self.libi.adddestdir('out'+str(j)+str(count)+'.png'))
   if j==0:
    convertstring+='-delay 30 '+self.libi.adddestdir('out'+str(j)+str(count)+'.png')+' -delay 3 '
  outimagename=self.libi.outimagename('logotext.',extension='gif')
#  outimagename1=self.libi.outimagename(outimagename,extension='mov')
#  outimagename2=self.libi.outimagename(outimagename1,extension='mov')
  self.libi.system(convertstring+'-delay 1 '+self.libi.adddestdir('out'+str(j)+str(count)+'.png')+' '+outimagename)
#  self.libi.system(r'ffmpeg -i '+self.scalepad(overlayimagename,targetdimension=(imagewidth,imageheight),upscale=True,padposition='0,0',padcolor='0x00000000')+' -i '+outimagename+' -filter_complex "[0:v][1:v]overlay=shortest=1" -pix_fmt rgba -vcodec png -y '+outimagename1)
#  self.libi.system(r'ffmpeg -i '+outimagename+' -i '+self.scalepad(overlayimagename,targetdimension=(imagewidth,imageheight),padposition='0,0',padcolor='0x00000000')+' -filter_complex "[0:v][1:v]overlay=eof_action=pass" -pix_fmt rgba -vcodec png -y '+outimagename1)
#  self.libi.system(r'ffmpeg -i '+outimagename1+' -ignore_loop 1 -i '+outimagename+' -filter_complex "[0:v][1:v]overlay=eof_action=pass" -pix_fmt rgba -vcodec png -y '+outimagename2)
  return outimagename

 def swipetext(self,text,size=0.4,alignment='l',duration=6,textcolor=(255,255,255,255),glasscolor=(0,0,0,0),outimagename=None):
  '''Generate swipe text gif
   text - text to draw=r'Hollow\\nWood'
   size - text width/video width=0.4
   alignment - bar alignment l/b=l, other than l/b no bar
   duration - duration of animation=6
   textcolor - color of text=(255,255,255,255)
   glasscolor - background color=(0,0,0,0)'''
  diff=[]
  offset=10
  stringlist=re.split(r'\\n',text)
  fnt=self.libi.getfont(stringlist if max([len(x) for x in stringlist]) >= 20 else ['a'*20],size,os.path.expanduser('~')+r'/.fonts/Consolas.ttf')
  textmaxindex=[len(i) for i in stringlist].index(max([len(i) for i in stringlist]))
  textcellheight=int(fnt.getsize(stringlist[textmaxindex])[1]+offset/4)
  stepcount=20
#  convertstring="convert -loop 0 -dispose Background -delay "+str((duration*100-duration*100*0.7)/(2*stepcount))+' '
  convertstring="convert -loop 0 -dispose Background -delay "+str((100*1)/stepcount)+' '
  for i in self.libi.stepvalue(textcellheight/2,0,len(stringlist)):
   diff.append(i)
  for count,j in enumerate(self.libi.stepvalue(textcellheight+textcellheight/2,(textcellheight-fnt.getsize(stringlist[textmaxindex])[1])/2,stepcount)):
   img=Image.new('RGBA',(fnt.getsize(stringlist[textmaxindex])[0]+(offset if alignment=='l' else 0),textcellheight*len(stringlist)+(offset if alignment=='b' else 0)),(0,0,0,0))
   draw=ImageDraw.Draw(img)
   if alignment=='l':
    draw.line((0,0,0,int((textcellheight*len(stringlist))*2/stepcount*(count+1))),fill=(00,64,00,255),width=int(offset/3))
   elif alignment=='b':
    draw.line((0,textcellheight*len(stringlist)+offset/2,fnt.getsize(stringlist[textmaxindex])[0]/stepcount*(count+1),textcellheight*len(stringlist)+offset/2),fill=(00,64,00,255),width=int(offset/3))
   for i in range(len(stringlist)):
    img1=Image.new('RGBA',(fnt.getsize(stringlist[textmaxindex])[0],textcellheight),(0,0,0,0))
    draw=ImageDraw.Draw(img1)
    if alignment=='l' or alignment=='b':
     draw.text((0,max((textcellheight-fnt.getsize(stringlist[textmaxindex])[1])/2,j-int(diff[i]))),stringlist[i],font=fnt,fill=textcolor)
    else:
     draw.text(((img1.width-fnt.getsize(stringlist[i])[0])/2,max((textcellheight-fnt.getsize(stringlist[textmaxindex])[1])/2,j-int(diff[i]))),stringlist[i],font=fnt,fill=textcolor)
    img.paste(img1,(int(offset*2/3) if alignment=='l' else 0,i*textcellheight))
   img.save(self.libi.adddestdir("swipetext"+str(count)+".png"))
   convertstring+=self.libi.adddestdir("swipetext"+str(count)+".png")+" "
#  convertstring+="-delay "+str(duration*100*0.7)+" swipetext"+str(count)+".png -delay "+str((duration*100-duration*100*0.7)/stepcount)+' '
  convertstring+="-delay "+str((duration-2)*100)+" "+self.adddestdir("swipetext"+str(count)+".png")+" -delay "+str((100*1)/(stepcount/2))+' '
  for count,j in enumerate(self.libi.stepvalue((textcellheight-fnt.getsize(stringlist[textmaxindex])[1])/2,-fnt.getsize(stringlist[textmaxindex])[1],int(stepcount/2))):
   img=Image.new('RGBA',(fnt.getsize(stringlist[textmaxindex])[0]+(offset if alignment=='l' else 0),textcellheight*len(stringlist)+(offset if alignment=='b' else 0)),(0,0,0,0))
   draw=ImageDraw.Draw(img)
   for i in range(len(stringlist)):
    img1=Image.new('RGBA',(fnt.getsize(stringlist[textmaxindex])[0],textcellheight),(0,0,0,0))
    draw=ImageDraw.Draw(img1)
    if alignment=='l' or alignment=='b':
     draw.text((0,j),stringlist[i],font=fnt,fill=(255,255,255,255))
    else:
     draw.text(((img1.width-fnt.getsize(stringlist[i])[0])/2,j),stringlist[i],font=fnt,fill=(255,255,255,255))
    img.paste(img1,(int(offset*2/3) if alignment=='l' else 0,i*textcellheight))
   img.save(self.libi.adddestdir("swipetext"+str(count)+'u'+".png"))
   convertstring+=self.libi.adddestdir("swipetext"+str(count)+'u'+".png")+" "
  outimagename=self.libi.outimagename('swipetext.',extension='gif')
  self.libi.system(convertstring+outimagename)
  return outimagename

 def omnitext(self,text,size=0.4,duration=6,alignment='o',shadecolor=(0,0,0,128),outimagename=None):
  '''Generate omni text gif image
   text - text to draw ex. - r'Qt\\nQScrollBar\\nQml'
   size - text width/video width =0.4
   duration - animation duration=6
   alignment - text alignment [li|o]=o
   backcolor - background color=(0,0,0,128)'''
  offset=10
  stringlist=[]
  fnt=self.libi.getfont(re.split(r'\\n',text) if max([len(x) for x in re.split(r'\\n',text)]) >= 20 else ['Q'*20],float(size),os.path.expanduser('~')+r'/.fonts/Consolas.ttf')
  fnts=self.libi.getfont(re.split(r'\\n',text) if max([len(x) for x in re.split(r'\\n',text)]) >= 20 else ['Q'*20],float(size)*0.5,os.path.expanduser('~')+r'/.fonts/Consolas.ttf')
  for i in range(len(re.split(r'\\n',text))):
   if re.search(r'(^|\\n)><',text):
    stringlist.append([re.sub(r'><(.*)',r'\1',re.split(r'\\n',text)[i]),None,int(fnt.getsize(re.sub(r'><(.*)',r'\1',re.split(r'\\n',text)[i]))[1]+offset),fnt] if re.search(r'^><',re.split(r'\\n',text)[i]) else [re.split(r'\\n',text)[i],None,int(fnts.getsize(re.split(r'\\n',text)[i])[1]+offset/6),fnts])
   else:
    stringlist.append([re.split(r'\\n',text)[i],None,int(fnt.getsize(re.split(r'\\n',text)[i])[1]+4*offset),fnt])
  for i in range(len(stringlist)-1,-1,-1):
   if not re.search(r'^[ ]*$',stringlist[i][0]):
    stringlist[i][2]+=int(offset-offset/6) if stringlist[i][3]==fnts else 0
    break
  textmaxindex=[stringlist[i][3].getsize(stringlist[i][0])[0] for i in range(len(stringlist))].index(max(stringlist[i][3].getsize(stringlist[i][0])[0] for i in range(len(stringlist))))
#  for i in range(len(stringlist)):
#   stringlist[i][2]=int(fnt.getsize(stringlist[i][0])[1]+offset) if stringlist[i][3]==fnt else int(fnts.getsize(stringlist[i][0])[1]+offset/6)
  glassrect=(stringlist[textmaxindex][3].getsize(stringlist[textmaxindex][0])[0],sum(stringlist[i][2] for i in range(len(stringlist)) if not re.search(r'^[ ]*$',stringlist[i][0])))
#  glassrect=(stringlist[textmaxindex][3].getsize(stringlist[textmaxindex][0])[0],sum(stringlist[i][2] for i in range(len(stringlist))))
#  animationrect=(glassrect[0]*2,glassrect[1]*2)
  animationrect=(glassrect[0]*2,sum(stringlist[i][2] for i in range(len(stringlist)))*2)
  print("glassrect animationrect {} {}".format(glassrect,animationrect))
#  sumtextcellheight=(animationrect[1]-glassrect[1])/2
  sumtextcellheight=(animationrect[1]-animationrect[1]/2)/2
  for i in range(len(stringlist)):
   sumtextcellheight+=0 if i==0 else stringlist[i-1][2]
   #stringlist[i][1]=(int((animationrect[0]-sum(stringlist[i][3].getsize(stringlist[i][0])[0] for i in range(len(stringlist)))/len(stringlist))/2) if orientation!='o' else int((animationrect[0]-stringlist[i][3].getsize(stringlist[i][0])[0])/2),sumtextcellheight)
   stringlist[i][1]=(int((animationrect[0]-stringlist[textmaxindex][3].getsize(stringlist[textmaxindex][0])[0])/2) if alignment[0]!='o' else int((animationrect[0]-stringlist[i][3].getsize(stringlist[i][0])[0])/2),sumtextcellheight)
  stepcount=22
  convertstring="convert -loop 0 -dispose Background -delay "+str(100/stepcount)+" "
  anglelist=[i for i in self.libi.stepvalue(-90,270,len(stringlist)+1) if i!=270]
  for i in range(1,int(len(anglelist)-1),2):
   tmp=anglelist[i]
   anglelist[i]=anglelist[len(anglelist)-1]
   for x in range(len(anglelist)-1,i+1,-1):
    anglelist[x]=anglelist[x-1]
   anglelist[i+1]=tmp
#  anglelist=[self.libi.getrectpoint(stringlist[count][1],(0,0,*animationrect),angle,(stringlist[count][3].getsize(stringlist[count][0])[0],stringlist[count][2])) for count,angle in enumerate(anglelist)]
  vertexlist=[self.libi.getrectpoint((animationrect[0]/2,stringlist[count][1][1]),(0,0,*animationrect),angle,(stringlist[count][3].getsize(stringlist[count][0])[0],stringlist[count][3].getsize(stringlist[count][0])[1])) for count,angle in enumerate(anglelist)]
  lineindex=0
#  for count,z in enumerate(zip(*(zip(self.libi.stepvalue(anglelist[i][0]-stringlist[i][3].getsize(stringlist[i][0])[0]/2,stringlist[i][1][0],stepcount),self.libi.stepvalue(anglelist[i][1],stringlist[i][1][1],stepcount)) for i in range(len(anglelist))))):
  for count,z in enumerate(zip(*(zip(self.libi.stepvalue(vertexlist[i][0]-(animationrect[0]/2-stringlist[i][1][0]),stringlist[i][1][0],stepcount),self.libi.stepvalue(vertexlist[i][1],stringlist[i][1][1],stepcount)) for i in range(len(vertexlist))))):
   img=Image.new('RGBA',animationrect,(0,0,0,0))
   draw=ImageDraw.Draw(img)
#   lineheight=(animationrect[1]-glassrect[1])/2+(count+1)/stepcount*glassrect[1]
   lineheight=(animationrect[1]-animationrect[1]/2)/2+(count+1)/stepcount*animationrect[1]/2
#   print("count,lineindex,lineheight,stringlist1,stringlist2  {} {} {} {} {}".format(count,lineindex,lineheight,stringlist[lineindex][1],stringlist[lineindex][2]))
   if (stringlist[lineindex][1][1]+stringlist[lineindex][2])<lineheight: lineindex+=1
   if re.search(r'^li',alignment):
    for j in range(lineindex):
     if not re.search(r'^[ ]*$',stringlist[j][0]): draw.line(((animationrect[0]-glassrect[0])/2-offset,stringlist[j][1][1],(animationrect[0]-glassrect[0])/2-offset,stringlist[j][1][1]+stringlist[j][2]),fill='red' if stringlist[j][3]==fnt else 'white',width=int(offset/4))
    if not re.search(r'^[ ]*$',stringlist[lineindex][0]): draw.line(((animationrect[0]-glassrect[0])/2-offset,stringlist[lineindex][1][1],(animationrect[0]-glassrect[0])/2-offset,lineheight-1),fill='red' if stringlist[lineindex][3]==fnt else 'white', width=int(offset/4))
   #print(z)
   for i in range(len(z)):
    #print("y {} {} {}".format(z[i][1],stringlist[i][1],stringlist[i][3].getsize(stringlist[i][0])))
#    draw.text((z[i][0],z[i][1]+(stringlist[i][2]-stringlist[i][3].getsize(stringlist[i][0])[1])/2),stringlist[i][0],font=stringlist[i][3],fill=("white",(0,255,0,255),"yellow","orange")[i%4] if alignment[0]=='o' else "yellow" if stringlist[i][3]==fnt else "white")
    self.libi.drawtextstroke(draw,z[i][0],z[i][1]+(stringlist[i][2]-stringlist[i][3].getsize(stringlist[i][0])[1])/2,stringlist[i][0],stringlist[i][3],((0,191,243),(0,255,0,255),"yellow","orange")[i%4] if alignment[0]=='o' else "yellow" if stringlist[i][3]==fnt else "white")
#    draw.text((z[i][0],z[i][1]),stringlist[i][0],font=stringlist[i][3],fill=("white",(0,255,0,255),"yellow","orange")[i%4] if orientation[0]=='o' else "yellow" if stringlist[i][3]==fnt else "white")
#    draw.text((z[i][0],z[i][1]),stringlist[i][0],font=stringlist[i][3],fill=("white","red","yellow","orange")[i%4] if orientation=='o' else "yellow" if stringlist[i][3]==fnt else "white")
   img.save(self.libi.adddestdir("omnitext"+str(count)+".png"))
   convertstring+=self.libi.adddestdir("omnitext"+str(count)+".png ")
  convertstring+="-delay "+str((duration-1)*100)+" "+self.libi.adddestdir("omnitext"+str(count)+".png")+" -delay 10 "+self.libi.adddestdir("omnitext"+str(count)+".png")+" "
  outimagename=self.libi.outimagename('omnitext.',extension='gif')
  self.libi.system(convertstring+outimagename)
  return outimagename

 def breakvideo(self,imagename,slice,join=False,delete=False,reencode=False,outimagename=None):
  '''break video in subvidoes
   imagename - name of video file
   slice - time slice ie. ('0-40,40-00:31,00:02:00-140')
   reencode - reencode the video audio
   join - join the sliced videos
   delete - time slice is deleted slices
   outimagename - output file name'''
  print("Make sure Audacity improved audio is replaced")
  beginstring="ffmpeg "
  outimagename=self.libi.outimagename(imagename)
#  keeplist=sorted([tuple(map(self.libi.getsecond,i.split('-'))) for i in re.split(r',',slice)],key=lambda x: float(x[0]))
  keeplist=[tuple(map(self.libi.getsecond,i.split('-'))) for i in re.split(r',',slice)]
  t=[None]*2
  i=0
  if delete and keeplist:
   keeplist=sorted(keeplist,key=lambda x: float(x[0]))
   while i<len(keeplist)-1:
    if int(keeplist[i][1])>int(keeplist[i+1][0]):
     t[0]=keeplist[i][0]
     t[1]=keeplist[i][1] if int(keeplist[i][1])>int(keeplist[i+1][1]) else keeplist[i+1][1]
     keeplist.pop(i)
     keeplist.pop(i)
     keeplist.insert(i,tuple(t))
    else:
     i=i+1
#  if delete and keeplist:
   t=[('0',keeplist[0][0]),(keeplist[-1][1],self.libi.exiftool(imagename,'Duration'))]
   keeplist=[(keeplist[i-1][1],keeplist[i][0]) for i in range(1,len(keeplist))]
   keeplist.insert(0,t[0])
   keeplist.append(t[1])
  print('keeplist',keeplist)
  for count,i in enumerate(keeplist):
   if join:
    beginstring+="-ss "+i[0]+" -to "+i[1]+" -i "+imagename+" "
   else:
#    self.libi.ffmpeg("ffmpeg -ss "+i[0]+" -to "+i[1]+" -i "+imagename+" -c copy -y "+re.sub(r'(.*)[.](.*)',r'\1{}.\2'.format(count),outimagefile))
    self.libi.ffmpeg("ffmpeg -ss "+i[0]+" -to "+i[1]+" -i "+imagename+" "+("" if reencode else "-c copy")+" -y "+re.sub(r'^(?P<id>.*)[.](?P<id1>.*)$',lambda m:m.group('id')+'_'+str(count)+'.'+m.group('id1'),imagename))
  if join:
   self.libi.system(beginstring+"-filter_complex \""+''.join('['+str(i)+':v]['+str(i)+':a]' for i in range(len(re.findall(r' -i ',beginstring))))+"concat=n="+str(len(re.findall(r' -i ',beginstring)))+':v=1:a=1[v][a]'+"\" -map \"[v]\" -map \"[a]\" -y "+outimagename)
   return outimagename
#  return ["input"+str(i)+".mp4" for i in range(0,count+1)]
  return [re.sub(r'^(?P<id>.*)[.](?P<id1>.*)$',lambda m:m.group('id')+'_'+str(i)+'.'+m.group('id1'),imagename) for i in range(0,count+1)]

 def addvideo(self,*videofile,outimagename=None):
  '''add videos
   videofile - videos list ie. 'input1.mp4','><input2.mp4','<>input3.mp4','=input4.mp4'
    butterfly ><,<> signifies rotate PI/2 c/ac
    =videofile - refrence videofile'''
#  print(f'utic.addvideo {videofile=}')
  dimension=[]
  beginstring="ffmpeg "
  returnstring="-filter_complex \""
  [dimension.append(tuple(map(int,self.libi.videoattribute(re.sub(r'^\s*(?:><|<>|=)?(.*)',r'\1',i))[0]))) for i in videofile]
#  maxdimension=(str(max([float(i[0]) for i in dimension])),str(max([float(i[1]) for i in dimension])))
  refdimension=dimension[[i for i in range(len(videofile)) if re.search(r'^\s*=',videofile[i])][0]] if any(re.search(r'^\s*=',i) for i in videofile) else sorted([(i,i[0]*i[1]) for i in dimension],key=lambda x:x[1])[0][0]
  print('dimension',dimension,'refdimension',refdimension)
#  for count,i in enumerate(re.split(',',videofile)):
  for count,i in enumerate(videofile):
   beginstring+="-i "+re.sub(r'(?:><|<>|=)?(.*)',r'\1',i)+" "
#   returnstring+="[{}:v]".format(len(re.findall(r' -i ',beginstring))-1)+("transpose={},".format(['><','<>'].index(re.sub('^\s*(><|<>).*',r'\1',i))+1) if re.search(r'^\s*(><|<>)',i) else '')+'scale='+':'.join(dimension[count])+":force_original_aspect_ratio=decrease"+",pad="+':'.join(maxdimension)+r':(ow-iw)/2:(oh-ih)/2'+'[io{}];'.format(count)
   returnstring+="[{}:v]".format(len(re.findall(r' -i ',beginstring))-1)+("transpose={},".format(['><','<>'].index(re.sub('^\s*(><|<>).*',r'\1',i))+1) if re.search(r'^\s*(><|<>)',i) else '')+('scale='+':'.join(tuple(map(str,refdimension)))+',' if dimension[count][0]*dimension[count][1]>refdimension[0]*refdimension[1] else '')+'setsar=sar=1,pad='+':'.join(tuple(map(str,refdimension)))+r':(ow-iw)/2:(oh-ih)/2[io{}];'.format(count) if dimension[count]!=refdimension else ""
  returnstring+=''.join([('[io'+str(i) if dimension[i]!=refdimension else '['+str(i)+':v')+']['+str(i)+':a]' for i in range(count+1)])+'concat=n={}:v=1:a=1[vout][aout]'.format(count+1)
  outimagename=self.libi.outimagename('videoadded.mp4')
  self.libi.ffmpeg(beginstring+returnstring+"\" -map \"[vout]\" -map \"[aout]\" -y "+outimagename)
  return outimagename

 def replaceaudio(self,videofile,audiofile,outimagename=None):
  '''replace audio in videofile with audofile
     videofile - video file mp4 for audio replacement
     audiofile - external audacity improved mp3 file'''
#  '''index[53]:videofile[mp4]:audiofile[mp3]'''
  print("**********************")
  print("audiofile must be from audocity")
  print("**********************")
  outimagename=self.libi.outimagename(videofile)
  self.libi.ffmpeg("ffmpeg -i "+videofile+" -i "+audiofile+" -map 0:v -map 1:a -c copy -y "+outimagename)
  return outimagename

 def cropmedia(self,imagename,begintime=None,duration=None,outimagename=None):
  '''crop the media file (.mp3|.mp4)
   begintime - where crop would begin=0.0
   duration - duration of crop
   outimagename - output image file name'''
  outimagename=self.libi.outimagename(imagename)
  self.libi.ffmpeg("ffmpeg -i "+imagename+" "+("-ss "+str(begintime)+" " if begintime else "")+"-t "+str(duration)+" -y "+outimagename)
  return outimagename

 def insertsilence(self,beginaudio,endaudio=None,silenceduration=None,outimagename=None):
  '''######.......###### beginaudio+silence+endaudio
   beginaudio - (filename,duration,-ss)
   endaudio - (filename,duration)=None
   silenceduration - silenceduration=None
   outimagename - output file name=None'''
  self.libi.debug("><utilc.insertsilence",beginaudio,endaudio,silenceduration)
  outimagename=re.sub(r'(.*)[.].*',r'\1',beginaudio[0])+str(self.libi.count())+'.mp3' if not outimagename else outimagename
  self.libi.system("ffmpeg"+(" -ss "+beginaudio[2] if len(beginaudio)>2 else "")+(" -t "+self.libi.getsecond(beginaudio[1]) if len(beginaudio)>1 else "")+" -i "+beginaudio[0]+((" -t "+self.libi.getsecond(endaudio[1]) if len(endaudio)>1 else "")+" -i "+endaudio[0] if endaudio else "")+" -filter_complex \"[0:a]"+("apad=pad_dur="+str(silenceduration)+"[aout];[aout]" if silenceduration else "")+("[1:a]concat=n=2:v=0:a=1[aout]" if endaudio else "")+"\" -map \"["+("aout" if endaudio or silenceduration else "a:0")+"]\""+" -y "+outimagename)
  return outimagename

 def scalepad(self,imagename,targetdimension='1366x768',upscale=False,padposition='(ow-iw)/2,(oh-ih)/2',begintime=0.0,duration=None,padcolor='0x000000ff',getscalestr=False,outimagename=None):
  '''scale imagename to targetdimension
   imagename - input gif/.mp4 to scale
   targetdimension - new output dimension i.e 2/3,5,6=0.5,0.4 or '1366x768'
   upscale - Scale upwards otherwise just pad around
   padposition -  x,y where imagename would placed in sclaed video,i.e '0,0' at top left
   padcolor - padcolor i.e (40,40,40,255)'''
  print(f'><utilc.scalepad imagename={imagename} targetdimension={targetdimension} upscale={upscale} padposition={padposition} begintime={begintime} duration={duration} padcolor={padcolor} getscalestr={getscalestr} outimagename={outimagename}')
  outimagename=self.libi.outimagename(imagename,extension=('mov' if re.search('[.]gif$',imagename,flags=re.I) else None))
  dimension=tuple(int(x) for x in re.split('x',targetdimension)) if not type(targetdimension)==tuple else targetdimension
  scalestr=(("scale="+(str(dimension[0])+':-1' if int(self.libi.dimension(imagename)[0])/dimension[0] > int(self.libi.dimension(imagename)[1])/dimension[1] else '-1:'+str(dimension[1]))+',') if upscale or int(self.libi.dimension(imagename)[0])>dimension[0] or int(self.libi.dimension(imagename)[1])>dimension[1] else '')+'pad='+str(dimension[0])+':'+str(dimension[1])+':'+re.sub(r',',':',re.sub(r'(?P<id>\<[WH]\>)',lambda m:'o'+m.group('id').lower(),re.sub(r'(?P<id>\<[wh]\>)',lambda m:'i'+m.group('id'),self.libi.co(padposition,(self.libi.dimension(imagename),dimension)))))+(':'+padcolor if padcolor else '')+',setsar=sar=1'
#  self.libi.ffmpeg("ffmpeg "+("-ss "+str(begintime)+" -t "+str(duration)+" " if duration else " ")+"-i "+imagename+" -filter_complex \""+(("scale="+(str(dimension[0])+':-1' if int(self.libi.dimension(imagename)[0])/dimension[0] > int(self.libi.dimension(imagename)[1])/dimension[1] else '-1:'+str(dimension[1]))+',') if upscale or int(self.libi.dimension(imagename)[0])>dimension[0] or int(self.libi.dimension(imagename)[1])>dimension[1] else '')+'pad='+str(dimension[0])+':'+str(dimension[1])+':'+re.sub(r',',':',re.sub(r'(?P<id>\<[WH]\>)',lambda m:'o'+m.group('id').lower(),re.sub(r'(?P<id>\<[wh]\>)',lambda m:'i'+m.group('id'),self.libi.co(padposition,(self.libi.dimension(imagename),dimension)))))+(':'+padcolor if padcolor else '')+"\""+(" -pix_fmt rgba -vcodec png " if re.search(r'[.]gif$',imagename,flags=re.I) else " -map 0:v -map 0:a -c:a copy")+" -y "+outimagename)
  self.libi.ffmpeg("ffmpeg "+("-ss "+str(begintime)+" -t "+str(duration)+" " if duration else " ")+"-i "+imagename+" -filter_complex \""+scalestr+"\""+(" -pix_fmt rgba -vcodec png " if re.search(r'[.](gif|mov)$',imagename,flags=re.I) else " -map 0:v -map 0:a -c:a copy")+" -y "+outimagename) if not getscalestr else None
  return scalestr if getscalestr else outimagename

 def d_(self,filename):
  downloaddir=('image','misc','document','audio')
  for i in range(len(downloaddir)):
   if os.path.isfile(r'./'+filename):
    break
   try:
    if requests.head(r'http://www.minhinc.com/'+downloaddir[i]+r'/'+filename).ok:
     with open(filename,'wb') as file:
      file.write(requests.get(r'http://www.minhinc.com/'+downloaddir[i]+r'/'+filename).content)
     break
   except:
    pass
   if i==len(downloaddir)-1:
#    raise FileNotFoundError(errno.ENOENT,os.strerror(errno.ENOENT),filename,'not found')
    raise FileNotFoundError
  return filename

 def screenshot(self,imagename,begintime=0.0,outimagename=None):
  '''take screen shot at begintime'''
  outimagename=self.libi.outimagename('screenshot.',extension='png')
  self.libi.ffmpeg("ffmpeg -ss "+self.libi.getsecond(begintime)+" -i "+imagename+" -vframes 1 -q:v 2 "+outimagename)
  return outimagename

 def color2transparent(self,imagename,colorhex,similarity=0.3,blend=0.0,outimagename=None):
  '''make 'colorhex' pixels transparent
   colorhex - pixel color to be make transparent. In hex format ie. 0x24b403
   similarity - much similar image color from colorhex. 0-1 complete same to everything=0.3
   blend - transparent level, 0-1 complete transparent to opaque=0.0'''
  outimagename=self.libi.outimagename(imagename,outimagename,extension='mov')
  self.libi.ffmpeg("ffmpeg -i "+imagename+" -filter_complex \"[0:v]colorkey="+colorhex+":"+str(similarity)+":"+str(blend)+"\" -pix_fmt rgba -vcodec png -y "+outimagename)
  return outimagename

 def slowfast(self,imagename,factor=0.5,outimagename=None):
  '''slow or speed up the video
   factor - speed up by factor,i.e. 0.5 slow down by half, factor=0.5'''
  outimagename=self.libi.outimagename(imagename,outimagename)
  factorstr=re.sub(r'^,','',','.join(['atempo=2.0' for x in range(int(math.log2(factor)))])+(',atempo='+str(factor/math.pow(2,int(math.log2(factor)))) if factor/math.pow(2,int(math.log2(factor))) != 1 else '') if factor>=1.0 else ','.join(['atempo=0.5' for x in range(int(math.log2(1/factor)))])+(',atempo='+str(factor*math.pow(2,int(math.log2(1/factor)))) if factor*math.pow(2,int(math.log2(1/factor))) != 1 else ''),flags=re.I)
  self.libi.ffmpeg("ffmpeg -i "+imagename+" -filter_complex \"[0:v]setpts="+str(float(1/factor))+"*PTS[v];[0:a]"+factorstr+"[a]\" -map \"[v]\" -map \"[a]\" -y "+outimagename)
  return outimagename
