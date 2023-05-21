import datetime
from skimage.metrics import structural_similarity as compare_ssim
import cv2
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
 def __init__(self,inputfile=None,libp=None):
  '''Enable debug True/False'''
  self.libi=libm.libc(inputfile=inputfile) if not libp else libp

 def setvideo(self,inputfile):
  self.libi.setvideo(inputfile)

 def addalpha(self,imagename,alpha,transparentcolor=None,outimagename=None):
  '''Add alpha to image/video (png/jpg/mp4)
  imagename - .jpg,.jpeg,.png,.gif,.mp4
  alpha - 0-255
          '12' filter number(fade[in/out]) in string or filter string
  transparentcolor - if a particular color needs become transparent(alpha=0),i.e. (244,0,0,255) or '#ff0000ff' or '0xff0000ff' '''
  filtername=None
  print("><addalpha",imagename,alpha,outimagename)
  outimagelist=[]
  if type(alpha)==str:
   outimagename=self.libi.outimagename(imagename,outimagename,extension='mp4' if re.search(r'mp4$',alpha) else 'mov')
   filtername=self.libi.filter[re.sub(r'^(.*)mp4$',r'\1',alpha)] if re.search(r'^\d+',alpha) else alpha
   self.libi.system('ffmpeg '+('-loop 1 ' if not re.search('video',self.libi.exiftool(imagename,'MIME Type'),flags=re.I) else '')+' -t '+re.sub(r'.*:d=(\d+).*',r'\1',filtername)+' -i '+imagename+' -filter_complex "[0:v]'+self.libi.filter['41']+r'[ov];[ov]'+filtername+'"'+(self.libi.vformat('mp4') if re.search(r'mp4$',alpha) else self.libi.vformat('mov'))+' -y '+outimagename)
   return outimagename
  for imagename in ([imagename] if type(imagename)==str else imagename):
   if alpha!=None:
    mask=Image.new(r'L',[int(i) for i in self.libi.videoattribute(imagename)[0]] if re.search(r'[.]mp4$',imagename,re.I) else Image.open(imagename).size,color=alpha)
    if re.search(r'video',self.libi.exiftool(imagename,'MIME Type'),flags=re.I):
     outimagename=self.libi.outimagename(imagename,outimagename,'mov')
     mask.save(self.libi.adddestdir('maskimage.png'))
     mask.close()
     self.libi.system("ffmpeg -i "+imagename+" -loop 1 -i "+self.libi.adddestdir('maskimage.png')+" -filter_complex \"[0][1]alphamerge\""+self.libi.vformat('mov')+" -y "+outimagename)
    else:
     outimagename=self.libi.outimagename(imagename,outimagename)
     img=Image.open(imagename).convert('RGBA')
     img.putalpha(mask)
     img.save(outimagename)
     img.close()
   if transparentcolor:
    imagename=outimagename if alpha!=None else imagename
    outimagename=self.libi.outimagename(imagename)
    self.libi.system('convert '+imagename+' -fuzz 10% -transparent '+('#'+''.join(str(hex(x)) for x in transparentcolor) if type(transparentcolor)==tuple else transparentcolor)+' '+outimagename)
   outimagelist.append(outimagename)
  return outimagelist[0] if len(outimagelist)==1 else outimagelist

 def addalpha2(self,imagename,alpha,outimagename=None):
  '''imagename=.mp4 or .png
  alpha=0-255 or 0.0 to 1.0 (float)'''
  print(f'><utilc.addalpha2 {(imagename,alpha,outimagename)=}')
  outimagename=self.libi.outimagename(imagename,outimagename,extension='mov' if re.search('video',self.libi.exiftool(imagename,'MIME Type'),flags=re.I) else 'png')
  alpha=type(alpha)==str and re.search('[.]',alpha) and float(alpha) or type(alpha)==str and int(alpha) or alpha
  mask=Image.new(r'L',[int(i) for i in self.libi.videoattribute(imagename)[0]] if re.search('video',self.libi.exiftool(imagename,'MIME Type'),flags=re.I) else Image.open(imagename).size,color=type(alpha)==int and alpha or int(255*alpha))
  if re.search('video',self.libi.exiftool(imagename,'MIME Type'),flags=re.I):
   mask.save(self.libi.adddestdir('maskimage.png'))
   mask.close()
   self.libi.system("ffmpeg -i "+imagename+" -loop 1 -i "+self.libi.adddestdir('maskimage.png')+" -filter_complex \"[0][1]alphamerge=shortest=1\""+self.libi.vformat('mov')+" -y "+outimagename)
  else:
   img=Image.open(imagename).convert('RGBA')
   img.putalpha(mask)
   img.save(outimagename)
   img.close()
  return outimagename
 """
 def image2gif(self,imagename,filtername,duration=None,backcolor='0x00000000',reversefilter=False,outimagename=None):
  '''-----------
  imagename - .png,.gif,.gif,.mp4 or list of .png or (400,200)<--imagesize of backcolor
             Note: add mov/mp4 at end for mov/mp4 generation otherwise mov by default,i.e. gifmp4,..
  filtername - filternumber or complete filter,i.e. '41' or 'blend=....' or 'gif' or 'gif41'
  duration - total duration of mp4=None
  backcolor - background glass color
  reversefilter - if backcolor is to be put next, [imagename][backcolor]blend=....
  outimagename - output mp4 name=<imagename>_<count>.mp4
  -------------
  gif/mov'''
  print(f'><utilc.image2gif imagename={imagename} filtername={filtername} duration={duration} reversefilter={reversefilter} backcolor={backcolor}')
  imagename=(int(self.libi.videowidth),int(self.libi.videoheight)) if not imagename else imagename
  outimagename=self.libi.outimagename(type(imagename)==tuple and type(imagename[0])==str and imagename[0] or type(imagename)==str and imagename or 'temp',outimagename,extension='mp4' if type(filtername)==tuple else re.search(r'^gif',filtername,flags=re.I) and 'gif' or re.search(r'mp4$',filtername,flags=re.I) and 'mp4' or 'mov') if not outimagename else outimagename
  filtername=tuple([self.libi.filter[re.sub(r'(mp4|mov)$','',str(x),flags=re.I)] if re.search(r'^\d+',str(x)) else x for x in (filtername if type(filtername)==tuple else [filtername])])[0 if not type(filtername)==tuple else slice(0,None)]
  if type(imagename)==tuple and type(imagename[0])==str and [re.search('(image|video)',self.libi.exiftool(x,'MIME Type'),flags=re.I) for x in imagename]:
   imagename=list(imagename)
   for count,x in enumerate(imagename[:]):
    imagename[count]=self.libi.outimagename(x)
    if re.search('image',self.libi.exiftool(x,'MIME Type'),flags=re.I):
     self.libi.system(r'convert -resize '+str(self.libi.videowidth)+'x'+str(self.libi.videoheight)+' '+x+' '+imagename[count])
    else:
     self.scalepad(x,outimagename=imagename[count])
   imagename=tuple(imagename)
  imagesize=[(2*(int(x[0])//2),2*(int(x[1])//2)) for i in (imagename if type(imagename)==tuple else [imagename]) for x in ([self.libi.videoattribute(i)[0]] if re.search('video',self.libi.exiftool(i,'MIME Type'),flags=re.I) else [Image.open(i).size])] if type(imagename)==tuple and type(imagename[0])==str or type(imagename)==str else [imagename]
  print(f'<=>utilc.image2gif imagesize={imagesize} {filtername=} outimagename={outimagename} imagename={imagename}')
#  returnstring='color=c='+backcolor+':size='+'x'.join(str(x) for x in sorted(imagesize,key=lambda m:m[0]*m[1])[-1])+':d='+str(duration)+r",format=rgba[black];"
  returnstring='color=c='+backcolor+':size='+'x'.join(str(x) for x in sorted(imagesize,key=lambda m:m[0]*m[1])[-1])+':d='+str(duration)+r"[black];"
  if (type(filtername)==tuple or re.search('zoompan',filtername) or type(imagename)==tuple and re.search(r'(^gif|mov$|mp4$)',filtername)):
   if type(filtername)==tuple or re.search('zoompan',filtername):
    for count,i in enumerate(imagename if type(imagename)==tuple else [imagename]):
     returnstring+=r'['+str(count)+r":v]scale="+'x'.join(str(x*10) for x in imagesize[count])+','+re.sub(r'\(25[*]',r'(25*'+str(duration//len(imagesize)-1),(filtername[count] if type(filtername)==tuple else filtername))+":d=25*"+str(round(1+float(duration)/len(imagesize),3))+':s='+'x'.join(str(x) for x in imagesize[count])+r",fade=t=in:st=0:d=1:alpha=0,fade=t=out:st="+str(round(float(duration)/len(imagesize),3))+r":d=1:alpha=0,setpts=PTS-STARTPTS+"+str(count)+r"*"+str(round(float(duration)/len(imagesize),3))+r"/TB[v"+str(count)+r"];"
    returnstring+=''.join((r'[black]' if x==0 else r'[ov'+str(x-1)+r']')+r'[v'+str(x)+r']overlay=(W-w)/2:(H-h)/2'+(r'[ov'+str(x)+r'];' if x!=(len(imagesize)-1) else ':shortest=1') for x in range(len(imagesize)))
   else:
    if re.search(r'^gif',filtername,flags=re.I):
     self.libi.system('convert -delay '+str(100*float(duration/len(imagename)))+' -dispose Background -loop 0 '+' '.join(imagename[count%len(imagename)] for count in range(len(imagename)-1))+' -delay '+str(100*(duration-float(duration/len(imagename))*(len(imagename)-1)))+' '+imagename[-1]+' '+self.libi.adddestdir(outimagename))
     if re.search(r'^gif\d+',filtername):
      return self.image2gif(outimagename,re.sub(r'^gif(\d+.*)',r'\1',filtername),duration,backcolor)
     if re.search(r'(mp4|mov)$',filtername,flags=re.I):
      self.libi.system('ffmpeg -ignore_loop 1 -i '+outimagename+' -filter_complex "[0:v]'+self.libi.filter['41']+'"'+(self.libi.vformat('mp4') if re.search(r'mp4$',filtername,flags=re.I) else self.libi.vformat('mov'))+' -y '+re.sub(r'[.]gif$','.'+re.sub(r'.*(mp4|mov)$',r'\1',filtername),outimagename))
     return re.sub(r'[.]gif$','.'+re.sub(r'.*(mp4|mov)$',r'\1',filtername),outimagename) if re.search(r'(mov|mp4)$',filtername,flags=re.I) else outimagename
    elif re.search(r'^(mp4|mov)',filtername,flags=re.I):
     self.libi.system('ffmpeg -framerate '+str(len(imagename)/duration)+re.sub(r'^(.*)(\d+)[.](.*)',r'\1'+'0'+str(len(r'\2'))+r'd.'+r'\3',imagename[0])+(self.libi.vformat('mp4') if re.search(r'^mp4',filtername,flags=re.I) else self.libi.vformat('mov'))+' -y '+outimagename)
    return outimagename
  elif re.search(r'^gif',filtername,flags=re.I):#mp4 to gif
   self.libi.system(r'ffmpeg -ss '+('0 -to '+str(duration or 4) if not re.search('-',str(duration)) else re.split('-',duration)[0]+' -t 4')+r' -i '+imagename+r' -r 6 -y '+outimagename)
   return outimagename
  else:
#   returnstring+=(r'[0:v]'+self.libi.filter['41']+r'[ov];' if type(imagename)==str else '')+((r'[black][ov]' if not reversefilter else r'[ov][black]') if type(imagename)==str else r'[black]')+filtername
   returnstring+=(r'[0:v]'+self.libi.filter['41']+r'[ov];' if type(imagename)==str else '')+(('[black]nullsink;[ov]' if re.search('^fade',filtername,flags=re.I) else r'[black][ov]' if not reversefilter else r'[ov][black]') if type(imagename)==str else r'[black]')+filtername
#   self.libi.system("ffmpeg -i "+self.libi.adddestdir('transparentpng.png')+" "+(("-loop 1 " if not re.search(r'[.](gif|mov|mp4)$',imagename) else "-ignore_loop 0 " if re.search(r'[.]gif$',imagename,re.I) else "")+"-t "+str(duration)+" " if duration else "")+"-i "+imagename+" -filter_complex \""+("[0][1]" if not re.search(r'^\[',filtername) else "")+filtername+"\" -pix_fmt rgba -vcodec png -y "+outimagename)
  print(f'<=>utilc.image2gif returnstring={returnstring}')
  self.libi.system("ffmpeg "+("-ignore_loop 0 "+str(duration) if type(imagename)==str and re.search(r'[.]gif$',imagename,flags=re.I) else f' -t {duration} ' if duration else '')+''.join(" -i "+x for x in type(imagename)==tuple and type(imagename[0])==str and imagename or type(imagename)==str and [imagename] or '')+" -filter_complex \""+returnstring+"\" "+(self.libi.vformat('mp4') if re.search(r'[.]mp4$',outimagename,flags=re.I) else self.libi.vformat('mov'))+" -y "+outimagename)
  return outimagename

 """
 def image2gif(self,imagename,duration):
  print(f'><utilc.image2gif {imagename=} {duration=}')
  imagenamelist=list(imagename)
  imagenamelist.sort(key=lambda m:Image.open(m).width*Image.open(m).height,reverse=True)
  for count,i in enumerate(imagenamelist[:]):
   imagenamelist[count]='logdir/'+re.sub(r'^.*/(.*)',r'\1',i)
   if not count:
    img=Image.open(i).convert('RGBA')
    img.resize((2*(img.width//2),2*(img.height//2))).save(imagenamelist[count])
   else:
    img=Image.new('RGBA',Image.open(imagenamelist[0]).size,color=(0,0,0,0))
    img2=Image.open(i).convert('RGBA')
    img.paste(img2,((img.width-img2.width)//2,(img.height-img2.height)//2),img2)
    img.save(imagenamelist[count])
  outimagename=self.libi.outimagename(imagenamelist[0],extension='gif')
  print(f'<=>utilc.image2gif {imagenamelist=}')
  self.libi.system('convert -delay '+str(25)+' -dispose Background -loop 0 '+' '.join((' '+imagenamelist[count])*int((duration*100)//(len(imagenamelist)*25)+((count+1)*((duration*100)%(len(imagenamelist)*25)))//(len(imagenamelist)*25)) for count in range(len(imagenamelist)))+' '+outimagename)
  return outimagename

 def image2mov(self,imagename,filter,duration,backcolor='0x00000000',outimagename=None):
  '''-----------
  imagename - .png,.gif,.mp4,tuple(.png)
  filter - i.e. blend=all_exp....
  duration - total duration of background
  backcolor - background glass color
  outimagename - output mp4 name=<imagename>_<count>.mp4
  -------------
  image2mov(imagename=('one.png','two.png','three.png'),filter=("fade=in:st=0:d=3:alpha=1","blend=all_expr='if(lte(Y,(H-T/1*H)),A,B)'"),duration=10,backcolor='0x00000000')
  image2mov(imagename='one.gif',filter="blend=all_expr='if(lte(Y,(H-T/1*H)),A,B)'",duration=4)
  image2mov(imagename='one.mp4',filter=("fade=in:st=0:d=3:alpha=1","blend=all_expr='if(lte(Y,(H-T/1*H)),A,B)'"),duration=10,backcolor='0x00000000')\
  '''
  print(f'><utilc.image2mov {imagename=} {filter=} {duration=} {backcolor=}')
  returnstring=''
  imagename=self.image2gif(imagename,duration) if not type(imagename)==str else imagename
  outimagename=self.libi.outimagename(imagename,extension='mov')
  dimension=not type(filter)==str and not type(filter[0])==str and [re.sub(r'^.*?(?P<id>\d+)%(?P<id2>\d+)%$',lambda m:str(int(2*((self.libi.videowidth*float(m.group('id')))//(2*100))))+'x'+str(int(2*((self.libi.videoheight*float(m.group('id2')))//(2*100)))),x[0]) for x in filter if re.search(r'%.*?%$',x[0])] or []
  filter=type(filter)==str and (filter,) or type(filter[0])==str and filter or [x[1] for x in filter]
  tmp=[x for x in filter if not re.search('^fade',x,flags=re.I)]
#  returnstring='color=c='+backcolor+':size='+'x'.join([(str(2*(int(x[0])//2)),str(2*(int(x[1])//2))) for x in ([self.libi.videoattribute(imagename)[0]] if re.search('video',self.libi.exiftool(imagename,'MIME Type'),flags=re.I) else [Image.open(imagename).size])][0])+':d='+str(duration)+r"[black];"+('[black]split='+str(len(tmp))+'[black]'*len(tmp)+';' if len(tmp)>1 else '')+'[0:v]'+self.libi.filter['41']+'[ov];'
  returnstring='color=c='+backcolor+':size='+('x'.join([(str(2*(int(x[0])//2)),str(2*(int(x[1])//2))) for x in ([self.libi.videoattribute(imagename)[0]] if re.search('video',self.libi.exiftool(imagename,'MIME Type'),flags=re.I) else [Image.open(imagename).size])][0]) if not dimension else dimension[0])+':d='+str(duration)+r"[black];"+('[black]split='+str(len(tmp))+'[black]'*len(tmp)+';' if len(tmp)>1 else '')+'[0:v]'+self.libi.filter['41']+'[ov];'
  for count,i in enumerate(not type(filter)==str and filter or (filter,)):
   returnstring+='[ov]'+i+'[ov];' if re.search('fade.*(in|out)',i) else '[black][ov]'+i+'[ov];'
  print(f'<=>utilc.image2mov returnstring={returnstring}')
  self.libi.system("ffmpeg "+((" -loop 1 " if not re.search(r'[.](gif|mov|mp4|webm)$',imagename,re.I) else " -ignore_loop 0 " if re.search(r'[.]gif$',imagename,re.I) else "")+" -t "+str(duration))+" -i "+imagename+" -filter_complex \""+re.sub(r'\[ov\];$','',returnstring)+"\" "+self.libi.vformat('mov')+" -y "+outimagename)
  return outimagename

 def text2image(self,text,textcolor='r',backcolor=(0,0,0,0),size=0.3,stroke=None,alignment='m',interlinegap=10,outimagename=None):
  '''\
            ----------------
  text - text i.e. 'hello\nworld' or in tuple,i.e. (('hello\nworld',None,(128,0,0,0.5),0.5,False,None,5),('Welcome',(0,40,0,255),(0,0,0,0),0.3,(125,0,0,255),'m',10),....)
  textcolor - default color of text = 'red' see lib.palettecolor
  backcolor - background color of text = (0,0,0,192)
  size - width of textline/video width = 0.4
  stroke - None or stroke color, (255,255,0,255)
  alignment - m:center l:left = 'm'
  interlinegap - margin from top,Top line no margin
            ----------------
  outimagename - output image file name = To be auto generated
            ----------------
  text2image('Hello World\nWelcome to the World')
  text2image(('Hello World\nWelcome to the World',))
  text2image('Hello World\nWelcome to the World',backcolor=(125,0,0,128),alignment='l',stroke=(255,0,255,255))
  text2image(('Hello World\nWelcome to the World',(128,0,0,255),(127,0,0,124)),))'''
  print(f'><utilc.text2image {text=} {textcolor=} {backcolor=} {size=} {stroke=} {alignment=} {interlinegap=}')
  stringlist=[]
  offset=int(size*40)
  if not type(text)==str:#richtext
   if type(text[0])==str:
    text=(text,)
   for i in [[j]+list(i[1:]) for i in text for j in re.split(r'\n',i[0])]:
    stringlist.append([i[0]]+list(self.text2image.__defaults__))
#    stringlist.append(tuple([self.text2image.__defaults__[count-1] if x==None else x for count,x in enumerate(i)]))
    for count,x in enumerate(i):
     stringlist[-1][count]=x
  else:
#   stringlist=(('\n'.join(re.split(r'\\n',text)),textcolor,backcolor,size,stroke,alignment,linemargin),)
   stringlist=tuple([(x,textcolor,backcolor,size,stroke,alignment,interlinegap) for x in re.split(re.search(r'\\n',text) and r'\\n' or r'\n',text)])
  '''
  imagewidth=max(self.libi.getfontsize(x[0],x[3])[0] for x in stringlist)+xoffset
  imageheight=[self.libi.getfontsize(x[0],x[3],lineheight=x[-1])[1]+yoffset for x in stringlist]
  '''
  minfontsize=min([self.libi.getfont(x[0],screenratio_p=x[3],widthheight=True).size for x in stringlist])
#  imagesize=[self.libi.getfont(x[0],screenratio_p=x[3],widthheight=True).getbbox(x[0],anchor="lt")[2:] for x in stringlist]
  imagesize=[ImageFont.truetype(os.path.expanduser('~')+'/.fonts/ufonts.com_tw-cen-mt.ttf',minfontsize).getbbox(x[0],anchor="lt")[2:] for x in stringlist]
  img=Image.new('RGBA',(max(x[0] for x in imagesize)+2*offset,sum(x[1] for x in imagesize)+sum(x[6] for count,x in enumerate(stringlist) if count)+2*offset*len(stringlist)),(0,0,0,0))
  print(f'<=>libc.text2image {stringlist=} {imagesize=} {img.size=}')
  draw=ImageDraw.Draw(img)
  #bottommargin=0
  for count,text in enumerate(stringlist):
   '''
   x1,y1=(re.search(r'^[Mm]',text[5]) and (imagewidth-self.libi.getfontsize(text[0],text[3],lineheight=text[-1])[0])/2-xoffset/2 or 0,sum([imageheight[i] for i in range(count)] or [0]))
   x2,y2=(re.search(r'^[Mm]',text[-2]) and (imagewidth+self.libi.getfontsize(text[0],text[3],lineheight=text[-1])[0])/2+xoffset/2 or imagewidth,sum(imageheight[i] for i in range(count+1)))
   '''
   x1,y1=(img.width-imagesize[count][0])//2-offset if re.search(r'^[mM]$',stringlist[count][5]) else 0,offset*2*count+sum(x[1]+stringlist[lcount+1][6] for lcount,x in enumerate(imagesize[:count]))
   x2,y2=x1+imagesize[count][0]+2*offset,y1+imagesize[count][1]+2*offset
   print(f"<=>text2image text={text} x1,y1,x2,y2={(x1,y1,x2,y2)} len(text[0])=",len(re.split(r'\n',text[0])))
#   draw.rectangle((x1,y1+1,x2,y2-1),fill=self.libi.palette(text[2]))
   draw.rectangle((x1,y1,x2,y2),fill=self.libi.palette(text[2]))
#   [draw.text((x1+xoffset/2,y1-yoffset/2+(counti and self.libi.getfontsize('\n'.join(re.split('\n',text[0])[:counti]),text[3],lineheight=text[-1])[1]+text[-1])),texti,font=self.libi.getfont(text[0],text[3]),fill=self.libi.palette(text[1]),stroke_width=text[4],stroke_fill=text[4] and (255,0,0,255) or None) for counti,texti in enumerate(re.split('\n',text[0]))]
#   draw.text((x1+offset,y1+offset),text[0],font=imagesize[count],fill=self.libi.palette(text[1]),stroke_width=text[4] and 2 or 0,stroke_fill=text[4] and 2)
#   draw.text((x1+(x2-x1)//2,y1+(y2-y1)//2),text[0],anchor='mm',font=self.libi.getfont(stringlist[count][0],screenratio_p=stringlist[count][3],widthheight=True),fill=self.libi.palette(text[1]),stroke_width=text[4] and 2 or 0,stroke_fill=text[4] and 2)
#   draw.text((x1+offset,y1+offset),text[0],anchor='lt',font=self.libi.getfont(stringlist[count][0],screenratio_p=stringlist[count][3],widthheight=True),fill=self.libi.palette(text[1]),stroke_width=text[4] and 2 or 0,stroke_fill=text[4] and 2)
   draw.text((x1+offset,y1+offset),text[0],anchor='lt',font=ImageFont.truetype(os.path.expanduser('~')+'/.fonts/ufonts.com_tw-cen-mt.ttf',minfontsize),fill=self.libi.palette(text[1]),stroke_width=text[4] and 2 or 0,stroke_fill=text[4] and 2)
  outimagename=self.libi.outimagename('textimage.',extension='png')
  print(f'libc.text2image x1,y1,x2,y2={(x1,y1,x2,y2)} outimagename={outimagename=}')
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
#  if textdata[1]:draw.text((xoffset+font.getsize(textdata[0])[0],font.getsize(textdata[0])[1]-font1.getsize(textdata[0])[1]-12),textdata[1],font=font1,fill=textcolor[0])
  if textdata[1]:draw.text((xoffset+font.getsize(textdata[0])[0],font.getsize(textdata[0])[1]-font1.getsize(textdata[0])[1]-14),textdata[1],font=font1,fill=textcolor[1])
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
    if textdata[1]:draw.text((xoffset+font.getsize(textdata[0])[0],font.getsize(textdata[0])[1]-font1.getsize(textdata[0])[1]-14),textdata[1],font=font1,fill=255)
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
#    self.libi.system("ffmpeg -ss "+i[0]+" -to "+i[1]+" -i "+imagename+" -c copy -y "+re.sub(r'(.*)[.](.*)',r'\1{}.\2'.format(count),outimagefile))
    self.libi.system("ffmpeg -ss "+i[0]+" -to "+i[1]+" -i "+imagename+" "+("" if reencode else "-c copy")+" -y "+re.sub(r'^(?P<id>.*)[.](?P<id1>.*)$',lambda m:m.group('id')+'_'+str(count)+'.'+m.group('id1'),imagename))
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
  self.libi.system(beginstring+returnstring+"\" -map \"[vout]\" -map \"[aout]\" -y "+outimagename)
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
  self.libi.system("ffmpeg -i "+videofile+" -i "+audiofile+" -map 0:v -map 1:a -c copy -y "+outimagename)
  return outimagename

 def cropmedia(self,imagename,begintime=None,duration=None,outimagename=None):
  '''crop the media file (.mp3|.mp4)
   begintime - where crop would begin=0.0
   duration - duration of crop
   outimagename - output image file name'''
  outimagename=self.libi.outimagename(imagename)
  self.libi.system("ffmpeg -i "+imagename+" "+("-ss "+str(begintime)+" " if begintime else "")+"-t "+str(duration)+" -y "+outimagename)
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

 """
 def scalepad(self,imagename,targetdimension=None,upscale=False,padposition='(ow-iw)/2,(oh-ih)/2',begintime=0.0,duration=None,padcolor='0x000000ff',getscalestr=False,outimagename=None):
  '''scale imagename to targetdimension
   imagename - input gif/.mp4 to scale
   targetdimension - new output dimension i.e 2/3,5,6=0.5,0.4 or '1366x768'
   upscale - Scale upwards otherwise just pad around
   padposition -  x,y where imagename would placed in sclaed video,i.e '0,0' at top left
   padcolor - padcolor i.e (40,40,40,255)'''
  print(f'><utilc.scalepad imagename={imagename} targetdimension={targetdimension} upscale={upscale} padposition={padposition} begintime={begintime} duration={duration} padcolor={padcolor} getscalestr={getscalestr} outimagename={outimagename}')
#  outimagename=self.libi.outimagename(imagename,extension=('mov' if re.search('[.]gif$',imagename,flags=re.I) else None)) if not outimagename else outimagename
  outimagename=self.libi.outimagename(imagename,extension=('mov' if re.search('[.]gif$',imagename,flags=re.I) or padcolor=='0x00000000' or padcolor==(0,0,0,0) else None)) if not outimagename else outimagename
#  dimension=tuple(int(x) for x in re.split('x',targetdimension)) if type(targetdimension)==str else targetdimension if type(targetdimension)==tuple else (int(self.libi.videowidth),int(self.libi.videoheight))
  dimension=tuple(int(x+1) if x%2 else int(x) for x in (re.split('x',targetdimension) if type(targetdimension)==str else targetdimension if type(targetdimension)==tuple else (int(self.libi.videowidth),int(self.libi.videoheight))))
#  scalestr=(("scale="+(str(dimension[0])+':-1' if int(self.libi.dimension(imagename)[0])/dimension[0] > int(self.libi.dimension(imagename)[1])/dimension[1] else '-1:'+str(dimension[1]))+',') if upscale or int(self.libi.dimension(imagename)[0])>dimension[0] or int(self.libi.dimension(imagename)[1])>dimension[1] else '')+'pad='+str(dimension[0])+':'+str(dimension[1])+':'+re.sub(r',',':',re.sub(r'(?P<id>\<[WH]\>)',lambda m:'o'+m.group('id').lower(),re.sub(r'(?P<id>\<[wh]\>)',lambda m:'i'+m.group('id'),self.libi.co(padposition,(self.libi.dimension(imagename),dimension)))))+(':'+padcolor if padcolor else '')+',setsar=sar=1'
#  scalestr=(("scale="+(str(dimension[0])+':-1' if int(self.libi.dimension(imagename)[0])/dimension[0] > int(self.libi.dimension(imagename)[1])/dimension[1] else '-1:'+str(dimension[1]))) if upscale or int(self.libi.dimension(imagename)[0])>dimension[0] or int(self.libi.dimension(imagename)[1])>dimension[1] else '')+(',pad='+str(dimension[0])+':'+str(dimension[1])+':'+re.sub(r',',':',re.sub(r'(?P<id>\<[WH]\>)',lambda m:'o'+m.group('id').lower(),re.sub(r'(?P<id>\<[wh]\>)',lambda m:'i'+m.group('id'),self.libi.co(padposition,(self.libi.dimension(imagename),dimension))))) if padposition else '')+(':'+padcolor if padposition and padcolor else '')+',setsar=sar=1'
  scalestr=(("scale="+(str(dimension[0])+':-1' if int(self.libi.dimension(imagename)[0])/dimension[0] > int(self.libi.dimension(imagename)[1])/dimension[1] else '-1:'+str(dimension[1])))+',' if upscale or int(self.libi.dimension(imagename)[0])>dimension[0] or int(self.libi.dimension(imagename)[1])>dimension[1] else '')+('pad='+str(dimension[0])+':'+str(dimension[1])+':'+re.sub(r',',':',re.sub(r'(?P<id>\<[WH]\>)',lambda m:'o'+m.group('id').lower(),re.sub(r'(?P<id>\<[wh]\>)',lambda m:'i'+m.group('id'),self.libi.co(padposition,(self.libi.dimension(imagename),dimension))))) if padposition else '')+(':'+padcolor if padposition and padcolor else '')+',setsar=sar=1'
#  self.libi.system("ffmpeg "+("-ss "+str(begintime)+" -t "+str(duration)+" " if duration else " ")+"-i "+imagename+" -filter_complex \""+(("scale="+(str(dimension[0])+':-1' if int(self.libi.dimension(imagename)[0])/dimension[0] > int(self.libi.dimension(imagename)[1])/dimension[1] else '-1:'+str(dimension[1]))+',') if upscale or int(self.libi.dimension(imagename)[0])>dimension[0] or int(self.libi.dimension(imagename)[1])>dimension[1] else '')+'pad='+str(dimension[0])+':'+str(dimension[1])+':'+re.sub(r',',':',re.sub(r'(?P<id>\<[WH]\>)',lambda m:'o'+m.group('id').lower(),re.sub(r'(?P<id>\<[wh]\>)',lambda m:'i'+m.group('id'),self.libi.co(padposition,(self.libi.dimension(imagename),dimension)))))+(':'+padcolor if padcolor else '')+"\""+(" -pix_fmt rgba -vcodec png " if re.search(r'[.]gif$',imagename,flags=re.I) else " -map 0:v -map 0:a -c:a copy")+" -y "+outimagename)
#  self.libi.system("ffmpeg "+("-ss "+str(begintime)+" -t "+str(duration)+" " if duration else " ")+"-i "+imagename+" -filter_complex \""+scalestr+"\""+(" -pix_fmt rgba -vcodec png " if re.search(r'[.](gif|mov)$',imagename,flags=re.I) else " -map 0:v -map 0:a -c:a copy")+" -y "+outimagename) if not getscalestr else None
#  self.libi.system("ffmpeg "+("-ss "+str(begintime)+" -t "+str(duration)+" " if duration else " ")+"-i "+imagename+" -filter_complex \""+scalestr+"\""+(self.libi.vformat('mov') if re.search(r'[.](gif|mov)$',imagename,flags=re.I) else self.libi.vformat('mp4'))+" -y "+outimagename) if not getscalestr else None
  self.libi.system("ffmpeg "+("-ss "+str(begintime)+" -t "+str(duration)+" " if duration else " ")+"-i "+imagename+" -filter_complex \""+scalestr+"\""+(self.libi.vformat('mov') if re.search(r'[.](gif|mov)$',imagename,flags=re.I) or padcolor=='0x00000000' else self.libi.vformat('mp4'))+" -y "+outimagename) if not getscalestr else None
  return scalestr if getscalestr else outimagename
 """

 def scalepad(self,imagename,scaledimension=None,paddimension=None,padposition='(ow-iw)/2,(oh-ih)/2',padcolor='0x000000ff',getscalestr=False,outimagename=None):
  '''scaledimension - target dimension scale 1600x900 or (1600,900)
  paddimension - pad dimension = (self.libi.videowidth,self.libi.videoheight)
  '''
  print(f'><utilc.scalepad {(imagename,scaledimension,paddimension,padposition,padcolor,getscalestr,outimagename)=}')
  if self.libi.videowidth==self.libi.videoheight==0:
   print(f'{"":-^40}\n{"Video Width Height 0":^40}\n{"":-^40}')
  padcolor='0x'+''.join(str(hex(padcolor[count])) for count in range(4)) if type(padcolor)==tuple else padcolor
  outimagename=self.libi.outimagename(imagename,extension=('mov' if re.search('[.]gif$',imagename,flags=re.I) or not re.search('ff$',padcolor,flags=re.I) else None)) if not outimagename else outimagename
  scaledimension=tuple(int(x+1) if int(x)%2 else int(x) for x in (re.split('x',scaledimension) if type(scaledimension)==str else scaledimension if type(scaledimension)==tuple else (int(self.libi.videowidth),int(self.libi.videoheight))))
  paddimension=tuple(int(x+1) if x%2 else int(x) for x in (re.split('x',paddimension) if type(paddimension)==str else paddimension if type(paddimension)==tuple else (int(self.libi.videowidth),int(self.libi.videoheight))))
#  scalestr=("scale="+(str(scaledimension[0])+':-1' if int(self.libi.dimension(imagename)[0])/scaledimension[0] > int(self.libi.dimension(imagename)[1])/scaledimension[1] else '-1:'+str(scaledimension[1])))+(',pad='+str(paddimension[0])+':'+str(paddimension[1])+':'+re.sub(r',',':',re.sub(r'(?P<id>\<[WH]\>)',lambda m:'o'+m.group('id').lower(),re.sub(r'(?P<id>\<[wh]\>)',lambda m:'i'+m.group('id'),self.libi.co(padposition,(self.libi.dimension(imagename),paddimension))))) if padposition else '')+(':'+padcolor if padposition and padcolor else '')+',setsar=sar=1'
  scalestr="scale="+str(scaledimension[0])+'x'+str(scaledimension[1])+(',pad='+str(paddimension[0])+':'+str(paddimension[1])+':'+re.sub(r',',':',re.sub(r'(?P<id>\<[WH]\>)',lambda m:'o'+m.group('id').lower(),re.sub(r'(?P<id>\<[wh]\>)',lambda m:'i'+m.group('id'),self.libi.co(padposition,(self.libi.dimension(imagename),paddimension))))) if padposition else '')+(':'+padcolor if padposition and padcolor else '')+',setsar=sar=1'
#  self.libi.system("ffmpeg "+("-ss "+str(begintime)+" -t "+str(duration)+" " if duration else " ")+"-i "+imagename+" -filter_complex \""+scalestr+"\""+(self.libi.vformat('mov') if re.search(r'[.](gif|mov)$',imagename,flags=re.I) or padcolor=='0x00000000' else self.libi.vformat('mp4'))+" -y "+outimagename) if not getscalestr else None
  self.libi.system("ffmpeg"+" -i "+imagename+" -filter_complex \""+scalestr+"\""+(self.libi.vformat('mov') if re.search(r'[.](gif|mov)$',imagename,flags=re.I) or not re.search('ff$',padcolor,flags=re.I) else self.libi.vformat('mp4'))+" -y "+outimagename) if not getscalestr else None
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

 def screenshot(self,imagename,begintime=0.0,endtime=0.0,singleframe=True,outimagename=None):
  '''take screen shot(s) at begintime uptil endtime
  outimagename - i.e screenshot%02d.png if singleframe is False else screenshot.png'''
  outimagename=self.libi.outimagename('screenshot',extension='png',outimagename=outimagename)
  self.libi.system("ffmpeg -ss "+self.libi.getsecond(begintime)+(" -to "+str(endtime) if endtime else '')+" -i "+imagename+(" -vframes 1" if singleframe else "")+" "+self.libi.adddestdir(outimagename))
  return outimagename

 def color2transparent(self,imagename,colorhex,similarity=0.3,blend=0.0,outimagename=None):
  '''make 'colorhex' pixels transparent
   colorhex - pixel color to be make transparent. In hex format ie. 0x24b403
   similarity - much similar image color from colorhex. 0-1 complete same to everything=0.3
   blend - transparent level, 0-1 complete transparent to opaque=0.0'''
  outimagename=self.libi.outimagename(imagename,outimagename,extension='mov')
  self.libi.system("ffmpeg -i "+imagename+" -filter_complex \"[0:v]colorkey="+colorhex+":"+str(similarity)+":"+str(blend)+"\""+self.libi.vformat('mov')+" -y "+outimagename)
  return outimagename

 def slowfast(self,imagename,factor=0.5,outimagename=None):
  '''slow or speed up the video
   factor - speed up by factor,i.e. 0.5 slow down by half, factor=0.5'''
  outimagename=self.libi.outimagename(imagename,outimagename)
  factorstr=re.sub(r'^,','',','.join(['atempo=2.0' for x in range(int(math.log2(factor)))])+(',atempo='+str(factor/math.pow(2,int(math.log2(factor)))) if factor/math.pow(2,int(math.log2(factor))) != 1 else '') if factor>=1.0 else ','.join(['atempo=0.5' for x in range(int(math.log2(1/factor)))])+(',atempo='+str(factor*math.pow(2,int(math.log2(1/factor)))) if factor*math.pow(2,int(math.log2(1/factor))) != 1 else ''),flags=re.I)
  self.libi.system("ffmpeg -i "+imagename+" -filter_complex \"[0:v]setpts="+str(float(1/factor))+"*PTS[v];[0:a]"+factorstr+"[a]\" -map \"[v]\" -map \"[a]\" -y "+outimagename)
  return outimagename

 def silencenaudiolist(self,audiofilemp3,syncimagevideomp4audiomp4=None,beginoffset=0,endoffset=0,filterdownaudiolevelbelow='-30dB',silenceduration=2):
  '''\
    audiofilemp3 - audacity audiomp4->audiofilemp3
    syncimagevideomp4audiomp4 - tuple of (syncimage,(videomp4,begintime,endtime),(audiomp4,begintime,endtime))
       syncimage - get referenceimage from recorded audiomp4, pass through utilc.screenshots(..singleshot=False),
       (videomp4,begintime,endtime) - (reference video,begintime,endtime)
       (audiomp4,begintime,endtime) - (annotated voice audio mp4,begintime,endtime)'''
  print(f'><utilc.silencenaudiolist {audiofilemp3=} {syncimagevideomp4audiomp4=} {beginoffset=} {endoffset=} {filterdownaudiolevelbelow=} {silenceduration=}')
  audiosignallist=[]
  substractvalue=None
  newaudiofilemp3=''
  audiolength=float(self.libi.getsecond(self.libi.videoattribute(audiofilemp3)[2]))
  for item in re.findall(r'silence_start:\s+(.*?)\s+.*?silence_end:\s+(.*?)\s+',self.libi.system(r'ffmpeg'+(' -ss'+str(beginoffset) if beginoffset else '')+(' -to'+str(endoffset) if endoffset else '')+' -i '+audiofilemp3+r' -af silencedetect=n='+filterdownaudiolevelbelow+':d='+str(silenceduration)+r" -f null -|& awk '/silencedetect/ {print $4,$5}'",popen=True),flags=re.I|re.DOTALL):
   if len(audiosignallist)>0:
    audiosignallist[-1][1]=float(item[0])
   audiosignallist.append([float(item[1]),None]) if float(item[1])>=beginoffset and abs(audiolength-float(item[1]))>1 else None
  print(f'<=>libc.silencenaudiolist ******* voice tuples ******* {tuple(tuple(x) for x in audiosignallist)=}')
  if syncimagevideomp4audiomp4:
   substractvalue=float(self.videocollidetimestamp(syncimagevideomp4audiomp4[0],*syncimagevideomp4audiomp4[2],destinationdirectory='snapshot2'))-float(self.videocollidetimestamp(syncimagevideomp4audiomp4[0],*syncimagevideomp4audiomp4[1],destinationdirectory='snapshot1'))
   for count,x in enumerate(audiosignallist[:]):
    if x[0]>substractvalue or x[1]>substractvalue:
     if x[1]>substractvalue:
      audiosignallist[count][0]=substractvalue
     break
   audiosignallist[:count]=''
   newaudiofilemp3=re.sub(r'^(.*)[.](.*)$',r'\1'+'__'+re.sub('[.]','_dot_',str(substractvalue))+'_.'+r'\2',audiofilemp3)
   self.libi.system('cp '+audiofilemp3+' '+newaudiofilemp3)
   return '\'('+newaudiofilemp3+',6),None,('+(','.join(str(x[0]-substractvalue)+'-'+str(x[1]-substractvalue) for x in audiosignallist))+')\''

 def videocollidetimestamp(self,imagename,videoname,begintime=0,endtime=0,destinationdirectory=None):
  print(f'><utilc.videocollidecollidepoint imagename={imagename} videoname={videoname} begintime={begintime} endtime={endtime}')
  outputdir=self.libi.destdir+r'/snapshot2' if not destinationdirectory else self.libi.adddestdir(destinationdirectory)
  diff=0.0
  if os.path.exists(outputdir):
   [os.remove(outputdir+r'/'+i) for i in os.listdir(outputdir)]
  else:
   os.mkdir(outputdir)
  self.screenshot(videoname,begintime=begintime,endtime=endtime,singleframe=False,outimagename=outputdir+r'/'+'out%04d.png')
  for count,i in enumerate(sorted(os.listdir(outputdir),key=lambda m:int(re.sub(r'^.*?(\d+)[.]png$',r'\1',m)))):
   diff=compare_ssim(cv2.cvtColor(cv2.imread(imagename),cv2.COLOR_BGR2GRAY),cv2.cvtColor(cv2.imread(outputdir+r'/'+i),cv2.COLOR_BGR2GRAY),full=True)[0]
   print(f'<=>utilc.videocollidetimestamp count={count} i={i} diff={diff}')
   if diff>0.5:
    print(f"<=>utilc.videocollidetimestamp i={outputdir+r'/'+i} diff={diff} timestamp={float(self.libi.getsecond(begintime))+count/float(self.libi.videoattribute(videoname)[1])}")
    break
  return float(self.libi.getsecond(begintime))+count/float(self.libi.videoattribute(videoname)[1])
