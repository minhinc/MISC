import os
import datetime
import re
import MySQLdb
import time
class databasec:
 def __init__(self,ct=True): #ct-createtable
  self.conn=None
  self.reconnect()
  if(ct):
   self.create()
 def create(self):
  crsr=self.conn.cursor()
  crsr.execute("CREATE TABLE IF NOT EXISTS track (email VARCHAR(80) NOT NULL PRIMARY KEY, uuid VARCHAR(80), company_id INT, tech_id INT, city_id INT, country_id INT, expire INT, status INT DEFAULT 0, message INT DEFAULT 0)") #status 0 normal, 1-registered, 2-unregistered message-unregistration reason
  crsr.execute("CREATE TABLE IF NOT EXISTS company (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT, name VARCHAR(240), phone VARCHAR(80), UNIQUE(name))")
  crsr.execute("CREATE TABLE IF NOT EXISTS city (id INT DEFAULT 0 PRIMARY KEY, name VARCHAR(80), country INT, UNIQUE(name,country))")
  crsr.execute("CREATE TABLE IF NOT EXISTS tech (id INT DEFAULT 0 PRIMARY KEY, name VARCHAR(80),UNIQUE(name))")
  crsr.execute("CREATE TABLE IF NOT EXISTS country (id INT DEFAULT 0 PRIMARY KEY, name VARCHAR(80),UNIQUE(name))")

  crsr.execute("CREATE TABLE IF NOT EXISTS message (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT, name VARCHAR(80))")
  crsr.execute("CREATE TABLE IF NOT EXISTS resume (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT, name VARCHAR(80), uuid VARCHAR(80), email VARCHAR(80), phone VARCHAR(80), address VARCHAR(280), UNIQUE(email))")

  crsr.execute("CREATE TABLE IF NOT EXISTS linkvisited (name VARCHAR(360) NOT NULL PRIMARY KEY)")
  crsr.execute("CREATE TABLE IF NOT EXISTS junkemail (name VARCHAR(80) NOT NULL PRIMARY KEY)")
  crsr.execute("CREATE TABLE IF NOT EXISTS junkextension (name VARCHAR(80) NOT NULL PRIMARY KEY)")

  crsr.execute("CREATE TABLE IF NOT EXISTS qt (id INT NOT NULL DEFAULT 0 PRIMARY KEY, name VARCHAR(80) NOT NULL, value VARCHAR(960), lab VARCHAR(480),UNIQUE(id))")
  crsr.execute("CREATE TABLE IF NOT EXISTS c (id INT NOT NULL DEFAULT 0 PRIMARY KEY, name VARCHAR(80) NOT NULL, value VARCHAR(960), lab VARCHAR(480),UNIQUE(id))")
  crsr.execute("CREATE TABLE IF NOT EXISTS cpp (id INT NOT NULL DEFAULT 0 PRIMARY KEY, name VARCHAR(80) NOT NULL, value VARCHAR(960), lab VARCHAR(480),UNIQUE(id))")
  crsr.execute("CREATE TABLE IF NOT EXISTS gl (id INT NOT NULL DEFAULT 0 PRIMARY KEY, name VARCHAR(80) NOT NULL, value VARCHAR(960), lab VARCHAR(480),UNIQUE(id))")
  crsr.execute("CREATE TABLE IF NOT EXISTS py (id INT NOT NULL DEFAULT 0 PRIMARY KEY, name VARCHAR(80) NOT NULL, value VARCHAR(960), lab VARCHAR(480),UNIQUE(id))")
  crsr.execute("CREATE TABLE IF NOT EXISTS li (id INT NOT NULL DEFAULT 0 PRIMARY KEY, name VARCHAR(80) NOT NULL, value VARCHAR(960), lab VARCHAR(480),UNIQUE(id))")
  crsr.execute("CREATE TABLE IF NOT EXISTS ldd (id INT NOT NULL DEFAULT 0 PRIMARY KEY, name VARCHAR(80) NOT NULL, value VARCHAR(960), lab VARCHAR(480),UNIQUE(id))")

  print('table created')
  self.conn.commit()
 def reconnect(self):
  try:
   self.conn=MySQLdb.connect(host='166.62.28.143',user='minhinc',passwd='pinku76minh',db='trackweb')
   print('database re-connected')
  except:
   print('database could not be connected')
   return False
  else:
   return True
 def fill(self,table,primary):
  try:
   crsr=self.conn.cursor()
   for rowprimary in primary:
    if(table=='track'):
     crsr.execute("SELECT COUNT(*) FROM track WHERE email='%s'" % (rowprimary[0], ))
     if crsr.fetchone()[0] == 0:
      crsr.execute("INSERT INTO track(email,uuid,company_id,tech_id,city_id,country_id,expire) VALUES('%s','%s','%d','%d','%d','%d','%d')" % rowprimary)
    elif(table=='city'):
     crsr.execute("SELECT COUNT(*) FROM city WHERE name='%s' and country='%d'" % (rowprimary[0],rowprimary[1] ))
     if crsr.fetchone()[0] == 0:
      crsr.execute("INSERT INTO city(name,country) VALUES('%s','%d')" % rowprimary)
    else:
      print("fill %s %s" % (table,rowprimary[0]))
      crsr.execute("INSERT INTO %s (name) VALUES('%s')" % (table, rowprimary[0]))
  except:
   if self.reconnect():
    self.fill(table,primary)
  else:
   self.conn.commit()
 def get(self,table,columnoutput='*',column='',columninput='', orderby=None,regex=None):
#  print("get %s,%s,%s,%s,%s,%s" % (table,columnoutput,column,columninput,orderby,regex))
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
   print("exception")
   if self.reconnect():
    self.get(table,columnoutput,column,columninput,orderby,regex)
  else:
   return crsr.fetchall()
 def update(self,table,column,value,where,wherevalue):
  try:
   self.conn.cursor().execute("UPDATE {} SET {}='{}' WHERE {}='{}'".format(table,column,value,where,wherevalue))
  except:
   self.reconnect()
   self.update(self,table,column,value,where,wherevalue)
 def search(self,table,columnvalue='',column='name'):
  try:
   crsr=self.conn.cursor()
   crsr.execute("SELECT COUNT(*) FROM %s WHERE %s='%s'" % (table,column,columnvalue))
  except:
   if self.reconnect():
    self.search(self.table,columnvalue,column)
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
    self.getemailcompany()
  else:
   return crsr.fetchall()
 def updatedate(self,mail):#called from sendmail
  try:
   self.conn.cursor().execute("UPDATE track SET expire='%d' WHERE email='%s'" % (int(re.sub('-','',str(datetime.date.today()+datetime.timedelta(days=60)))),mail))
  except:
   if self.reconnect():
    self.updatedate(mail)
  else:
   self.conn.commit()
 def close(self):
  try:
   self.conn.commit()
   self.conn.close()
  except:
   print("connection already disconnected")
