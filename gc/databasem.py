import os
import sqlite3
class databasec:
 def __init__(self):
  self.conn=None
  self.conn=sqlite3.connect('track.db')
  crsr=self.conn.cursor()
  crsr.execute('''CREATE TABLE IF NOT EXISTS track (email TEXT NOT NULL PRIMARY KEY, company_id INTEGER, tech_id INTEGER, city_id INTEGER, country_id INTEGER, expire INTEGER)''')
  crsr.execute('''CREATE TABLE IF NOT EXISTS company (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, name TEXT,UNIQUE(name))''')
  crsr.execute('''CREATE TABLE IF NOT EXISTS tech (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, name TEXT,UNIQUE(name))''')
  crsr.execute('''CREATE TABLE IF NOT EXISTS city (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, name TEXT,country INTEGER, UNIQUE(name,country))''')
  crsr.execute('''CREATE TABLE IF NOT EXISTS country (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, name TEXT,UNIQUE(name))''')
  self.conn.commit()
  print('database created')
 def fill(self,table,primary):
  print("table, primary %s %s" % (table,primary))
  crsr=self.conn.cursor()
  for rowprimary in primary:
   if(table=='track'):
    if crsr.execute('SELECT COUNT(*) FROM track WHERE email=?', (rowprimary[0], )).fetchone()[0] == 0:
     crsr.execute('INSERT INTO track(email,company_id,tech_id,city_id,country_id,expire) VALUES(?,?,?,?,?,?)',rowprimary)
   elif(table=='company'):
    if crsr.execute('SELECT COUNT(*) FROM company WHERE name=?', (rowprimary[0], )).fetchone()[0] == 0:
     crsr.execute('INSERT INTO company (name) VALUES(?)',rowprimary)
   elif(table=='tech'):
    if crsr.execute('SELECT COUNT(*) FROM tech WHERE name=?', (rowprimary[0], )).fetchone()[0] == 0:
     crsr.execute('INSERT INTO tech (name) VALUES(?)',rowprimary)
   elif(table=='city'):
    if crsr.execute('SELECT COUNT(*) FROM city WHERE name=? and country=?', (rowprimary[0],rowprimary[1] )).fetchone()[0] == 0:
     crsr.execute('INSERT INTO city(name,country) VALUES(?,?)',rowprimary)
   elif(table=='country'):
    if crsr.execute('SELECT COUNT(*) FROM country WHERE name=?', (rowprimary[0], )).fetchone()[0] == 0:
     crsr.execute('INSERT INTO country (name) VALUES(?)',rowprimary)
  self.conn.commit()
 def get(self,table,columnoutput='*',column='',columninput=''):
  crsr=self.conn.cursor()
  if (column==''):
   crsr.execute('SELECT {value} FROM {tablename}'.format(value=columnoutput,tablename=table))
  else:
   crsr.execute('SELECT %s FROM %s WHERE %s=?' % (columnoutput,table,column), (columninput,))
  return crsr.fetchall()
 def close(self):
  self.conn.commit()
  self.conn.close()
