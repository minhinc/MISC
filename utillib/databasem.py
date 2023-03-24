import os
import datetime
import re
import sys;sys.path.append(os.path.expanduser('~')+r'/tmp')
if re.search(r'^(win|cygwin).*',sys.platform,flags=re.I):
 import pymysql
 pymysql.install_as_MySQLdb()
import MySQLdb
import time
from MISC.utillib.util import Util
class databasec:
 def __init__(self,ct=True): #ct-createtable
  self.conn=None
  self.cc=0#connection count
  while self.cc<4 and not self.reconnect():
   print(f'problem in connection.. {self.cc=}')
   self.cc+=1
  self.cc=0 if self.cc<4 else self.cc
  if(ct and self.cc<4):
   self.create()
  self.tbl=Util.gettable()
 def create(self):
  crsr=self.conn.cursor()
  crsr.execute("CREATE TABLE IF NOT EXISTS track (email VARCHAR(80) NOT NULL PRIMARY KEY, uuid VARCHAR(80), company_id INT, tech_id INT, country_id INT, date INT, status INT DEFAULT 0, message INT DEFAULT 0)") #status 0 normal, 1-registered, 2-unregistered, 3-senderror message-unregistration reason
  crsr.execute("CREATE TABLE IF NOT EXISTS company (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT, name VARCHAR(240), UNIQUE(name))")
#  crsr.execute("CREATE TABLE IF NOT EXISTS city (id INT  DEFAULT 0, name VARCHAR(80), country INT, PRIMARY KEY(name,country))")
  crsr.execute("CREATE TABLE IF NOT EXISTS tech (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT, name VARCHAR(80), content TEXT, UNIQUE(name))")
  crsr.execute("CREATE TABLE IF NOT EXISTS country (id INT DEFAULT 0 PRIMARY KEY, name VARCHAR(80),UNIQUE(name))")

  crsr.execute("CREATE TABLE IF NOT EXISTS message (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT, name VARCHAR(512), UNIQUE(name))")
#  crsr.execute("CREATE TABLE IF NOT EXISTS resume (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT, name VARCHAR(80), uuid VARCHAR(80), email VARCHAR(80), phone VARCHAR(80), address VARCHAR(280), text BLOB, UNIQUE(email))")

  crsr.execute("CREATE TABLE IF NOT EXISTS linkvisited (name VARCHAR(360) NOT NULL PRIMARY KEY,date INT)")
  crsr.execute("CREATE TABLE IF NOT EXISTS junkemail (name VARCHAR(80) NOT NULL PRIMARY KEY)")
  crsr.execute("CREATE TABLE IF NOT EXISTS junkextension (name VARCHAR(80) NOT NULL PRIMARY KEY)")

#  crsr.execute("CREATE TABLE IF NOT EXISTS adsense (id BIGINT NOT NULL DEFAULT 0 PRIMARY KEY, name VARCHAR(80), value VARCHAR(1000), width INT DEFAULT 0, height INT DEFAULT 0, UNIQUE(name))")

  crsr.execute("CREATE TABLE IF NOT EXISTS qt (id INT NOT NULL DEFAULT 0 PRIMARY KEY, name VARCHAR(80), lab TEXT, content MEDIUMTEXT, UNIQUE(id))")
  crsr.execute("CREATE TABLE IF NOT EXISTS qml (id INT NOT NULL DEFAULT 0 PRIMARY KEY, name VARCHAR(80), lab TEXT, content MEDIUMTEXT, UNIQUE(id))")
  crsr.execute("CREATE TABLE IF NOT EXISTS c (id INT NOT NULL DEFAULT 0 PRIMARY KEY, name VARCHAR(80), lab TEXT, content MEDIUMTEXT, UNIQUE(id))")
  crsr.execute("CREATE TABLE IF NOT EXISTS cpp (id INT NOT NULL DEFAULT 0 PRIMARY KEY, name VARCHAR(80), lab TEXT, content MEDIUMTEXT, UNIQUE(id))")
  crsr.execute("CREATE TABLE IF NOT EXISTS gl (id INT NOT NULL DEFAULT 0 PRIMARY KEY, name VARCHAR(80), lab TEXT, content MEDIUMTEXT, UNIQUE(id))")
  crsr.execute("CREATE TABLE IF NOT EXISTS py (id INT NOT NULL DEFAULT 0 PRIMARY KEY, name VARCHAR(80), lab TEXT, content MEDIUMTEXT, UNIQUE(id))")
  crsr.execute("CREATE TABLE IF NOT EXISTS li (id INT NOT NULL DEFAULT 0 PRIMARY KEY, name VARCHAR(80), lab TEXT, content MEDIUMTEXT, UNIQUE(id))")
  crsr.execute("CREATE TABLE IF NOT EXISTS ldd (id INT NOT NULL DEFAULT 0 PRIMARY KEY, name VARCHAR(80), lab TEXT, content MEDIUMTEXT, UNIQUE(id))")
  crsr.execute("CREATE TABLE IF NOT EXISTS dp (id INT NOT NULL DEFAULT 0 PRIMARY KEY, name VARCHAR(80), lab TEXT, content MEDIUMTEXT, UNIQUE(id))")
  crsr.execute("CREATE TABLE IF NOT EXISTS kv (id INT NOT NULL DEFAULT 0 PRIMARY KEY, name VARCHAR(80), lab TEXT, content MEDIUMTEXT, UNIQUE(id))")
  crsr.execute("CREATE TABLE IF NOT EXISTS ai (id INT NOT NULL DEFAULT 0 PRIMARY KEY, name VARCHAR(80), lab TEXT, content MEDIUMTEXT, UNIQUE(id))")
  crsr.execute("CREATE TABLE IF NOT EXISTS ml (id INT NOT NULL DEFAULT 0 PRIMARY KEY, name VARCHAR(80), lab TEXT, content MEDIUMTEXT, UNIQUE(id))")

#data in html
  crsr.execute("CREATE TABLE IF NOT EXISTS headername (id INT NOT NULL DEFAULT 0 PRIMARY KEY, name VARCHAR(80), content VARCHAR(16000), UNIQUE(name))")

  print('table created')
  self.conn.commit()
 def reconnect(self):
 # print(f'databasec.reconnect {self.conn=} {self.cc=}')
  passwd=re.split('\s+',re.split('\n',open(os.path.expanduser('~/passwd')).read())[0])
  if not hasattr(databasec.reconnect,'lastconnecttime'):
   setattr(databasec.reconnect,'lastconnecttime',int(time.time()))
  if (int(time.time())-databasec.reconnect.lastconnecttime) > 600: # 5 minutes connection works
   print(f'last connection works for 5 minutes or more so restting self.cc')
   self.cc=0
  elif self.cc>4:
   print(f'number of retry exceeds {self.cc=} cannot connect')
   self.conn=None 
   return False
  try:
   self.conn=MySQLdb.connect(host=re.split(r'\s+',re.split('\n',open(os.path.expanduser('~/passwd')).read())[0])[0],user=re.split(r'\s+',re.split('\n',open(os.path.expanduser('~/passwd')).read())[0])[1],passwd=re.split(r'\s+',re.split('\n',open(os.path.expanduser('~/passwd')).read())[0])[2],db=re.split(r'\s+',re.split('\n',open(os.path.expanduser('~/passwd')).read())[0])[3],connect_timeout=10,read_timeout=10,write_timeout=10)
   print('database re-connected',file=sys.stderr)
  except:
   print('database could not be connected')
   self.conn=None
   return False
  else:
   self.cc=self.cc+1
   databasec.reconnect.lastconnecttime=int(time.time())
   '''
   if self.cc>4:
    print("number of retry %s" % self.cc)
    return False
   '''
   return True

 '''
 def fillbulk(self,table,*splitline):
  print(f'databasec.fillbulk {table=} {splitline=}')
  selectq=None
  tbl=dict()
  try:
   crsr=self.conn.cursor()
   [tbl.__setitem__(re.sub(r'^(\w+).*$',r'\1',i[0]),re.findall(r'(\w+)\s+(\w*CHAR|\w*INT|\w*TEXT|\w*BLOB)',i[1])) for i in re.findall('CREATE TABLE.*?(\w+)\s*\((.*?)\)"\s*\)',open('databasem.py').read())]
   selectq=f'INSERT INTO {table}('+','.join(i[0] for i in tbl[table])+r') VALUES('+('%s,'*len(tbl[table]))[:-1]+r')'
   col=[int(re.sub(r'^[\'"]?(.*?)[\'"]?$',r'\1',str(splitline[i]))) if tbl[table][i][1]=='INT' else re.sub(r'^[\'"]?(.*?)[\'"]?$',r'\1',splitline[i]) for i in range(len(splitline))]
   #print(f'{tbl=} {table=} {splitline=} {selectq=} {col=}')
   crsr.execute(selectq,col)
  except Exception as ec:
   print(f'fillbulk {ec=} {type(ec)=}')
   if type(ec)!=MySQLdb._exceptions.IntegrityError and self.reconnect():
    return self.fillbulk(table,*splitline)
   else:
    print(f'{ec=}')
    return False
  else:
   self.conn.commit()
   return True

 def fill(self,table,primary=None,fetchmany=False):
#  print(f'databasec.fill {table=} {primary=} {fetchmany=}')
  try:
   crsr=self.conn.cursor()
   if not primary:
    crsr.execute("INSERT INTO {} () VALUES ()".format(table))
   elif fetchmany:
    if table=='linkvisited':
     crsr.executemany("INSERT INTO linkvisited(name,date) VALUES(%s,%s)",primary)
   else:
    for rowprimary in primary:
     if(table=='track'):
      [self.update('track','tech_id',int(rowprimary[3]),'email',rowprimary[0]) for rowprimary in primary if crsr.execute("SELECT COUNT(*) FROM track WHERE email='%s' and tech_id!='%d' and status<2" % (rowprimary[0],int(rowprimary[3]) )) and crsr.fetchone()[0] != 0]
      [self.update('track','country_id',int(rowprimary[5]),'email',rowprimary[0]) for rowprimary in primary if crsr.execute("SELECT COUNT(*) FROM track WHERE email='%s' and country_id!='%d' and status<2" % (rowprimary[0],int(rowprimary[5]) )) and crsr.fetchone()[0] != 0]
#       [self.delete('track','email',rowprimary[0]) for rowprimary in primary if crsr.execute("SELECT COUNT(*) FROM track WHERE email='%s' and tech_id!='%d' and status<2" % (rowprimary[0],int(rowprimary[3]) )) and crsr.fetchone()[0] != 0]
      [crsr.execute("INSERT INTO track(email,uuid,company_id,tech_id,country_id,date) VALUES('%s','%s','%d','%d','%d','%d')" % rowprimary) for rowprimary in primary if crsr.execute("SELECT COUNT(*) FROM track WHERE email='%s'" % (rowprimary[0], )) and crsr.fetchone()[0] == 0]
     elif(table=='city'):
       [crsr.execute("INSERT INTO city(name,country) VALUES('%s','%d')" % rowprimary) for rowprimary in primary if crsr.execute("SELECT COUNT(*) FROM city WHERE name='%s' and country='%d'" % (rowprimary[0],rowprimary[1] )) and crsr.fetchone()[0] == 0]
     elif re.search(r'^(qt|qml|py|gl|c|cpp|ldd|li|dp|ai)$',table,flags=re.I):
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

 def get(self,table,columnoutput='*',column='',columninput='', orderby=None,regex=None,compare='='):
#  print(f"databasec.get {table=} {columnoutput=} {column=} {columninput=} {orderby=} {regex=}")
  try:
   crsr=self.conn.cursor()
   if (column==''):
    if orderby:
#     crsr.execute("SELECT {} FROM {} ORDER BY {}".format(columnoutput,table,orderby))
     crsr.execute("SELECT {} FROM {} ORDER BY {}{}".format(columnoutput,table,orderby[0] if type(orderby)==tuple else orderby,' DESC LIMIT '+str(orderby[1]) if type(orderby)==tuple else ''))
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
#     crsr.execute("SELECT {} FROM {} WHERE {}='{}'".format(columnoutput,table,column,columninput))
#     selectq = """SELECT %s FROM %s WHERE %s=%%s;""" % (columnoutput,table,column)
     selectq = """SELECT %s FROM %s WHERE %s%s%%s;""" % (columnoutput,table,column,compare)
     crsr.execute(selectq,(columninput,))
  except:
   #print("exception")
   if self.reconnect():
    return self.get(table,columnoutput,column,columninput,orderby,regex)
   else:
    return False
  else:
   return crsr.fetchall()

 def update(self,table,column,value,where,wherevalue):
#  print(f'databasec.update {table=} {column=} {value=} {where=} {wherevalue=}')
  try:
   if type(column)==tuple:
    for column,value in zip(column,value):
     self.conn.cursor().execute("UPDATE {} SET {}='{}' WHERE {}='{}'".format(table,column,value,where,wherevalue))
   else:
 #   self.conn.cursor().execute("UPDATE {} SET {}='{}' WHERE {}='{}'".format(table,column,value,where,wherevalue))
    selectq = """UPDATE %s SET %s=%%s WHERE %s LIKE %%s;""" % (table, column, where)
    self.conn.cursor().execute(selectq,(value,wherevalue))
  except:
   if self.reconnect():
    return self.update(self,table,column,value,where,wherevalue)
   else:
    return False
  else:
   return True
 def search(self,table,columnvalue='',column='name',regex=False):
#  print(f'databasec.search {table=} {columnvalue=} {column=} {regex=}')
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
 '''

 def search2(self,table,*column,mode=''):
  """\
  search2('track','expire','>',20211011,'status','<',2,mode='search')
  search2('track','expire','R','2022.*',mode='search')#regular expression ordered by date
  search2('track','date','expire','>',20211011,'status','<',2,mode='get')
  search2('track','date','expire','R','2022.*',mode='get')#regular expression
  search2('track','*','expire','ROdate','2022.*',mode='get')#regular expression ordered by date
  search2('track','date','202111012,'email','=''abc@def.com',mode='update')
  search2('track',('date','202111012,'email','=''abc@def.com'),('date','202111012,'email','=''abc@def.com'),mode='updatebulk')
  search2('linkvisited','date','<',20220101,mode='delete')
  search2('linkvisited','name','R','.*junkweb.*',mode='delete')
  search2('track',0,'ding',mode='insert')#id->0 for autoincrement
  search2('message',(0,'dingdong'),(0,'singsong'),mode='insertbulk')#id->0 for autoincrement
  search2('py',mode='trunc')
  search2('py',mode='drop')
  search2('',mode='showtables')\
  """
  selectq=col=None
#  print(f'<=>databasec.search2 {table=} {column=} {mode=}')
  try:
   crsr=self.conn.cursor()
   if mode=='search':
    selectq=("""SELECT count(*) FROM %s WHERE """+' and '.join(["""%s%s%%s""" for x in range(int(len(column)/3))])) % (table,*[(count+1)%2 and x or column[count+1]!='R' and x or ' REGEXP ' for count,x in enumerate(column) if (count+1)%3])
    col=[x for count,x in enumerate(column) if not (count+1)%3]
   elif mode=='delete':
    selectq=("""DELETE FROM %s WHERE """+' and '.join(["""%s %s %%s""" for x in range(int(len(column)/3))])) % (table,*[(count+1)%2 and x or column[count+1]!='R' and x or ' REGEXP ' for count,x in enumerate(column) if (count+1)%3])
    col=[x for count,x in enumerate(column) if not (count+1)%3]
   elif mode=='get':
#    selectq=("""SELECT %s FROM %s WHERE """+' and '.join(["""%s%s%%s""" for x in range(int(len(column[1:])/3))])) % (column[0],table,*[(count+1)%2 and x or column[count+1][0]!='R' and x or 'REGEX" for count,x in enumerate(column[1:]) if (count+1)%3])+(column[1]=='O' and f'ORDER BY {column[2:]}' or '')
    if len(column)>1:
     selectq=("""SELECT %s FROM %s WHERE """+' and '.join(["""%s%s%%s""" for x in range(int(len(column[1:])/3))])+(len(column[2])>1 and column[2][1]=='O' and f' ORDER BY {column[2][2:]}' or '')) % (column[0],table,*[(count+1)%2 and x or column[count+1][0]!='R' and x or ' REGEXP ' for count,x in enumerate(column[1:]) if (count+1)%3])
    else:
     selectq=f'SELECT {len(column)==1 and column[0] or "*"} FROM {table}'
    col=[x for count,x in enumerate(column[1:]) if not (count+1)%3]
   elif mode=='DROP':
    selectq="DROP TABLE IF EXISTS %s"
    col=[table]
   elif mode=='trunc':
    selectq=f'TRUNCATE TABLE {table}'
    col=[]
   elif mode=='showtables':
    selectq='SHOW TABLES'
    col=[]
   elif mode=='update':
    selectq = ("""UPDATE %s SET %s=%%s WHERE """+' and '.join(["""%s%s%%s""" for x in range(int(len(column[2:])/3))])) % (table,column[0],*[x for count,x in enumerate(column[2:]) if (count+1)%3])
    col=(column[1],*[x for count,x in enumerate(column[2:]) if not (count+1)%3])
   elif mode=='updatebulk':
    selectq=f'UPDATE {table} SET {column[0][0]}=%s WHERE {column[0][2]}{column[0][3]}%s'
    col=[[x[i] for i in range(len(x)) if i in [1,4]] for x in column]
   elif mode=='insert':
    selectq=f'INSERT INTO {table}('+','.join(i[0] for i in self.tbl[table])+r') VALUES('+('%s,'*len(self.tbl[table]))[:-1]+r')'
    col=[int(re.sub(r'^[\'"]?(.*?)[\'"]?$',r'\1',str(column[i]))) if self.tbl[table][i][1]=='INT' else re.sub(r'^[\'"]?(.*?)[\'"]?$',r'\1',column[i]) for i in range(len(column))]
   elif mode=='insertbulk':
    selectq=f'INSERT INTO {table}('+','.join(i[0] for i in self.tbl[table])+r') VALUES('+('%s,'*len(self.tbl[table]))[:-1]+r') ON DUPLICATE KEY UPDATE '+','.join(str(i[0])+r'=values('+str(i[0])+r')' for i in self.tbl[table])
#    col=[[int(re.sub(r'^[\'"]?(.*?)[\'"]?$',r'\1',str(x[i]))) if self.tbl[table][i][1]=='INT' else re.sub(r'^[\'"]?(.*?)[\'"]?$',r'\1',x[i]) for i in range(len(x))] for x in column]
    col=column
#   print(f'<=>databasec.search2 {selectq=} {col=}')
   if mode=='insertbulk' or mode=='updatebulk':
    crsr.executemany(selectq,col)
   else:
    crsr.execute(selectq,col)
  except Exception as ec:
   print(f'search2 {type(ec)=}')
   if type(ec)==MySQLdb._exceptions.OperationalError and self.reconnect():
    return self.search2(table,*column,mode=mode)
   else:
    return False
  else:
   if mode=='search':
    if crsr.fetchone()[0]!=0:
     return True
   elif mode in ['get','showtables']:
    return crsr.fetchall()
   elif mode in ['delete','insert','insertbulk','update','updatebulk','trunc','drop']:
    self.conn.commit()
    return True
   return False

 '''
 def get2(self,table,output,*column):
  """get2('track','email',('expire','>',20211011,'status','<',2)"""
  try:
   crsr=self.conn.cursor()
   selectq=("""SELECT %s FROM %s WHERE """+' and '.join(["""%s%s%%s""" for x in range(int(len(column)/3))])) % (output,table,*[x for count,x in enumerate(column) if (count+1)%3])
   crsr.execute(selectq,[x for count,x in enumerate(column) if not (count+1)%3])
  except:
   if self.reconnect():
    return self.get2(table,output,*column)
   else:
    return False
  else:
   return crsr.fetchall()

 def getemailcompany(self):#called only from dbpushpull.py
  try:
   crsr=self.conn.cursor()
#   crsr.execute("SELECT track.email,company.name FROM track JOIN company ON track.company_id=company.id WHERE %s>=track.expire ORDER BY track.company_id" % (int(re.sub('-','',datetime.date.today().isoformat())),))
   crsr.execute("SELECT track.email,company.name FROM track JOIN company ON track.company_id=company.id WHERE %s>=track.date and track.status<2 ORDER BY track.company_id" % (int(re.sub('-','',datetime.date.today().isoformat())),))
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
  try:
   crsr=self.conn.cursor()
   if table=='linkvisited':
    crsr.execute("DELETE FROM {} WHERE {} < {}".format(table,where,wherevalue))
   else:
    crsr.execute("DELETE FROM {} WHERE {}='{}'".format(table,where,wherevalue))
  except:
   if self.reconnect():
    return self.delete(table,where,wherevalue)
  else:
   self.conn.commit()
 '''
 def close(self):
  try:
   self.conn.commit()
   self.conn.close()
  except:
   print("connection already disconnected")
