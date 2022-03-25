from fuzzywuzzy import fuzz,process
from collections import OrderedDict
import re

class machinelearningrequest():
 def __init__(self):
  super(machinelearningrequest,self).__init__()
#  self.blockedemail=' '.join(self.db.get('blockedemail'))
#  self.junkemail=r'^('+(''.join([x[0]+'|' for x in self.db.get('junkemail')]))[:-1]+')$'

 def getmatching(self,*splitline,email=False,percent=50,muteprint=False):
  print(f'matchinelearningrequest.getmatchingemail {splitline=}') if not muteprint else None
  THRESHOLD=10
  out=[]
  out.extend(process.extract(splitline[0],splitline[1:],limit=None))
  print(f'out11 {out=}') if not muteprint else None
  if email:
   for i in splitline[1:]:
#    out.append((i,int(process.extract(splitline[0],(' '.join(re.split(r'\.',re.split(r'@',i)[1])[:-1]),),limit=None)[0][1]*0.67+process.extract(re.split(r'\s+',splitline[0])[0],(re.split(r'\.',re.split(r'@',i)[1])[0],),limit=None)[0][1]*0.33)))
    out.append((i,int(process.extract(splitline[0],(' '.join(re.split(r'\.',re.split(r'@',i)[1])[:-1]),),limit=None)[0][1]*0.67+process.extract(re.split(r'\s+',splitline[0])[0],(' '.join(re.split(r'\.',re.split(r'@',i)[1])[:-1]),),limit=None)[0][1]*0.33)))
    out.append((i,process.extract(splitline[0],(re.split(r'@',i)[0],),limit=None)[0][1]-THRESHOLD)) if len(re.split(r'@',i)[0]) > 2 else None
    out.append((i,fuzz.ratio(''.join([x[0] for x in re.split(r'\s+',splitline[0])]).lower(),re.split(r'\.',re.split(r'@',i)[1])[0].lower()))) if len(re.split(r'\s+',splitline[0])) > 1 else None
   print(f'out22 {out=}') if not muteprint else None
   for j in [x for x in out if x[1]>=percent]:
    if j in out:
     index=out.index(j)
     out[index]=(j[0],sum([x[1] for x in out if j[0]==x[0] and x[1]>=percent]))
     [out.remove(x) for x in out[index+1:] if x in out and x[0]==out[index][0] and x[1]>=percent]
  out.sort(key=lambda x:x[1],reverse=True)
  print(f'out33 {out=}') if not muteprint else None
  return list(OrderedDict.fromkeys([t[0] for t in out if t[1]>=percent]))
   
'''
 def getmatching(self,*splitline,percent=(50,50),count=2,mode=None):#count=None for all
#  print(f'matchinelearningrequest.getmatching {splitline=}')
  out=[]
#  index=0
  for i in splitline[1:]:
#   out.append((i,fuzz.partial_token_set_ratio(re.split(r'\s+',splitline[0])[0],' '.join(re.split(r'(?:@|\.)',i)[:-1]))))
   if mode=='email':
    out.append(i.lower()) if fuzz.partial_token_set_ratio(re.split(r'\s+',splitline[0])[0],re.split(r'\.',re.split(r'@',i)[1])[0]) > percent[0] else None
    out.append(i.lower()) if fuzz.partial_token_set_ratio(re.split(r'\s+',splitline[0])[0],' '.join(re.split(r'\.',re.split(r'@',i)[0]))) > 80  else None
   else:
    out.append([i,fuzz.partial_token_set_ratio(re.split(r'\s+',splitline[0])[0],' '.join(re.split(r'(?:@|\.)',i)))])
  out=[x[0] for x in sorted(out,key=lambda x:x[1],reverse=True) if x[1]>percent[0]][:count] if mode!='email' else out
#  print(f'22 {out=}')
  out[0:0]=[x[0].lower() if mode=='email' else x[0] for x in process.extract(splitline[0],splitline[1:]) if x[1]>percent[1]][:count]
#  print(f'33 {out=}')

#  while mode=='email' and index<len(out)-1:
#   [out.pop(out.index(y[0],index+1,len(out))) if y[0] in out[index+1:] else None for y in process.extract(out[index],out[index+1:]) if y[1]>=85]
#   index+=1
#  print(f'44 {out=}')
  return list(OrderedDict.fromkeys(out))
'''
