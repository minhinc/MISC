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
TM=20;PH=1375-TM;hc=0
LH=22;HH=40;CHH=40;HHH=50;CHG=95;HCG=40;CCG=80;OFST=25#lineheight,headerheight,contentheaderheight,contentheadergap,headercontentgap,contentcontentgap
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
 pagenumber+=1
 hc=0
 for data in db.get(tech,'*','name','[[:<:]]h2_',orderby='id',regex=True):
  htmlstr+=""" <div class="header2" style="margin-top:%spx;">
  <pre class="header" style="line-height:%spx">%s</pre>
  <pre class="content" style="height:%spx">%s</pre>
 </div>
""" % (0 if not hc else OFST*5,HH,re.sub(r'^h2_','',data[1]),len(re.findall(r'\n',data[2]))*LH+OFST,data[2])
  hc=HH+(len(re.findall(r'\n',data[2]))+1)*LH+OFST if not hc else hc+5*OFST+HH+(len(re.findall(r'\n',data[2]))+1)*LH+OFST
 
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
     if re.search(r'AfterNoon',agendadaydata[k]['data'],flags=re.I):
      agendadaydata[k]['data']=re.sub(r'XXX',str(CHG+(PH-hc)/hf if (PH-hc)/hf < PH/4 else CHG+(2*(PH-hc))/(3*hf)),agendadaydata[k]['data'])
      hc=hc+(PH-hc)/hf if (PH-hc)/hf < PH/4 else hc+(2*(PH-hc))/(3*hf)
     else:
      agendadaydata[k]['data']=re.sub(r'XXX',str(CHG+(PH-hc)/hf),agendadaydata[k]['data'])
      hc=hc+(PH-hc)/hf
    agendadaydata[k]['data']=re.sub(r'YYY',str(HCG),agendadaydata[k]['data'])
    hf=hf-1
   else:
    if re.search(r'height:\d+px">\n$',htmlstr,flags=re.DOTALL):
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
 LH=20;HBH=21;CH=15;HLH=10;CNTTHR=3*LH
 hc=contentlength=headerheight=lineheight=0
 cnt=fixheader=header=""
 dayhalf=''
 tech=sys.argv[1]
 tstr=''
 code=codes=False
 smax=0
 smin=10*LH
 hcs=0
 CP=5
 CC=2#columncount
 columns=columnb=1
 CHS=9#codeheightshort
 NEWLINEWIDTH=LINEWIDTH=86
 cscount=linecount=0
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
   htmlstr+="""<div class="pg" style="margin-top:%spx;height:%spx">
""" % (TM,PH)
   for ii in re.split(r'\n',db.get(tech,'content','id',day[k][i])[0][0]):
    NEWLINEWIDTH=LINEWIDTH+len(re.findall(r'<b>',ii[0:LINEWIDTH]))*3+len(re.findall(r'</b>',ii[0:LINEWIDTH]))*4
    if len(ii)<=NEWLINEWIDTH:
     cnt+=ii+'\n'
    else:
     while len(ii)>NEWLINEWIDTH and re.search(r'\s',ii[0:NEWLINEWIDTH+1]):
      tstr1,tstr2=re.split(r'<><>',re.sub(r'^(.*)\s+(.*)$','\\1<><>\\2',ii[0:NEWLINEWIDTH+1],flags=re.DOTALL))
      cnt+=tstr1+'\n'
      ii=tstr2+ii[NEWLINEWIDTH+1:]
      NEWLINEWIDTH=LINEWIDTH+len(re.findall(r'<b>',ii[0:LINEWIDTH]))*3+len(re.findall(r'</b>',ii[0:LINEWIDTH]))*4
     else:
      cnt+=ii+'\n'
   if re.search(r'^[\s\n]*$',cnt,flags=re.DOTALL): continue
   header=''
   fixheader=re.sub(r'^\n(.*)\n$','\\1',re.sub(r'\n+','\n',''.join([re.sub(r'</?h>','\n',e) for e in re.findall(r'<h>.*?</h>',cnt,flags=re.DOTALL)])),flags=re.DOTALL)
   print("fixheader><%s<>" % fixheader)
   while cnt:
    if re.search(r'^\s*<h>.*',cnt):
     header,cnt=re.split(r'<><>',re.sub(r'^\s*<h>\n(.*?)\n</h>\n(.*)$','\\1<><>\\2',cnt,flags=re.DOTALL))
     headerheight=(len(re.findall(r'\n',fixheader))-len(re.findall(r'\n',header)))*HLH+(len(re.findall(r'\n',header))+1)*HBH+42+32 #42+32 is for header day and topic
     print("headerheight %s" % headerheight)
     tstr=""" <div class="slideheader" style="height:%spx">
  <pre class="day">%s</pre>
  <pre class="topic">%s</pre>
  <ul class="slidecontent">
""" % (headerheight,'Day '+str(k+1)+' '+dayhalf,'  '+str(day[k][i])+'. '+db.get(tech,'name','id',day[k][i])[0][0])
     for line in [line for line in re.split(r'('+re.escape(header)+r')',fixheader) if line]:
      line=re.sub(r'^\n*(.*)\n*$','\\1',line,flags=re.DOTALL)
      for ii in [ii for ii in re.split(r'^[*]',line,flags=re.M) if ii]:
       tstr+="""   <li class="%s"><pre>%s</pre></li>""" % ("big" if line==header else "sml",re.sub(r'\n*(.*)\n*$','\\1',ii,flags=re.DOTALL))
     tstr+='''  
  </ul>
 </div>
'''
     header=tstr
    code=False
    prog,cnt=re.split(r'<><>',re.sub(r'(.*?)\n?(<h>.*)','\\1<><>\\2',cnt,flags=re.DOTALL)) if re.search(r'<h>',cnt) else (cnt,'')
    if re.search(r'<a>.*?</a>',prog,flags=re.DOTALL):
     header+='<pre class="slideabstract">\n'+re.sub(r'<((?!(b>|/b>)).*?)>',r'&lt;\1&gt;',re.sub(r'&',r'&amp;',re.sub(r'^.*<a>\n*(.*?)\n*</a>.*$','\\1',prog,flags=re.DOTALL)),flags=re.DOTALL)+'\n</pre>'
     prog=re.sub(r'^.*</a>\n?(.*)$','\\1',prog,flags=re.DOTALL)
    lineheight=LH
    if header:
     header+='<pre class="slidecontent">\n'
    else:
     htmlstr+='<pre class="slidecontent">\n'
    linecount=0
    for line in prog.split('\n'):
     linecount+=1
     lineheight=CH if code else CHS if codes else LH
     if re.search(r'<i>.*</i>',line):
      with Image.open(urllib2.urlopen(re.sub(r'<i>(.*?)</i>','\\1',line))) as img:
       lineheight=img.height
      line="""%s<img class="img" src="%s" style="height:%spx"/>%s
""" % ('<a href="'+re.sub(r'<i>(.*)_s[.](.*)</i>','\\1.\\2',line)+'">' if re.search(r'_s[.]',line) else '' ,re.sub(r'<i>(.*?)</i>','\\1',line),lineheight,'</a>' if re.search(r'_s[.]',line) else '')
     elif re.search(r'<c>',line):
      lineheight=CH
      if re.search(r'<c>.*</c>',line):
       line=r'<pre class="code">'+(re.sub(r'<',r'&lt;',re.sub(r'>',r'&gt;',re.sub(r'&',r'&amp;',re.sub(r'<c>(.*)</c>','\\1',line)))) if not re.search(r'.*<\s*(pre|b).*$',re.sub(r'<c>(.*)</c>','\\1',line)) else re.sub(r'<c>(.*)</c>','\\1',line))+'</pre>'
       smax+=lineheight/3
      else:
       if header:
        header+='<pre class="code">'
       else:
        htmlstr+='<pre class="code">'
       code=True
       continue
     elif re.search(r'</c>',line):
      if header:
       header+='</pre>'
      else:
       htmlstr+='</pre>'
      code=False
      continue
     elif re.search(r'<cs>',line):
      codes=True
      lineheight=CHS
      if header:
       htmlstr+=header
       hc+=headerheight+contentlength
       header=''
       headerheight=contentlength=0
      hcs=hc
      hc+=CP
      htmlstr+='<pre class="codes">'
      for cc,ii in enumerate(prog.split('\n')[linecount:]):
       if re.search(r'</cs>',ii):
        cscount=cc
        smax=smin+2*CHS if smin > (cscount*CHS)/CC else int((cscount*CHS)/CC)+2*CHS
        break
      continue
     elif re.search(r'</cs>',line):
      if header:
       header+='</pre><pre style="clear:both"></pre>'
      else:
       htmlstr+='</pre><pre style="clear:both"></pre>'
      codes=False
      if columns>1:
       hc=PH-BTMOFST
       columns=1
      elif columnb>1:
       hc=hcs+smax
       columnb=1
      continue
     else:
      line=re.sub(r'<',r'&lt;',re.sub(r'>',r'&gt;',re.sub(r'&',r'&amp;',line)))+'\n' if not re.search(r'.*<\s*(pre|b).*$',line) else line+'\n'
#      print("hc,lineheight,headerheight,contentlength,line,%s,%s,%s,%s><%s<>" % (hc,lineheight,headerheight,contentlength,line))
     if (PH-hc-headerheight-contentlength-lineheight-BTMOFST)<0:
      if header:
       htmlstr+="""<pre class="ftr">&copy www.minhinc.com</pre><pre class="pn">%s</pre>
</div> <div class="pg" style="margin-top:%spx;height:%spx">
%s%s""" % (pagenumber,TM,PH,header,line)
       hc=headerheight+contentlength+lineheight
       header=''
       headerheight=contentlength=0
       pagenumber+=1
      elif not codes:  
       htmlstr+="""%s
<pre class="ftr">&copy www.minhinc.com</pre><pre class="pn">%s</pre>
</div>
<div class="pg" style="margin-top:%spx;height:%spx">
%s""" % ('</pre></pre>' if code else '</pre>',pagenumber,TM,PH,'<pre class="slidecontent">\n<pre class="code">'+line if code else '<pre class="slidecontent">\n'+line)
       hc=lineheight
       pagenumber+=1
      else:
       cscount-=1
       if (hc-hcs)<smin and columns==1:
        htmlstr,tstr=re.split(r'<><>',re.sub(r'(.*)(<pre class="codes">.*)','\\1<><>\\2',htmlstr,flags=re.DOTALL))
        htmlstr+="""<pre class="ftr">&copy www.minhinc.com</pre><pre class="pn">%s</pre>
</div>
<div class="pg" style="margin-top:%spx;height:%spx">
%s""" % (pagenumber,TM,PH,'<pre class="slidecontent">\n'+tstr+line)
        pagenumber+=1
        hc=hc-hcs+lineheight
        hcs=0
       else:
        columns+=1
        if columns<=CC:
         htmlstr+='</pre><pre class=codes>'+line
         hc=hcs+lineheight+CP#codepadding
        else:
         smax=smin+2*CHS if smin > (cscount*CHS)/CC else int((cscount*CHS)/CC)+2*CHS
         htmlstr+="""%s
<pre class="ftr">&copy www.minhincone.com</pre><pre class="pn">%s</pre>
</div>
<div class="pg" style="margin-top:%spx;height:%spx">
%s""" % ('</pre>',pagenumber,TM,PH,'<pre class="slidecontent">\n<pre class="codes">'+line)
         pagenumber+=1
         columns=1
         hcs=0
         hc=lineheight+CP
     else:
      if not codes:
       if header:
        if (contentlength+lineheight)>CNTTHR:
         htmlstr+=header+line
         hc+=headerheight+contentlength+lineheight
         header=''
         headerheight=contentlength=0
        else:
         header+=line
         contentlength+=lineheight
       else:
        htmlstr+=line
        hc+=lineheight
      else:
       cscount-=1
       if (hc-hcs+lineheight)>smax and columns == 1:
        columnb+=1
        if columnb<=CC:
         htmlstr+="""%s%s""" % ('</pre>','<pre class=codes>'+line)
         hc=hcs+lineheight+CP
        else:
         htmlstr+='</pre><pre style="clear:both" class="codes">'+line
         hcs=hc
         hc+=lineheight+CP
         columnb=1
       else:
        htmlstr+=line
        hc+=lineheight
    else:
     if header:
      htmlstr+=header
      hc+=headerheight+contentlength#LH is for </pre> one empty newline
      header=''
      headerheight=contentlength=0
     htmlstr+='</pre>'
   htmlstr+="""<pre class="ftr">&copy www.minhinc.com</pre><pre class="pn">%s</pre>
</div>
""" % pagenumber
   pagenumber+=1
   hc=0
  if not pagenumber%2:
   htmlstr+="""<div class="pg" style="margin-top:%spx;height:%spx">
%s
<pre class="ftr">&copy www.minhinc.com</pre><pre class="pn">%s</pre>
</div>
""" % (TM,PH,'<pre style="text-align:center;line-height:'+str(PH)+'px;font-size:24pt">Left Blank</pre>',pagenumber)
   pagenumber+=1

def preparetailer():
 f.write(htmlstr+"""%s
%s
""" % (open('footer.txt').read(),'</body></html>'))
 f.close()
def preparepdf():
 import pdfkit
 import os
 os.environ['NO_AT_BRIDGE']=str(1)
 print("preparing pdf...")
 with open('tmp.html','w') as file:
  file.write(re.sub(r'.*?(<META.*agenda.css"\s+media="all"/>).*?(<div\s+class="pg".*)',r'<html>\n<head>\n\1\n</head>\n<body>\n\2\n</body>\n</html>',htmlstr,flags=re.DOTALL))
 pdfkit.from_file('tmp.html','advance-'+sys.argv[1]+'-agenda.pdf')
   
  
prepareheader()
preparedisclaimer()
preparecontent()
preparetailer()
preparepdf()
