import time
import os
import re
import datetime
import sys
import urllib.request as urllib2
import databasem
#import urllib2#for python2.7
if len(sys.argv)!=5:
 print(''' ---usage---
 python3 getcontactm_c.py "South Africa" za Qt 5
 python3 getcontactm_c.py "South Africa" za all 5''') # 5->pages
trycount=page=0
fetchstr=[]
tech='keywords='+sys.argv[3] if sys.argv[3] != 'all' else ''
while page<int(sys.argv[4]) and trycount<8:
 try:
  for i in [re.sub(r',"companyName":"([^"]*)","formattedLocation":"([^"]*)",','\\1 \\2',name) for name in re.findall(r',"companyName":"[^"]*","formattedLocation":"[^"]*",',repr(urllib2.urlopen(urllib2.Request('https://www.linkedin.com/jobs/search/?'+tech+'&location='+re.sub(r'\s','%20',sys.argv[1])+'&locationId='+sys.argv[2]+'%3A0&start='+str(page*25),headers={'User-Agent': 'Mozilla/44.0.2'}),timeout=90).read().decode('utf-8')))]:
#  for i in [re.sub(r',"companyName":"([^"]*)","formattedLocation":"([^"]*)",','\\1 \\2',name) for name in re.findall(r',"companyName":"[^"]*","formattedLocation":"[^"]*",',repr(urllib2.urlopen(urllib2.Request('https://www.linkedin.com/jobs/search/?'+tech+'&location='+re.sub(r'\s','%20',sys.argv[1])+'&locationId='+sys.argv[2]+'&start='+str(page*25),headers={'User-Agent': 'Mozilla/44.0.2'}),timeout=90).read().decode('utf-8')))]:
   i=re.sub(r'(â|ā|á|ą|ã|à|å|à|ä|å|æ|Ā|Ã|Ä|À|Á|Â|Ã|Ä|Å|Æ)','a',i)
   i=re.sub(r'(ç|Ç)','c',i)
   i=re.sub(r'Ð','d',i)
   i=re.sub(r'(é|è|ě|ê|ë|É|È|É|Ê|Ë)','e',i)
   i=re.sub(r'ẖ','h',i)
   i=re.sub(r'(í|ì|ï|ī|î|İ|Í|Ì|Í|Î|Ï)','i',i)
   i=re.sub(r'(Ł|ł)','l',i)
   i=re.sub(r'(ñ|ń|Ñ)','n',i)
   i=re.sub(r'(ö|Ō|ó|ô|õ|ò|Ó|Ö|Ò|Ó|Ô|Õ|Ö)','o',i)
   i=re.sub(r'ř','r',i)
   i=re.sub(r'(ü|ú|Ù|Ú|Û|Ü|ù)','u',i)
   i=re.sub(r'ş','s',i)
   i=re.sub(r'(ý|ÿ)','y',i)
   i=re.sub(r'ź','z',i)
   i=re.sub(r'(Ø|ø)','0',i)
   fetchstr.append(i)
 except:
  time.sleep(1)
  trycount=trycount+1
  print("trying... page,trycount %s,%s" % (page,trycount))
 else:
  page=page+1
  trycount=0
  print("incrementing page to %s" % page)
fetchstr=list(set(fetchstr))
print('\n'.join(fetchstr))
open('test.txt','w').write('\n'.join(fetchstr))
db=databasem.databasec(False)
mail=[]
junkextn=r'^('+(''.join([x[0]+'|' for x in db.get('junkextension')]))[:-1]+')$'
junkemail=r'^('+(''.join([x[0]+'|' for x in db.get('junkemail')]))[:-1]+')$'
for line in [ line for line in fetchstr if not db.search('linkvisited',re.sub(r'[^a-zA-Z0-9._%-]','_','https://www.google.co.in/search?q='+re.sub('\s+','+',line)+r'&btnG=Search',flags=re.I)) ]:
 try:
  data=repr(urllib2.urlopen(urllib2.Request('https://www.google.co.in/search?q='+re.sub('\s+','+',line)+r'&btnG=Search',headers={'User-Agent': 'Mozilla/44.0.2'}),timeout=90).read())
  db.fill('linkvisited',((re.sub(r'[^a-zA-Z0-9._%-]','_','https://www.google.co.in/search?q='+re.sub('\s+','+',line)+r'&btnG=Search'),),))
  db.update('linkvisited','date',int(re.sub('-','',datetime.date.today().isoformat())),'name',re.sub(r'[^a-zA-Z0-9._%-]','_','https://www.google.co.in/search?q='+re.sub('\s+','+',line)+r'&btnG=Search'))
  for x in [ x for x in re.findall(r'url\?q=(http[^&]+)',data) if not db.search('linkvisited',re.sub(r'[^a-zA-Z0-9._%-]','_',x,flags=re.I)) and not re.search(junkextn,x,flags=re.I)]:
   print(" %s" % x)
   try:
    mail.extend([ x for x in re.findall(r'([A-Za-z0-9._%-]+\@\w+[.](?:\w+[.]?)*\b)',repr(urllib2.urlopen(urllib2.Request(x,headers={'User-Agent': 'Mozilla/44.0.2'}),timeout=10).read())) if not re.search(junkemail,x,flags=re.I) ])
   except:
    print(' error:'+x)
  db.fill('linkvisited',[ (re.sub(r'[^a-zA-Z0-9._%-]','_',x),int(re.sub('-','',datetime.date.today().isoformat()))) for x in re.findall(r'url\?q=(http[^&]+)',data) if not db.search('linkvisited',re.sub(r'[^a-zA-Z0-9._%-]','_',x,flags=re.I)) and not re.search(junkextn,x,flags=re.I) ],fetchmany=True)
 except:
  print('google error')
 if len(set(mail)):
  if len(set(mail))<100:
   print('#'+re.sub(r'(^\s*|\s*$)','',line)+' '+str(fetchstr.index(line)+1)+'/'+str(len(fetchstr))+'\n'+' '.join(set(mail)))
   with open('test_people.txt','a') as file:
    file.write("%s%s" % ('\n' if os.stat('test_people.txt').st_size else '',re.sub(r'(^\s*|\s*$)','',line)+' '+' '.join(set([x.lower() for x in mail]))))
  else:
   print('--not included--#'+re.sub(r'(^\s*|\s*$)','',line)+'\n'+' '.join(set(mail)))
 mail=[]
