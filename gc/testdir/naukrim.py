import time
import re
import sys
sys.path.append('../util')
from util.utilm import utilc
from basefetchm import basefetchc
class naukric(basefetchc):
 def __init__(self):
  basefetchc.__init__(self,"naukri.com")
 def process(self):
  trycount_l=pc_l=0
  fetchstr_l=[]
  tech=sys.argv[3]
  utili=utilc()
  if re.search(r'^C\+\+$',sys.argv[3],flags=re.I):
   tech='c-plus-plus'
  print("tech %s" % tech)
  while pc_l<int(sys.argv[4]) and trycount_l<8:
   extension=('-'+str(pc_l+1)) if pc_l else ''
   try:
    for i in [re.sub(r'<span class="org">([^<]*)<.*?<span class="loc">.*?<span>([^<]*)<','\\1 \\2',name) for name in re.findall(r'<span class="org">[^<]*<.*?<span class="loc">.*?<span>[^<]*<',utili.download('https://www.naukri.com/'+tech+'-jobs-in-'+sys.argv[1].lower()+extension))]:
     fetchstr_l.append(i)
   except:
    time.sleep(1)
    trycount_l=trycount_l+1
    print("trying... page,trycount %s,%s" % (pc_l,trycount_l))
   else:
    pc_l=pc_l+1
    trycount_l=0
    print("incrementing page to %s" % pc_l)
  return list(set(fetchstr_l))
