import MySQLdb
import sys
import re
import databasem
def _id_(db,country):
 if not country.isdigit():
  return db.get('country','id','name',country)[0][0]
 else:
  return int(country)
if len(sys.argv)<=2:
  print("usage\npython seed.py drop blocked visitedlink\npython seed.py insert city \"Los Angles,United State Of Americas\"\n")
  exit(-1)
if re.search('create',sys.argv[1],flags=re.I):
 dbi=databasem.databasec()
else:
 dbi=databasem.databasec(False)
 crsr=dbi.conn.cursor()
 if re.search('dump',sys.argv[1],flags=re.I):
  crsr.execute("SHOW TABLES")
  for (table_name,) in crsr:
   print(table_name)
 elif re.search('drop',sys.argv[1],flags=re.I):
  for i in range(2,len(sys.argv)):
   print("i %d" % i)
   crsr.execute("DROP TABLE IF EXISTS %s" % (sys.argv[i],))
 elif re.search('trun',sys.argv[1],flags=re.I):
  for i in range(2,len(sys.argv)):
   crsr.execute("TRUNCATE TABLE %s" % (sys.argv[2],))
 elif re.search('delete',sys.argv[1],flags=re.I):
  crsr.execute("DELETE FROM %s WHERE %s='%s'" % (sys.argv[2],sys.argv[3],sys.argv[4]))
 elif re.search('insert', sys.argv[1],flags=re.I):
  if re.search('city', sys.argv[2],flags=re.I):
   for i in range(3,len(sys.argv)):
    dbi.fill('city',((re.sub(r'^([^,]+),.*',r'\1',sys.argv[i]).lower(),_id_(dbi,re.sub(r'^[^,]+,(.*)$',r'\1',sys.argv[i]).lower())),))
    print("%s - %d" % (re.sub(r'^([^,]+),.*',r'\1',sys.argv[i]),_id_(dbi,re.sub(r'^[^,]+,(.*)$',r'\1',sys.argv[i]).lower())))
  elif re.search('country',sys.argv[2],flags=re.I):
   for i in range(3,len(sys.argv)):
    print("adding %s %s" % (i,sys.argv[i]))
    dbi.fill('country',((sys.argv[i].lower(),),))
    print("update %s %s" % (i,sys.argv[i]))
    dbi.update('country','id',i-2,'id',0)
  else:
   for i in range(3,len(sys.argv)):
    dbi.fill(sys.argv[2],((sys.argv[i].lower(),),))
    print("%d - %s" % (i,sys.argv[i]))
 elif re.search('update',sys.argv[1],flags=re.I):
  dbi.update(sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5],sys.argv[6])
 elif re.search('print',sys.argv[1],flags=re.I):
  for i in dbi.get(sys.argv[2]):
   print(i)
dbi.close()
