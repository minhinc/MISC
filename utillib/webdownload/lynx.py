import os,sys,re;sys.path.append('/home/pi/tmp')
from MISC.utillib.webdownload.webdownload import _webdownloadc
from MISC.extra.config import _configi as print

class _lynxc(_webdownloadc):
 def getdata(self,*,url_,**kwarg):
  '''url_(s) url of the page to be downloaded
kwarg(d) dictionary with keyword mode=[-source|-dump] (-source)'''
  print(f'>< {url_=} {kwarg=}')
  mode='-source'
  if 'mode' in kwarg:
   mode=kwarg['mode']
  stream=os.popen(f'lynx {mode} {url_}')
  stream._stream.reconfigure(encoding='latin', newline="") # Now the stream is configured in the encoding 'latin'
  return stream.read()
from MISC.extra.config import _configi;_configi.cmc(__name__,_lynxc)
