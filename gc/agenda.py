import sys
import re
from databasem import databasec
if len(sys.argv)<4:
 print(''' ---usage---
 agenda.py <tech> <company> <iddaywise>
 agenda.py qt claysol "1 2 3:4 L" "4 5 6:L"
 agenda.py qt '' "1 2 3:4 L" "4 5 6:L"''')
 exit(-1)
day=[]
tech=sys.argv[1]
company=sys.argv[2] if not re.search(r'^(''|"")$',sys.argv[2],flags=re.I) else None
for i in range(3,len(sys.argv)):
 if re.search(r':',sys.argv[i]):
  day.append(sys.argv[i].split(':')[0].split()+[':']+sys.argv[i].split(':')[1].split())
 else:
  day.append(sys.argv[i].split())
f=open('advance-'+tech+'-agenda.html','w')
db=databasec(False)
#PH=1250;hc=0
PH=1347;hc=0
LH=21;HH=45;DH=65;DHCG=30;DCCG=80;TM=40;OFST=25#dayheadercontentgap,daycontentcontentgap,pagemargin
BTMOFST=25
htmlstr="";pagenumber=0
def prepareheader():
 global htmlstr;global pagenumber
 global PH;global hc;
 top='';toph=0;left=True;
 global tech
 l='';header=''
 numofline=0
 htmlstr+='''<html>
<head>
<META http-equiv="Content-Type" content="text/html; charset=UTF-8">
<link rel="stylesheet" type="text/css" href="./agenda.css" media="all"/>
</head>
<body>
<div class=pg>
'''

 for data in db.get(tech,'*','name','[[:<:]]h_',orderby='id',regex=True):
  numofline=numofline+max(len(re.findall(r'\n',str(data[1])))+1,len(re.findall(r'\n',str(data[2])))+1)
 print("numofline %d" % numofline)
 htmlstr+=""" <pre class=title>%s</pre>
 <pre class=subtitle>%s</pre>
 <pre class=company>%s</pre>
""" % (db.get(tech,'value','name','title')[0][0],db.get(tech,'value','name','subtitle')[0][0],'('+company+')' if company else '')

 for data in db.get(tech,'*','name','[[:<:]]h_',orderby='id',regex=True):
  if not re.search(r'h_hr',data[1]):
   htmlstr+=""" <div style="height:%spx;">
  <div class="headerleft"> <pre>%s</pre></div>
  <div class="headerright"> <pre>%s</pre></div>
 </div>
""" % (max(len(re.findall(r'\n',data[1]))+1,len(re.findall(r'\n',data[2]))+1)*LH+(50*OFST)/numofline,re.sub(r'^h_','',data[1]),data[2])
  else:
   htmlstr+=''' <hr>
'''
 pagenumber=pagenumber+1
 htmlstr+="""<pre class="ftr">&copy www.MinhInc.com</pre><pre class="pn">%s</pre>
</div>

<div class=pg>
""" % pagenumber
 for data in db.get(tech,'*','name','[[:<:]]h2_',orderby='id',regex=True):
  htmlstr+=""" <div class="header2" style="margin-top:%spx;">
  <pre class="header">%s</pre>
  <pre class="content" style="height:%spx">%s</pre>
 </div>
""" % (TM if not hc else OFST*5,re.sub(r'^h2_','',data[1]),len(re.findall(r'\n',data[2]))*LH+OFST,data[2])
  hc=TM+HH+len(re.findall(r'\n',data[2]))*LH+OFST if not hc else hc+5*OFST+HH+len(re.findall(r'\n',data[2]))*LH+OFST
  print("h2_ hc calculated is %s" % hc)
 print("h2_ hc total calculated is %s" % hc)

 for k in range(0,len(day)):
  left=True
  for i in range(0,len(day[k])):
   if not re.search(r'^(\d+|:|l|L)$',day[k][i],flags=re.I):
    print("new tech,ik %s %s" % (tech,day[k][i]))
    tech=day[k][i]
    continue
   if left and top:
    toph=DCCG+HH+toph*LH+OFST
    if re.search(r'XXX',top):
     toph+=DH+DHCG
    printdata(top,toph,calculateh(k,i,l))
    top='';toph=0;
   if not re.search(r'^[Ll:]$',day[k][i]):
    l=db.get(tech,'lab','id',day[k][i])[0][0] if l=='' else l+'\n'+db.get(tech,'lab','id',day[k][i])[0][0];
   if i==0 or day[k][i]==':':
    left=True
    header=""" <div class="dayheader" style="margin-top:XXXpx"><pre>Day %s %s</pre><hr></div>
""" % (k+1,"Afternoon" if day[k][i]==':' else "Morning")
    if day[k][i]==':':
     continue
   top+=header+' <div class="dayheaderleft" style="margin-top:YYYpx">' if left else ' <div class="dayheaderright" style="margin-top:YYYpx">'
   header=''
   top+="""
  <pre class="%s">%s</pre>
  <ul class="%s" style="height:%spx;float:%s">
""" % ('dayheader','     Lab' if re.search(r'[Ll]',day[k][i]) else '  Lecture - '+db.get(tech,'name','id',day[k][i])[0][0],'daycontent',len(re.findall(r'\n',l))*LH+OFST if re.search(r'^[Ll]$',day[k][i]) else len(re.findall(r'\n',db.get(tech,'value','id',day[k][i])[0][0]))*LH+OFST,'left' if left else 'right')  
   for le in [re.sub(r'\n$','',e) for e in re.split(r'[*]',l if  re.search(r'^[Ll]$',day[k][i]) else db.get(tech,'value','id',day[k][i])[0][0]) if e]:
    top+="""   <li><pre>%s</pre></li>
""" % le
   top+='''
  </ul>
 </div>
'''
   toph=max(toph,len(re.findall(r'\n',l)) if re.search(r'^[Ll]$',day[k][i]) else len(re.findall(r'\n',db.get(tech,'value','id',day[k][i])[0][0])))
   if re.search(r'[Ll]',day[k][i]):
    l=''
   left=not left
 printdata(top,DCCG+DH+DHCG+HH+toph*LH+OFST,0)
def calculateh(k,i,l):
 print("calculateh k,i%s,%s" % (k,i))
 th=0;tr=0;reth=0
 ltech=tech
 for t in range(i,len(day[k])):
  if not re.search(r'^(\d+|:|l|L)$',day[k][t],flags=re.I):
   ltech=day[k][t]
   continue
  tr=tr+1
  if tr>2:
   reth+=DCCG+HH+th*LH+OFST
   print("reth %s" % reth)
   return reth
  if not re.search(r'^[Ll:]$',day[k][t]):
   l=db.get(ltech,'lab','id',day[k][t])[0][0] if l=='' else l+'\n'+db.get(ltech,'lab','id',day[k][t])[0][0]
  if t==0 or day[k][t]==':':
   if t!=i:
    reth+=DCCG+HH+th*LH+OFST
    print("reth1 %s" % reth)
    return reth
   reth=DH+DHCG
   if day[k][t]==':':
    tr=tr-1
    continue
  th=max(th,len(re.findall(r'\n',l)) if re.search(r'^[Ll]$',day[k][t]) else len(re.findall(r'\n',db.get(ltech,'value','id',day[k][t])[0][0])))
 reth+=DCCG+HH+th*LH+OFST
 print("><calculate %s" % reth)
 return reth
 
def printdata(top,toph,bottomh):
 global htmlstr;global pagenumber
 global PH;global hc;global DCCG;global TM;global BTMOFST
 num=1;den=2;
 print("printdata hc,toph,bottomh %s,%s,%s" % (hc,toph,bottomh))
 if not hasattr(printdata,"daycounter"):
  printdata.daycounter=' '
 m=re.search(r'(day.*)(Morning|Afternoon)',top,flags=re.I)
 if m:
  if printdata.daycounter!=m.group(1):
   num=3;den=4;
 if not re.search(r'XXX',top):
  top=re.sub(r'YYY','XXX',top)
 else:
  top=re.sub(r'YYY',str(DHCG),top)
 if PH>(hc+toph+bottomh+BTMOFST):
  if hc==0:
   hc=toph-DCCG+TM
   htmlstr+=re.sub(r'XXX',str(TM),top)
  else:
   hc=hc+toph
   htmlstr+=re.sub(r'XXX',str(DCCG),top)
 elif PH>(hc+toph+BTMOFST):
  if hc==0:
   hc=toph-DCCG+TM
   htmlstr+=re.sub(r'XXX',str(TM),top)
  else:
 # elif (PH-hc-toph)<(PH/100):
   print("num den %s,%s" % (num,den))
   htmlstr+=re.sub(r'XXX',str((((PH-hc-toph-BTMOFST)*num)/den)+DCCG),top)
   pagenumber=pagenumber+1
   htmlstr+="""<pre class="ftr">&copy www.MinhInc.com</pre><pre class="pn">%s</pre>
</div>

<div class="pg">
""" % pagenumber
   hc=0
 # else:
 #  hc=hc+toph
 #  f.write(re.sub(r'XXX',str(DCCG),top))
 else:
  hc=toph-DCCG+TM
  pagenumber=pagenumber+1
  htmlstr+="""<pre class="ftr">&copy www.MinhInc.com</pre><pre class="pn">%s</pre>
</div>

<div class="pg">
""" % pagenumber
  htmlstr+=re.sub(r'XXX',str(TM),top)
 print("><printdata hc %d" % hc)
 

def preparetailer():
 global htmlstr;global pagenumber;
 global tech
 htmlstr+="""
<pre class="ftr">&copy www.minhinc.com</pre><pre class="pn">%s</pre>
</div>

<div class="pg">
<a class="logo" href="http://www.minhinc.com"><pre class="copy">&copy</pre><pre class="logot"> Minh</pre>
<pre class="logob">A SOFTWARE RESEARCH FIRM</pre></a><img class="logo" src="./minh.png"/>
</body>
</html>""" % pagenumber
 f.write(re.sub(r'<pre class="ftr"[^\d]*\d+','',htmlstr))
 f.close()
 with open('tmp.html','w') as file:
  file.write(htmlstr)
 import pdfkit
 import os
 os.environ['NO_AT_BRIDGE']=str(1)
 print("preparing pdf...")
 pdfkit.from_file('tmp.html','advance-'+tech+'-agenda.pdf')

prepareheader()
#prepareday()
preparetailer()
