import sys
import re
from databasem import databasec
day=[]
tech=sys.argv[1]
company=sys.argv[2]
for i in range(3,len(sys.argv)):
 day.append(sys.argv[i].split(':')[0].split()+[':']+sys.argv[i].split(':')[1].split())
f=open('abc.txt','w')
db=databasec(False)
PH=1250;hc=0
LH=25;HH=45;DH=65;DHCG=30;DCG=50;TM=40;OFST=25#dayheadercontentgap,daycontentgap,pagemargin
BTMOFST=25
def prepareheader():
 global PH;global hc;
 top='';toph=0;left=True;
 l='';header=''
 f.write("""<html>
<head>
<META http-equiv="Content-Type" content="text/html; charset=UTF-8">
<link rel="stylesheet" type="text/css" href="./agenda.css" media="all"/>
</head>
<body>
<div class=pg>
""")

 f.write(""" <pre class=title>%s</pre>
 <pre class=subtitle>%s</pre>
 <pre class=company>(%s)</pre>
""" % (db.get(tech,'value','name','title')[0][0],db.get(tech,'value','name','subtitle')[0][0],db.get(tech,'value','name','company')[0][0]))

 for data in db.get(tech,'*','name','[[:<:]]h_',orderby='id',regex=True):
  if not re.search(r'h_hr',data[1]):
   f.write(""" <div style="height:%spx;">
  <div class="headerleft"> <pre>%s</pre></div>
  <div class="headerright"> <pre>%s</pre></div>
 </div>
""" % (max(len(re.findall(r'\n',data[1]))+1,len(re.findall(r'\n',data[2]))+1)*LH+OFST,re.sub(r'^h_','',data[1]),data[2]))
  else:
   f.write(''' <hr>
''')
 f.write('''</div>

<div class=pg>
''')
 for data in db.get(tech,'*','name','[[:<:]]h2_',orderby='id',regex=True):
  f.write(""" <div class="header2" style="margin-top:%spx;height:%spx">
  <pre class="header">%s</pre>
  <pre class="content">%s</pre>
 </div>
""" % (TM if not hc else OFST*3,HH+len(re.findall(r'\n',data[2]))*LH+OFST,re.sub(r'^h2_','',data[1]),data[2]))
  hc=TM+HH+len(re.findall(r'\n',data[2]))*LH+OFST if not hc else hc+3*OFST+HH+len(re.findall(r'\n',data[2]))*LH+OFST

 for k in range(0,len(day)):
  left=True
  for i in range(0,len(day[k])):
   if left and top:
    toph=DCG+HH+toph*LH+OFST
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
 printdata(top,DCG+DH+DHCG+HH+toph*LH+OFST,0)
def calculateh(k,i,l):
 print("calculateh k,i,l %s,%s,%s" % (k,i,l))
 th=0;tr=0;reth=0
 for t in range(i,len(day[k])):
  tr=tr+1
  if tr>2:
   print("reth %s" % reth)
   reth+=DCG+HH+th*LH+OFST
   return reth
  if not re.search(r'^[Ll:]$',day[k][t]):
   l=db.get(tech,'lab','id',day[k][t])[0][0] if l=='' else l+'\n'+db.get(tech,'lab','id',day[k][t])[0][0]
  if t==0 or day[k][t]==':':
   if t!=i:
    reth+=DCG+HH+th*LH+OFST
    print("reth %s" % reth)
    return reth
   reth=DH+DHCG
   if day[k][t]==':':
    tr=tr-1
    continue
  th=max(th,len(re.findall(r'\n',l)) if re.search(r'^[Ll]$',day[k][t]) else len(re.findall(r'\n',db.get(tech,'value','id',day[k][t])[0][0])))
 reth+=DCG+HH+th*LH+OFST
 print("><calculate %s" % reth)
 return reth
 
def printdata(top,toph,bottomh):
 global PH;global hc;global DCG;global TM;global BTMOFST
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
   hc=toph-DCG+TM
   f.write(re.sub(r'XXX',str(TM),top))
  else:
   hc=hc+toph
   f.write(re.sub(r'XXX',str(DCG),top))
 elif PH>(hc+toph+BTMOFST):
  if hc==0:
   hc=toph-DCG+TM
   f.write(re.sub(r'XXX',str(TM),top))
  else:
 # elif (PH-hc-toph)<(PH/100):
   print("num den %s,%s" % (num,den))
   f.write(re.sub(r'XXX',str((((PH-hc-toph-BTMOFST)*num)/den)+DCG),top))
   f.write('''</div>
<div class="pg">
''')
   hc=0
 # else:
 #  hc=hc+toph
 #  f.write(re.sub(r'XXX',str(DCG),top))
 else:
  hc=toph-DCG+TM
  f.write('''</div>
<div class="pg">
''')
  f.write(re.sub(r'XXX',str(TM),top))
 print("><printdata hc %d" % hc)
 

def preparetailer():
 f.write('''
 <pre class="ftr">&copy www.minhinc.com</pre>
</div>
</html>''')
 f.close()

prepareheader()
#prepareday()
preparetailer()
