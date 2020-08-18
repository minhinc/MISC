from PIL import Image,ImageDraw,ImageFont
import textwrap
import re
import overlaym
class textc:
 '''##textc##'''
 def __init__(self,libip):
  self.libi=libip

 def dialogtext(self,args_p,filter_p,beginstring_p,returnstring_p,count_p):
  '''40:sbring1\\nsbring2..:<size>:<filterpos>:<duration[6,3]>:<transitiontime[F]>:<l[br]|m[br]><filter[^br]>:<textcolor>:<backcolor>:<glasscolor>'''
  index,s,size,filterpos,duration,transitiontime,orientation,filter,textcolor,backcolor,glasscolor=self.libi.split(args_p[0],(None,None,0.4,'(W-w),(H-h)/2','6,3',1.0,'lr',filter_p,'(255,255,255,255)','(0,0,0,192)','(0,0,0,0)'))
  self.libi.debug("><textm::dialogtext",index,s,size,filterpos,duration,filter,transitiontime,orientation,filter,textcolor,backcolor,glasscolor)
  stringlist=[]
  offset=4
  duration=tuple((int(i) for i in (re.findall(r'\d+',duration) if len(re.findall(r'\d+',duration))==2 else re.findall(r'\d+',duration)+['0'])))
  for i in re.split(r'\\n',s):
   if re.search(r'^\s*$',i): stringlist.append(i)
   else: [stringlist.append(x) for x in textwrap.wrap(i,width=40,drop_whitespace=False)]
  fnt=self.libi.getfont(stringlist if max([len(x) for x in stringlist]) >= 20 else ['Q'*20],float(size),'/home/pi/.fonts/Consolas.ttf')
  textcolor=tuple((int(i) for i in re.findall(r'\d+',textcolor)))
  backcolor=tuple((int(i) for i in re.findall(r'\d+',backcolor)))
  glasscolor=tuple((int(i) for i in re.findall(r'\d+',glasscolor)))
  textmaxindex=[len(i) for i in stringlist].index(max(len(i) for i in stringlist))
  textcellheight=fnt.getsize(stringlist[textmaxindex])[1]+offset
  imagewidth=fnt.getsize(stringlist[textmaxindex])[0]+offset
  img=Image.new('RGBA',(imagewidth,textcellheight*len(stringlist)),backcolor)
  mask=Image.new(r'L',img.size,color=0)
  draw=ImageDraw.Draw(img)
  drawmask=ImageDraw.Draw(mask)
  for i in range(len(stringlist)):
   draw.text(((imagewidth-fnt.getsize(stringlist[i])[0])/2 if re.search(r'm',orientation) else offset/2,i*textcellheight+(textcellheight-fnt.getsize(stringlist[i])[1])/2),stringlist[i],font=fnt,fill=textcolor)
   drawmask.rectangle(((imagewidth-fnt.getsize(stringlist[i])[0])/2-offset/2,i*textcellheight+offset/4,(imagewidth+fnt.getsize(stringlist[i])[0])/2+offset/2,(i+1)*textcellheight-offset/4),fill=backcolor[3])
   drawmask.text(((imagewidth-fnt.getsize(stringlist[i])[0])/2,i*textcellheight+(textcellheight-fnt.getsize(stringlist[i])[1])/2),stringlist[i],font=fnt,fill=textcolor[3])
  if re.search(r'm',orientation): img.putalpha(mask)
  img.save("textimage.png")
  img.close()
  return self.libi.blendimage(args_p,self.libi.filterlist[1000+('b','r').index(orientation[1])][0] if len(orientation)==2 else self.libi.filterlist[filter][0],beginstring_p,returnstring_p,count_p,'textimage.png',duration_p=duration,filterpos_p=filterpos,transitiontime_p=transitiontime,glasscolor_p=glasscolor)
 
 def swipetext(self,args_p,filter_p,beginstring_p,returnstring_p,count_p):
  '''41:<text1\\ntext2\\n..>:<size>:<filterpos>:<duration>:<l|b>:<textcolor[(rgba)]>:<glasscolor(rgba)>'''
  diff=[]
  offset=10
  index,stringlist,size,filter,animationduration,orientation,textcolor,glasscolor=self.libi.split(args_p[0],(None,None,0.5,'(W-w)/2,(H-h)/2',6,'l','(255,255,255,255)','(0,0,0,0)'))
  textcolor=tuple((int(i) for i in re.findall(r'\d+',textcolor)))
  glasscolor=tuple((int(i) for i in re.findall(r'\d+',glasscolor)))
  stringlist=re.split(r'\\n',stringlist)
  self.libi.debug("textm::swipetext",stringlist,size,filter,animationduration,orientation,textcolor,glasscolor)
  fnt=self.libi.getfont(stringlist if max([len(x) for x in stringlist]) >= 20 else ['a'*20],size,'/home/pi/.fonts/Consolas.ttf')
  textmaxindex=[len(i) for i in stringlist].index(max([len(i) for i in stringlist]))
  textcellheight=int(fnt.getsize(stringlist[textmaxindex])[1]*1.2)
  stepcount=20
  convertstring="convert -loop 0 -dispose Background -delay "+str((animationduration*100-animationduration*100*0.7)/(2*stepcount))+' '
  for i in self.libi.stepvalue(textcellheight/2,0,len(stringlist)):
   diff.append(i)
  for count,j in enumerate(self.libi.stepvalue(textcellheight+textcellheight/2,(textcellheight-fnt.getsize(stringlist[textmaxindex])[1])/2,stepcount)):
   img=Image.new('RGBA',(fnt.getsize(stringlist[textmaxindex])[0]+(offset if orientation=='l' else 0),textcellheight*len(stringlist)+(offset if orientation=='b' else 0)),(0,0,0,0))
   draw=ImageDraw.Draw(img)
   if orientation=='l':
    draw.line((0,0,0,int((textcellheight*len(stringlist))*2/stepcount*(count+1))),fill=(00,64,00,255),width=int(offset/3))
   else:
    draw.line((0,textcellheight*len(stringlist)+offset/2,fnt.getsize(stringlist[textmaxindex])[0]/stepcount*(count+1),textcellheight*len(stringlist)+offset/2),fill=(00,64,00,255),width=int(offset/3))
   for i in range(len(stringlist)):
    img1=Image.new('RGBA',(fnt.getsize(stringlist[textmaxindex])[0],textcellheight),(0,0,0,0))
    draw=ImageDraw.Draw(img1)
    draw.text((0,max((textcellheight-fnt.getsize(stringlist[textmaxindex])[1])/2,j-int(diff[i]))),stringlist[i],font=fnt,fill=textcolor)
    img.paste(img1,(int(offset*2/3) if orientation=='l' else 0,i*textcellheight))
   img.save("swipetext"+str(count)+".png")
   convertstring+="swipetext"+str(count)+".png "
  convertstring+="-delay "+str(animationduration*100*0.7)+" swipetext"+str(count)+".png -delay "+str((animationduration*100-animationduration*100*0.7)/stepcount)+' '
  for count,j in enumerate(self.libi.stepvalue((textcellheight-fnt.getsize(stringlist[textmaxindex])[1])/2,-fnt.getsize(stringlist[textmaxindex])[1],int(stepcount/2))):
   img=Image.new('RGBA',(fnt.getsize(stringlist[textmaxindex])[0]+(offset if orientation=='l' else 0),textcellheight*len(stringlist)+(offset if orientation=='b' else 0)),(0,0,0,0))
   draw=ImageDraw.Draw(img)
   for i in range(len(stringlist)):
    img1=Image.new('RGBA',(fnt.getsize(stringlist[textmaxindex])[0],textcellheight),(0,0,0,0))
    draw=ImageDraw.Draw(img1)
    draw.text((0,j),stringlist[i],font=fnt,fill=(255,255,255,255))
    img.paste(img1,(int(offset*2/3) if orientation=='l' else 0,i*textcellheight))
   img.save("swipetext"+str(count)+'u'+".png")
   convertstring+="swipetext"+str(count)+'u'+".png "
  self.libi.system(convertstring+"swipetext.gif")
  return self.libi.blendimage(args_p,filter_p,beginstring_p,returnstring_p,count_p,'swipetext.gif',duration_p=(animationduration,0),filterpos_p=filter,transitiontime_p=0.0,glasscolor_p=glasscolor)

 def logotext(self,args_p,filter_p,beginstring_p,returnstring_p,count_p):
  '''<42>:<size>:<filterpos>'''
  index,size,filterpos=self.libi.split(args_p[0],(None,0.5,self.libi.filterlist[filter_p][0]))
  filterpos=re.sub(r'\\:',r':',self.libi.convertfilter(filterpos,True))
  font=self.libi.getfont(['Minh, Inc.'],size,'/home/pi/.fonts/tw-cen-mt-bold.ttf')
  font1=self.libi.getfont(['Minh, Inc.'],size*0.8,'/home/pi/.fonts/tw-cen-mt-bold.ttf')
  font2=self.libi.getfont(['A Software Research Firm'],size,'/home/pi/.fonts/tw-cen-mt-bold.ttf')
  imagewidth=max(font.getsize('Minh, Inc.')[0],font1.getsize('Minh, Inc.')[0],font2.getsize('A Software Research Firm')[0])
  img=Image.new('RGBA',(imagewidth,int(font.getsize('Minh, Inc.')[1]*1.2+font2.getsize('A Software Research Firm')[1])),(0,0,0,0))
  draw=ImageDraw.Draw(img)
  xoffset=(font2.getsize('A Software Research Firm')[0]-(font.getsize('Minh ')[0]+font1.getsize('Inc.')[0]))/2
  draw.text((xoffset,0),"Minh ",font=font,fill=(0,64,0,255))
  draw.text((xoffset+font.getsize('Minh ')[0],font.getsize('Minh ')[1]-font1.getsize('Minh ')[1]),'Inc.',font=font1,fill=(0,64,0,255))
  draw.text((0,font.getsize('Minh')[1]*1.2),'A Software Research Firm',font=font2,fill=(200,200,200,255))
  img.save('frnt.png')
  convertstring='convert -loop 0 -dispose Background -delay 4 '
  for j in range(2):
   for count,i in enumerate(self.libi.stepvalue(0,imagewidth+int(font.getsize('Minh, Inc.')[1]*1.2+font2.getsize('A Software Research Firm')[1]),22)):
    img=Image.open(r'frnt.png').convert('RGBA')
    mask=Image.new(r'L',img.size,color=0)
    draw=ImageDraw.Draw(mask)
    draw.text((xoffset,0),"Minh ",font=font,fill=255)
    draw.text((xoffset+font.getsize('Minh ')[0],font.getsize('Minh ')[1]-font1.getsize('Minh ')[1]),'Inc.',font=font1,fill=255)
    draw.text((0,font.getsize('Minh')[1]*1.2),'A Software Research Firm',font=font2,fill=255)
    if j==0:
     draw.polygon([(i,0),(0,i),(0,imagewidth*2),(imagewidth*2,0)],fill=0)
    else:
     draw.polygon([(0,0),(i,0),(0,i)],fill=0)
    img.putalpha(mask)
    convertstring+='out'+str(j)+str(count)+'.png '
    img.save('out'+str(j)+str(count)+'.png')
   if j==0:
    convertstring+='-delay 30 out'+str(j)+str(count)+'.png -delay 3 '
  self.libi.system(convertstring+'-delay 1 out'+str(j)+str(count)+'.png logotext.gif')
  beginstring_p+="-i logotext.gif "
  for j in range(1,len(args_p)):
   returnstring_p+="["+str(len(re.findall(r' -i ',beginstring_p))-1)+":v]setpts=PTS+"+self.libi.getsecond(args_p[j])+"/TB[bio"+str(count_p)+"];"+("[0:v]" if not count_p else "[io"+str(count_p-1)+"]")+"[bio"+str(count_p)+"]"+filterpos+"[io"+str(count_p)+"];"
   count_p=count_p+1
  return (beginstring_p,returnstring_p,count_p)

 def omnitext(self,args_p,filter_p,beginstring_p,returnstring_p,count_p):
  '''43:<text1\\ntext2\\n><text3\\n..>:<size>:<filterpos>:<duration>:<l[i]|o>:<shade[rgba]>'''
  offset=10
  index,s,size,filterpos,animationduration,orientation,shadecolor=self.libi.split(args_p[0],(None,None,0.5,self.libi.filterlist[filter_p][0],5,'li','(0,0,0,128)'))
  stringlist=[]
  filterpos=re.sub(r'\\:',r':',self.libi.convertfilter(filterpos,True))
  shadecolor=tuple((int(i) for i in re.findall(r'\d+',shadecolor)))
  fnt=self.libi.getfont(re.split(r'\\n',s) if max([len(x) for x in re.split(r'\\n',s)]) >= 20 else ['Q'*20],float(size),'/home/pi/.fonts/Consolas.ttf')
  fnts=self.libi.getfont(re.split(r'\\n',s) if max([len(x) for x in re.split(r'\\n',s)]) >= 20 else ['Q'*20],float(size)*0.5,'/home/pi/.fonts/Consolas.ttf')
  for i in range(len(re.split(r'\\n',s))):
   if re.search(r'(^|\\n)><',s):
    stringlist.append([re.sub(r'><(.*)',r'\1',re.split(r'\\n',s)[i]),None,int(fnt.getsize(re.sub(r'><(.*)',r'\1',re.split(r'\\n',s)[i]))[1]+offset),fnt] if re.search(r'^><',re.split(r'\\n',s)[i]) else [re.split(r'\\n',s)[i],None,int(fnts.getsize(re.split(r'\\n',s)[i])[1]+offset/6),fnts])
   else:
    stringlist.append([re.split(r'\\n',s)[i],None,int(fnt.getsize(re.split(r'\\n',s)[i])[1]+offset),fnt])
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
   stringlist[i][1]=(int((animationrect[0]-stringlist[textmaxindex][3].getsize(stringlist[textmaxindex][0])[0])/2) if orientation[0]!='o' else int((animationrect[0]-stringlist[i][3].getsize(stringlist[i][0])[0])/2),sumtextcellheight)
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
   if re.search(r'^li',orientation):
    for j in range(lineindex):
     if not re.search(r'^[ ]*$',stringlist[j][0]): draw.line(((animationrect[0]-glassrect[0])/2-offset,stringlist[j][1][1],(animationrect[0]-glassrect[0])/2-offset,stringlist[j][1][1]+stringlist[j][2]),fill='red' if stringlist[j][3]==fnt else 'white',width=int(offset/4))
    if not re.search(r'^[ ]*$',stringlist[lineindex][0]): draw.line(((animationrect[0]-glassrect[0])/2-offset,stringlist[lineindex][1][1],(animationrect[0]-glassrect[0])/2-offset,lineheight-1),fill='red' if stringlist[lineindex][3]==fnt else 'white', width=int(offset/4))
   #print(z)
   for i in range(len(z)):
    #print("y {} {} {}".format(z[i][1],stringlist[i][1],stringlist[i][3].getsize(stringlist[i][0])))
    draw.text((z[i][0],z[i][1]+(stringlist[i][2]-stringlist[i][3].getsize(stringlist[i][0])[1])/2),stringlist[i][0],font=stringlist[i][3],fill=("white",(0,255,0,255),"yellow","orange")[i%4] if orientation[0]=='o' else "yellow" if stringlist[i][3]==fnt else "white")
#    draw.text((z[i][0],z[i][1]),stringlist[i][0],font=stringlist[i][3],fill=("white",(0,255,0,255),"yellow","orange")[i%4] if orientation[0]=='o' else "yellow" if stringlist[i][3]==fnt else "white")
#    draw.text((z[i][0],z[i][1]),stringlist[i][0],font=stringlist[i][3],fill=("white","red","yellow","orange")[i%4] if orientation=='o' else "yellow" if stringlist[i][3]==fnt else "white")
   img.save("omnitext"+str(count)+".png")
   convertstring+="omnitext"+str(count)+".png "
  convertstring+="-delay "+str((animationduration-1)*100)+" omnitext"+str(count)+".png -delay 10 omnitext"+str(count)+".png "
  self.libi.system(convertstring+"omnitext.gif")
  #if re.search(r's',orientation):
#  if shadecolor!=(0,0,0,0):
#   print("s found")
#   img=Image.new('RGBA',(glassrect[0]+3*offset,glassrect[1]),shadecolor)
#   img.save('back_'+str(count_p)+'.png')
#   beginstring_p+='-i back_'+str(count_p)+'.png '
#   imagecount=str(len(re.findall(r' -i ',beginstring_p))-1)
  beginstring_p+="-i omnitext.gif "
  for j in range(1,len(args_p)):
   #if re.search(r's',orientation):
#   if shadecolor!=(0,0,0,0):
#    returnstring_p+=("[0:v]" if not count_p else "[io"+str(count_p-1)+"]")+"["+imagecount+":v]"+re.sub(r'eof_action=pass','enable=\'between(t,'+str(float(self.libi.getsecond(args_p[j])))+','+str(float(self.libi.getsecond(args_p[j]))+animationduration)+')\'',filter)+"[io"+str(count_p)+"];"
#    count_p=count_p+1
#   returnstring_p+="["+str(len(re.findall(r' -i ',beginstring_p))-1)+":v]setpts=PTS+"+self.libi.getsecond(args_p[j])+"/TB[bio"+str(count_p)+"];"+("[0:v]" if not count_p else "[io"+str(count_p-1)+"]")+"[bio"+str(count_p)+"]"+filter+"[io"+str(count_p)+"];"
   returnstring_p+='color=0x'+''.join(re.sub(r'^0x','0',hex(int(i)))[-2:] for i in shadecolor[:3])+'@'+str(round(shadecolor[3]/255,3) if shadecolor[3] else 0)+':s='+'x'.join([str(glassrect[0]+3*offset),str(glassrect[1])])+"[i];"+("[0:v]" if not count_p else "[io"+str(count_p-1)+"]")+"[i]"+filterpos+":enable=between'(t,"+str(float(self.libi.getsecond(args_p[j]))+0.5)+","+str(float(self.libi.getsecond(args_p[j]))+animationduration)+")'[int];"+"["+str(len(re.findall(r' -i ',beginstring_p))-1)+":v]setpts=PTS+"+self.libi.getsecond(args_p[j])+"/TB[bio"+str(count_p)+"];[int][bio"+str(count_p)+"]"+filterpos+"[io"+str(count_p)+"];"
   count_p=count_p+1
  return (beginstring_p,returnstring_p,count_p)
