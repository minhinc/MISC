import os
import datetime
import re
import MySQLdb
class databasec:
 def __init__(self):
  self.conn=None
  self.conn=MySQLdb.connect(host='166.62.28.143',user='minhinc',passwd='pinku76minh',db='trackweb')
  print('database connected')
  crsr=self.conn.cursor()
  crsr.execute("CREATE TABLE IF NOT EXISTS track (email VARCHAR(80) NOT NULL PRIMARY KEY, company_id INT, tech_id INT, city_id INT, country_id INT, expire INT)")
  crsr.execute("CREATE TABLE IF NOT EXISTS company (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT, name VARCHAR(80),UNIQUE(name))")
  crsr.execute("CREATE TABLE IF NOT EXISTS tech (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT, name VARCHAR(80),UNIQUE(name))")
  crsr.execute("CREATE TABLE IF NOT EXISTS city (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT, name VARCHAR(80),country INT, UNIQUE(name,country))")
  crsr.execute("CREATE TABLE IF NOT EXISTS country (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT, name VARCHAR(80),UNIQUE(name))")
  print('table created')
  self.conn.commit()
 def reconnect(self):
  if(self.conn.open==False):
   self.conn=MySQLdb.connect(host='166.62.28.143',user='minhinc',passwd='pinku76minh',db='trackweb')
   print('database re-connected')
 def fill(self,table,primary):
  self.reconnect()
#  print("table, primary %s %s" % (table,primary))
  crsr=self.conn.cursor()
  for rowprimary in primary:
   if(table=='track'):
    crsr.execute("SELECT COUNT(*) FROM track WHERE email='%s'" % (rowprimary[0], ))
    if crsr.fetchone()[0] == 0:
     crsr.execute("INSERT INTO track(email,company_id,tech_id,city_id,country_id,expire) VALUES('%s','%d','%d','%d','%d','%d')" % rowprimary)
   elif(table=='company'):
    crsr.execute("SELECT COUNT(*) FROM company WHERE name='%s'" % (rowprimary[0], ))
    if crsr.fetchone()[0] == 0:
     crsr.execute("INSERT INTO company (name) VALUES('%s')" % rowprimary)
   elif(table=='tech'):
    crsr.execute("SELECT COUNT(*) FROM tech WHERE name='%s'" % (rowprimary[0], ))
    if crsr.fetchone()[0] == 0:
     crsr.execute("INSERT INTO tech (name) VALUES('%s')" % rowprimary)
   elif(table=='city'):
    crsr.execute("SELECT COUNT(*) FROM city WHERE name='%s' and country='%d'" % (rowprimary[0],rowprimary[1] ))
    if crsr.fetchone()[0] == 0:
     crsr.execute("INSERT INTO city(name,country) VALUES('%s','%d')" % rowprimary)
   elif(table=='country'):
    crsr.execute("SELECT COUNT(*) FROM country WHERE name='%s'" % (rowprimary[0], ))
    if crsr.fetchone()[0] == 0:
     crsr.execute("INSERT INTO country (name) VALUES('%s')" % rowprimary)
  self.conn.commit()
 def get(self,table,columnoutput='*',column='',columninput=''):
  self.reconnect()
  crsr=self.conn.cursor()
  if (column==''):
   crsr.execute("SELECT {} FROM {}".format(columnoutput,table))
  else:
#  crsr.execute("SELECT %s FROM %s WHERE %s='%s'" % (columnoutput,table,column,columninput))
   crsr.execute("SELECT {} FROM {} WHERE {}='{}'".format(columnoutput,table,column,columninput))
  return crsr.fetchall()
 def getemailcompany(self):#called only from dbpushpull.py
  self.reconnect()
  crsr=self.conn.cursor()
  crsr.execute("SELECT track.email,company.name FROM track JOIN company ON track.company_id=company.id WHERE %s>=track.expire ORDER BY track.company_id" % (int(re.sub('-','',datetime.date.today().isoformat())),))
  return crsr.fetchall()
 def updatedate(self,mail):#called from sendmail
  self.reconnect()
  self.conn.cursor().execute("UPDATE track SET expire='%d' WHERE email='%s'" % (int(re.sub('-','',str(datetime.date.today()+datetime.timedelta(days=60)))),mail))
  self.conn.commit()
 def close(self):
  self.conn.commit()
  self.conn.close()
