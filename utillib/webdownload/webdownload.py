from abc import ABC, abstractmethod
import os,sys,re;sys.path.append('/home/pi/tmp')
from MISC.extra.config import _configi as print

class _webdownloadc(ABC):
# browserhash={'lynx':_lynxi}
 browserhash={}

# @abstractmethod
 def getdata(self,*,url_,browser_='lynx',**kwarg):
  '''browser_(s) browser application to searched,i.e. lynx, chrome (lynx)
url_(s) url of the page to be browsed'''
  print(f'>< {url_=} {kwarg=}')
  return _webdownloadc.browserhash[browser_].getdata(url_=url_,**kwarg)

 def getemail(self,text_):
  return [x.lower() for x in re.findall(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,6}\b",text_) if not re.search(r'(\.{2,}|@\.|\.@)',x)]

 def googlelink(self,searchtext_,pagecount_=0):
  return r'https://www.google.com/search?q='+re.sub(r'\s+','+',searchtext_)+('' if not pagecount_ else fr'&start={pagecount_*20}')

from MISC.extra.config import _configi;_configi.cmc(__name__,_webdownloadc)
from MISC.utillib.webdownload.lynx import _lynxi
_webdownloadi.browserhash['lynx']=_lynxi
