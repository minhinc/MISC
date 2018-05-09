import sys
import re
from PIL import Image
from databasem import databasec
import urllib.request as urllib2
import string
if len(sys.argv)<4:
 print(''' ---usage---
 agenda.py <tech> <company> <iddaywise>
 agenda.py qt claysol "1 2 3:4 L" "4 5 6:L"
 agenda.py qt '' "1 2 3:4 L" "4 5 6:L"''')
 exit(-1)
day=[]
company=sys.argv[2] if not re.search(r'^(''|"")$',sys.argv[2],flags=re.I) else None
for i in range(3,len(sys.argv)):
 if re.search(r':',sys.argv[i]):
  day.append(sys.argv[i].split(':')[0].split()+[':']+sys.argv[i].split(':')[1].split())
 else:
  day.append(sys.argv[i].split())
f=open('advance-'+sys.argv[1]+'-agenda.html','w')
db=databasec(False)
TM=20;PH=1368-TM;hc=0
LH=24;HH=40;CHH=40;HHH=50;CHG=95;HCG=40;CCG=80;OFST=25#lineheight,headerheight,contentheaderheight,contentheadergap,headercontentgap,contentcontentgap
BTMOFST=20
htmlstr="";pagenumber=0
def prepareheader():
 global htmlstr;global pagenumber
 global PH;global hc;
 top='';left=True;
 tech=sys.argv[1]
 l='';header=''
 numofline=0
 height=0
 agendadaydata=[]
 htmlstr+="""<html>
<head>
<title>%s</title>
<META http-equiv="Content-Type" content="text/html; charset=UTF-8">
<link rel="stylesheet" type="text/css" href="../css/main.css" media="all"/>
<link rel="stylesheet" type="text/css" href="../css/agenda.css" media="all"/>
%s
<div class="pg" style="margin-top:%spx;height:%spx">
""" % ('Minh, Inc. Software development and Outsourcing | '+string.capwords(tech)+' Training Bangalore',open('header.txt').read(),2*TM,PH-TM)

 for data in db.get(tech,'*','name','[[:<:]]h_',orderby='id',regex=True):
  numofline=numofline+max(len(re.findall(r'\n',str(data[1])))+1,len(re.findall(r'\n',str(data[2])))+1)
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
""" % (max(len(re.findall(r'\n',data[1]))+1,len(re.findall(r'\n',data[2]))+1)*LH+int((50*OFST)/numofline),re.sub(r'^h_','',data[1]),data[2])
  else:
   htmlstr+=''' <hr>
'''
 pagenumber=pagenumber+1
 htmlstr+="""<pre class="ftr">&copy www.MinhInc.com</pre><pre class="pn">%s</pre>
</div>

<div class="pg" style="margin-top:%spx;height:%spx">
""" % (pagenumber,TM,PH)
 hc=0
 for data in db.get(tech,'*','name','[[:<:]]h2_',orderby='id',regex=True):
  htmlstr+=""" <div class="header2" style="margin-top:%spx;">
  <pre class="header">%s</pre>
  <pre class="content" style="height:%spx">%s</pre>
 </div>
""" % (0 if not hc else OFST*5,re.sub(r'^h2_','',data[1]),len(re.findall(r'\n',data[2]))*LH+OFST,data[2])
  hc=HH+len(re.findall(r'\n',data[2]))*LH+OFST if not hc else hc+5*OFST+HH+len(re.findall(r'\n',data[2]))*LH+OFST
 
 for k in range(0,len(day)):
  for i in range(0,len(day[k])):
   if not re.search(r'^(\d+|:|l|L)$',day[k][i],flags=re.I):
    tech=day[k][i]
    continue
   if not re.search(r'^[Ll:]$',day[k][i]):
    l=db.get(tech,'lab','id',day[k][i])[0][0] if l=='' else l+'\n'+db.get(tech,'lab','id',day[k][i])[0][0];
   if top and (left or i==0 or day[k][i]==':'):
    top=header+top
    height=height+CHG+HHH+HCG+CHH if header else height+CCG+CHH
    agendadaydata.append({'height':height,'data':top})
    top=header=''
    height=0
   if i==0 or day[k][i]==':':
    left=True
    header=""" <div class="dayheader" style="margin-top:XXXpx;height:%spx"><pre>Day %s %s</pre><hr></div>
""" % (str(HHH),k+1,"Afternoon" if day[k][i]==':' else "Morning")
    if day[k][i]==':':
     continue
   top+=""" <div class=%s style="margin-top:YYYpx;height:%spx">
  <pre class="%s" style="line-height:%spx">%s</pre>
  <ul class="%s" style="padding-top:10px;float:%s">
""" % ('dayheaderleft' if left else 'dayheaderright',(len(re.findall(r'\n',l))+1)*LH+CHH if re.search(r'^[Ll]$',day[k][i]) else (len(re.findall(r'\n',db.get(tech,'value','id',day[k][i])[0][0]))+1)*LH+CHH,'dayheader',str(CHH),'     Lab' if re.search(r'[Ll]',day[k][i]) else '  Lecture - '+db.get(tech,'name','id',day[k][i])[0][0],'daycontent','left' if left else 'right')  
   for le in [re.sub(r'\n$','',e) for e in re.split(r'[*]',l if  re.search(r'^[Ll]$',day[k][i]) else db.get(tech,'value','id',day[k][i])[0][0]) if e]:
    top+="""   <li><pre>%s</pre></li>
""" % le
   top+='''
  </ul>
 </div>
'''
   height=max(height,(len(re.findall(r'\n',l))+1)*LH+10 if re.search(r'^[Ll]$',day[k][i]) else (len(re.findall(r'\n',db.get(tech,'value','id',day[k][i])[0][0]))+1)*LH+10)#10 is ul padding top
   if re.search(r'^[Ll]$',day[k][i]): l=''
   left=not left
 if top:
  top=header+top
  height=height+CHG+HHH+HCG+CHH if header else height+CCG+CHH
  agendadaydata.append({'height':height,'data':top})

 hc+=BTMOFST
 boundry=hf=cf=ii=0
 for k in range(0,len(agendadaydata)):
  if k==boundry: ii=k
  while k==boundry and ii<len(agendadaydata) and (PH-hc-agendadaydata[ii]['height'])>0:
   hc+=agendadaydata[ii]['height']
   if re.search(r'XXX',agendadaydata[ii]['data']):
    hf+=1
   else:
    cf+=1
   ii+=1
  else:
   if re.search(r'XXX',agendadaydata[k]['data']):
    if re.search(r'height:\d+px">\n$',htmlstr,flags=re.DOTALL):
     agendadaydata[k]['data']=re.sub(r'XXX',str(0),agendadaydata[k]['data'])
     hc=hc-CHG
    else:
     agendadaydata[k]['data']=re.sub(r'XXX',str(CHG+(PH-hc)/hf),agendadaydata[k]['data'])
     hc=hc+(PH-hc)/hf
    agendadaydata[k]['data']=re.sub(r'YYY',str(HCG),agendadaydata[k]['data'])
    hf=hf-1
   else:
    if re.search(r'<div class="pg" style="height:\d+px">\n$',htmlstr,flags=re.DOTALL):
     agendadaydata[k]['data']=re.sub(r'YYY',str(0),agendadaydata[k]['data'])
     hc=hc-CCG
    else:
     if not hf:
      agendadaydata[k]['data']=re.sub(r'YYY',str(CCG+(PH-hc)/(4*cf)),agendadaydata[k]['data'])
      hc=hc+(PH-hc)/(4*cf)
     else:
      agendadaydata[k]['data']=re.sub(r'YYY',str(CCG),agendadaydata[k]['data'])
    cf=cf-1
   boundry=ii
  htmlstr+=agendadaydata[k]['data']
  if k+1==boundry: 
   htmlstr+=""" <pre class="ftr">&copy www.MinhInc.com</pre><pre class="pn">%s</pre>
</div>
%s
""" % (pagenumber,'<div class="pg" style="margin-top:'+str(TM)+'px;height:'+str(PH)+'px">' if (k+1)!=len(agendadaydata) else '')
   pagenumber=pagenumber+1
   hc=BTMOFST

def preparedisclaimer():
 global htmlstr,pagenumber
 htmlstr+="""<div class="pg" style="margin-top:%spx;height:%spx">
 <pre class="slidetitle" style="margin-top:%spx">%s</pre>
 <pre class="slidesubtitle style="margin-top:%spx">%s</pre>
 <pre class="ftr">&copy www.MinhInc.com</pre><pre class="pn">%s</pre>
</div>
<div class="pg" style="margin-top:%spx;height:%spx">
 <pre class="slidedisclaimer" style="margin-top:%spx">%s</pre>
 <pre class="ftr">&copy www.MinhInc.com</pre><pre class="pn">%s</pre>
</div>
""" % (TM,PH-TM,TM*2,string.capwords(sys.argv[1])+' Essentials',TM,string.capwords(sys.argv[1])+' Essenstials- Training Course',pagenumber+1,TM,PH-TM,2*TM,'''DISCLAIMER

This document is edited on Cent OS 5 using Open Office 3.1.1 Draw Package.

CentOS is freely download from centos.org/download
Open Office 3.1.1 can be obtained through yum or through openoffice.org

Text of this document is written in Bembo Std Otf(13 pt) font.

Code parts are written in Consolas (10 pts) font.

This training material is provided through Minh, Inc, B'lore, India
Document is available at minhinc.com/training/advance-c-slides.pdf
For suggestion(s) or complaint(s) write to us at training@minhinc.com

Document modified on 05/2018

Document contains xx pages.''',pagenumber+2)
pagenumber+=2

def preparecontent():
 global htmlstr,pagenumber
 global PH,TM,OFST,BTMOFST
 LH=24;HBH=19;CH=15;HLH=10;CNTTHR=6*LH
 HTBF=22 # headeroffsetbefore and headeroffsetafter
 hc=contentlength=headerheight=lineheight=0
 cnt=fixheader=header=""
 dayhalf=''
 tech=sys.argv[1]
 tstr=''
 code=False
 htmlstr+="""<div class="pg" style="margin-top:%spx;height:%spx">
""" % (TM,PH)
 for k in range(0,len(day)):
  dayhalf='Morning'
  for i in range(0,len(day[k])):
   if not re.search(r'^(\d+|:|l|L)$',day[k][i],flags=re.I):
    tech=day[k][i]
    continue
   if re.search(r'^(:|l|L)$',day[k][i],flags=re.I):
    if day[k][i]==':':
     dayhalf='Afternoon'
    continue
   for ii in re.split(r'\n',db.get(tech,'content','id',day[k][i])[0][0],flags=re.DOTALL):
    if not ii:
     cnt+='\n'
     continue
    for kk in range(0,len(ii),84):
     cnt+=ii[kk:kk+84]+'\n'
   if re.search(r'^[\s\n]*$',cnt,flags=re.DOTALL): continue
   header=''
   fixheader=re.sub(r'^\n(.*)\n$','\\1',re.sub(r'\n+','\n',''.join([re.sub(r'</?h>','\n',e) for e in re.findall(r'<h>.*?</h>',cnt,flags=re.DOTALL)])),flags=re.DOTALL)
   print("fixheader><%s<>" % fixheader)
   while cnt:
    if re.search(r'^\s*<h>.*',cnt):
     header,cnt=re.split(r'<><>',re.sub(r'^\s*<h>\n?(.*?)\n?</h>\n*(.*)','\\1<><>\\2',cnt,flags=re.DOTALL))
     headerheight=(len(re.findall(r'\n',fixheader))+2)*HBH-(len(re.findall(r'\n',header))+1)*(HBH-HLH)+HTBF+3*HBH #3*HBH is for header day and topic
     tstr=""" <div class="slideheader" style="margin-top:XXXpx;margin-bottom:%spx;height:%spx">
  <pre class="day">%s</pre>
  <pre class="topic">%s</pre>
  <ul class="content">
""" % (HTBF,headerheight,'Day '+str(k+1)+' '+dayhalf,'  '+str(day[k][i])+'. '+db.get(tech,'name','id',day[k][i])[0][0])
     for line in [line for line in re.split(r'('+re.escape(header)+r')',fixheader) if line]:
      line=re.sub(r'^\n*(.*)\n*$','\\1',line,flags=re.DOTALL)
      for ii in [ii for ii in re.split(r'^[*]',line,flags=re.M) if ii]:
       tstr+="""   <li class="%s"><pre>%s</pre></li>""" % ("big" if line==header else "sml",re.sub(r'\n*(.*)\n*$','\\1',ii,flags=re.DOTALL))
     tstr+='''  
  </ul>
 </div>
'''
     header=tstr
    print("cnt><%s<>,header><%s<>" % (cnt,header))
    if re.sub(r'^(.*?)<h>.*','\\1',cnt,flags=re.DOTALL):
#    if re.search(r'.+<h>.*$',cnt,flags=re.DOTALL):
     print("entered")
     prog,cnt=re.split(r'<><>',re.sub(r'^(.*?)\n(<h>.*)','\\1<><>\\2',cnt,flags=re.DOTALL)) if re.search(r'<h>',cnt) else (re.sub(r'\n?$','',cnt),'')
     lineheight=LH
     if header:
      header+=''' <pre class="slidecontent">
'''
      contentlength+=LH
     else:
      htmlstr+=''' <pre class="slidecontent">
'''
      hc+=LH
     for line in prog.split('\n'):
      lineheight=CH if code else LH
      if re.search(r'<i>.*</i>',line):
       print("line%s" % line)
       with Image.open(urllib2.urlopen(re.sub(r'<i>(.*?)</i>','\\1',line))) as img:
        lineheight=img.height
       line="""<img class="img" src="%s"/>""" % re.sub(r'<i>(.*?)</i>','\\1',line)+'\n'
      elif re.search(r'<c>',line):
       if header:
        header+='''  <pre class="code">
'''
        contentlength+=LH
       else:
        htmlstr+='''  <pre class="code">
'''
        hc+=LH
       lineheight=CH
       code=True
       continue
      elif re.search(r'</c>',line):
       if header:
        header+='''  </pre>
'''
        contentlength+=LH
       else:
        htmlstr+='''  </pre>
'''
        hc+=LH
       code=False
       continue
      else:
       line+='\n'
#      print("line><%s<>,contentlength><%s<>,lineheight><%s<>,CNTTHR><%s<>,hc><%s<>" % (line,contentlength,lineheight,CNTTHR,hc))
      if (PH-hc-headerheight-contentlength-lineheight-BTMOFST)<0:
       if header:
        htmlstr+="""<pre class="ftr">&copy www.minhinc.com</pre><pre class="pn">%s</pre>
</div>
<div class="pg" style="margin-top:%spx;height:%spx">
%s
""" % (pagenumber,TM,PH,re.sub(r'XXX',str(0),header)+line)
        hc=headerheight+contentlength+lineheight
        header=''
        headerheight=contentlength=0
       else:
        htmlstr+="""%s
<pre class="ftr">&copy www.minhinc.com</pre><pre class="pn">%s</pre>
</div>
<div class="pg" style="margin-top:%spx;height:%spx">
%s
""" % ('  </pre></pre>' if code else ' </pre>',pagenumber,TM,PH,' <pre class="slidecontent"><pre class="code">\n'+re.sub(r'\n?$','',line) if code else '<pre class="slidecontent">\n'+re.sub(r'\n?$','',line))
        hc=lineheight
       pagenumber+=1
      else:
       if header:
        if (contentlength+lineheight)>=CNTTHR:
         header=re.sub(r'XXX',str(0),header) if re.search(r'height:\d+px\n?$',htmlstr,flags=re.DOTALL) else re.sub(r'XXX',str(HTBF),header)
#         print("current line><%s<>" % line)
         htmlstr+=header+line
         hc+=HTBF+headerheight+contentlength+lineheight
         header=''
         headerheight=contentlength=0
        else:
         header+=line
         contentlength+=lineheight
       else:
#        print("<><><>current line><%s<>" % line)
        htmlstr+=line
        hc+=lineheight
     else:
      if header:
       htmlstr+=re.sub(r'XXX',str(HTBF),header)
       hc+=HTBF+headerheight+contentlength+lineheight+LH#LH is for </pre> one empty newline
       header=''
       headerheight=contentlength=0
      htmlstr+=''' </pre>
'''
 htmlstr+="""<pre class="ftr">&copy www.minhinc.com</pre><pre class="pn">%s</pre>
</div>
""" % pagenumber

def preparetailer():
 f.write(htmlstr+"""%s
%s
""" % (open('footer.txt').read(),'</body></html>'))
 f.close()
 with open('tmp.html','w') as file:
  file.write(htmlstr)
# import pdfkit
# import os
# os.environ['NO_AT_BRIDGE']=str(1)
# print("preparing pdf...")
# pdfkit.from_file('tmp.html','advance-'+sys.argv[1]+'-agenda.pdf')
   
  
prepareheader()
preparedisclaimer()
preparecontent()
preparetailer()
