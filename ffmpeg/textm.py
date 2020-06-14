from PIL import Image,ImageDraw,ImageFont
import re
import overlaym
class textc:
 '''##text##'''
 position=[
            [r'(W-fnt.getsize(stringlist_p[0])[0])/2',r'max(H-offset*i,firstoffset)'],
            [r'(W-fnt.getsize(stringlist_p[0])[0])/2',r'min(offset*i-fnt.getsize(stringlist_p[0])[1],firstoffset)',r'(W-fnt.getsize(stringlist_p[1])[0])/2',r'max(H-offset*i,firstoffset+1*(offset+fnt.getsize(stringlist_p[1])[1]))'],
            [r'(W-fnt.getsize(stringlist_p[0])[0])/2',r'min(offset*i-fnt.getsize(stringlist_p[0])[1],firstoffset)',r'min(-fnt.getsize(stringlist_p[1])[0]+((fnt.getsize(stringlist_p[1])[0]+(W-fnt.getsize(stringlist_p[1])[0])/2)/totalstep)*i,(W-fnt.getsize(stringlist_p[1])[0])/2)',r'max(H-((H-(firstoffset+fnt.getsize(stringlist_p[0])[1]+offset))/totalstep)*i,firstoffset+fnt.getsize(stringlist_p[0])[1]+offset)', r'max(W-((W-(W-fnt.getsize(stringlist_p[2])[0])/2)/totalstep)*i,(W-fnt.getsize(stringlist_p[2])[0])/2)',r'max(H-((H-(firstoffset+2*(fnt.getsize(stringlist_p[0])[1]+offset)))/totalstep)*i,firstoffset+2*(offset+fnt.getsize(stringlist_p[2])[1]))'],
            [r'(W-fnt.getsize(stringlist_p[0])[0])/2',r'min(offset*i-fnt.getsize(stringlist_p[0])[1],firstoffset)', r'min(-fnt.getsize(stringlist_p[1])[0]+((fnt.getsize(stringlist_p[1])[0]+(W-fnt.getsize(stringlist_p[1])[0])/2)/totalstep)*i,(W-fnt.getsize(stringlist_p[1])[0])/2)',r'firstoffset+1*(offset+fnt.getsize(stringlist_p[1])[1])',r'max(W-((W-(W-fnt.getsize(stringlist_p[2])[0])/2)/totalstep)*i,(W-fnt.getsize(stringlist_p[2])[0])/2)',r'firstoffset+2*(offset+fnt.getsize(stringlist_p[2])[1])',r'(W-fnt.getsize(stringlist_p[3])[0])/2',r'max(H-offset*i,firstoffset+3*(offset+fnt.getsize(stringlist_p[3])[1]))']
          ]
 def __init__(self,libip):
  self.libi=libip
  self.overlayi=overlaym.overlayc(libip)

# def messagebox(self,stringlist_p,size_p=0.5):
 def messagebox(self,args_p,filter_p,beginstring_p,returnstring_p,count_p):
  stringlist_p=self.libi.split(args_p[0])[1].split(r'\n')
  size_p=0.5 if len(self.libi.split(args_p[0]))<=2 else self.libi.split(args_p[0])[2]
  print("libc::messagebox<> {} {}".format(stringlist_p,size_p))
  offset=10
  fnt=self.libi.getfont(stringlist_p if max([len(x) for x in stringlist_p]) >= 20 else ['a'*20],size_p,'/home/pi/.fonts/tw-cen-mt-bold.ttf')
  convertstring="convert -loop 0 -dispose Background -delay 3 "
  for i in range(int(self.libi.videowidth*size_p/offset+(len(stringlist_p)-1)*4)):
   img=Image.new('RGBA',(int(self.libi.videowidth*size_p),max(len(stringlist_p)*(fnt.getsize(stringlist_p[0])[1]+offset),int(self.libi.videoheight*size_p))),(255,255,255,0))
   draw=ImageDraw.Draw(img)
   draw.line((0,0,0,len(stringlist_p)*(offset+fnt.getsize(stringlist_p[0])[1])),fill=(00,64,00,255),width=int(offset*2/3))
   for j in range(len(stringlist_p)):
    #self.drawtextstroke(draw,max(offset,-i*offset+self.videowidth*size_p+j*4*offset),offset/2+j*(offset-1+fnt.getsize(stringlist_p[0])[1]),stringlist_p[j],fnt,"white",strokecolor_p="blue",adj_p=0.5)
    draw.text((max(offset,-i*offset+self.libi.videowidth*size_p+j*4*offset),offset/2+j*(offset-1+fnt.getsize(stringlist_p[0])[1])),stringlist_p[j],font=fnt,fill="blue")
   img.save("messagebox"+str(i)+".png")
   convertstring+="messagebox"+str(i)+".png "
  convertstring+="-delay 800 messagebox"+str(i)+".png -delay 10 messagebox"+str(i)+".png "
  self.libi.system(convertstring+"msgbox.gif")
  return (beginstring_p,returnstring_p,count_p)

 def stilltext(self,stringlist_p):
  print("libc::stilltext<> {}".format(stringlist_p))
  offset=10
  fnt=self.getfont(stringlist_p if max([len(x) for x in stringlist_p]) >= int(40*size_p) else ['a'*int(40*size_p)],size_p,'/home/pi/.fonts/tw-cen-mt-bold.ttf')
  img=Image.new('RGBA',(int(self.videowidth*size_p),max(len(stringlist_p)*(fnt.getsize(stringlist_p[0])[1]+offset),int(self.videoheight*size_p))),(182,23,28,128))
  draw=ImageDraw.Draw(img)
  for i in range(len(stringlist_p)):
   draw.line(0,(offset+fnt.getsize(stringlist_p[max(0,i-1)])[1])*i,0,(offset+fnt.getsize(stringlist_p[i])[1])*(i+1),fill=(enablecolor if enable[i] else disablecolor),width=int(offset*2/3))
   self.drawtextstroke(draw,offset,offset/2+i*(offset-1+fnt.getsize(stringlist_p[i])[1]),stringlist_p[i],fnt,"yellow",adj_p=0.5)
  img.save("stilltext.png")
  return "stilltext.png"

 def messagebox1(self,stringlist_p,size_p=0.5):
  print("libc::messagebox<> {}".format(stringlist_p))
  offset=10
  fnt=self.getfont(stringlist_p if max([len(x) for x in stringlist_p]) >= 20 else ['a'*20],size_p,'/home/pi/.fonts/tw-cen-mt-condensed-3.ttf')
  convertstring="convert -loop 0 -dispose Background -delay 3 "
  for i in range(int(self.videowidth*size_p/offset+(len(stringlist_p)-1)*4)):
   img=Image.new('RGBA',(int(self.videowidth*size_p),max(len(stringlist_p)*(fnt.getsize(stringlist_p[0])[1]+offset),int(self.videoheight*size_p))),(255,255,255,0))
   draw=ImageDraw.Draw(img)
   draw.line((0,0,0,len(stringlist_p)*(offset+fnt.getsize(stringlist_p[0])[1])),fill=(00,64,00,255),width=int(offset*2/3))
   for j in range(len(stringlist_p)):
    #self.drawtextstroke(draw,max(offset,-i*offset+self.videowidth*size_p+j*4*offset),offset/2+j*(offset-1+fnt.getsize(stringlist_p[0])[1]),stringlist_p[j],fnt,"white",strokecolor_p="blue",adj_p=0.5)
    draw.text((max(offset,-i*offset+self.videowidth*size_p+j*4*offset),offset/2+j*(offset-1+fnt.getsize(stringlist_p[0])[1])),stringlist_p[j],font=fnt,fill="white")
   img.save("title"+str(i)+".png")
   convertstring+="title"+str(i)+".png "
  convertstring+="-delay 800 title"+str(i)+".png -delay 10 title"+str(i)+".png "
  print(convertstring+"msgbox.gif")
  return convertstring+"title.gif"

 def titletext(self,stringlist_p):
  '''"301:Qt\\nQScrollBar\\nQScrollArea:10" 00:00:02 00:00:40.234
  <index>:<string>:<duration>'''
  print("libc::titletext<> {}".format(stringlist_p))
  offset=10
  fnt=self.getfont(stringlist_p,0.5)
  firstoffset=(self.videoheight-fnt.getsize(stringlist_p[0])[1]*len(stringlist_p)-offset*(len(stringlist_p)-1))/2
  totalstep=int((firstoffset+fnt.getsize(stringlist_p[0])[1])/offset)
  print("totalstep,firstoffset {},{}".format(totalstep,firstoffset))
  convertstring="convert -loop 0 -dispose Background -delay 10 "
  for i in range(totalstep+4):
   img=Image.new('RGBA',(320,240),(255,255,255,0))
   draw=ImageDraw.Draw(img)
   for j in range(len(stringlist_p)):
    self.drawtextstroke(draw,eval(re.sub(r'\bW\b',r'self.videowidth',re.sub(r'\bH\b',r'self.videoheight',position[len(stringlist_p)-1][j*2]))),eval(re.sub(r'\bW\b',r'self.videowidth',re.sub(r'\bH\b',r'self.videoheight',position[len(stringlist_p)-1][j*2+1]))),stringlist_p[j],fnt,("yellow","green","white","orange")[j],adj_p=1)
   img.save("title"+str(i)+".png")
   convertstring+="title"+str(i)+".png "
  convertstring+="-delay 800 title"+str(i)+".png -delay 10 "
  for i in range(max([len(x) for x in stringlist_p])):
   img=Image.new('RGBA',(320,240),(255,255,255,0))
   draw=ImageDraw.Draw(img)
   for j in range(len(stringlist_p)):
    if i>=(max([len(x) for x in stringlist_p])-len(stringlist_p[j]))/2:
     self.drawtextstroke(draw,(320-fnt.getsize(stringlist_p[j])[0])/2+fnt.getsize(stringlist_p[j][0])[0]*i,firstoffset+j*(offset+fnt.getsize(stringlist_p[j])[1]),stringlist_p[j][i:],fnt,("white","green","yellow","orange")[j],adj_p=1)
    else:
     self.drawtextstroke(draw,(320-fnt.getsize(stringlist_p[j])[0])/2,firstoffset+j*(offset+fnt.getsize(stringlist_p[j])[1]),stringlist_p[j],fnt,("white","green","yellow","orange")[j],adj_p=1)
   img.save("titlewipe"+str(i)+".png")
   convertstring+="titlewipe"+str(i)+".png "
  print(convertstring+"title.gif")
  return convertstring+"title.gif"

 def annotation(self,string_p):
  xoffset_n=20
  yoffset_n=10
  print("libc::wipelr<> {}".format(string_p))
  fnt=self.getfont((string_p,),0.5)
  def create_image(text_p):
   img=Image.new('RGBA',(fnt.getsize(string_p)[0]+xoffset_n,fnt.getsize(string_p)[1]+yoffset_n),(255,255,255,0))
   draw=ImageDraw.Draw(img)
   draw.rectangle([0,0,fnt.getsize(text_p)[0]+(xoffset_n/2 if text_p!=string_p else xoffset_n),fnt.getsize(string_p)[1]+yoffset_n],fill=(182,28,23,255))
   self.drawtextstroke(draw,xoffset_n/2,yoffset_n/2,text_p,fnt,"white",adj_p=1)
   return img
  def wipe_image(text_p):
   img=Image.new('RGBA',(fnt.getsize(string_p)[0]+xoffset_n,fnt.getsize(string_p)[1]+yoffset_n),(255,255,255,0))
   draw=ImageDraw.Draw(img)
   draw.rectangle([fnt.getsize(re.sub(text_p+r'$',r'',string_p))[0]+(0 if text_p==string_p else xoffset_n/2 if text_p else xoffset_n),0,fnt.getsize(string_p)[0]+xoffset_n,fnt.getsize(string_p)[1]+yoffset_n],fill=(200,38,35,255))
   self.drawtextstroke(draw,fnt.getsize(re.sub(text_p+r'$',r'',string_p))[0]+xoffset_n/2,yoffset_n/2,text_p,fnt,"white",adj_p=1)
   return img
  convertstring="convert -loop 0 -dispose Background"
  for i in range(len(string_p)):
   create_image(string_p[:i+1]).save("p"+str(i)+".png")
   convertstring=convertstring+(" -delay 500 p" if i+1==len(string_p) else " p")+str(i)+".png"
  convertstring=convertstring+" -delay 10 "
  for i in range(len(string_p)+1):
   wipe_image(string_p[i:len(string_p)+1]).save("p"+str(i+len(string_p))+".png")
   convertstring=convertstring+" p"+str(i+len(string_p))+".png"
  print(convertstring+" "+"annotation.gif")
  self.libi.system(convertstring+" "+"annotation.gif")
  return convertstring+" "+"annotation.gif"
