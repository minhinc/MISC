import os,sys;sys.path.append(os.path.expanduser('~')+r'/tmp')
import time
import re
from MISC.utillib.util import Util
from MISC.ffmpeg.libm import libc
if re.search(r'^(win|cygwin)',sys.platform,flags=re.I):
 import pymysql
 pymysql.install_as_MySQLdb()
import MySQLdb
import MISC.utillib.databasem as databasem
libi=libc()
def _id_(db,country):
 if not country.isdigit():
  return db.get('country','id','name',country)[0][0]
 else:
  return int(country)
def usage():
 print(''' ---usage---
 python seed.py create # create tables
 python seed.py dump # show tables
 python seed.py trunc junkextension visitedlink
 python seed.py drop junkextension visitedlink
 python seed.py insert junkextension "0,.*[.]doc$"
 python seed.py insert country "101,United State Of Americas"
 python seed.py insert gl "((101,Introduction, , ),(102,OpenGL integration with Kivy, , ))"
 python seed.py delete linkvisited name R .*minh.* #regexp
 python seed.py delete linkvisited date = 20180318
 python seed.py update track status 2 email = sales@minhinc.com
 python seed.py print [<tablename>] i.e. "print track" or "print"
 python seed.py push [<tablename>] <datafilename> i.e. "push qt data.txt" or "push data.txt"
 python seed.py search track name R .*minh.*''')
if len(sys.argv)<=1:
 usage()
elif re.search('create',sys.argv[1],flags=re.I):
 dbi=databasem.databasec(True)
 dbi.close()
else:
 dbi=databasem.databasec(False)
 if re.search('dump',sys.argv[1],flags=re.I):
  for (table,) in dbi.search2('',mode='showtables'):
   print(table)
 elif re.search('push',sys.argv[1],flags=re.I):
  tabledict=dict([(x[0],re.sub(r'^\n','',x[1])) for x in re.findall(r'(?:^|\n)[ \t]+(\w+)[ \t]+(.*?)(?=\n\s+|$)',open(sys.argv[2 if len(sys.argv)==3 else 3]).read(),flags=re.DOTALL)])
  if len(sys.argv)>3:
   tabledict=dict([(sys.argv[2],tabledict[sys.argv[2]])])
  print(f'push {tabledict.keys()=}')
  for i in tabledict:
   print(f'<=>push truncating {i=}')
   dbi.search2(i,mode='trunc')
   dbi.search2(i,*[[Util.converttolatin1(x) for x in re.split(Util.DELIMITER,eval(line))] for line in re.split('\n',tabledict[i]) if line],mode='insertbulk')
 elif re.search('youtube',sys.argv[1],flags=re.I):
  from selenium import webdriver
  import json
  fileexists=False
  driver=None
  if os.path.isfile('r.txt') and int(time.time()-os.stat('r.txt').st_mtime)<3600:
   fileexists=True
   print("--File r.txt exists in current directory---")
  if not fileexists:
   driver=webdriver.Chrome()
   driver.get('https://www.youtube.com/channel/UChmiKM2jr7e9iUOrVPKRTXQ/videos')
   for i in range(20):
    driver.execute_script("window.scrollBy(0,250)")
    print("window scroll {}".format(i))
    time.sleep(1)
   open('r.txt','w').write(driver.page_source)
  jsonstring=[]
  for i in [(re.sub(r'.*title="([^"]*)".*',r'\1',i),re.sub(r'.*href="/watch\?v=([^"]*)".*',r'\1',i)) for i in re.findall(r'title=".*href="/watch\?v=[^"]*"',open('r.txt').read() if fileexists else driver.page_source)]:
   if len(sys.argv)>2: 
    if re.search(r'^('+sys.argv[2]+r')',i[0],flags=re.I):
     jsonstring.append([i[0],i[1]])
   else:
    jsonstring.append([i[0],i[1]])
  print(json.dumps(jsonstring))
  if len(sys.argv)>3:
   youtubecontent=re.sub(r'.*?({.*}).*',r'\1',str(dbi.get('tech','content','name',sys.argv[3])).replace('\\n','\n').replace(", '",", \n'"),flags=re.DOTALL|re.I)
   if re.search(r'"youtube"\s*:',youtubecontent,flags=re.I):
    dbi.search2('tech','content',re.sub(r'(.*"youtube"\s*:\s*).*?(,?\s*\n.*)',r'\1'+json.dumps(jsonstring)+r'\2',youtubecontent,flags=re.DOTALL|re.I),'name','=',sys.argv[3],mode='update')
  if not fileexists: driver.close()
 elif re.search('print',sys.argv[1],flags=re.I):
  for i in ((sys.argv[2],) if len(sys.argv)>=3 else [x[0] for x in dbi.search2('',mode='showtables')]):
   print('      '+i+'      ')
#   [print(Util.converttolatin1(Util.DELIMITER.join(str(y) if type(y)==int else y for y in x))) for x in dbi.search2(i,'*','name','R','.*',mode='get')]
   [print(repr(Util.DELIMITER.join(str(y) if type(y)==int else y for y in x))) for x in dbi.search2(i,'*',mode='get')]
#   for i in [Util.converttolatin1(Util.DELIMITER.join(str(y) if type(y)==int else y for y in x)) for x in dbi.search2(i,'*','name','R','.*',mode='get')]:
#    print(i)
#    print(eval(repr(i)))
 elif len(sys.argv)<=2:
  usage()
 elif sys.argv[1] in ['drop','trunc']:
  [dbi.search2(table,mode=sys.argv[1]) for table in sys.argv[2:]]
  print(f'dropped table(s) {sys.argv[2:]}')
 elif re.search('delete',sys.argv[1],flags=re.I):
  print(dbi.search2(*sys.argv[2:],mode='delete'))
 elif re.search('insert', sys.argv[1],flags=re.I):
  tmptuple=libi.str2tuple(sys.argv[3])
  print(f'{tmptuple=} {len(tmptuple)=}')
  print(dbi.search2(sys.argv[2],*tmptuple,mode=('insert' if not type(tmptuple)=='tuple' else 'insertbulk')))
 elif re.search('update',sys.argv[1],flags=re.I):
  print(dbi.search2(sys.argv[2],sys.argv[3],Util.converttolatin1(sys.argv[4]),*sys.argv[5:],mode='update'))
 elif re.search('search',sys.argv[1],flags=re.I):
  print(dbi.search2(*sys.argv[2:],mode='search'))
 elif re.search('get',sys.argv[1],flags=re.I):
#  print(dbi.search2(*sys.argv[2:],mode='get')[0][Slice() if sys.argv[2]=='*' else 0])
  print(dbi.search2(*sys.argv[2:],mode='get')[0][sys.argv[3]=='*' and slice(0,None) or 0])
