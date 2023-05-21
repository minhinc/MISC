import urllib.request
import requests
import re
import os
from PIL import Image,ImageDraw
import time#D
import sys
sys.path.append(os.path.expanduser('~')+'/tmp/')
#from gtc.databasem import databasec
from .databasem import databasec
from io import BytesIO
from MISC.ffmpeg.libm import libc
from MISC.utillib.util import Util
def gets(file,head=False,get=False,binary=False,stream=False,retrycount=1,size=None,timeout=(10,20)):
 '''requests
  HEAD request, response datastructure is returned
  response.ok to check success
  response.headers for complete hash/dict'''
 print('><gets ',file)
 if not re.search(r'^http',file,flags=re.I) and os.path.isfile(file):
  print('local file',file)
  return file
 if not hasattr(gets,'session'):
  setattr(gets,'session',requests.Session())
 session=getattr(gets,'session')
 if not re.search(r'^http',file,flags=re.I):
  file='http://'+file
 response=None
 data=None
# print("><gets,head,get,file",head,get,file)
 if head:
  try:
   response=session.head(file,timeout=timeout[0])
   if not get:
    return response if response.ok else None
  except Exception as e:
   print("heads exception",file,type(e))
#   return response if not get else ''
   return None
# print('head over')
 if (head and get and response.ok and (re.search(r'text',response.headers['Content-Type'],flags=re.I) if 'Content-Type' in response.headers and not (binary or stream) else True) and (int(response.headers['Content-Length'])<=size*1024 if 'Content-Length' in response.headers and size else True)) or (not head and get):
  now=time.time()
  while retrycount:
   try:
 #   retrycount-=1
    data=session.get(file,timeout=timeout[1])
   except Exception as e:
    retrycount-=1
    print("gets exception",type(e),":",e.__class__.__name__,int(time.time()-now),":",file)
    data=None
   else:
    break
#   if data and data.ok:
#    break
   print('<requestm.gets> trying... retrycount',retrycount)
   time.sleep(1)
  if not data or not data.ok:
#   return ''
   return ('',retrycount)
  elif stream:
   return BytesIO(data.content)
  elif binary:
   return data.content
  else:
#   return data.text
   return (data.text,retrycount)
 else:
#  return ''
  return ('',retrycount)

def get(file,head=False,get=False,binary=False,size=None,timeout=30):
 '''get the file if size is less than 100KB'''
 if not re.search(r'^http',file,flags=re.I):
  file='http://'+file
 try:
  response=urllib.request.urlopen(file)
  if head:
   return response
 except:
  print('except skipped',file)
  return response
  
 headertypelist=list(filter(lambda x:'Content-Type' in x,response.getheaders()))
 headercontentlist=list(filter(lambda x:'Content-Length' in x,response.getheaders()))
 print('headertypelist,headercontent,size',headertypelist,headercontentlist)
 if (head and get and not headertypelist or re.search(r'text',headertypelist[0][1],flags=re.I)) and (not headercontentlist or not size or int(headercontentlist[0][1])<=size*1024) or (not head and get):
  if binary:
   return response.read()
  else:
   return response.read().decode('utf-8')
 else:
#  print('skipped',file,headertypelist)
  return ''

def getgoogle(linkp,countp,timeout=(10,20)):
 '''get from google search'''
# print("><getgoogle",linkp)
 linklist=[]
 for i in range(countp):
  linklist.extend([x for x in re.findall(r'/url\?q=([^&]+)',gets(r'https://www.google.com/search?q='+re.sub('\s+','+',linkp)+(r'&start='+str(i*10) if i else ''),get=True,timeout=timeout),flags=re.I) if not re.search(r'accounts.google',x,flags=re.I)])
# print("linklist {}".format(linklist))
 return linklist

def adsenserect(width,height,criteria='.*desktop.*',factor=0.1):
# print("><adsenserect width,height,factor",width,height,factor)
 if not hasattr(adsenserect,'rect'):
  db=databasec(False)
  adsensecode=[(i[2],i[3:]) for i in db.search2('adsense','*','name','R',criteria) if i[3:]!=(0,0)]
  rect=[i[1] for i in adsensecode]
  setattr(adsenserect,'adsensecode',adsensecode)
  setattr(adsenserect,'rect',rect)
 else:
  adsensecode=getattr(adsenserect,'adsensecode')
  rect=getattr(adsenserect,'rect')

 def getrect(x,y,width,height,xrectcount=0,yrectcount=0,factor=0.1):
#  print('><getrect,x,y,width,height,xrectcount,yrectcount,factor',x,y,width,height,xrectcount,yrectcount,factor)
  nonlocal rect
  ixyarealist=None
  ilist=[i for i in range(len(rect)) if rect[i][0]<=width and rect[i][1]<=height]
  #print("getrect",x,y,width,height,(xrectcount,yrectcount),ilist)
  if len(ilist):
   for i in ilist:
    tixyarealist=[[[i,x,y,xrectcount,yrectcount]],0]
    area=getrect(x+rect[i][0],y,width-rect[i][0],rect[i][1],xrectcount+1,yrectcount,factor)
    if not area:
      tixyarealist[1]+=(width-rect[i][0])*rect[i][1]
    else:
#     tixyarealist[2].extend(area[2])
     tixyarealist[0].extend(area[0])
     tixyarealist[1]+=area[1]
    area=getrect(x,y+rect[i][1],width,height-rect[i][1],xrectcount,yrectcount+1,factor)
    if not area:
      tixyarealist[1]+=width*(height-rect[i][1])
    else:
#     tixyarealist[2].extend(area[2])
     tixyarealist[0].extend(area[0])
     tixyarealist[1]+=area[1]

#    ixyarealist=tixyarealist if not ixyarealist else ixyarealist
    if not ixyarealist:
     ixyarealist=tixyarealist
#    elif tixyarealist[1]<ixyarealist[1]:
    elif tixyarealist[1]-((len(ixyarealist[0])-len(tixyarealist[0]))*sum([rect[x[0]][0]*rect[x[0]][1] for x in tixyarealist[0]])*factor if len(tixyarealist[0])<len(ixyarealist[0]) else 0) < ixyarealist[1]-((len(tixyarealist[0])-len(ixyarealist[0]))*sum([rect[x[0]][0]*rect[x[0]][1] for x in ixyarealist[0]])*factor if len(ixyarealist[0])<len(tixyarealist[0]) else 0):
     ixyarealist=tixyarealist
  else:
    return False
  return ixyarealist
 rectposition=getrect(0,0,width,height,factor=factor)
 if not rectposition:
  return []
 xoffset,yoffset=int((width-max([x[1]+rect[x[0]][0] for x in rectposition[0]]))/(max([x[3] for x in rectposition[0]])+2)),int((height-max([x[2]+rect[x[0]][1] for x in rectposition[0]]))/(max([x[4] for x in rectposition[0]])+2))
 return [re.sub(r'style="',"style=\"position:absolute;left:"+str(x[1]+int(int((x[3]+1)*xoffset)))+"px;top:"+str(x[2]+int((x[4]+1)*yoffset))+"px;",adsensecode[x[0]][0]) for x in rectposition[0]]

def youtubeimage(youtubeid,pushonserver=False):
 """<- (imageurl,img.size)"""
 print(f'><youtubeimage {youtubeid=}')
 if os.path.exists(os.path.expanduser('~')+r'/tmp/imageglobe/image/'+youtubeid+r'.jpg'):
#  print(f'image {youtubeid=}.jpg available at {os.path.expanduser("~")+r"/tmp/MISC/image"}')
  img=Image.open(os.path.expanduser('~')+r'/tmp/imageglobe/image/'+youtubeid+r'.jpg')
 else:
  with Image.open(gets(r'https://img.youtube.com/vi/'+youtubeid+r'/sddefault.jpg',get=True,stream=True,retrycount=4)) as img:
   with Image.open(os.path.expanduser('~')+r'/tmp/imageglobe/image/youtubebutton.png') as youtubebuttonimg:
    youtubebuttonimg=youtubebuttonimg.resize((img.width//5,img.height//5))
    img.paste(youtubebuttonimg,(int((img.width-youtubebuttonimg.width)/2),int((img.height-youtubebuttonimg.height)/2)),youtubebuttonimg)
    img=img.crop((0,int((img.height-(img.width*9)/16)/2),img.width,int((img.height+(img.width*9)/16)/2)))
    print('image ',youtubeid+r'.jpg not available at /image uploading...')
    img.save(os.path.expanduser('~')+r'/tmp/imageglobe/image/'+youtubeid+".jpg")
#    os.system(r'~/tmp/ftp.sh -f put image ./'+youtubeid+'.jpg') if pushonserver else None
    Util.ftp('put','image','./'+youtubeid+'.jpg') if pushonserver else None
 #print('imagewidth',img.size)
 #return (r'http://minhinc.000webhostapp.com/image/'+youtubeid+'.jpg',img.size)
 return (r'http://minhinc.42web.io/image/'+youtubeid+'.jpg',img.size)

def adsensepaste(width,height,stylecode='',backend='desktop',factor=0.2):
 rightdiv=''
 if not hasattr(adsensepaste,'responsivesquare'):
  setattr(adsensepaste,'responsivesquare',databasec(False).get('adsense','value','name','responsivesquare')[0][0])
  print('responsivesquare',getattr(adsensepaste,'responsivesquare'))
 if re.search(r'^m',backend,flags=re.I):
  rightdiv=re.sub(r'\s*data-ad-format="auto".*responsive="true"',r'',re.sub(r'(class="adsbygoogle)',r'\1 adslot_1',re.sub(r'display:block',r'display:inline-block;height:'+str(height)+'px;',getattr(adsensepaste,'responsivesquare'),flags=re.I|re.DOTALL),flags=re.I|re.DOTALL),flags=re.I|re.DOTALL) if height>=50 else ''
  rightdiv="<div align=\"center\" style=\"width:100%;height:"+str(height)+"px;"+stylecode+"\">"+rightdiv+r'</div>' if rightdiv else ''
 elif re.search(r'^d',backend,flags=re.I):
  rightdiv=''.join(adsenserect(width,height,criteria=('.*desktop.*'),factor=factor))
  rightdiv=re.sub(r'\s*data-ad-format="auto".*responsive="true"',r'',re.sub(r'(class="adsbygoogle)',r'\1 adslot_1',re.sub(r'display:block',r'display:inline-block;height:'+str(height)+'px;',getattr(adsensepaste,'responsivesquare'),flags=re.I|re.DOTALL),flags=re.I|re.DOTALL),flags=re.I|re.DOTALL) if not rightdiv and height>=50 else rightdiv
  rightdiv=("<div style=\"width:"+str(int(width))+"px;height:"+str(height)+"px;position:relative;"+stylecode+"\" align=\"center\">"+rightdiv+r'</div>' if rightdiv else '')+(r'<div class="clr"></div>' if re.search(r'float\s*:\s*right',stylecode,flags=re.I) else '')
 else:
  rightdiv="<div align=\"center\" style=\"width:100%;\""+getattr(adsensepaste,'responsivesquare')+r'</div>'
 return rightdiv

def syncyoutube(*youtubelinklist):
# print(f'syncyoutube>< {youtubelinklist=}')
 trycount=2
 data=''
 while trycount:
  data=os.popen(r'~/tmp/ftp.sh ls image').read()
  print(f'syncyoutube {data=}')
  if data and not re.search(r'not connected',data,flags=re.I) and re.search(r'[.](jpg|png|jpeg|gif)',data,flags=re.I):
   break
  else:
   print(f'error data not found {trycount=}')
   trycount-=1
 else:
  return
 ftpstring=''
 for i in [re.sub(r'.*\?v=(.*)$',r'\1',i) for i in youtubelinklist]:
  if not re.search(i+r'.jpg\n',data):
   if not os.path.exists(os.path.expanduser('~')+r'/tmp/imageglobe/image/'+i+r'.jpg'):
    youtubeimage(i)
   ftpstring+=r' ./'+i+'.jpg'
 print(f'syncyoutube {ftpstring=}')
 if ftpstring:
  os.system('cd ~/tmp/imageglobe/image/;~/tmp/ftp.sh mput image'+ftpstring)

def preparemainfront(urltitle,subscriber):
 libi=libc()
 x='main_front.png'
 print(f'TEST {urltitle=} {subscriber=}')
 img=Image.open(os.path.expanduser('~')+'/tmp/imageglobe/image/main_front_orig.png').convert('RGBA')
 img2=Image.open(os.path.expanduser('~')+'/tmp/imageglobe/image/'+re.sub('^.*?v=(.*)',r'\1'+'.jpg',urltitle[0])).convert('RGBA').resize((940-210,564-172))
 img.paste(img2,(210,172,940,564),img2)
 img2=Image.new('RGBA',(706,34),(255,255,255,255))
 draw=ImageDraw.Draw(img2)
 draw.text((0,0),urltitle[1],fill=(0,0,0,255),font=libi.getfont(urltitle[1],1.0,widthheight=True,setvideo=(706,34)))
 img.paste(img2,(176,664,882,698),img2)
 img2=Image.new('RGBA',(110,18),(255,255,255,255))
 draw=ImageDraw.Draw(img2)
 draw.text((0,0),subscriber,fill=(40,40,40,255),font=libi.getfont(subscriber,1.0,widthheight=True,setvideo=(110,18)))
 img.paste(img2,(238,728,348,746),img2)
 img.save(os.path.expanduser('~')+'/tmp/imageglobe/image/'+x)
 if not os.path.exists(os.path.expanduser('~')+'/tmp/imageglobe/image/'+x) or not re.search(x,Util.ftp('ls','image'),flags=re.M) or int(re.sub(r'^.*?(\d+)(?:\s+\S+){3}\s+'+x+r'\s*.*',r'\1',Util.ftp('ls','image'),flags=re.DOTALL))!=os.path.getsize(os.path.expanduser('~')+'/tmp/imageglobe/image/'+x):
   print(f'<=>requestm.preparemainfront image {x} being uploaded')
   Util.ftp('put','image',os.path.expanduser('~')+'/tmp/imageglobe/image/main_front.png',localdir=os.path.expanduser('~')+'/tmp/imageglobe/image/')
