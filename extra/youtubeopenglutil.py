import math
import numpy as np
import re

class equation:
# def ellipse(self,angle,duration,rx,ry,precision=0.1):
 def ellipse(self,angle,duration,rx,ry,precision=0.1):
#  data=[(math.cos(i*math.pi/180),math.sin(i*math.pi/180)) for i in np.arange(360,0,-(360*precision)/duration)]
  data=[(math.cos(i*math.pi/180),-math.sin(i*math.pi/180)) for i in np.arange(angle[0],angle[1],(precision*(angle[1]-angle[0]))/duration)]
  data=[(round(rx*i[0],3),round(ry*i[1],3)) for i in data]
#  data=data[(len(data)*angle[0])//360:(len(data)*angle[1])//360] if angle else data
  print(f'equation.ellipse {len(data)=} {data=}')
  return data

 def affixtimestamp(self,begintime,data,precision=0.1):
  return [(timebegin+count*precision,*i) for count,i in enumerate(data)]

def getcoord(*,begintime=None,duration=None,attribtuple=None):
 if not hasattr(getcoord,'timespan'):
  setattr(getcoord,'timespan',0)
  setattr(getcoord,'equation',equation())
 global file
 attribtuple=(attribtuple,) if not type(attribtuple)==tuple and not type(attribtuple)==list else attribtuple

 print(f'TEST {attribtuple=} {begintime=} {duration=}')
 for i in attribtuple[:]:
  if type(i['id'])==tuple or type(i['id'])==list:
   print(f'TEST1 {attribtuple=}\n{i=}')
   for j in i['id'][1:]:
    attribtuple.append(i.copy())
    attribtuple[-1]['id']=j
   i['id']=i['id'][0]
 print(f'TEST2 {attribtuple=}')

 precision=0.1
 lastkey=None
 begintime=getcoord.timespan+float(re.sub('^[+]','',begintime)) if type(begintime)==str else begintime
 getcoord.timespan=begintime+duration
 for i in attribtuple:
  if not 'begintime' in i and begintime:
   i['begintime']=begintime
  elif type(i['begintime'])==str:
   i['begintime']=begintime+float(re.sub('^[+]','',i['begintime']))
  if not 'duration' in i and duration:
   i['duration']=duration
  if 'equation' in i and 'angle' in i:
   i['duration']=(i['duration'] if 'duration' in i else duration)*(360/i['angle'])
 begintime=min(x['begintime'] for x in attribtuple)
 duration=max(x['begintime']+x['duration'] for x in attribtuple)-begintime
  
 for i in range(int(duration/precision)):
  currenttime=begintime+i*precision
  for j in attribtuple:
   if j['begintime']<=currenttime<j['begintime']+j['duration']:
#    file.write(f"\n{round(begintime+i*precision,5)} {j['id']} {j['key'][0]}") if lastkey!=j['key'][0] and j['key'][0]!='s' else None
#    file.write(f"\n{round(begintime+i*precision,5)} {j['id']} {j['key'][0] if j['key'][0] != 's' else 'g'}") if lastkey!=j['key'][0] else None
    file.write(f"\n{round(begintime+i*precision,5)} {j['id']} {j['key'][0] if j['key'][0] != 's' else 'G'}") if lastkey!=j['key'][0] else None
    lastkey=j['key'][0]
    if not 'equation' in j and 'angle' in j:
     file.write(f"\n{round(begintime+i*precision,5)} {j['id']} {list(((j['angle']*precision)/j['duration'],*j['key'][1]))}")
    elif 'equation' in j:
     if currenttime==j['begintime']:
      j['data']=getcoord.equation.ellipse(*j['equation'])
      j['count']=0
     else:
      j['count']+=1
     file.write(f"\n{round(begintime+i*precision,5)} {j['id']} [f,{j['data'][j['count']][0]},0,{j['data'][j['count']][1]}]") if j['count']<len(j['data']) else None
    elif len(j['key'])==2:
#     print(f'{j=}')
     fraction=round(math.pow(j['key'][1],precision/j['duration']),5)
     file.write(f"\n{round(begintime+i*precision,5)} {j['id']} [s,{fraction},{fraction},{fraction}]")
    else:
     file.write(f"\n{round(begintime+i*precision,5)} {j['id']} {[(j['key'][2][count]-j['key'][1][count])/(j['duration']/precision) for count in range(3)]}")
    if 'image' in j and j['begintime']+j['image'][0][0]<=currenttime:
     file.write(f"\n{round(begintime+i*precision,5)} {j['id']} texture_{j['image'][0][1]}")
     j['image'][0:1]=[]
file=open('t2.txt','w')

'''
file.write(f'\n1 1 g')
file.write(f'\n1 27 C')
[file.write(f'\n{i*0.1} 1 N') for i in range(280)]
getcoord(begintime=29,duration=10,attribtuple=({'id':1,'angle':20,'key':['g',(1,0,0)]}))
[file.write(f'\n{getcoord.timespan+2} {i} C') for i in (8,9,10,11,12,13,15,17,19,25,27)]
#file.write(f'\n{getcoord.timespan+2} 25 C')
file.write(f'\n{getcoord.timespan+2} 27 [f,0,0.5,2]')
file.write(f'\n{getcoord.timespan+2} 27 G')
file.write(f'\n{getcoord.timespan+2} 28 [s,4,4,4]')
file.write(f'\n{getcoord.timespan+2} 29 [s,4,4,4]')
getcoord(begintime='+3',duration=10,attribtuple=({'id':28,'angle':720,'key':['G',(0,1,0)]},{'id':28,'key':['s',2]},{'id':29,'key':['s',2]}))
getcoord(begintime='+2',duration=10,attribtuple=({'id':28,'angle':720,'key':['G',(0,1,0)]},{'id':28,'angle':119,'key':['g',(0,0,1)]}))
getcoord(begintime='+2',duration=10,attribtuple=({'id':27,'key':['g',(0,0,0),(0,-0.5,-2)]},{'id':28,'key':['g',(0,0,0),(-12,0,0)]},{'id':28,'key':['s',0.2]},{'id':29,'key':['s',0.2]}))
[file.write(f'\n{getcoord.timespan+2} {i} C') for i in (8,9,10,11,12,13,15,17,19,23,24,25)]
#getcoord(begintime='+4',duration=15,attribtuple=({'id':25,'duration':10,'angle':17,'key':['g',(0,0,1)]},{'id':12,'duration':10,'angle':17,'key':['g',(0,0,1)]},{'id':26,'equation':1,'angle':90,'key':['g']},{'id':26,'angle':360*10/4,'key':['G',(0,1,0)]},{'id':13,'angle':360*4/4,'key':['g',(0,1,0)]},{'id':13,'angle':360*0.5/4,'key':['G',(0,1,0)]},{'id':15,'angle':360*0.7/4,'key':['g',(0,1,0)]},{'id':17,'angle':360*40/4,'key':['G',(0,1,0)]},{'id':17,'angle':360/4,'key':['g',(0,1,0)]},{'id':21,'angle':360*30/4,'key':['G',(0,1,0)]},{'id':21,'angle':360*0.5/4,'key':['g',(0,1,0)]},{'id':23,'angle':360*40*2/4,'key':['G',(0,1,0)]},{'id':23,'angle':360/(12*4),'key':['g',(0,1,0)]}))
getcoord(begintime='+4',duration=15,attribtuple=({'id':1,'begintime':'+10','duration':5,'key':['g',(3,1.0,-25),(0,0,0)]},{'id':27,'duration':10,'angle':17,'key':['g',(0,0,1)]},{'id':12,'duration':10,'angle':17,'key':['g',(0,0,1)]},{'id':28,'equation':1,'angle':90,'key':['g']},{'id':28,'angle':360*10/4,'key':['G',(0,1,0)]},{'id':13,'angle':360*4/4,'key':['g',(0,1,0)]},{'id':13,'angle':360*0.5/4,'key':['G',(0,1,0)]},{'id':15,'angle':360*0.7/4,'key':['g',(0,1,0)]},{'id':17,'angle':360*40/4,'key':['G',(0,1,0)]},{'id':17,'angle':360/4,'key':['g',(0,1,0)]},{'id':21,'angle':360*30/4,'key':['G',(0,1,0)]},{'id':21,'angle':360*0.5/4,'key':['g',(0,1,0)]},{'id':25,'angle':360*40*2/4,'key':['G',(0,1,0)]},{'id':25,'angle':360/(12*4),'key':['g',(0,1,0)]}))
[file.write(f'\n{getcoord.timespan+2} {i} C') for i in (8,9,10,11,12,13,15,17,20,23,24,25,27)]
getcoord(begintime='+4',duration=15,attribtuple=({'id':19,'duration':5,'key':['g',(-1.3,0,0),(0,0,0)]},{'id':21,'begintime':'+5','duration':10,'key':['s',4]},{'id':21,'begintime':'+5','duration':10,'angle':360,'key':['G',(0,1,0)]},{'id':22,'key':['s',4]},{'id':23,'key':['s',4]},{'id':24,'key':['s',4]},{'id':23,'angle':360*4,'key':['G',(0,1,0)]},{'id':24,'angle':360*0.8,'key':['G',(0,1,0)]}))
'''
'''
file.write(f'\n1 1 g')
#file.write(f'\n1 18 [f,4,0,0]')
#file.write(f'\n1 26 [f,10,0,0]')
#[file.write(f'\n1 {i} C') for i in (18,26)]
[file.write(f'\n{i*0.1} 1 N') for i in range(260)]
getcoord(begintime=29,duration=10,attribtuple=({'id':1,'angle':20,'key':['g',(1,0,0)]},{'id':1,'key':['g',(0,0,0),(-13,0,0)]}))
[file.write(f'\n{getcoord.timespan+1} {i} c') for i in (18,26)]
getcoord(begintime='+2',duration=50,attribtuple=({'id':18,'duration':4,'key':['g',(0,0,0),(11.3,0,0)]},{'id':18,'begintime':'+6','duration':4,'key':['s',3]},{'id':19,'begintime':'+6','duration':4,'key':['s',3]},{'id':18,'begintime':'+11','duration':15,'angle':23,'key':['g',(0,0,1)]},{'id':18,'begintime':'+28','duration':12,'angle':360*2,'key':['G',(0,1,0)]},{'id':18,'begintime':'+28','duration':12,'angle':360*2,'key':['G',(0,1,0)]},{'id':18,'begintime':'+42','duration':8,'key':['g',(11.3,0,0),(0,0,0)]},{'id':18,'begintime':'+42','duration':8,'key':['s',0.3]},{'id':19,'begintime':'+42','duration':8,'key':['s',0.3]},{'id':26,'duration':4,'key':['g',(0,0,0),(12.3,0,0)]},{'id':26,'begintime':'+6','duration':4,'key':['s',3]},{'id':27,'begintime':'+6','duration':4,'key':['s',3]},{'id':26,'begintime':'+11','duration':15,'angle':98,'key':['g',(0,0,1)]},{'id':26,'begintime':'+28','duration':12,'angle':360*2*4/3,'key':['G',(0,1,0)]},{'id':26,'begintime':'+42','duration':8,'key':['g',(12.3,0,0),(0,0,0)]},{'id':26,'begintime':'+42','duration':8,'key':['s',0.3]},{'id':27,'begintime':'+42','duration':8,'key':['s',0.3]}))
file.write(f'\n{getcoord.timespan+2} 29 [118,0,0,1]')
getcoord(begintime='+2',duration=60,attribtuple=({'id':1,'duration':10,'key':['g',(-13,0,0),(0,0,0)]},{'id':14,'angle':360*365/16,'key':['G',(0,1,0)]},{'id':14,'angle':360*4,'key':['g',(0,1,0)]},{'id':16,'angle':360*1.6,'key':['g',(0,1,0)]},{'id':16,'angle':-360*1.2,'key':['G',(0,1,0)]},{'id':18,'angle':360*365/4,'key':['G',(0,1,0)]},{'id':18,'angle':360,'key':['g',(0,1,0)]},{'id':22,'angle':360*365/6,'key':['G',(0,1,0)]},{'id':22,'angle':360*0.5,'key':['g',(0,1,0)]},{'id':24,'angle':360*30/4,'key':['G',(0,1,0)]},{'id':24,'angle':360*0.5/4,'key':['g',(0,1,0)]},{'id':29,'angle':360*40*2/4,'key':['G',(0,1,0)]},{'id':29,'angle':360/(12*4),'key':['g',(0,1,0)]},{'id':26,'angle':360*365*2/4,'key':['G',(0,1,0)]},{'id':26,'angle':360/10,'key':['g',(0,1,0)]},{'id':29,'equation':[12,7.2],'angle':90,'key':['g']},{'id':13,'angle':17,'duration':10,'key':['g',(0,0,1)]},{'id':28,'angle':17,'duration':10,'key':['g',(0,0,1)]}))

file.write(f'\n1 1 g')
file.write(f'\n1 9 [f,6,0,0]')
[file.write(f'\n{i*0.1} 1 N') for i in range(140)]
getcoord(begintime=16,duration=5,attribtuple=({'id':1,'duration':5,'angle':30,'key':['g',(1,0,0)]}))
getcoord(begintime="+2",duration=5,attribtuple=({'id':1,'key':['g',(0,0,0),(-8,0,0)]},{'id':9,'key':['g',(0,0,0),(3,0,0)]}))
file.write(f'\n{getcoord.timespan+1} 9 c')
getcoord(begintime="+4",duration=20,attribtuple=({'id':9,'angle':360*4,'key':['G',(0,1,0)]},{'id':9,'begintime':'+10','duration':5,'angle':23,'key':['g',(0,0,1)]}))
getcoord(begintime="+2",duration=5,attribtuple=({'id':1,'key':['g',(-8,0,0),(0,0,0)]},{'id':9,'key':['g',(3,0,0),(0,0,0)]}))
file.write(f'\n{getcoord.timespan+1} 9 c')
getcoord(begintime="+2",duration=120,attribtuple=({'id':9,'equation':[None,120,6,6],'key':['g']},{'id':9,'angle':360*4,'key':['G',(0,1,0)]}))
getcoord(begintime="+0",duration=120,attribtuple=({'id':9,'equation':[None,120,6,6],'key':['g']},{'id':9,'angle':360*4,'key':['G',(0,1,0)]}))
file.write(f'\n1 1 g')
[file.write(f'\n{i*0.1} 1 N') for i in range(370)]
getcoord(begintime=34,duration=5,attribtuple=({'id':1,'duration':5,'angle':30,'key':['g',(1,0,0)]}))
#getcoord(begintime='+2',duration=60,attribtuple=({'id':1,'begintime':'+5','duration':5,'key':['g',(10,0,30),(0,0,0)]},{'id':14,'angle':360*6,'key':['g',(0,1,0)]},{'id':16,'angle':360*1.6,'key':['g',(0,1,0)]},{'id':18,'angle':360*12,'key':['G',(0,1,0)]},{'id':18,'angle':360,'key':['g',(0,1,0)]},{'id':22,'angle':360*11,'key':['G',(0,1,0)]},{'id':22,'angle':360*0.5,'key':['g',(0,1,0)]},{'id':24,'angle':360*24,'key':['G',(0,1,0)]},{'id':24,'angle':360/12,'key':['g',(0,1,0)]},{'id':26,'angle':360*24,'key':['G',(0,1,0)]},{'id':26,'angle':360/14,'key':['g',(0,1,0)]},{'id':28,'equation':[(60*10,5),14,14],'key':['g']},{'id':28,'duration':5,'angle':360*4,'key':['G',(0,1,0)]},{'id':28,'begintime':'+5','duration':5,'key':['g',(0,0,0),(10,0,0)]},{'id':28,'begintime':'+5','duration':5,'key':['s',4]},{'id':29,'begintime':'+5','duration':5,'key':['s',4]},{'id':28,'begintime':'+5','duration':5,'angle':-28,'key':['G',(0,0,1)]}))
#getcoord(begintime='+2',duration=60,attribtuple=({'id':1,'begintime':'+5','duration':5,'key':['g',(10,0,30),(0,0,0)]},{'id':1,'begintime':'+24','duration':5,'key':['g',(0,0,0),(10,0,30)]},{'id':14,'angle':360*6,'key':['g',(0,1,0)]},{'id':16,'angle':360*1.6,'key':['g',(0,1,0)]},{'id':18,'angle':360*12,'key':['G',(0,1,0)]},{'id':18,'angle':360,'key':['g',(0,1,0)]},{'id':22,'angle':360*11,'key':['G',(0,1,0)]},{'id':22,'angle':360*0.5,'key':['g',(0,1,0)]},{'id':24,'angle':360*24,'key':['G',(0,1,0)]},{'id':24,'angle':360/12,'key':['g',(0,1,0)]},{'id':26,'angle':360*24,'key':['G',(0,1,0)]},{'id':26,'angle':360/14,'key':['g',(0,1,0)]},{'id':28,'equation':[(60*10,5),14,14],'key':['g']},{'id':28,'angle':360*4,'key':['G',(0,1,0)]},{'id':28,'begintime':'+5','duration':5,'key':['g',(0,0,0),(4,0,0)]},{'id':28,'begintime':'+5','duration':5,'key':['s',4]},{'id':29,'begintime':'+5','duration':5,'key':['s',4]},{'id':28,'begintime':'+5','duration':5,'angle':-28,'key':['g',(0,0,1)]},{'id':28,'begintime':'+5','duration':5,'angle':-30,'key':['g',(1,0,0)]},{'id':28,'begintime':'+12','duration':10,'angle':30,'key':['g',(0,0,1)]},{'id':28,'begintime':'+24','duration':5,'key':['g',(4,0,0),(0,0,0)]},{'id':28,'begintime':'+24','duration':5,'key':['s',0.25]},{'id':29,'begintime':'+24','duration':5,'key':['s',0.25]},{'id':28,'begintime':'+29','duration':31,'equation':[(60*10,31),14,14],'key':['g']}))
getcoord(begintime='+2',duration=60,attribtuple=({'id':1,'begintime':'+5','duration':5,'key':['g',(10,0,30),(0,0,0)]},{'id':1,'begintime':'+24','duration':5,'key':['g',(0,0,0),(10,0,30)]},{'id':14,'angle':360*6,'key':['g',(0,1,0)]},{'id':16,'angle':360*1.6,'key':['g',(0,1,0)]},{'id':18,'angle':360*12,'key':['G',(0,1,0)]},{'id':18,'angle':360,'key':['g',(0,1,0)]},{'id':22,'angle':360*11,'key':['G',(0,1,0)]},{'id':22,'angle':360*0.5,'key':['g',(0,1,0)]},{'id':24,'angle':360*24,'key':['G',(0,1,0)]},{'id':24,'angle':360/12,'key':['g',(0,1,0)]},{'id':26,'angle':360*24,'key':['G',(0,1,0)]},{'id':26,'angle':360/14,'key':['g',(0,1,0)]},{'id':28,'duration':5,'equation':[(0,(360*5)/(10)),5,14,14],'key':['g']},{'id':28,'angle':360*4,'key':['G',(0,1,0)]},{'id':28,'begintime':'+5','duration':5,'key':['g',(0,0,0),(4,0,0)]},{'id':28,'begintime':'+5','duration':5,'key':['s',4]},{'id':29,'begintime':'+5','duration':5,'key':['s',4]},{'id':28,'begintime':'+5','duration':5,'angle':-28,'key':['g',(0,0,1)]},{'id':28,'begintime':'+5','duration':5,'angle':-30,'key':['g',(1,0,0)]},{'id':28,'begintime':'+12','duration':10,'angle':30,'key':['g',(0,0,1)]},{'id':28,'begintime':'+24','duration':5,'key':['g',(4,0,0),(0,0,0)]},{'id':28,'begintime':'+24','duration':5,'key':['s',0.25]},{'id':29,'begintime':'+24','duration':5,'key':['s',0.25]},{'id':28,'begintime':'+29','duration':31,'equation':[(180,180+(360*31)/(60*2)),31,14,14],'key':['g']}))

file.write(f'\n1 1 g')
file.write(f'\n1 35 [118,0,0,1]')
[file.write(f'\n{i*0.1} 1 [0,0,-1]') for i in range(44)]
getcoord(begintime=8,duration=5,attribtuple=({'id':1,'duration':5,'angle':20,'key':['g',(1,0,0)]}))
getcoord(begintime='+2',duration=60,attribtuple=({'id':16,'angle':360*2,'key':['G',(0,1,0)]},{'id':16,'angle':360*5,'key':['g',(0,1,0)]},{'id':18,'angle':-360*1.2,'key':['G',(0,1,0)]},{'id':18,'angle':360*1.2,'key':['g',(0,1,0)]},{'id':20,'angle':360*10,'key':['G',(0,1,0)]},{'id':20,'angle':360,'key':['g',(0,1,0)]},{'id':24,'angle':360*9,'key':['G',(0,1,0)]},{'id':24,'angle':360*0.5,'key':['g',(0,1,0)]},{'id':26,'angle':360*20,'key':['G',(0,1,0)]},{'id':26,'angle':360/3,'key':['g',(0,1,0)]},{'id':28,'angle':360*24,'key':['G',(0,1,0)]},{'id':28,'angle':360/3.5,'key':['g',(0,1,0)]},{'id':30,'angle':360*20,'key':['G',(0,1,0)]},{'id':30,'angle':360/4,'key':['g',(0,1,0)]},{'id':32,'angle':360*20,'key':['G',(0,1,0)]},{'id':32,'angle':360/5,'key':['g',(0,1,0)]},{'id':35,'equation':[(0,180),60,16,12.8],'key':['g']},{'id':34,'angle':17,'duration':5,'key':['g',(0,0,1)]},{'id':15,'duration':5,'angle':17,'key':['g',(0,0,1)]}))
getcoord(begintime='+0',duration=60,attribtuple=({'id':1,'angle':360,'duration':60,'key':['g',(0,1,0)]},{'id':16,'angle':360*2,'key':['G',(0,1,0)]},{'id':16,'angle':360*5,'key':['g',(0,1,0)]},{'id':18,'angle':-360*1.2,'key':['G',(0,1,0)]},{'id':18,'angle':360*1.2,'key':['g',(0,1,0)]},{'id':20,'angle':360*10,'key':['G',(0,1,0)]},{'id':20,'angle':360,'key':['g',(0,1,0)]},{'id':24,'angle':360*9,'key':['G',(0,1,0)]},{'id':24,'angle':360*0.5,'key':['g',(0,1,0)]},{'id':26,'angle':360*20,'key':['G',(0,1,0)]},{'id':26,'angle':360/3,'key':['g',(0,1,0)]},{'id':28,'angle':360*24,'key':['G',(0,1,0)]},{'id':28,'angle':360/3.5,'key':['g',(0,1,0)]},{'id':30,'angle':360*20,'key':['G',(0,1,0)]},{'id':30,'angle':360/4,'key':['g',(0,1,0)]},{'id':32,'angle':360*20,'key':['G',(0,1,0)]},{'id':32,'angle':360/5,'key':['g',(0,1,0)]},{'id':35,'equation':[(180,360),60,16,12.8],'key':['g']}))
file.write(f'\n1 12 c')
file.write(f'\n1 16 c')
[file.write(f'\n{i*0.1} 1 [0,0,-1]') for i in range(30)]
#getcoord(begintime=5,duration=10,attribtuple=({'id':1,'duration':5,'angle':20,'key':['g',(1,0,0)]},{'id':10,'angle':-360*1.2,'key':['G',(0,1,0)]},{'id':10,'angle':360*1.2,'key':['g',(0,1,0)]},{'id':16,'equation':[(0,360*12),10,2,2],'key':['g']},{'id':12,'angle':360*30,'key':['G',(0,1,0)]},{'id':12,'equation':[(0,360),10,8,8],'key':['g']},{'id':19,'angle':360*9,'key':['G',(0,1,0)]},{'id':19,'angle':360*0.5,'key':['g',(0,1,0)]}))
getcoord(begintime=5,duration=60,attribtuple=({'id':1,'duration':5,'angle':20,'key':['g',(1,0,0)]},{'id':10,'angle':-360*1.2,'key':['G',(0,1,0)]},{'id':10,'angle':360*1.2,'key':['g',(0,1,0)]},{'id':16,'angle':360*12,'key':['g',(0,1,0)]},{'id':12,'angle':360*30,'key':['G',(0,1,0)]},{'id':12,'equation':[(0,360),60,8,8],'key':['g']},{'id':19,'angle':360*9,'key':['G',(0,1,0)]},{'id':19,'angle':360*0.5,'key':['g',(0,1,0)]}))
#getcoord(begintime="+0",duration=2,attribtuple=({'id':16,'equation':[(0,360*12),60,2,2],'key':['g']},{'id':12,'angle':360*30/30,'key':['G',(0,1,0)]}))
#getcoord(begintime="+0",duration=2,attribtuple=({'id':16,'angle':360*12/30,'key':['g',(0,1,0)]},{'id':12,'angle':360*30/30,'key':['G',(0,1,0)]}))
#getcoord(begintime="+0",duration=60,attribtuple=({'id':1,'duration':5,'key':['g',(0,0,0),(-8,0,20)]},{'id':16,'duration':20,'equation':[(0,360*12),60,2,2],'key':['g']},{'id':12,'duration':20,'angle':360*30,'key':['G',(0,1,0)]},{'id':12,'begintime':'+10','duration':10,'angle':-23,'key':['g',(0,0,1)]},{'id':14,'begintime':'+20','duration':4,'key':['s',2]},{'id':12,'begintime':'+20','duration':4,'key':['s',2]},{'id':13,'begintime':'+20','duration':4,'key':['s',2]},{'id':16,'begintime':'+25','duration':35,'equation':[(0,180),35,2,2],'key':['g']},{'id':12,'begintime':'+25','duration':35,'angle':270,'key':['G',(0,1,0)]}))
file.write(f'\n{getcoord.timespan+1} 12 c')
file.write(f'\n{getcoord.timespan+1} 16 c')
getcoord(begintime="+0",duration=50,attribtuple=({'id':1,'duration':5,'key':['g',(0,0,0),(-8,0,20)]},{'id':16,'duration':20,'angle':360*12/3,'key':['g',(0,1,0)]},{'id':12,'duration':20,'angle':360*30/3,'key':['G',(0,1,0)]},{'id':12,'begintime':'+10','duration':10,'angle':-23,'key':['g',(0,0,1)]},{'id':14,'begintime':'+20','duration':4,'key':['s',2]},{'id':12,'begintime':'+20','duration':4,'key':['s',2]},{'id':13,'begintime':'+20','duration':4,'key':['s',2]},{'id':16,'begintime':'+25','duration':25,'angle':195,'key':['g',(0,1,0)]},{'id':12,'begintime':'+25','duration':25,'angle':270,'key':['G',(0,1,0)]}))
#getcoord(begintime="+2",duration=5,attribtuple=({'id':1,'angle':-90,'key':['g',(0,1,0)]}))
getcoord(begintime="+2",duration=10,attribtuple=({'id':1,'duration':5,'key':['g',(-8,0,20),(0,0,0)]},{'id':1,'begintime':'+5','duration':5,'angle':-70,'key':['g',(0,1,0)]},{'id':1,'duration':5,'angle':-10,'key':['g',(1,0,0)]}))
getcoord(begintime="+2",duration=10,attribtuple=({'id':1,'key':['g',(0,0,0),(0,0,20)]}))
getcoord(begintime="+20",duration=10,attribtuple=({'id':1,'begintime':'+5','duration':5,'angle':-230,'key':['g',(0,1,0)]}))

file.write(f'\n1 1 g')
file.write(f'\n1 12 c')
file.write(f'\n1 17 c')
[file.write(f'\n{i*0.1} 1 [0,0,-1]') for i in range(30)]
getcoord(begintime=5,duration=10,attribtuple=({'id':1,'duration':5,'angle':20,'key':['g',(1,0,0)]},{'id':10,'angle':-360*1.2,'key':['G',(0,1,0)]},{'id':10,'angle':360*1.2,'key':['g',(0,1,0)]},{'id':17,'angle':360*12,'key':['g',(0,1,0)]},{'id':12,'angle':360*30,'key':['G',(0,1,0)]},{'id':12,'equation':[(0,360),10,8,8],'key':['g']},{'id':19,'angle':360*9,'key':['G',(0,1,0)]},{'id':19,'angle':360*0.5,'key':['g',(0,1,0)]}))
file.write(f'\n{getcoord.timespan+1} 12 c')
file.write(f'\n{getcoord.timespan+1} 17 c')
getcoord(begintime="+0",duration=60,attribtuple=({'id':1,'duration':5,'key':['g',(0,0,0),(-8,0,20)]},{'id':17,'duration':20,'angle':360*12/3,'key':['g',(0,1,0)]},{'id':12,'duration':20,'angle':360*30/3,'key':['G',(0,1,0)]},{'id':12,'begintime':'+10','duration':10,'angle':-23,'key':['g',(0,0,1)]},{'id':15,'begintime':'+20','duration':4,'key':['s',2]},{'id':12,'begintime':'+20','duration':4,'key':['s',2]},{'id':13,'begintime':'+20','duration':4,'key':['s',2]},{'id':17,'begintime':'+25','duration':25,'angle':180,'key':['g',(0,1,0)]},{'id':17,'begintime':'+55','duration':5,'angle':180/14,'key':['g',(0,1,0)]}))
getcoord(begintime="+10",duration=15,attribtuple=({'id':1,'duration':5,'key':['g',(-8,0,20),(0,0,0)]},{'id':1,'begintime':'+2','duration':5,'angle':-70,'key':['g',(0,1,0)]},{'id':1,'begintime':'+10','duration':5,'angle':-20,'key':['G',(1,0,0)]}))
getcoord(begintime="+0",duration=40,attribtuple=({'id':1,'begintime':'+5','duration':5,'angle':-15,'key':['g',(0,1,0)]},{'id':1,'begintime':'+20','duration':10,'angle':-90,'key':['g',(0,0,1)]},{'id':12,'begintime':'+35','duration':5,'key':['s',0.1]},{'id':13,'begintime':'+35','duration':5,'key':['s',0.1]}))
file.write(f'\n{getcoord.timespan} 8 C')
file.write(f'\n{getcoord.timespan} 9 C')
file.write(f'\n{getcoord.timespan} 16 C')
file.write(f'\n{getcoord.timespan} 19 C')
getcoord(begintime='+5',duration=60,attribtuple=({'id':1,'duration':5,'angle':-20,'key':['g',(1,0,0)]},{'id':1,'begintime':'+10','duration':10,'key':['g',(0,0,0),(0,0,20)]},{'id':1,'begintime':'+30','duration':10,'angle':180,'key':['g',(0,1,0)]},{'id':12,'begintime':'+55','duration':5,'key':['s',10]},{'id':13,'begintime':'+55','duration':5,'key':['s',10]}))
#getcoord(begintime="+1",duration=60,attribtuple=({'id':1,'begintime':'+10','duration':5,'angle':-30,'key':['g',(0,1,0)]},{'id':1,'duration':5,'angle':10,'key':['g',(1,0,0)]},{'id':1,'begintime':'+20','duration':10,'angle':-90,'key':['g',(0,0,1)]}))#,{'id':1,'duration':10,'begintime':'+30','key':['g',(0,0,0),(0,0,-25)]},{'id':17,'begintime':'+40','duration':5,'key':['s',3]}))


file.write(f'\n1 1 g')
file.write(f'\n1 12 c')
file.write(f'\n1 17 c')
[file.write(f'\n{i*0.1} 1 [0,0,-1]') for i in range(30)]
getcoord(begintime=5,duration=10,attribtuple=({'id':1,'duration':5,'angle':20,'key':['g',(1,0,0)]},{'id':10,'angle':-360*1.2,'key':['G',(0,1,0)]},{'id':10,'angle':360*1.2,'key':['g',(0,1,0)]},{'id':17,'angle':360*12,'key':['g',(0,1,0)]},{'id':12,'angle':360*30,'key':['G',(0,1,0)]},{'id':12,'equation':[(0,360),10,8,8],'key':['g']},{'id':19,'angle':360*9,'key':['G',(0,1,0)]},{'id':19,'angle':360*0.5,'key':['g',(0,1,0)]}))
file.write(f'\n{getcoord.timespan+1} 12 c')
file.write(f'\n{getcoord.timespan+1} 17 c')
getcoord(begintime="+0",duration=40,attribtuple=({'id':1,'duration':5,'key':['g',(0,0,0),(-8,0,20)]},{'id':17,'duration':20,'angle':360*12/3,'key':['g',(0,1,0)]},{'id':12,'duration':20,'angle':360*30/3,'key':['G',(0,1,0)]},{'id':12,'begintime':'+10','duration':10,'angle':-23,'key':['g',(0,0,1)]},{'id':15,'begintime':'+20','duration':4,'key':['s',2]},{'id':12,'begintime':'+20','duration':4,'key':['s',2]},{'id':13,'begintime':'+20','duration':4,'key':['s',2]},{'id':17,'begintime':'+25','duration':15,'angle':180,'key':['g',(0,1,0)]}))
#getcoord(begintime="+1",duration=14+60,attribtuple=({'id':1,'duration':2,'key':['g',(-8,0,20),(0,0,0)]},{'id':1,'begintime':'+2','duration':2,'angle':-90,'key':['g',(0,1,0)]},{'id':1,'begintime':'+5','duration':2,'angle':-20,'key':['G',(1,0,0)]},{'id':1,'begintime':'+8','duration':2,'angle':20,'key':['g',(1,0,0)]},{'id':12,'begintime':'+11','duration':2,'key':['s',0.1]},{'id':13,'begintime':'+11','duration':2,'key':['s',0.1]},{'id':1,'begintime':'+13','duration':1,'angle':-90,'key':['g',(0,0,1)]},{'id':17,'begintime':'+14','duration':60,'angle':180,'key':['g',(0,1,0)]},{'id':1,'begintime':'+14','duration':60,'angle':-180,'key':['G',(0,1,0)]},{'id':1,'begintime':'+14','duration':60,'angle':90,'key':['g',(0,0,1)]})))#,{'id':1,'begintime':'+33','duration':2,'key':['g',(0,0,10),(0,0,0)]}))
getcoord(begintime="+1",duration=15,attribtuple=({'id':1,'duration':2,'key':['g',(-8,0,30),(0,0,0)]},{'id':1,'begintime':'+2','duration':2,'angle':-90,'key':['g',(0,1,0)]},{'id':1,'begintime':'+5','duration':2,'angle':-20,'key':['G',(1,0,0)]},{'id':12,'begintime':'+11','duration':2,'key':['s',0.2]},{'id':13,'begintime':'+11','duration':2,'key':['s',0.2]},{'id':15,'begintime':'+11','duration':2,'key':['s',2]},{'id':1,'begintime':'+13','duration':2,'angle':-90,'key':['g',(0,0,1)]}))
#file.write(f'\n{getcoord.timespan} 8 C')
#file.write(f'\n{getcoord.timespan} 9 C')
#file.write(f'\n{getcoord.timespan} 16 C')
file.write(f'\n{getcoord.timespan} 12 c')
file.write(f'\n{getcoord.timespan} 18 C')
getcoord(begintime="+10",duration=60,attribtuple=({'id':17,'angle':180,'key':['g',(0,1,0)]},{'id':1,'angle':-180,'key':['G',(0,1,0)]},{'id':1,'angle':90,'key':['g',(0,0,1)]},{'id':1,'begintime':'+30','duration':30,'angle':25,'key':['g',(1,0,0)]},{'id':1,'begintime':'+30','duration':30,'key':['g',(0,0,0),(0,0,10)]}))

file.write(f'\n1 1 g')
file.write(f'\n1 12 c')
file.write(f'\n1 17 c')
[file.write(f'\n{i*0.1} 1 [0,0,-1]') for i in range(30)]
getcoord(begintime=5,duration=10,attribtuple=({'id':1,'duration':5,'angle':20,'key':['g',(1,0,0)]},{'id':10,'angle':-360*1.2,'key':['G',(0,1,0)]},{'id':10,'angle':360*1.2,'key':['g',(0,1,0)]},{'id':17,'angle':360*12,'key':['g',(0,1,0)]},{'id':12,'angle':360*30,'key':['G',(0,1,0)]},{'id':12,'equation':[(0,360),10,8,8],'key':['g']},{'id':19,'angle':360*9,'key':['G',(0,1,0)]},{'id':19,'angle':360*0.5,'key':['g',(0,1,0)]}))
file.write(f'\n{getcoord.timespan+1} 12 c')
file.write(f'\n{getcoord.timespan+1} 17 c')
getcoord(begintime="+0",duration=60,attribtuple=({'id':1,'duration':5,'key':['g',(0,0,0),(-8,0,20)]},{'id':17,'duration':20,'angle':360*12/3,'key':['g',(0,1,0)]},{'id':12,'duration':20,'angle':360*30/3,'key':['G',(0,1,0)]},{'id':12,'begintime':'+10','duration':10,'angle':-23,'key':['g',(0,0,1)]},{'id':15,'begintime':'+20','duration':4,'key':['s',2]},{'id':12,'begintime':'+20','duration':4,'key':['s',2]},{'id':13,'begintime':'+20','duration':4,'key':['s',2]},{'id':17,'begintime':'+25','duration':15,'angle':360,'key':['g',(0,1,0)]},{'id':1,'begintime':'+40','duration':5,'angle':80,'key':['g',(0,1,0)]},{'id':1,'begintime':'+40','duration':5,'key':['g',(0,0,0),(4,0,0)]},{'id':12,'begintime':'+50','duration':4,'key':['s',0.2]},{'id':13,'begintime':'+50','duration':4,'key':['s',0.2]}))
getcoord(begintime="+0",duration=60,attribtuple=({'id':17,'angle':180,'key':['g',(0,1,0)]},{'id':1,'angle':-170,'key':['G',(0,1,0)]},{'id':1,'key':['g',(0,0,0),(0,0,-10)]},{'id':1,'angle':-5,'key':['G',(1,0,0)]},{'id':12,'key':['s',0.5]},{'id':13,'key':['s',0.5]},{'id':15,'duration':1,'key':['s',1.3]}))
file.write(f'\n{getcoord.timespan} 12 c')
getcoord(begintime="+5",duration=10,attribtuple=({'id':12,'key':['s',4]},{'id':13,'key':['s',4]},{'id':1,'angle':10,'key':['g',(0,1,0)]},{'id':1,'angle':15,'key':['g',(0,0,1)]},{'id':1,'angle':10,'key':['g',(1,0,0)]}))
'''

'''
[file.write(f'\n1 {x} C') for x in (9,11,13,15,17,19,21,23,25)]
file.write(f'\n2 1 g')
getcoord(begintime=2,duration=14,attribtuple=({'id':1,'duration':10,'key':['g',(0,0,0),(-10,0,-30)]},{'id':18,'begintime':'+11','duration':3,'angle':10,'key':['g',(1,0,0)]}))
getcoord(begintime='+4',duration=10,attribtuple=({'id':8,'key':['s',0.01*0.33]},{'id':10,'key':['s',0.01*0.9]},{'id':12,'key':['s',0.01]},{'id':14,'key':['s',0.01*0.5]},{'id':16,'key':['s',0.1]},{'id':18,'key':['s',0.09]},{'id':20,'key':['s',0.04]},{'id':22,'key':['s',0.04]},{'id':24,'key':['s',0.01*0.2]}))
getcoord(begintime='+2',duration=6,attribtuple=({'id':8,'key':['g',(0,0,0),(-1,0,0)]},{'id':10,'key':['g',(0,0,0),(-3,0,0)]},{'id':12,'key':['g',(0,0,0),(-5,0,0)]},{'id':14,'key':['g',(0,0,0),(-7,0,0)]},{'id':16,'key':['g',(0,0,0),(-9,0,0)]},{'id':18,'key':['g',(0,0,0),(-12.2,0,0)]},{'id':20,'key':['g',(0,0,0),(-15.5,0,0)]},{'id':22,'key':['g',(0,0,0),(-17.55,0,0)]},{'id':24,'key':['g',(0,0,0),(-19.6,0,0)]}))
getcoord(begintime='+2',duration=4,attribtuple=({'id':1,'key':['g',(0,0,0),(8.5,0,40)]}))
getcoord(begintime='+10',duration=4,attribtuple=({'id':1,'key':['g',(10.5,0,40),(0,0,0)]}))
getcoord(begintime='+2',duration=6,attribtuple=({'id':8,'key':['g',(-1.1,0,0),(0,0,0)]},{'id':10,'key':['g',(-3.2,0,0),(0,0,0)]},{'id':12,'key':['g',(-5.3,0,0),(0,0,0)]},{'id':14,'key':['g',(-7.4,0,0),(0,0,0)]},{'id':16,'key':['g',(-9.5,0,0),(0,0,0)]},{'id':18,'key':['g',(-12.8,0,0),(0,0,0)]},{'id':20,'key':['g',(-16.5,0,0),(0,0,0)]},{'id':22,'key':['g',(-18.95,0,0),(0,0,0)]},{'id':24,'key':['g',(-21.4,0,0),(0,0,0)]}))
getcoord(begintime='+4',duration=10,attribtuple=({'id':8,'key':['s',1/(0.01*0.33)]},{'id':10,'key':['s',1/(0.01*0.9)]},{'id':12,'key':['s',1/0.01]},{'id':14,'key':['s',1/(0.01*0.5)]},{'id':16,'key':['s',1/0.1]},{'id':18,'key':['s',1/0.09]},{'id':20,'key':['s',1/0.04]},{'id':22,'key':['s',1/0.04]},{'id':24,'key':['s',1/(0.01*0.2)]}))
[file.write(f'\n{getcoord.timespan+2} {x} C') for x in (9,11,13,15,17,19,21,23,25)]
getcoord(begintime='+5',duration=10,attribtuple=({'id':8,'duration':10,'angle':2,'key':['g',(0,0,1)]},{'id':8,'angle':360*5/60,'key':['G',(0,1,0)]},{'id':10,'duration':10,'angle':-3,'key':['g',(0,0,1)]},{'id':10,'angle':-360*5/243,'key':['G',(0,1,0)]},{'id':12,'duration':10,'angle':23,'key':['g',(0,0,1)]},{'id':12,'angle':360*5,'key':['G',(0,1,0)]},{'id':14,'duration':10,'angle':28,'key':['g',(0,0,1)]},{'id':14,'angle':360*5*(24/26),'key':['G',(0,1,0)]},{'id':16,'duration':10,'angle':3,'key':['g',(0,0,1)]},{'id':16,'angle':360*5*2,'key':['G',(0,1,0)]},{'id':18,'duration':10,'angle':27,'key':['g',(0,0,1)]},{'id':18,'angle':360*5*24/10,'key':['G',(0,1,0)]},{'id':20,'duration':10,'angle':98,'key':['g',(0,0,1)]},{'id':20,'angle':360*5*24/17,'key':['G',(0,1,0)]},{'id':22,'duration':10,'angle':28,'key':['g',(0,0,1)]},{'id':22,'angle':360*5*24/16,'key':['G',(0,1,0)]},{'id':24,'duration':10,'angle':119,'key':['g',(0,0,1)]},{'id':24,'angle':360*5*24/153,'key':['G',(0,1,0)]}))
[file.write(f'\n{getcoord.timespan+2} {x} C') for x in range(10,25+1) if not x in [12,13]]
getcoord(begintime='+5',duration=70,attribtuple=[{'id':8,'duration':1,'key':['g',(0,0,0),(6,0,0)]},{'id':8,'begintime':'+2','duration':1,'key':['g',(0,0,0),(0,-1,0)]},{'id':12,'duration':1,'key':['g',(0,0,0),(7,0,0)]},{'id':12,'begintime':'+2','duration':1,'key':['g',(0,0,0),(0,-1,0)]},{'id':(8,9),'begintime':'+8','duration':5,'key':['s',0.33]},{'id':(8,9),'begintime':'+18','duration':5,'key':['s',0.01]},{'id':(12,13),'begintime':'+18','duration':5,'key':['s',0.01]},{'id':8,'begintime':'+24','duration':2,'key':['g',(0,0,0),(-6.3,1,0)]},{'id':12,'begintime':'+24','duration':2,'key':['g',(0,0,0),(-11,1,0)]},{'id':1,'begintime':'+24','duration':2,'key':['g',(0,0,0),(10,0,40)]},{'id':1,'begintime':'+31','duration':2,'key':['g',(10,0,40),(0,0,0)]},{'id':8,'begintime':'+31','duration':2,'key':['g',(-6.3,1,0),(0,0,0)]},{'id':12,'begintime':'+31','duration':2,'key':['g',(-11,1,0),(0,0,0)]},{'id':(8,9),'begintime':'+38','duration':5,'key':['s',1/(0.01*0.33)]},{'id':(12,13),'begintime':'+38','duration':5,'key':['s',1/0.01]},{'id':8,'begintime':'+48','duration':22,'angle':360*5/10,'key':['G',(0,1,0)]},{'id':12,'begintime':'+48','duration':22,'angle':360*5,'key':['G',(0,1,0)]},{'id':8,'begintime':'+53','duration':1,'key':['g',(0,0,0),(0,1,0)]},{'id':12,'begintime':'+53','duration':1,'key':['g',(0,0,0),(0,1,0)]},{'id':8,'begintime':'+60','duration':1,'key':['g',(0,0,0),(2,0,0)]},{'id':12,'begintime':'+60','duration':1,'key':['g',(0,0,0),(6,0,0)]},{'id':8,'begintime':'+68','duration':1,'key':['g',(0,0,0),(-8,0,0)]},{'id':12,'begintime':'+68','duration':1,'key':['g',(0,0,0),(-13,0,0)]}])
[file.write(f'\n{getcoord.timespan} {x} C') for x in range(10,25+1) if not x in [12,13]]

[file.write(f'\n{getcoord.timespan} {x} C') for x in (9,11,13,15,17,19,21,23,25)]
[file.write(f'\n{getcoord.timespan} {x} c') for x in (8,10,12,14,16,18,20,22,24)]
getcoord(begintime='+0',duration=20,attribtuple=({'id':8,'duration':10,'angle':2,'key':['g',(0,0,1)]},{'id':8,'angle':360*5/60,'key':['G',(0,1,0)]},{'id':10,'duration':10,'angle':-3,'key':['g',(0,0,1)]},{'id':10,'angle':-360*5/243,'key':['G',(0,1,0)]},{'id':12,'duration':10,'angle':23,'key':['g',(0,0,1)]},{'id':12,'angle':360*5,'key':['G',(0,1,0)]},{'id':14,'duration':10,'angle':28,'key':['g',(0,0,1)]},{'id':14,'angle':360*5*(24/26),'key':['G',(0,1,0)]},{'id':16,'duration':10,'angle':3,'key':['g',(0,0,1)]},{'id':16,'angle':360*5*2,'key':['G',(0,1,0)]},{'id':18,'duration':10,'angle':27,'key':['g',(0,0,1)]},{'id':18,'angle':360*5*24/10,'key':['G',(0,1,0)]},{'id':20,'duration':10,'angle':98,'key':['g',(0,0,1)]},{'id':20,'angle':360*5*24/17,'key':['G',(0,1,0)]},{'id':22,'duration':10,'angle':28,'key':['g',(0,0,1)]},{'id':22,'angle':360*5*24/16,'key':['G',(0,1,0)]},{'id':24,'duration':10,'angle':119,'key':['g',(0,0,1)]},{'id':24,'angle':360*5*24/153,'key':['G',(0,1,0)]}))
[file.write(f'\n{getcoord.timespan+2} {x} C') for x in range(8,25+1) if not x in [10,11,12,13]]
getcoord(begintime='+5',duration=15,attribtuple=[{'id':10,'duration':1,'key':['g',(0,0,0),(5,0,0)]},{'id':12,'duration':1,'key':['g',(0,0,0),(12,0,0)]},{'id':1,'begintime':'+3','duration':3,'key':['g',(0,0,0),(3,0,0)]},{'id':10,'begintime':'+7','duration':1,'angle':3,'key':['g',(0,0,1)]},{'id':12,'begintime':'+7','duration':1,'angle':-23,'key':['g',(0,0,1)]},{'id':1,'begintime':'+11','duration':4,'angle':40,'key':['g',(0,1,0)]}])
[file.write(f'\n{getcoord.timespan+2} {x} c') for x in (10,12)]
getcoord(begintime='+4',duration=32,attribtuple=[{'id':10,'angle':-360*2,'key':['G',(0,1,0)]},{'id':12,'angle':360*2,'key':['G',(0,1,0)]},{'id':(10,12),'duration':2,'angle':90,'key':['g',(0,0,1)]},{'id':(10,12),'begintime':'+3','duration':2,'angle':-70,'key':['g',(0,1,0)]},{'id':(10,12),'begintime':'+6','duration':2,'key':['s',2]},{'id':(11,13),'begintime':'+6','duration':2,'key':['s',1.5]},{'id':(11,13),'begintime':'+18','duration':1,'key':['s',1/1.5]},{'id':(10,12),'begintime':'+18','duration':1,'key':['s',1/2]},{'id':(10,12),'begintime':'+20','duration':1,'angle':70,'key':['g',(0,1,0)]},{'id':(10,12),'begintime':'+22','duration':1,'angle':-90,'key':['g',(0,0,1)]},{'id':1,'begintime':'+24','duration':2,'angle':-40,'key':['g',(0,1,0)]},{'id':10,'begintime':'+27','duration':2,'key':['g',(0,0,0),(-2,0,0)]},{'id':12,'begintime':'+27','duration':2,'key':['g',(0,0,0),(-5,0,0)]},{'id':10,'begintime':'+27','duration':2,'angle':-3,'key':['g',(0,0,1)]},{'id':12,'begintime':'+27','duration':2,'angle':23,'key':['g',(0,0,1)]},{'id':1,'begintime':'+30','duration':2,'key':['g',(0,0,0),(-3,0,0)]}])
[file.write(f'\n{getcoord.timespan+1} {x} c') for x in (10,12)]
getcoord(begintime='+3',duration=62,attribtuple=[{'id':(10,12),'duration':2,'key':['g',(0,0,0),(0,-1,0)]},{'id':(10,11),'begintime':'+8','duration':5,'key':['s',0.95]},{'id':(10,11),'begintime':'+18','duration':5,'key':['s',0.01]},{'id':(12,13),'begintime':'+18','duration':5,'key':['s',0.01]},{'id':10,'begintime':'+24','duration':2,'key':['g',(0,0,0),(-6,1,0)]},{'id':12,'begintime':'+24','duration':2,'key':['g',(0,0,0),(-11,1,0)]},{'id':1,'begintime':'+24','duration':2,'key':['g',(0,0,0),(8.2,0,40)]},{'id':1,'begintime':'+31','duration':2,'key':['g',(8.2,0,40),(0,0,0)]},{'id':10,'begintime':'+31','duration':2,'key':['g',(-6,1,0),(0,0,0)]},{'id':12,'begintime':'+31','duration':2,'key':['g',(-11,1,0),(0,0,0)]},{'id':(10,11),'begintime':'+38','duration':5,'key':['s',1/(0.01*0.9)]},{'id':(12,13),'begintime':'+38','duration':5,'key':['s',1/0.01]},{'id':10,'begintime':'+48','duration':14,'angle':-360*5/10,'key':['G',(0,1,0)]},{'id':12,'begintime':'+48','duration':14,'angle':360*5,'key':['G',(0,1,0)]},{'id':(10,12),'begintime':'+50','duration':1,'key':['g',(0,0,0),(0,1,0)]},{'id':10,'begintime':'+52','duration':1,'key':['g',(0,0,0),(2,0,0)]},{'id':12,'begintime':'+52','duration':1,'key':['g',(0,0,0),(5,0,0)]},{'id':10,'begintime':'+60','duration':1,'key':['g',(0,0,0),(-5,0,0)]},{'id':12,'begintime':'+60','duration':1,'key':['g',(0,0,0),(-12,0,0)]}])
[file.write(f'\n{getcoord.timespan} {x} C') for x in range(8,25+1) if not x in [10,11,12,13]]
[file.write(f'\n{getcoord.timespan} {x} c') for x in range(8,25+1) if not x in [10,11,12,13]]
getcoord(begintime='+0',duration=10,attribtuple=({'id':8,'angle':360*5/60,'key':['G',(0,1,0)]},{'id':10,'angle':-360*5/243,'key':['G',(0,1,0)]},{'id':12,'angle':360*5,'key':['G',(0,1,0)]},{'id':14,'angle':360*5*(24/26),'key':['G',(0,1,0)]},{'id':16,'angle':360*5*2,'key':['G',(0,1,0)]},{'id':18,'angle':360*5*24/10,'key':['G',(0,1,0)]},{'id':20,'angle':360*5*24/17,'key':['G',(0,1,0)]},{'id':22,'angle':360*5*24/16,'key':['G',(0,1,0)]},{'id':24,'angle':360*5*24/153,'key':['G',(0,1,0)]}))


[file.write(f'\n1 {x} C') for x in (9,11,13,14,15,17,18,19,21,23,25,27,29)]
file.write(f'\n2 1 g')
getcoord(begintime=2,duration=14,attribtuple=({'id':1,'duration':10,'key':['g',(0,0,0),(-10,0,-30)]},{'id':22,'begintime':'+11','duration':3,'angle':10,'key':['g',(1,0,0)]}))
[file.write(f'\n{getcoord.timespan} {x} C') for x in (9,11,13,17,21,23,25,27,29)]
[file.write(f'\n{getcoord.timespan} {x} c') for x in (8,10,12,16,20,22,24,26,28)]
getcoord(begintime='+0',duration=20,attribtuple=({'id':8,'duration':10,'angle':2,'key':['g',(0,0,1)]},{'id':8,'angle':360*5/60,'key':['G',(0,1,0)]},{'id':10,'duration':10,'angle':-3,'key':['g',(0,0,1)]},{'id':10,'angle':-360*5/243,'key':['G',(0,1,0)]},{'id':12,'duration':10,'angle':23,'key':['g',(0,0,1)]},{'id':12,'angle':360*5,'key':['G',(0,1,0)]},{'id':16,'duration':10,'angle':28,'key':['g',(0,0,1)]},{'id':16,'angle':360*5*(24/26),'key':['G',(0,1,0)]},{'id':20,'duration':10,'angle':3,'key':['g',(0,0,1)]},{'id':20,'angle':360*5*2,'key':['G',(0,1,0)]},{'id':22,'duration':10,'angle':27,'key':['g',(0,0,1)]},{'id':22,'angle':360*5*24/10,'key':['G',(0,1,0)]},{'id':24,'duration':10,'angle':98,'key':['g',(0,0,1)]},{'id':24,'angle':360*5*24/17,'key':['G',(0,1,0)]},{'id':26,'duration':10,'angle':28,'key':['g',(0,0,1)]},{'id':26,'angle':360*5*24/16,'key':['G',(0,1,0)]},{'id':28,'duration':10,'angle':119,'key':['g',(0,0,1)]},{'id':28,'angle':360*5*24/153,'key':['G',(0,1,0)]}))
[file.write(f'\n{getcoord.timespan+2} {x} C') for x in range(8,29+1) if not x in [12,13,14,15,16,17,18,19]]
getcoord(begintime='+5',duration=5,attribtuple=[{'id':12,'duration':2,'key':['g',(0,0,0),(1,0,0)]},{'id':16,'duration':2,'key':['g',(0,0,0),(7,0,0)]},{'id':(12,16),'begintime':'+3','duration':2,'key':['g',(0,0,0),(0,-1,0)]}])
getcoord(begintime='+3',duration=43,attribtuple=[{'id':(16,17),'duration':5,'key':['s',0.47]},{'id':(12,13,16,17),'begintime':'+11','duration':5,'key':['s',0.01]},{'id':12,'begintime':'+18','duration':2,'key':['g',(0,0,0),(-6,1,0)]},{'id':16,'begintime':'+18','duration':2,'key':['g',(0,0,0),(-13.5,1,0)]},{'id':1,'begintime':'+18','duration':2,'key':['g',(0,0,0),(8.2,0,40)]},{'id':1,'begintime':'+23','duration':2,'key':['g',(8.2,0,40),(0,0,0)]},{'id':12,'begintime':'+23','duration':2,'key':['g',(-6,1,0),(0,0,0)]},{'id':16,'begintime':'+23','duration':2,'key':['g',(-13.5,1,0),(0,0,0)]},{'id':(16,17),'begintime':'+29','duration':5,'key':['s',1/(0.01*0.47)]},{'id':(12,13),'begintime':'+29','duration':5,'key':['s',1/0.01]},{'id':12,'begintime':'+35','duration':8,'angle':360*5,'key':['G',(0,1,0)]},{'id':16,'begintime':'+35','duration':8,'angle':360*5*(24/26),'key':['G',(0,1,0)]}])
[file.write(f'\n{getcoord.timespan} {x} C') for x in (14,18,19)]
getcoord(begintime='+0',duration=30,attribtuple=[{'id':12,'angle':360*5,'key':['G',(0,1,0)]},{'id':14,'angle':360*1.5,'key':['g',(0,1,0)]},{'id':16,'angle':360*5*(24/26),'key':['G',(0,1,0)]},{'id':18,'angle':360*4,'key':['g',(0,1,0)]},{'id':19,'angle':360*0.9,'key':['g',(0,1,0)]}])
[file.write(f'\n{getcoord.timespan} {x} C') for x in (14,18,19)]
getcoord(begintime='+0',duration=20,attribtuple=[{'id':12,'angle':360*5,'key':['G',(0,1,0)]},{'id':(12,16),'duration':2,'key':['g',(0,0,0),(0,1,0)]},{'id':16,'angle':360*5*(24/26),'key':['G',(0,1,0)]},{'id':12,'begintime':'+8','duration':2,'key':['g',(0,0,0),(1,0,0)]},{'id':16,'begintime':'+8','duration':2,'key':['g',(0,0,0),(4,0,0)]},{'id':12,'begintime':'+17','duration':2,'key':['g',(0,0,0),(-2,0,0)]},{'id':16,'begintime':'+17','duration':2,'key':['g',(0,0,0),(-11,0,0)]}])
[file.write(f'\n{getcoord.timespan} {x} C') for x in range(8,29+1) if not x in [12,13,14,15,16,17,18,19]]
getcoord(begintime='+0',duration=20,attribtuple=({'id':8,'angle':360*5/60,'key':['G',(0,1,0)]},{'id':10,'angle':-360*5/243,'key':['G',(0,1,0)]},{'id':12,'angle':360*5,'key':['G',(0,1,0)]},{'id':16,'angle':360*5*(24/26),'key':['G',(0,1,0)]},{'id':20,'angle':360*5*2,'key':['G',(0,1,0)]},{'id':22,'angle':360*5*24/10,'key':['G',(0,1,0)]},{'id':24,'angle':360*5*24/17,'key':['G',(0,1,0)]},{'id':26,'angle':360*5*24/16,'key':['G',(0,1,0)]},{'id':28,'angle':360*5*24/153,'key':['G',(0,1,0)]}))
#,{'id':(10,12),'begintime':'+50','duration':1,'key':['g',(0,0,0),(0,1,0)]},{'id':10,'begintime':'+52','duration':1,'key':['g',(0,0,0),(2,0,0)]},{'id':12,'begintime':'+52','duration':1,'key':['g',(0,0,0),(5,0,0)]},{'id':10,'begintime':'+60','duration':1,'key':['g',(0,0,0),(-5,0,0)]},{'id':12,'begintime':'+60','duration':1,'key':['g',(0,0,0),(-12,0,0)]}])



[file.write(f'\n1 {x} C') for x in (9,11,13,14,15,17,19,20,21,22,23,24,26,28,30,32)]
file.write(f'\n2 1 g')
getcoord(begintime=2,duration=14,attribtuple=({'id':1,'duration':10,'key':['g',(0,0,0),(-10,0,-30)]}))
[file.write(f'\n{getcoord.timespan} {x} C') for x in (9,11,13,17,19,26,28,30,32)]
[file.write(f'\n{getcoord.timespan} {x} c') for x in (8,10,12,16,18,25,27,29,31)]
getcoord(begintime='+1',duration=12,attribtuple=({'id':8,'duration':10,'angle':2,'key':['g',(0,0,1)]},{'id':8,'angle':360*5/60,'key':['G',(0,1,0)]},{'id':10,'duration':10,'angle':-3,'key':['g',(0,0,1)]},{'id':10,'angle':-360*5/243,'key':['G',(0,1,0)]},{'id':12,'duration':10,'angle':23,'key':['g',(0,0,1)]},{'id':12,'angle':360*5,'key':['G',(0,1,0)]},{'id':16,'duration':10,'angle':28,'key':['g',(0,0,1)]},{'id':16,'angle':360*5*(24/26),'key':['G',(0,1,0)]},{'id':18,'duration':10,'angle':3,'key':['g',(0,0,1)]},{'id':18,'angle':360*5*2,'key':['G',(0,1,0)]},{'id':25,'duration':5,'angle':10,'key':['g',(1,0,0)]},{'id':25,'begintime':'+6','duration':3,'angle':27,'key':['g',(0,0,1)]},{'id':25,'angle':360*5*24/10,'key':['G',(0,1,0)]},{'id':27,'duration':10,'angle':98,'key':['g',(0,0,1)]},{'id':27,'angle':360*5*24/17,'key':['G',(0,1,0)]},{'id':29,'duration':10,'angle':28,'key':['g',(0,0,1)]},{'id':29,'angle':360*5*24/16,'key':['G',(0,1,0)]},{'id':31,'duration':10,'angle':119,'key':['g',(0,0,1)]},{'id':31,'angle':360*5*24/153,'key':['G',(0,1,0)]}))
[file.write(f'\n{getcoord.timespan+2} {x} C') for x in range(8,32+1) if not x in [12,13,14,15,18,19,20,21,22,23,24]]
getcoord(begintime='+2',duration=5,attribtuple=[{'id':12,'duration':2,'key':['g',(0,0,0),(1,0,0)]},{'id':18,'duration':2,'key':['g',(0,0,0),(3,0,0)]},{'id':(12,18),'begintime':'+3','duration':2,'key':['g',(0,0,0),(0,-1,0)]}])
getcoord(begintime='+3',duration=34,attribtuple=[{'id':(12,13),'duration':5,'key':['s',0.1]},{'id':(12,13,18,19),'begintime':'+7','duration':5,'key':['s',0.1]},{'id':12,'begintime':'+14','duration':2,'key':['g',(0,0,0),(-6,1,0)]},{'id':18,'begintime':'+14','duration':2,'key':['g',(0,0,0),(-11.5,1,0)]},{'id':1,'begintime':'+14','duration':2,'key':['g',(0,0,0),(8.2,0,40)]},{'id':1,'begintime':'+19','duration':2,'key':['g',(8.2,0,40),(0,0,0)]},{'id':12,'begintime':'+19','duration':2,'key':['g',(-6,1,0),(0,0,0)]},{'id':18,'begintime':'+19','duration':2,'key':['g',(-11.5,1,0),(0,0,0)]},{'id':(18,19),'begintime':'+24','duration':5,'key':['s',1/0.1]},{'id':(12,13),'begintime':'+24','duration':5,'key':['s',1/0.01]},{'id':12,'begintime':'+30','duration':4,'angle':360*5/7,'key':['G',(0,1,0)]},{'id':18,'begintime':'+30','duration':4,'angle':360*5*2/7,'key':['G',(0,1,0)]}])
[file.write(f'\n{getcoord.timespan} {x} C') for x in (14,20,21,22,23,24)]
getcoord(begintime='+0',duration=30,attribtuple=[{'id':12,'angle':360*5,'key':['G',(0,1,0)]},{'id':14,'angle':360*1.5,'key':['g',(0,1,0)]},{'id':18,'angle':360*5*2,'key':['G',(0,1,0)]},{'id':20,'angle':360*5*2,'key':['g',(0,1,0)]},{'id':21,'angle':360*5*6/5,'key':['g',(0,1,0)]},{'id':22,'angle':360*5*4/5,'key':['g',(0,1,0)]},{'id':23,'angle':360*5*2/5,'key':['g',(0,1,0)],},{'id':24,'angle':360*5*1/5,'key':['g',(0,1,0)]}])
[file.write(f'\n{getcoord.timespan} {x} C') for x in (14,20,21,22,23,24)]
getcoord(begintime='+0',duration=20,attribtuple=[{'id':12,'angle':360*5*0.66,'key':['G',(0,1,0)]},{'id':(12,18),'duration':2,'key':['g',(0,0,0),(0,1,0)]},{'id':18,'angle':360*5*2*0.66,'key':['G',(0,1,0)]},{'id':12,'begintime':'+8','duration':2,'key':['g',(0,0,0),(1,0,0)]},{'id':18,'begintime':'+8','duration':2,'key':['g',(0,0,0),(4,0,0)]},{'id':12,'begintime':'+17','duration':2,'key':['g',(0,0,0),(-2,0,0)]},{'id':18,'begintime':'+17','duration':2,'key':['g',(0,0,0),(-7,0,0)]}])
[file.write(f'\n{getcoord.timespan} {x} C') for x in range(8,32+1) if not x in [12,13,14,15,18,19,20,21,22,23,24]]
getcoord(begintime='+0',duration=12,attribtuple=({'id':8,'angle':360*5/60,'key':['G',(0,1,0)]},{'id':10,'angle':-360*5/243,'key':['G',(0,1,0)]},{'id':12,'angle':360*5,'key':['G',(0,1,0)]},{'id':16,'angle':360*5*(24/26),'key':['G',(0,1,0)]},{'id':18,'angle':360*5*2,'key':['G',(0,1,0)]},{'id':25,'angle':360*5*24/10,'key':['G',(0,1,0)]},{'id':27,'angle':360*5*24/17,'key':['G',(0,1,0)]},{'id':29,'angle':360*5*24/16,'key':['G',(0,1,0)]},{'id':31,'angle':360*5*24/153,'key':['G',(0,1,0)]}))
'''

[file.write(f'\n1 {x} C') for x in (9,11,13,14,15,17,19,21,22,23,24,25,26,27,29,31,33)]
file.write(f'\n2 1 g')
getcoord(begintime=2,duration=14,attribtuple=({'id':1,'duration':10,'key':['g',(0,0,0),(-10,0,-30)]}))
[file.write(f'\n{getcoord.timespan} {x} C') for x in (9,11,13,17,19,21,29,31,33)]
[file.write(f'\n{getcoord.timespan} {x} c') for x in (8,10,12,16,18,20,28,30,32)]
getcoord(begintime='+1',duration=12,attribtuple=({'id':8,'duration':10,'angle':2,'key':['g',(0,0,1)]},{'id':8,'angle':360*5/60,'key':['G',(0,1,0)]},{'id':10,'duration':10,'angle':-3,'key':['g',(0,0,1)]},{'id':10,'angle':-360*5/243,'key':['G',(0,1,0)]},{'id':12,'duration':10,'angle':23,'key':['g',(0,0,1)]},{'id':12,'angle':360*5,'key':['G',(0,1,0)]},{'id':16,'duration':10,'angle':28,'key':['g',(0,0,1)]},{'id':16,'angle':360*5*(24/26),'key':['G',(0,1,0)]},{'id':18,'duration':10,'angle':3,'key':['g',(0,0,1)]},{'id':18,'angle':360*5*2,'key':['G',(0,1,0)]},{'id':20,'duration':5,'angle':10,'key':['g',(1,0,0)]},{'id':20,'begintime':'+6','duration':3,'angle':27,'key':['g',(0,0,1)]},{'id':20,'angle':360*5*24/10,'key':['G',(0,1,0)]},{'id':28,'duration':10,'angle':98,'key':['g',(0,0,1)]},{'id':28,'angle':360*5*24/17,'key':['G',(0,1,0)]},{'id':30,'duration':10,'angle':28,'key':['g',(0,0,1)]},{'id':30,'angle':360*5*24/16,'key':['G',(0,1,0)]},{'id':32,'duration':10,'angle':119,'key':['g',(0,0,1)]},{'id':32,'angle':360*5*24/153,'key':['G',(0,1,0)]}))
[file.write(f'\n{getcoord.timespan+2} {x} C') for x in range(8,32+1) if not x in [12,13,14,15,20,21,22,23,24,25,26,27]]
getcoord(begintime='+2',duration=5,attribtuple=[{'id':12,'duration':5,'angle':-23,'key':['g',(0,0,1)]},{'id':20,'duration':5,'angle':-27,'key':['g',(0,0,1)]},{'id':12,'duration':2,'key':['g',(0,0,0),(1,0,0)]},{'id':20,'duration':2,'key':['g',(0,0,0),(3,0,0)]},{'id':(12,20),'begintime':'+3','duration':2,'key':['g',(0,0,0),(0,-1,0)]}])
getcoord(begintime='+3',duration=34,attribtuple=[{'id':(12,13),'duration':5,'key':['s',0.1]},{'id':(12,13,20,21),'begintime':'+7','duration':5,'key':['s',0.1]},{'id':12,'begintime':'+14','duration':2,'key':['g',(0,0,0),(-6,1,0)]},{'id':20,'begintime':'+14','duration':2,'key':['g',(0,0,0),(-14.8,1,0)]},{'id':1,'begintime':'+14','duration':2,'key':['g',(0,0,0),(8.2,0,40)]},{'id':1,'begintime':'+19','duration':2,'key':['g',(8.2,0,40),(0,0,0)]},{'id':12,'begintime':'+19','duration':2,'key':['g',(-6,1,0),(0,0,0)]},{'id':20,'begintime':'+19','duration':2,'key':['g',(-14.8,1,0),(0,0,0)]},{'id':(20,21),'begintime':'+24','duration':5,'key':['s',1/0.1]},{'id':(12,13),'begintime':'+24','duration':5,'key':['s',1/0.01]},{'id':12,'begintime':'+30','duration':4,'angle':360*5/7,'key':['G',(0,1,0)]},{'id':20,'begintime':'+30','duration':4,'angle':360*5*2/7,'key':['G',(0,1,0)]}])
[file.write(f'\n{getcoord.timespan} {x} C') for x in (14,22,23,24,25,26,27)]
getcoord(begintime='+0',duration=30,attribtuple=[{'id':12,'duration':5,'angle':23,'key':['g',(0,0,1)]},{'id':20,'duration':5,'angle':27,'key':['g',(0,0,1)]},{'id':12,'angle':360*5,'key':['G',(0,1,0)]},{'id':14,'angle':360*1.5,'key':['g',(0,1,0)]},{'id':20,'angle':360*5*2,'key':['G',(0,1,0)]},{'id':22,'angle':360*5*2,'key':['g',(0,1,0)]},{'id':23,'angle':360*5*6/5,'key':['g',(0,1,0)]},{'id':24,'angle':360*5*4/5,'key':['g',(0,1,0)]},{'id':25,'angle':360*5*2/5,'key':['g',(0,1,0)],},{'id':26,'angle':360*5*1/5,'key':['g',(0,1,0)]},{'id':27,'angle':360*5*1/7,'key':['g',(0,1,0)]}])
[file.write(f'\n{getcoord.timespan} {x} C') for x in (14,22,23,24,25,26,27)]
getcoord(begintime='+0',duration=30,attribtuple=[{'id':12,'angle':360*5,'key':['G',(0,1,0)]},{'id':(12,20),'duration':2,'key':['g',(0,0,0),(0,1,0)]},{'id':20,'angle':360*5*2,'key':['G',(0,1,0)]},{'id':12,'begintime':'+14','duration':2,'key':['g',(0,0,0),(1,0,0)]},{'id':20,'begintime':'+14','duration':2,'key':['g',(0,0,0),(4,0,0)]},{'id':12,'begintime':'+27','duration':2,'key':['g',(0,0,0),(-2,0,0)]},{'id':20,'begintime':'+27','duration':2,'key':['g',(0,0,0),(-7,0,0)]}])
[file.write(f'\n{getcoord.timespan} {x} C') for x in range(8,32+1) if not x in [12,13,14,15,20,21,22,23,24,25,26,27]]
getcoord(begintime='+0',duration=12,attribtuple=({'id':8,'angle':360*5/60,'key':['G',(0,1,0)]},{'id':10,'angle':-360*5/243,'key':['G',(0,1,0)]},{'id':12,'angle':360*5,'key':['G',(0,1,0)]},{'id':16,'angle':360*5*(24/26),'key':['G',(0,1,0)]},{'id':18,'angle':360*5*2,'key':['G',(0,1,0)]},{'id':20,'angle':360*5*24/10,'key':['G',(0,1,0)]},{'id':28,'angle':360*5*24/17,'key':['G',(0,1,0)]},{'id':30,'angle':360*5*24/16,'key':['G',(0,1,0)]},{'id':32,'angle':360*5*24/153,'key':['G',(0,1,0)]}))
