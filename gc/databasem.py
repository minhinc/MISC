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
  crsr.execute("CREATE TABLE IF NOT EXISTS track (email VARCHAR(80) NOT NULL PRIMARY KEY, uuid VARCHAR(80), company_id INT, tech_id INT, city_id INT, country_id INT, expire INT, status INT DEFAULT 0, message INT DEFAULT 0)") #status 0 normal, 1-registered, 2-unregistered
  crsr.execute("CREATE TABLE IF NOT EXISTS company (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT, name VARCHAR(240), phone VARCHAR(80), expire INT, UNIQUE(name,phone))")
  crsr.execute("CREATE TABLE IF NOT EXISTS city (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT, name VARCHAR(80),country INT, UNIQUE(name,country))")
  crsr.execute("CREATE TABLE IF NOT EXISTS tech (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT, name VARCHAR(80),UNIQUE(name))")
  crsr.execute("CREATE TABLE IF NOT EXISTS country (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT, name VARCHAR(80), mtopic INT,UNIQUE(name))")
  crsr.execute("CREATE TABLE IF NOT EXISTS message (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT, name VARCHAR(80))")
  crsr.execute("CREATE TABLE IF NOT EXISTS mtopic (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT, name VARCHAR(80), ic INT DEFAULT 0, UNIQUE(name))")
  crsr.execute("CREATE TABLE IF NOT EXISTS resume (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT, name VARCHAR(80), uuid VARCHAR(80), email VARCHAR(80), phone VARCHAR(80), address VARCHAR(280), UNIQUE(email))")

  crsr.execute("CREATE TABLE IF NOT EXISTS linkvisited (name VARCHAR(360) NOT NULL PRIMARY KEY)")
  crsr.execute("CREATE TABLE IF NOT EXISTS junkemail (name VARCHAR(80) NOT NULL PRIMARY KEY)")
  crsr.execute("CREATE TABLE IF NOT EXISTS junkextension (name VARCHAR(80) NOT NULL PRIMARY KEY)")

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
    elif(table == 'company'):
     crsr.execute("SELECT COUNT(*) FROM company WHERE name='%s'" % (rowprimary[0], ))
     if crsr.fetchone()[0] == 0:
      crsr.execute("INSERT INTO company(name,phone) VALUES('%s','%s')" % rowprimary)
    elif(table=='city'):
     crsr.execute("SELECT COUNT(*) FROM city WHERE name='%s' and country='%d'" % (rowprimary[0],rowprimary[1] ))
     if crsr.fetchone()[0] == 0:
      crsr.execute("INSERT INTO city(name,country) VALUES('%s','%d')" % rowprimary)
    elif(table=='tech' or table=='country' or table=='status' or table=='message' or table=='mtopic' or table=='linkvisited' or table=='junkextension' or table=='junkemail'):
     crsr.execute("SELECT COUNT(*) FROM %s WHERE name='%s'" % (table, rowprimary[0]))
     if crsr.fetchone()[0] == 0:
      crsr.execute("INSERT INTO %s (name) VALUES('%s')" % (table, rowprimary[0]))
  except:
   if self.reconnect():
    self.fill(table,primary)
  else:
   self.conn.commit()
 def get(self,table,columnoutput='*',column='',columninput='', orderby=''):
  try:
   crsr=self.conn.cursor()
   if (column=='' and orderby != '' ):
    crsr.execute("SELECT {} FROM {} ORDER BY {}.{}".format(columnoutput,table,table,orderby))
   elif (column==''):
    crsr.execute("SELECT {} FROM {}".format(columnoutput,table))
   else:
    crsr.execute("SELECT {} FROM {} WHERE {}='{}'".format(columnoutput,table,column,columninput))
  except:
   if self.reconnect():
    self.get(table,columnoutput,column,columninput,orderby)
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
