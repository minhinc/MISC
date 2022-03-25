import time
import re
import sys
#sys.path.append('../util')
#from util.utilm import utilc
#from basefetchm import basefetchc
#class naukric(basefetchc):
class naukric:
 def __init__(self):
#  basefetchc.__init__(self,"naukri.com")
  self.name="naukri.com"
 def process(self,driverp):
  trycount_l=pc_l=0
  fetchstr_l=[]
  tech=sys.argv[3]
#  utili=utilc()
  if re.search(r'^C\+\+$',sys.argv[3],flags=re.I):
   tech='c-plus-plus'
  print("tech %s" % tech)
  while pc_l<int(sys.argv[4]) and trycount_l<8:
   extension=('-'+str(pc_l+1)) if pc_l else ''
   try:
#    for i in [re.sub(r'<span class="org">([^<]*)<.*?<span class="loc">.*?<span>([^<]*)<','\\1 \\2',name) for name in re.findall(r'<span class="org">[^<]*<.*?<span class="loc">.*?<span>[^<]*<',utili.download('https://www.naukri.com/'+tech+'-jobs-in-'+sys.argv[1].lower()+extension))]:
    print('><naukri.com https://www.naukri.com/'+tech+'-jobs-in-'+sys.argv[1].lower()+extension)
    driverp.get('https://www.naukri.com/'+tech+'-jobs-in-'+sys.argv[1].lower()+extension)

    ht=driverp.execute_script("return document.documentElement.scrollHeight;")
    while True:
     prev_ht=driverp.execute_script("return document.documentElement.scrollHeight;")
     driverp.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
     time.sleep(2)
     ht=driverp.execute_script("return document.documentElement.scrollHeight;")
     print(f'{prev_ht=} {ht=}')
     if prev_ht==ht:
      break

    '''
    for i in range(2):
     driverp.execute_script("window.scrollBy(0,250)")
     print("window scroll {}".format(i))
     time.sleep(1)
    '''

    for i in [i for i in re.findall(r'target="_blank" title="[^"]*"\s*>.*?</a>',driverp.page_source) if re.sub(r'.*title="(.*?)".*',r'\1',i,flags=re.I) == re.sub(r'.*>(.*?)</a>.*',r'\1',i,flags=re.I) and not re.search(r'(Naukri|Ambition Box)',i,flags=re.I)]:
     fetchstr_l.append(re.sub(r'.*>(.*?)</a>.*',r'\1',i,flags=re.I)+' '+sys.argv[1])
   except:
    time.sleep(1)
    trycount_l=trycount_l+1
    print("trying... page,trycount %s,%s" % (pc_l,trycount_l))
   else:
    pc_l=pc_l+1
    trycount_l=0
    print("incrementing page to %s" % pc_l)
  return list(set(fetchstr_l))
