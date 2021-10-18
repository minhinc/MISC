import sys
import time
import os
import re
if re.search(r'^(win|cygwin)',sys.platform,flags=re.I):
 import pymysql
 pymysql.install_as_MySQLdb()
import MySQLdb
import databasem
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
 python seed.py insert junkextension .*[.]doc$
 python seed.py insert country 101 "United State Of Americas"
 python seed.py insert city 101 "Los Angles,United State Of Americas"
 python seed.py insert gl 101 "OpenGL integration with Qt"
 python seed.py delete linkvisited [regexp] name .*minh.*
 python seed.py delete linkvisited date 20180318
 python seed.py update track status 2 email sales@minhinc.com
 python seed.py print <tablename> i.e. "print track" or "print"
 python seed.py push [<tablename>] <datafilename> i.e. "push qt data.txt" or "push data.txt"
 python seed.py search track [regex] name .*minh.*''')
if len(sys.argv)<=1:
 usage()
elif re.search('create',sys.argv[1],flags=re.I):
 dbi=databasem.databasec()
 dbi.close()
else:
 dbi=databasem.databasec(False)
 try:
  crsr=dbi.conn.cursor()
 except Exception as e:
  print('e.type',type(e))
 if re.search('dump',sys.argv[1],flags=re.I):
  crsr.execute("SHOW TABLES")
  for (table_name,) in crsr:
   print(table_name)
 elif re.search('push',sys.argv[1],flags=re.I):
  tempvar1=None
  selectq=None
  tbl=dict()
  [tbl.__setitem__(re.sub(r'^(\w+).*$',r'\1',i[0]),re.findall(r'(\w+)\s+(\w*CHAR|\w*INT|\w*TEXT|\w*BLOB)',i[1])) for i in re.findall('CREATE TABLE.*?(\w+)\s*\((.*?)\)"\s*\)',open('databasem.py').read())]
  print('tbl',tbl)
  with open(sys.argv[2 if len(sys.argv)<=3 else 3]) as file:
   for line in [line.strip('\n') for line in file]:
    if re.search(r'^(database re-connected|\s*$)',line,flags=re.I):
     continue
    if re.search(r'^[ ]+\w+',line):
     tempvar1=re.sub(r'^\s*(\w+).*$',r'\1',line,flags=re.I)
     if len(sys.argv)>3 and not re.search(r'^'+tempvar1+r'$',sys.argv[2],flags=re.I):
      tempvar1=None
     else:
      selectq=f'INSERT INTO {tempvar1}('+','.join(i[0] for i in tbl[tempvar1])+r') VALUES('+('%s,'*len(tbl[tempvar1]))[:-1]+r')'
      print(f'truncating {tempvar1}')
      crsr.execute("TRUNCATE TABLE %s" % (tempvar1,))
     continue
    if tempvar1:
     splitline=re.split('!ABS SBA!',line)
     col=[int(re.sub(r'^[\'"]?(.*?)[\'"]?$',r'\1',splitline[i]).encode('utf-8').decode('unicode_escape')) if tbl[tempvar1][i][1]=='INT' else re.sub(r'^[\'"]?(.*?)[\'"]?$',r'\1',splitline[i]).encode('utf-8').decode('unicode_escape') for i in range(len(splitline))]
     crsr.execute(selectq,col)
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
    dbi.update('tech','content',re.sub(r'(.*"youtube"\s*:\s*).*?(,?\s*\n.*)',r'\1'+json.dumps(jsonstring)+r'\2',youtubecontent,flags=re.DOTALL|re.I),'name',sys.argv[3])
  if not fileexists: driver.close()
 elif re.search('print',sys.argv[1],flags=re.I):
  tempvar1=None
  if len(sys.argv)>2:
#   tempvar1=sys.argv[2:]
   tempvar1=sys.argv[2:3]
  else:
   crsr.execute('SHOW TABLES')
   tempvar1=[i[0] for i in crsr]
  for i in tempvar1:
   print(f'      {i}      ')
   for j in dbi.get(i):
    if len(sys.argv)>3:
     print([j[int(x)] for x in sys.argv[3:]])
    else:
     print(repr('!ABS SBA!'.join(str(k) if type(k)!=str else k for k in j)))
 elif len(sys.argv)<=2:
  usage()
 elif re.search('drop',sys.argv[1],flags=re.I):
  for i in range(2,len(sys.argv)):
   crsr.execute("DROP TABLE IF EXISTS %s" % (sys.argv[i],))
   print("dropped table %s" % sys.argv[i])
 elif re.search('trun',sys.argv[1],flags=re.I):
  for i in range(2,len(sys.argv)):
   crsr.execute("TRUNCATE TABLE %s" % (sys.argv[2],))
   print("truncated table %s" % sys.argv[i])
 elif re.search('delete',sys.argv[1],flags=re.I):
  if re.search(r'(reg|rgx)',sys.argv[3],flags=re.I):
   for i in range(5,len(sys.argv)):
    crsr.execute("DELETE FROM %s WHERE %s REGEXP '%s'" % (sys.argv[2],sys.argv[4],sys.argv[i]))
    print("deleted from table %s field %s value %s" % (sys.argv[2],sys.argv[4],sys.argv[i]))
  else:
   for i in range(4,len(sys.argv)):
    crsr.execute("DELETE FROM %s WHERE %s='%s'" % (sys.argv[2],sys.argv[3],sys.argv[i]))
    print("deleted from table %s field %s value %s" % (sys.argv[2],sys.argv[3],sys.argv[i]))
 elif re.search('insert', sys.argv[1],flags=re.I):
  if re.search('city', sys.argv[2],flags=re.I):
   for i in range(4,len(sys.argv)):
    dbi.fill('city',((re.sub(r'^([^,]+),.*',r'\1',sys.argv[i]).lower(),_id_(dbi,re.sub(r'^[^,]+,(.*)$',r'\1',sys.argv[i]).lower())),))
    dbi.update('city','id',int(sys.argv[3])+i-4,'name',re.sub(r'^([^,]+),.*',r'\1',sys.argv[i]).lower())
    print("%s - %d" % (re.sub(r'^([^,]+),.*',r'\1',sys.argv[i]),_id_(dbi,re.sub(r'^[^,]+,(.*)$',r'\1',sys.argv[i]).lower())))
  elif re.search('country',sys.argv[2],flags=re.I):
   for i in range(4,len(sys.argv)):
    dbi.fill('country',((sys.argv[i],),))
    dbi.update('country','id',int(sys.argv[3])+i-4,'id',0)
    print("inserted into country %s" % sys.argv[i])
  elif re.search('^(qt|qml|gl|c|cpp|py|ldd|li|dp|ai|headername)$',sys.argv[2],flags=re.I):
   dbi.fill(sys.argv[2],((sys.argv[4],),))
   dbi.update(sys.argv[2],'id',int(sys.argv[3]),'id',0)
   if len(sys.argv)>=6:
    dbi.update(sys.argv[2],'value',sys.argv[5],'id',int(sys.argv[3]))
   if len(sys.argv)>=7:
    dbi.update(sys.argv[2],'lab',sys.argv[6],'id',int(sys.argv[3]))
  elif len(sys.argv)<=3:
   dbi.fill(sys.argv[2])
   print('inserted empty row in table')
  else:
   for i in range(3,len(sys.argv)):
    dbi.fill(sys.argv[2],((sys.argv[i],),))
    print("inserted into table %s value %s" % (sys.argv[2],sys.argv[i]))
 elif re.search('update',sys.argv[1],flags=re.I):
  dbi.update(sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5],sys.argv[6])
  print("updated table %s field %s value %s for %s = %s" % (sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5],sys.argv[6]))
 elif re.search('search',sys.argv[1],flags=re.I):
  if re.search(r'reg',sys.argv[3],flags=re.I):
   if dbi.search(sys.argv[2],sys.argv[5],sys.argv[4],regex=True):
    print(dbi.get(sys.argv[2],'*',sys.argv[4],sys.argv[5],regex=True))
  else:
   if dbi.search(sys.argv[2],sys.argv[4],sys.argv[3]):
#    print(str(dbi.get(sys.argv[2],'*',sys.argv[3],sys.argv[4])).replace('\\n','\n').replace(", '",", \n'"))
#    print(str(dbi.get(sys.argv[2],'*',sys.argv[3],sys.argv[4])).replace(r'\\',"!double escape!").replace(r'\n','\n').replace('!double escape!',r'\\'))
    print(str(dbi.get(sys.argv[2],'*',sys.argv[3],sys.argv[4])).encode('utf-8').decode('unicode_escape'))
 dbi.close()
