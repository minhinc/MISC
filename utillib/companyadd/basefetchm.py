import urllib.request as urllib2
class basefetchc:
 def __init__(self,namep):
  self.name=namep
 def download(self,link):
#  print("link %s" % link)
  return repr(urllib2.urlopen(urllib2.Request(link,headers={'User-Agent': 'Mozilla/44.0.2'}),timeout=90).read().decode('utf-8'))
