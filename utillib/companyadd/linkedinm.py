import time
import re
import sys
#import html.parser
#sys.path.append('../util/')
#from util.utilm import utilc
#from basefetchm import basefetchc
#
#class linkedinc(basefetchc):
class linkedinc:
 def __init__(self):
#  basefetchc.__init__(self,"Linked In")
#  self.utili=utilc('linkedin')
   self.name='linkedin'
 def process(self,driverp):
#  trycount_l=pc_l=0
  fetchstr_l=[]
#  html_parser = html.parser.HTMLParser()
  tech=sys.argv[3]
  if re.search(r'^C\+\+$',sys.argv[3],flags=re.I):
   tech='c%2B%2B'
#  while pc_l<int(sys.argv[4]) and trycount_l<21:
  try:
   print('><linkedin https://www.linkedin.com/jobs/search/?keywords='+tech+'&location='+re.sub(r'\s','%20',sys.argv[1])+'&locationId='+sys.argv[2]+'%3A0&start=0')
   driverp.get('https://www.linkedin.com/jobs/search/?keywords='+tech+'&location='+re.sub(r'\s','%20',sys.argv[1])+'&locationId='+sys.argv[2]+'%3A0&start=0')
   for i in range(10*int(sys.argv[4])):
    driverp.execute_script("window.scrollBy(0,250)")
    if not i%10:
     print("page number {}".format(int(i/10)))
    time.sleep(1)
#   open('t.txt','w').write(driverp.page_source)
   #for i in [re.sub(r'alt="(.*).*?<span class="job-result-card__location">(.*)?</span>',r'\1 \2',i,flags=re.I) for i in re.findall(r'alt="[^"]*".*?<span class="job-result-card__location">.*?</span>',driverp.page_source) if not re.search(r'alt="$',i)]:
#   for i in [re.sub(r'alt="([^"]*).*<span class="job-result-card__location">(.*)',r'\1 \2',i,flags=re.I) for i in re.findall(r'alt="[^"]*.*?<span class="job-result-card__location">[^<]*',open('t.txt').read()) if not re.search(r'alt="$',i)]:
   for i in [re.sub(r'alt="([^"]*).*<span class="job-result-card__location">(.*)',r'\1 \2',i,flags=re.I) for i in re.findall(r'alt="[^"]*.*?<span class="job-result-card__location">[^<]*',driverp.page_source) if not re.search(r'alt="$',i)]:
    fetchstr_l.append(i)
  except:
#    time.sleep(1)
#    trycount_l=trycount_l+1
#    print("trying... page,trycount %s,%s" % (pc_l,trycount_l))
   print("exception happened.....")
#   else:
#    pc_l=pc_l+1
#    trycount_l=0
#    print("incrementing page to %s" % pc_l)
#  self.utili.close()
  return list(set(fetchstr_l))
