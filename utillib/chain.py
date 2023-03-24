import os,sys;sys.path.append(os.path.expanduser('~')+r'/tmp')
if len(sys.argv)<2:
 print(f'usage - chain.py <tech> <country> <pagecount> [<tech> <country> <pagecount>]\npython3 chain.py qt india 2\npython3 chain.py qt india 2 python australia 2')
 sys.exit(-1)
from MISC.utillib.naukri import naukri
from MISC.utillib.linkedin import linkedin
from MISC.utillib.google import google
from MISC.utillib.fetcher import fetcher
from machinelearningrequest import machinelearningrequest
from seleniumrequest import seleniumrequest
from databaserequest import databaserequest
chain=[]
retval=None
ml=machinelearningrequest()
db=databaserequest()
for i in 'naukri','linkedin','google':
 chain.append(eval(i+'()'))
for i in range(int(len(sys.argv)/3)):
 url_t=[ml.getmatching(sys.argv[i*3+1],*[x[1] for x in db.db.search2('tech',mode='get')])[0].lower(),ml.getmatching(sys.argv[i*3+2],*[x[1] for x in db.db.search2('country',mode='get')])[0].lower(),int(sys.argv[i*3+3])]
 while url_t:
  url=url_t
  url_t=[]
  for i in chain:
   retval=i.get(*url)
   url_t.extend(retval) if retval else None
 print(f'final {url=}')
seleniumrequest.close()
[i.quitfetcherthread() for i in chain if type(i)==google]
