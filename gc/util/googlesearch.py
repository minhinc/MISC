import re
import urllib.request as urllib2

#  data=repr(urllib2.urlopen(urllib2.Request('https://www.google.co.in/search?q='+re.sub('\s+','+',line)+r'&btnG=Search',headers={'User-Agent': 'Mozilla/44.0.2'}),timeout=90).read())
#  data=repr(utili.download('https://www.google.co.in/search?q='+re.sub('\s+','+',line)))

def download(searchstring,pagecount):
 return repr(urllib2.urlopen(urllib2.Request(r'http://www.google.com/search?source=hp&ei=zR1UW_zFCpv8rQGCkYiwAw&q='+re.sub('\s+','+',searchstring)+(r'&start='+str(pagecount*10) if pagecount else '')+r'&oq='+re.sub('\s+','+',searchstring),headers={'User-Agent': 'Mozilla/44.0.2'}),timeout=90).read().decode('utf-8'))

def getlinklist(searchstring,pagecount):
 linklist=[]
 for i in range(0,pagecount):
  linklist.extend(re.findall(r'url\?q=(http[^&]+)',download(searchstring,i)))
 return linklist  

def getcompanylist(searchstring,pagecount):
 linklist=[]
 for i in range(0,pagecount):
#  linklist.extend(re.findall(r'url\?q=https?://(?:www[.])?((?:\w+[.]?)+)[.]\w+[&/]',download(searchstring,i),flags=re.I))
  linklist.extend(re.findall(r'url\?q=https?://(?:www[.])?((?:[a-zA-Z0-9._%-]+[.]?)+)+?[&/]?',download(searchstring,i),flags=re.I))
 return linklist
