import time
import re
import sys
from basefetchm import basefetchc
class linkedinc(basefetchc):
 def __init__(self):
  basefetchc.__init__(self,"Linked In")
 def process(self):
  trycount_l=pc_l=0
  fetchstr_l=[]
  while pc_l<int(sys.argv[4]) and trycount_l<21:
   try:
    #for i in [re.sub(r',"companyName":"([^"]*)","formattedLocation":"([^"]*)",','\\1 \\2',name) for name in re.findall(r',"companyName":"[^"]*","formattedLocation":"[^"]*",',self.download('https://www.linkedin.com/jobs/search/?'+sys.argv[3]+'&location='+re.sub(r'\s','%20',sys.argv[1])+'&locationId='+sys.argv[2]+'&start='+str(pc_l*25)))]:
    for i in [re.sub(r',"companyName":"([^"]*)","formattedLocation":"([^"]*)",','\\1 \\2',name) for name in re.findall(r',"companyName":"[^"]*","formattedLocation":"[^"]*",',self.download('https://www.linkedin.com/jobs/search/?keywords='+sys.argv[3]+'&location='+re.sub(r'\s','%20',sys.argv[1])+'&locationId='+sys.argv[2]+'%3A0&start='+str(pc_l*25)))]:
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
