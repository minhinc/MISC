from machinelearningrequest import machinelearningrequest
from seleniumrequest import seleniumrequest
from databaserequest import databaserequest
import datetime
import re,os,glob
import fetcher

class google(seleniumrequest,databaserequest,machinelearningrequest):
 def __init__(self,display=True):
  super(google,self).__init__(display,'linkedin')
  self.fetcher=fetcher.fetcher()
 def get(self,*url):
  """uRl
  get("companyx france",r"http://lotusinc.com/","companyy nigeria",r"http://asadtech.com/")"""
  companylink=None
  print(f'{"########### google.get ###############":^100}\n{url=!r:^100}')
  file=None
  if not (len(url)==3 and type(url[2])==int):
   [os.remove(x) for x in glob.glob(r'*_email.txt')]
   file=open(re.sub(':','-',datetime.datetime.now().isoformat())+'_email.txt','w')
   for count,i in enumerate(url[:]):
    self.getlink(self.googlelink(re.split(self.DELIMITER,i[0])[0]+' '+self.getmatching(re.split(self.DELIMITER,i[0])[2],*re.findall(r'^.*?#(.*)?\s+[.]\w{2}',open('data/country.txt').read(),flags=re.M),muteprint=True)[0]),'linkedin') if companylink==None else None
    url[count].extend([x for x in set([re.sub(r'^(.*?)/+$',r'\1',x.get_attribute('href')) for x in self.webdriverdict['linkedin'].find_elements_by_xpath("//div[@class='yuRUbf']/a[1]")]) if self.validlink(x)]) if companylink==None else url[count].extend(companylink)
    companylink=self.fetcher.get(i,file=file,companyname=url[count+1][0] if (count+1)<len(url) else None) if len(i)>1 else print(f'google fetcher not called')
    print(f'google fetcher processed {count+1}/{len(url)} {i=}')
   file.close()
  return []
 def quitfetcherthread(self):
  self.fetcher.quitthread()
