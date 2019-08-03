import time
import re
import sys
import html.parser
sys.path.append('../util/')
from util.utilm import utilc
from basefetchm import basefetchc

class linkedinc(basefetchc):
 def __init__(self):
  basefetchc.__init__(self,"Linked In")
  self.utili=utilc('linkedin')
 def process(self):
  trycount_l=pc_l=0
  fetchstr_l=[]
  html_parser = html.parser.HTMLParser()
  tech=sys.argv[3]
  if re.search(r'^C\+\+$',sys.argv[3],flags=re.I):
   tech='c%2B%2B'
  while pc_l<int(sys.argv[4]) and trycount_l<21:
   try:
   # for i in [re.sub(r'"name":"([^"]*)"','\\1 '+sys.argv[1],name,flags=re.I) for name in re.findall(r'"name":"[^"]*"',html_parser.unescape(utili.getlinkedin_1('https://www.linkedin.com/jobs/search/?keywords='+sys.argv[3]+'&location='+re.sub(r'\s','%20',sys.argv[1])+'&locationId='+sys.argv[2]+'%3A0&start='+str(pc_l*25))),flags=re.I) if not re.search(r'"name":"string"',name,flags=re.I)]:
    for i in [re.sub(r'"name":"([^"]*)"','\\1 '+sys.argv[1],name,flags=re.I) for name in re.findall(r'"name":"[^"]*"',html_parser.unescape(self.utili.getlinkedin_1('https://www.linkedin.com/jobs/search/?keywords='+tech+'&location='+re.sub(r'\s','%20',sys.argv[1])+'&locationId='+sys.argv[2]+'%3A0&start='+str(pc_l*25))),flags=re.I) if not re.search(r'"name":"string"',name,flags=re.I)]:
     fetchstr_l.append(i)
   except:
    time.sleep(1)
    trycount_l=trycount_l+1
    print("trying... page,trycount %s,%s" % (pc_l,trycount_l))
   else:
    pc_l=pc_l+1
    trycount_l=0
    print("incrementing page to %s" % pc_l)
  self.utili.close()
  return list(set(fetchstr_l))
