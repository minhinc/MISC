import urllib.request
import requests
import re
import os
from PIL import Image
import time#D
import sys
#sys.path.append('..')
#from gtc.databasem import databasec
from databasem import databasec
from io import BytesIO
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
    retrycount-=1
    data=session.get(file,timeout=timeout[1])
   except Exception as e:
    print("gets exception",type(e),":",e.__class__.__name__,int(time.time()-now),":",file)
    data=None
   if data and data.ok:
    break
   print('<requestm.gets> trying... retrycount',retrycount)
   time.sleep(1)
  if not data or not data.ok:
   return ''
  elif stream:
   return BytesIO(data.content)
  elif binary:
   return data.content
  else:
   return data.text
 else:
  return ''

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
  adsensecode=[(i[2],i[3:]) for i in db.get('adsense','*','name',criteria,regex=True) if i[3:]!=(0,0)]
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

def youtubeimage(youtubeid):
 if gets(r'http://minhinc.000webhostapp.com/image/'+youtubeid+r'.jpg',head=True):# and Image.open(gets(r'https://img.youtube.com/vi/'+youtubeid+r'/sddefault.jpg',get=True,retrycount=4,stream=True)).width==Image.open(gets(r'http://www.minhinc.com/image/'+youtubeid+r'.jpg',get=True,stream=True,retrycount=4)).width:
  print('image {}{}'.format(youtubeid,r'.jpg available at /image'))
  img=Image.open(gets(r'http://minhinc.000webhostapp.com/image/'+youtubeid+r'.jpg',get=True,stream=True,retrycount=4))
 else:
  with Image.open(gets(r'https://img.youtube.com/vi/'+youtubeid+r'/sddefault.jpg',get=True,stream=True,retrycount=4)) as img:
   with Image.open(gets(r'http://minhinc.000webhostapp.com/image/youtubebutton.png',get=True,stream=True,retrycount=4)) as youtubebuttonimg:
    img.paste(youtubebuttonimg,(int((img.width-youtubebuttonimg.width)/2),int((img.height-youtubebuttonimg.height)/2)),youtubebuttonimg)
    img=img.crop((0,int((img.height-(img.width*9)/16)/2),img.width,int((img.height+(img.width*9)/16)/2)))
    img.save(youtubeid+".jpg")
    print('image ',youtubeid+r'.jpg not available at /image uploading...')
    os.system(r'~/tmp/ftp.sh -f put image ./'+youtubeid+'.jpg')
 print('imagewidth',img.size)
 return (r'http://minhinc.000webhostapp.com/image/'+youtubeid+'.jpg',img.size)

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
