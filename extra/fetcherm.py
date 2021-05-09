import os,re
import sys
sys.path.append('MISC/gtc')
from databasem import databasec
import time
import numpy as np
import matplotlib.pyplot as plt
class fetcherc:
 def __init__(self):
  self.db=databasec(False)
 def statepage(self,state,url):
#  text=os.popen('lynx -dump -nolist '+url).read()
  currentdata='_'.join([re.sub(r'^(.*?)\s*\d.*?\s*(\d+)$',r'\2_\1',i) for i in re.split(r'\n\s*',re.sub(r'^.*Party\s*Won\s*Leading\s*Total\s*(.*?)\n\s*Total\s*\d+\s*\d+.*$',r'\1',os.popen(r'lynx -dump -nolist '+url).read(),flags=re.I|re.DOTALL))])
  lastdata=self.db.get('election','data',orderby=('id',1))
  print('lastdata',lastdata)
  print('currentdata',currentdata)
  if lastdata==() or lastdata[0][0]!=currentdata:
   self.db.fill('election')
   self.db.update('election',('state','hrmnsc','data'),(state,str(time.localtime().tm_hour)+'.'+str(int((time.localtime().tm_min*100)/60)).zfill(2),currentdata),'id',self.db.get('election','id',orderby=('id',1))[0][0])
   return self.db.get('election','*','state',state)
  else:
   return None

# def getgraph(self,state,constituency='all',party='all'):
 def getgraph(self,data,state):
#  print('data',data)
  plist=dict()
  for count,i in enumerate(data):
   print('i',i)
   for key in plist:
    plist[key].append(None)
   party,vote=(re.split(r'_',i[3])[1::2],re.split(r'_',i[3])[::2])
   print('plist,party:vote',plist,party,vote)
   for j in range(len(party)):
    if party[j] not in plist:
     plist[party[j]]=[None]*(count+1)
    plist[party[j]][-1]=vote[j]
  print('data {}\nplist {}'.format(data,plist))
  for key in plist:
#   plt.plot(float(data[::,2]),plist[key],color=self.db.get('electionparty','color','name',key)[0][0])
   x=[float(i) for i in data[:,2]]
   y=[int(i) if i else i for i in plist[key]]
   print('x,y',x,y)
#   plt.plot([float(i) for i in data[:,2]],plist[key])
   plt.plot(x,y)
  plt.grid()
  plt.gca().legend(tuple(plist.keys()),bbox_to_anchor=(0,1),loc='upper left',mode="expand",fontsize=6)
  plt.title(state)
  plt.xlabel('hour:min')
  plt.ylabel('seats')
  plt.savefig('election.png')
  plt.clf()
  os.system('~/tmp/ftp.sh mput image election.png')
  print('sent')
##    plt.xticks(np.arange(7.0,max(x)+2,0.5)
#  plt.show()

if __name__=='__main__':
 f=fetcherc()
 while True:
  data=f.statepage('westbengal',r'https://results.eci.gov.in/Result2021/partywiseresult-S25.htm?st=S25')
  if data:
   f.getgraph(np.array(data),'westbengal')
  else:
   print('No data',time.localtime())
  time.sleep(300)
