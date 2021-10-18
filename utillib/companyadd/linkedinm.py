import time
import re
import sys
class linkedinc:
 def __init__(self):
   self.name='linkedin'
 def process(self,driverp):
  fetchstr_l=[]
  tech=sys.argv[3]
  if re.search(r'^C\+\+$',sys.argv[3],flags=re.I):
   tech='c%2B%2B'
  try:
   print('><linkedin https://www.linkedin.com/jobs/search/?keywords='+tech+'&location='+re.sub(r'\s','%20',sys.argv[1])+'&locationId='+sys.argv[2]+'%3A0&start=0')
   driverp.get('https://www.linkedin.com/jobs/search/?keywords='+tech+'&location='+re.sub(r'\s','%20',sys.argv[1])+'&locationId='+sys.argv[2]+'%3A0&start=0')
   for i in range(10*int(sys.argv[4])):
    driverp.execute_script("window.scrollBy(0,250)")
    if not i%10:
     print("page number {}".format(int(i/10)))
    time.sleep(1)
   open('linkedindata.txt','w').write(driverp.page_source)
#   for i in [re.sub(r'alt="([^"]*).*<span class="job-result-card__location">(.*)',r'\1 \2',i,flags=re.I) for i in re.findall(r'alt="[^"]*.*?<span class="job-result-card__location">[^<]*',driverp.page_source) if not re.search(r'alt="$',i)]:
   companylist=[re.sub(r'alt="([^"]*).*<span class="job-result-card__location">(.*)',r'\1 \2',i,flags=re.I) for i in re.findall(r'alt="[^"]*.*?<span class="job-result-card__location">[^<]*',driverp.page_source) if not re.search(r'alt="$',i)]
   if len(companylist):
    fetchstr_l.extend(companylist)
   else:
    print('alternative')
    fetchstr_l.extend([' '.join(i) for i in re.findall(r'div class="base-search-card__info">.*?data-tracking-client-ingraph.*?\n\s*?(\w+[\w .]*?)\s*</a>.*?<span class="job-search-card__location">\s*(\w+[\w .,]*)\n',driverp.page_source,flags=re.I|re.DOTALL)])
#    fetchstr_l.append(i)
  except:
   print("exception happened.....")
  return list(set(fetchstr_l))
