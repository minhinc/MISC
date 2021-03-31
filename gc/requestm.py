import urllib.request
import requests
import re
import os
from PIL import Image
import time#D
from databasem import databasec
def gets(file,head=False,get=False,binary=False,size=None,stream=False,timeout=(10,20)):
 '''requests
  HEAD request, response datastructure is returned
  response.ok to check success
  response.headers for complete hash/dict'''
 if not re.search(r'^http',file,flags=re.I):
  file='http://'+file
 response=None
 data=None
 if head:
  try:
   response=requests.head(file)
   if not get:
    return response
  except:
   print("heads exception",file)
   return response if not get else ''
 if (head and get and response.ok and (re.search(r'text',response.headers['Content-Type'],flags=re.I) if 'Content-Type' in response.headers and not binary else True) and (int(response.headers['Content-Length'])<=size*1024 if 'Content-Length' in response.headers and size else True)) or (not head and get):
  now=time.time()
  try:
   data=requests.get(file,stream=stream,timeout=timeout)
  except Exception as e:
   print("gets exception",type(e),":",e.__class__.__name__,int(time.time()-now),":",file)
   return ''
  if stream:
   return data.raw
  elif binary:
   return data.content
  else:
   return data.text

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
#  rect=list(zip(list(zip(*self.idrect))[1],list(zip(*self.idrect))[2]))
 if not hasattr(adsenserect,'rect'):
  print('><adsenserect setting')
  db=databasec(False)
#  idrect=[(i[0],i[3:]) for i in db.get('adsense') if i[3:] != (0,0)]
  adsensecode=[(i[2],i[3:]) for i in db.get('adsense','*','name',criteria,regex=True) if i[3:]!=(0,0)]
  rect=[i[1] for i in adsensecode]
#  rect=[i[1] for i in idrect]
#  setattr(adsenserect,'db',db)
#  setattr(adsenserect,'idrect',idrect)
  setattr(adsenserect,'adsensecode',adsensecode)
  setattr(adsenserect,'rect',rect)
 else:
#  print('><adsenserect getting')
#  db=getattr(adsenserect,'db')
#  idrect=getattr(adsenserect,'idrect')
  adsensecode=getattr(adsenserect,'adsensecode')
  rect=getattr(adsenserect,'rect')
# print('adesensecode,rect',adsensecode,rect)

 def getrect(x,y,width,height,xrectcount=0,yrectcount=0,factor=0.1):
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
#    print("compared",tixyarealist,'::',ixyarealist,"::",tixyarealist[1]-((len(ixyarealist[0])-len(tixyarealist[0]))*sum([rect[x[0]][0]*rect[x[0]][1] for x in tixyarealist[0]])/10 if len(tixyarealist[0])<len(ixyarealist[0]) else 0),'::',ixyarealist[1]-((len(tixyarealist[0])-len(ixyarealist[0]))*sum([rect[x[0]][0]*rect[x[0]][1] for x in ixyarealist[0]])/10 if len(ixyarealist[0])<len(tixyarealist[0]) else 0))

    if not ixyarealist:
     ixyarealist=tixyarealist
#    elif tixyarealist[1]<ixyarealist[1]:
    elif tixyarealist[1]-((len(ixyarealist[0])-len(tixyarealist[0]))*sum([rect[x[0]][0]*rect[x[0]][1] for x in tixyarealist[0]])*factor if len(tixyarealist[0])<len(ixyarealist[0]) else 0) < ixyarealist[1]-((len(tixyarealist[0])-len(ixyarealist[0]))*sum([rect[x[0]][0]*rect[x[0]][1] for x in ixyarealist[0]])*factor if len(ixyarealist[0])<len(tixyarealist[0]) else 0):
     ixyarealist=tixyarealist
#    print("new ixyarealist",ixyarealist)
  else:
    return False
 # print(delim,"returning i,ixyarealist",i,ixyarealist)
  return ixyarealist
 rectposition=getrect(0,0,width,height,factor)
 if not rectposition:
  return []
# print('rectposition',rectposition)
 xoffset,yoffset=int((width-max([x[1]+rect[x[0]][0] for x in rectposition[0]]))/(max([x[3] for x in rectposition[0]])+2)),int((height-max([x[2]+rect[x[0]][1] for x in rectposition[0]]))/(max([x[4] for x in rectposition[0]])+2))
# print('xoffset,yoffset',xoffset,yoffset)
# return [("<div style=\"position:absolute;left:"+str(x[1]+x[3]*xoffset)+"px;top:"+str(x[2]+x[4]*yoffset)+"px;\">"+db.get('adsense','value','id',idrect[x[0]][0])[0][0]+"</div>") for x in rectposition[0]]
# return [("<div style=\"width:"+str(rect[x[0]][0])+"px;height:"+str(rect[x[0]][1])+"px;position:absolute;left:"+str(x[1]+int(int((x[3]+1)*xoffset)))+"px;top:"+str(x[2]+int((x[4]+1)*yoffset))+"px;\">"+adsensecode[x[0]][0]+"</div>") for x in rectposition[0]]
 return [re.sub(r'style="',"style=\"position:absolute;left:"+str(x[1]+int(int((x[3]+1)*xoffset)))+"px;top:"+str(x[2]+int((x[4]+1)*yoffset))+"px;",adsensecode[x[0]][0]) for x in rectposition[0]]

def youtubeimage(youtubeid):
 print('><youtubeimage:',youtubeid,':')
 if gets(r'http://www.minhinc.com/image/'+youtubeid+r'.png',head=True).ok:
  print('image ',youtubeid,r'.png available at /image')
  img=Image.open(gets(r'https://img.youtube.com/vi/'+youtubeid+r'/0.jpg',get=True,stream=True))
 else:
  with Image.open(gets(r'https://img.youtube.com/vi/'+youtubeid+r'/0.jpg',get=True,stream=True)) as img:
   with Image.open(gets(r'http://www.minhinc.com/image/youtubebutton.png',get=True,stream=True)) as youtubebuttonimg:
    img.paste(youtubebuttonimg,(int((img.width-youtubebuttonimg.width)/2),int((img.height-youtubebuttonimg.height)/2)),youtubebuttonimg)
    img.save(youtubeid+".png")
    print('image ',youtubeid,r'.png not available at /image uploading...')
    os.system(r'~/tmp/ftp.sh -f put image ./'+youtubeid+'.png')
 print('imagewidth',img.size)
 return (r'http://www.minhinc.com/image/'+youtubeid+'.png',img.size)
