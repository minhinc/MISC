import re
import sys
from databasem import databasec

sys.path.append('./testdir')
from testdir import *
import testdir


if len(sys.argv)<=5:
 print(''' ---usage---
 python3 getcontactm_c.py "South Africa" za Qt 5 [<file>]
 python3 getcontactm_c.py "South Africa" za all 5''') # 5->pages

filename='test.txt' if len(sys.argv)<=5 else sys.argv[5]
file=open(filename,'w')
db=databasec(False)
for fetcher in [eval(fetcher)() for fetcher in testdir.__all__]:
 file.write("#################\n")
 file.write("## "+fetcher.name+"\n")
 file.write("#################\n")
 print("## "+fetcher.name)
 for i in fetcher.process():
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
  if not db.search('linkvisited',re.sub(r'[^a-zA-Z0-9._%-]','_','https://www.google.co.in/search?q='+re.sub('\s+','+',i)+r'&btnG=Search'),'name'):
   file.write(i+'\n')
   print(i)
db.close()
file.close()
