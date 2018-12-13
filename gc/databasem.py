import os
import datetime
import re
import sys
if re.search(r'^(win|cygwin).*',sys.platform,flags=re.I):
 import pymysql
 pymysql.install_as_MySQLdb()
import MySQLdb
import time
class databasec:
 def __init__(self,ct=True): #ct-createtable
  self.conn=None
  self.cc=0#connection count
  self.reconnect()
  if(ct):
   self.create()
 def create(self):
  crsr=self.conn.cursor()
  crsr.execute("CREATE TABLE IF NOT EXISTS track (email VARCHAR(80) NOT NULL PRIMARY KEY, uuid VARCHAR(80), company_id INT, tech_id INT, city_id INT, country_id INT, expire INT, status INT DEFAULT 0, message INT DEFAULT 0)") #status 0 normal, 1-registered, 2-unregistered, 3-senderror message-unregistration reason
  crsr.execute("CREATE TABLE IF NOT EXISTS company (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT, name VARCHAR(240), phone VARCHAR(80), UNIQUE(name))")
  crsr.execute("CREATE TABLE IF NOT EXISTS city (id INT  DEFAULT 0, name VARCHAR(80), country INT, PRIMARY KEY(name,country),FOREIGN KEY(country) REFERENCES country(id))")
  crsr.execute("CREATE TABLE IF NOT EXISTS tech (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT, name VARCHAR(80), content VARCHAR(40900), UNIQUE(name))")
  crsr.execute("CREATE TABLE IF NOT EXISTS country (id INT DEFAULT 0 PRIMARY KEY, name VARCHAR(80),UNIQUE(name))")

  crsr.execute("CREATE TABLE IF NOT EXISTS message (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT, name VARCHAR(80))")
  crsr.execute("CREATE TABLE IF NOT EXISTS resume (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT, name VARCHAR(80), uuid VARCHAR(80), email VARCHAR(80), phone VARCHAR(80), address VARCHAR(280), UNIQUE(email))")

  crsr.execute("CREATE TABLE IF NOT EXISTS linkvisited (name VARCHAR(360) NOT NULL PRIMARY KEY,date INT)")
  crsr.execute("CREATE TABLE IF NOT EXISTS junkemail (name VARCHAR(80) NOT NULL PRIMARY KEY)")
  crsr.execute("CREATE TABLE IF NOT EXISTS junkextension (name VARCHAR(80) NOT NULL PRIMARY KEY)")

  crsr.execute("CREATE TABLE IF NOT EXISTS qt (id INT NOT NULL DEFAULT 0 PRIMARY KEY, name VARCHAR(80) NOT NULL, value VARCHAR(960), lab VARCHAR(480), content VARCHAR(90000), UNIQUE(id))")
  crsr.execute("CREATE TABLE IF NOT EXISTS qml (id INT NOT NULL DEFAULT 0 PRIMARY KEY, name VARCHAR(80) NOT NULL, value VARCHAR(960), lab VARCHAR(480), content VARCHAR(90000), UNIQUE(id))")
  crsr.execute("CREATE TABLE IF NOT EXISTS c (id INT NOT NULL DEFAULT 0 PRIMARY KEY, name VARCHAR(80) NOT NULL, value VARCHAR(960), lab VARCHAR(480), content VARCHAR(90000), UNIQUE(id))")
  crsr.execute("CREATE TABLE IF NOT EXISTS cpp (id INT NOT NULL DEFAULT 0 PRIMARY KEY, name VARCHAR(80) NOT NULL, value VARCHAR(960), lab VARCHAR(480), content VARCHAR(90000), UNIQUE(id))")
  crsr.execute("CREATE TABLE IF NOT EXISTS gl (id INT NOT NULL DEFAULT 0 PRIMARY KEY, name VARCHAR(80) NOT NULL, value VARCHAR(960), lab VARCHAR(480), content VARCHAR(90000), UNIQUE(id))")
  crsr.execute("CREATE TABLE IF NOT EXISTS py (id INT NOT NULL DEFAULT 0 PRIMARY KEY, name VARCHAR(80) NOT NULL, value VARCHAR(960), lab VARCHAR(480), content VARCHAR(90000), UNIQUE(id))")
  crsr.execute("CREATE TABLE IF NOT EXISTS li (id INT NOT NULL DEFAULT 0 PRIMARY KEY, name VARCHAR(80) NOT NULL, value VARCHAR(960), lab VARCHAR(480), content VARCHAR(90000), UNIQUE(id))")
  crsr.execute("CREATE TABLE IF NOT EXISTS ldd (id INT NOT NULL DEFAULT 0 PRIMARY KEY, name VARCHAR(80) NOT NULL, value VARCHAR(960), lab VARCHAR(480), content VARCHAR(90000), UNIQUE(id))")
  crsr.execute("CREATE TABLE IF NOT EXISTS dp (id INT NOT NULL DEFAULT 0 PRIMARY KEY, name VARCHAR(80) NOT NULL, value VARCHAR(960), lab VARCHAR(480), content VARCHAR(90000), UNIQUE(id))")

#data in html
  crsr.execute("CREATE TABLE IF NOT EXISTS headername (id INT NOT NULL DEFAULT 0 PRIMARY KEY, name VARCHAR(80) NOT NULL, value VARCHAR(160), content VARCHAR(40960), UNIQUE(name))")

  print('table created')
  self.conn.commit()
 def reconnect(self):
  try:
#   self.conn=MySQLdb.connect(host='166.62.28.143',user='minhinc',passwd='pinku76minh',db='trackweb')
   self.conn=MySQLdb.connect(host=re.split('\n',open(os.path.expanduser('~/passwd')).read())[0],user=re.split('\n',open(os.path.expanduser('~/passwd')).read())[1],passwd=re.split('\n',open(os.path.expanduser('~/passwd')).read())[2],db=re.split('\n',open(os.path.expanduser('~/passwd')).read())[3])
   print('database re-connected')
  except:
   print('database could not be connected')
   return False
  else:
   self.cc=self.cc+1
   if self.cc>4:
    print("number of retry %s" % self.cc)
    return False
   return True
 def fill(self,table,primary,fetchmany=False):
  try:
   crsr=self.conn.cursor()
   if fetchmany:
    if table=='linkvisited':
     crsr.executemany("INSERT INTO linkvisited(name,date) VALUES(%s,%s)",primary)
   else:
    for rowprimary in primary:
     if(table=='track'):
      [self.update('track','tech_id',int(rowprimary[3]),'email',rowprimary[0]) for rowprimary in primary if crsr.execute("SELECT COUNT(*) FROM track WHERE email='%s' and tech_id!='%d' and status<2" % (rowprimary[0],int(rowprimary[3]) )) and crsr.fetchone()[0] != 0]
#       [self.delete('track','email',rowprimary[0]) for rowprimary in primary if crsr.execute("SELECT COUNT(*) FROM track WHERE email='%s' and tech_id!='%d' and status<2" % (rowprimary[0],int(rowprimary[3]) )) and crsr.fetchone()[0] != 0]
      [crsr.execute("INSERT INTO track(email,uuid,company_id,tech_id,city_id,country_id,expire) VALUES('%s','%s','%d','%d','%d','%d','%d')" % rowprimary) for rowprimary in primary if crsr.execute("SELECT COUNT(*) FROM track WHERE email='%s'" % (rowprimary[0], )) and crsr.fetchone()[0] == 0]
     elif(table=='city'):
       [crsr.execute("INSERT INTO city(name,country) VALUES('%s','%d')" % rowprimary) for rowprimary in primary if crsr.execute("SELECT COUNT(*) FROM city WHERE name='%s' and country='%d'" % (rowprimary[0],rowprimary[1] )) and crsr.fetchone()[0] == 0]
     elif re.search(r'^(qt|qml|py|gl|c|cpp|ldd|li|dp)$',table,flags=re.I):
       [crsr.execute("INSERT INTO %s (name) VALUES('%s')" % (table, rowprimary[0])) for rowprimary in primary if crsr.execute("SELECT COUNT(*) FROM %s WHERE id='%d'" % (table, 0 )) and crsr.fetchone()[0] == 0]
     else:
       [crsr.execute("INSERT INTO %s (name) VALUES('%s')" % (table, rowprimary[0])) for rowprimary in primary if crsr.execute("SELECT COUNT(*) FROM %s WHERE name='%s'" % (table,rowprimary[0] )) and crsr.fetchone()[0] == 0]
  except:
   if self.reconnect():
    return self.fill(table,primary,fetchmany)
   else:
    return False
  else:
   self.conn.commit()
   return True
 def get(self,table,columnoutput='*',column='',columninput='', orderby=None,regex=None):
  #print("get %s,%s,%s,%s,%s,%s" % (table,columnoutput,column,columninput,orderby,regex))
  try:
   crsr=self.conn.cursor()
   if (column==''):
    if orderby:
     crsr.execute("SELECT {} FROM {} ORDER BY {}".format(columnoutput,table,orderby))
    else:
     crsr.execute("SELECT {} FROM {}".format(columnoutput,table))
   elif regex:
    if orderby:
     crsr.execute("SELECT {} FROM {} WHERE {} REGEXP '{}' ORDER BY {}".format(columnoutput,table,column,columninput,orderby))
    else:
     crsr.execute("SELECT {} FROM {} WHERE {} REGEXP '{}'".format(columnoutput,table,column,columninput))
   else:
    if orderby:
     crsr.execute("SELECT {} FROM {} WHERE {}='{}' ORDER BY {}".format(columnoutput,table,column,columninput,orderby))
    else:
     crsr.execute("SELECT {} FROM {} WHERE {}='{}'".format(columnoutput,table,column,columninput))
  except:
   #print("exception")
   if self.reconnect():
    return self.get(table,columnoutput,column,columninput,orderby,regex)
   else:
    return False
  else:
   return crsr.fetchall()
 def update(self,table,column,value,where,wherevalue):
  try:
   self.conn.cursor().execute("UPDATE {} SET {}='{}' WHERE {}='{}'".format(table,column,value,where,wherevalue))
  except:
   if self.reconnect():
    return self.update(self,table,column,value,where,wherevalue)
   else:
    return False
  else:
   return True
 def search(self,table,columnvalue='',column='name',regex=False):
  #print("table,columnvalue,column,regex %s,%s,%s,%s" % (table,columnvalue,column,regex))
  try:
   crsr=self.conn.cursor()
   if not regex:
    crsr.execute("SELECT COUNT(*) FROM %s WHERE %s='%s'" % (table,column,columnvalue))
   else:
    crsr.execute("SELECT COUNT(*) FROM %s WHERE %s REGEXP '%s'" % (table,column,columnvalue))
  except:
   if self.reconnect():
    return self.search(table,columnvalue,column)
   else:
    return False
  else:
   if crsr.fetchone()[0] == 0:
    return False
   return True
 def getemailcompany(self):#called only from dbpushpull.py
  try:
   crsr=self.conn.cursor()
   crsr.execute("SELECT track.email,company.name FROM track JOIN company ON track.company_id=company.id WHERE %s>=track.expire ORDER BY track.company_id" % (int(re.sub('-','',datetime.date.today().isoformat())),))
  except:
   if self.reconnect():
    return self.getemailcompany()
   else:
    return False
  else:
   return crsr.fetchall()
 def updatedate(self,mail):#called from sendmail
  try:
   self.conn.cursor().execute("UPDATE track SET expire='%d' WHERE email='%s'" % (int(re.sub('-','',str(datetime.date.today()+datetime.timedelta(days=60)))),mail))
  except:
   if self.reconnect():
    return self.updatedate(mail)
   else:
    return False
  else:
   self.conn.commit()
   return True
 def delete(self,table,where,wherevalue):
  crsr=self.conn.cursor()
  if table=='linkvisited':
   crsr.execute("DELETE FROM {} WHERE {} < {}".format(table,where,wherevalue))
  else:
   crsr.execute("DELETE FROM {} WHERE {}='{}'".format(table,where,wherevalue))
  self.conn.commit()
 def close(self):
  try:
   self.conn.commit()
   self.conn.close()
  except:
   print("connection already disconnected")
