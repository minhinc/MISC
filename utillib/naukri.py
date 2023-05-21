from unidecode import unidecode
from seleniumrequest import seleniumrequest
from databaserequest import databaserequest
import re,time

class naukri(seleniumrequest,databaserequest):
 def __init__(self,display=True):
  super(naukri,self).__init__(display,'linkedin')
 def get(self,*url):
  """url
  get("ai","india",10)
  get(('company abcd,r'http://naukri.com/qt'),('company def',r'http://naukri.com/cpp'))"""
  print(f'{"########################   naukri.get   ######################":^100s}\n{url=!r:^100s}')
  fetchstr_l=[]
  if len(url)==3 and type(url[2])==int and re.search(r'^\s*india\s*$',url[1],flags=re.I):
   for i in range(url[2]):
    print(f'fetching page count {i}')
    super(naukri,self).getlink(r'https://www.naukri.com/'+(re.sub(r'(c\+\+|cpp)','c-plus-plus',url[0],flags=re.I) if re.search(r'(c\+\+|cpp)',url[0],flags=re.I) else 'python' if url[0]=='py' else 'opengl' if url[0]=='gl' else 'kivy' if url[0]=='kv' else 'machine-learning' if url[0]=='ml' else url[0])+'-jobs-in-'+url[1].lower()+('-'+str(i+1) if i else ''),'linkedin')
    #open(url[0]+url[1]+'naukri.txt','w').write(self.webdriverdict['linkedin'].page_source)
    job=self.webdriverdict['linkedin'].find_elements_by_xpath("//div[@class='jobTupleHeader']/div[1]")
    print(f'<=>naukri {len(job)=}')
    if len(job)==0:
     break
    for count,j in enumerate(job):
     href=re.sub(r'^(.*?)\?src=jobsearchDesk\&.*$',r'\1',j.find_element_by_xpath(".//a").get_attribute('href')) if len(j.find_elements_by_xpath(".//a")) else ''
     #print(f'naukri {self.junkextn=} {href=}')
     companyname=unidecode(self.pruneline(re.sub(r'^\s*(.*?)\s*$',r'\1',j.find_element_by_xpath(".//div[contains(@class,'companyInfo')]/a").get_attribute('text')))+self.DELIMITER+url[0]+self.DELIMITER+url[1] if len(j.find_elements_by_xpath(".//div[contains(@class,'companyInfo')]/a")) else '')
     fetchstr_l.append([companyname, href if href and self.validlink(href) else '']) if companyname and self.validlink(self.googlelink(re.split(self.DELIMITER,companyname)[0])) else None
     fetchstr_l[-1].pop() if fetchstr_l and not fetchstr_l[-1][-1] else None
     print(f'^naukri {count} {companyname=}')
#   fetchstr_l.extend([i.get_attribute('href') for i in self.webdriverdict['linkedin'].find_elements_by_xpath("//div[@class='jobTupleHeader']/div/a[1]")])
#   fetchstr_l.extend([i.get_attribute('text') for i in self.webdriverdict['linkedin'].find_elements_by_xpath("//div[@class='mt-7 companyInfo subheading lh16']/a[1]")])
  print(f'naukri {len(fetchstr_l)=}')
  return [list(tup1) for tup1 in {tuple(item) for item in fetchstr_l }]
