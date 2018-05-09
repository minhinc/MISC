import sys
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
 python seed.py delete linkvisited [regexp] name .*minh.*
 python seed.py delete linkvisited date 20180318
 python seed.py update track status 2 email sales@minhinc.com
 python seed.py print track
 python seed.py search track [regex] name .*minh.*''')
if len(sys.argv)<=1:
 usage()
elif re.search('create',sys.argv[1],flags=re.I):
 dbi=databasem.databasec()
 dbi.close()
else:
 dbi=databasem.databasec(False)
 crsr=dbi.conn.cursor()
 if re.search('dump',sys.argv[1],flags=re.I):
  crsr.execute("SHOW TABLES")
  for (table_name,) in crsr:
   print(table_name)
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
  elif re.search('^(qt|qml|gl|c|cpp|py|ldd|li)$',sys.argv[2],flags=re.I):
   dbi.fill(sys.argv[2],((sys.argv[4],),))
   dbi.update(sys.argv[2],'id',int(sys.argv[3]),'id',0)
   if len(sys.argv)>=6:
    dbi.update(sys.argv[2],'value',sys.argv[5],'id',int(sys.argv[3]))
   if len(sys.argv)>=7:
    dbi.update(sys.argv[2],'lab',sys.argv[6],'id',int(sys.argv[3]))
  else:
   for i in range(3,len(sys.argv)):
    dbi.fill(sys.argv[2],((sys.argv[i],),))
    print("inserted into table %s value %s" % (sys.argv[2],sys.argv[i]))
 elif re.search('update',sys.argv[1],flags=re.I):
  dbi.update(sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5],sys.argv[6])
  print("updated table %s field %s value %s" % (sys.argv[2],sys.argv[3],sys.argv[4]))
 elif re.search('print',sys.argv[1],flags=re.I):
  for i in dbi.get(sys.argv[2]):
   print(i)
 elif re.search('search',sys.argv[1],flags=re.I):
  if re.search(r'reg',sys.argv[3],flags=re.I):
   if dbi.search(sys.argv[2],sys.argv[5],sys.argv[4],regex=True):
    print(dbi.get(sys.argv[2],'*',sys.argv[4],sys.argv[5],regex=True))
  else:
   if dbi.search(sys.argv[2],sys.argv[4],sys.argv[3]):
    print(str(dbi.get(sys.argv[2],'*',sys.argv[3],sys.argv[4])).replace('\\n','\n').replace(", '",", \n'"))
 dbi.close()
