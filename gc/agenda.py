import sys
import re
from PIL import Image
from databasem import databasec
import urllib.request as urllib2
import urllib.error as urllib3
import string
print(sys.argv)
if len(sys.argv)<6 or not re.search(r'^(m|d).*',sys.argv[1],flags=re.I) or not re.search(r'^(agenda|pdf|php)$',sys.argv[2],flags=re.I):
 print(''' ---usage---
 agenda.py <backend> <mode> <tech> <company> <iddaywise>
 agenda.py mobile php qt '' "1 2 3:4 L" "4 5 6:L"
 agenda.py [desktop|mobile] [agenda|pdf|php] [c|cpp|gl|li|ldd|py|qt|qml] '' "1 2 3:4 L" "4 5 6:L"''')
 exit(-1)
class agenda:
 def __init__(self):
  self.backend=sys.argv[1]
  self.mode=sys.argv[2]
  self.tech=sys.argv[3]
  self.company=sys.argv[4]
  self.day=[]
  for i in range(5,len(sys.argv)):
   if re.search(r':',sys.argv[i]):
    self.day.append(sys.argv[i].split(':')[0].split()+[':']+sys.argv[i].split(':')[1].split())
   else:
    self.day.append(sys.argv[i].split())
  self.TM=20
#  self.PH=(1375 if self.mode=="agenda" else 1415 if self.tech!='qt' else 1430)-self.TM
  self.PH=(1375 if self.mode=="agenda" else 1415)-self.TM
  self.BTMOFST=20
  self.hc=0
  self.htmlstr=''
  if self.backend[0]=='m':
   self.file=open('advance-'+self.tech+'-slides_m.txt','w')
  else:
   self.file=open('advance-'+self.tech+'-slides.txt','w')
  self.db=databasec(False)
  self.pagenumber=0
  self.prepareagenda()
  if self.mode!='agenda':
   self.preparecontent()
  self.preparepdf()
 def prepareagenda(self):
  LH=22;HH=40;OFST=25#headerheight
  CHH=40;HHH=50;CHG=95;HCG=40;CCG=80#contentheaderheight,contentheadergap,headercontentgap,contentcontentgap
  numofline=0
  top='';left=True;
  l='';header=''
  height=0
  agendadaydata=[]
  subtopiccount=0
  self.placetopbreak(True)
  self.htmlstr+=""" <pre class=title>%s</pre>
 <pre class=subtitle>%s</pre>
 <pre class=company>%s</pre>
""" % (self.db.get(self.tech,'value','name','title')[0][0],self.db.get(self.tech,'value','name','subtitle')[0][0],'('+self.company+')' if self.company else '')
  for data in self.db.get(self.tech,'*','name','[[:<:]]h_',orderby='id',regex=True):
   numofline=numofline+max(len(re.findall(r'\n',str(data[1])))+1,len(re.findall(r'\n',str(data[2])))+1)
  for data in self.db.get(self.tech,'*','name','[[:<:]]h_',orderby='id',regex=True):
   if not re.search(r'h_hr',data[1]):
    self.htmlstr+=""" <div style="height:%spx;">
   <div class="headerleft"> <pre>%s</pre></div>
   <div class="headerright"> <pre>%s</pre></div>
  </div>
""" % (max(len(re.findall(r'\n',data[1]))+1,len(re.findall(r'\n',data[2]))+1)*LH+int((50*OFST)/numofline),re.sub(r'^h_','',data[1]),data[2])
   else:
    self.htmlstr+=''' <hr>
'''
  self.placepagebreak()
  self.hc=0
  for data in self.db.get(self.tech,'*','name','[[:<:]]h2_',orderby='id',regex=True):
   self.htmlstr+=""" <div class="header2" style="margin-top:%spx;">
   <pre class="header" style="line-height:%spx">%s</pre>
   <pre class="content" style="height:%spx">%s</pre>
  </div>
""" % (0 if not self.hc and self.backend!='m' else OFST*5,HH,re.sub(r'^h2_','',data[1]),len(re.findall(r'\n',data[2]))*LH+OFST,data[2])
   self.hc=HH+(len(re.findall(r'\n',data[2]))+1)*LH+OFST if not self.hc else self.hc+5*OFST+HH+(len(re.findall(r'\n',data[2]))+1)*LH+OFST
  
  for k in range(0,len(self.day)):
   for i in range(0,len(self.day[k])):
    if not re.search(r'^(\d+|:|l|L)$',self.day[k][i],flags=re.I):
     self.tech=self.day[k][i]
     continue
    if not re.search(r'^[Ll:]$',self.day[k][i]):
     l=self.db.get(self.tech,'lab','id',self.day[k][i])[0][0] if l=='' else l+('\n'+self.db.get(self.tech,'lab','id',self.day[k][i])[0][0] if self.db.get(self.tech,'lab','id',self.day[k][i])[0][0] else '')
    if top and (left or i==0 or self.day[k][i]==':' or (i==1 and not re.search(r'^(\d+|:|l|L)$',self.day[k][0],flags=re.I))):
     top=header+top
     height=height+CHG+HHH+HCG+CHH if header else height+CCG+CHH
     agendadaydata.append({'height':height,'data':top})
     top=header=''
     height=0
    if i==0 or self.day[k][i]==':' or (i==1 and not re.search(r'^(\d+|:|l|L)$',self.day[k][0],flags=re.I)):
     left=True
     header=""" <div class="dayheader" style="margin-top:XXXpx;height:%spx"><pre>Day %s %s</pre><hr></div>
""" % (str(HHH),k+1,"Afternoon" if self.day[k][i]==':' else "Morning")
     if self.day[k][i]==':':
      continue
    top+=""" <div class=%s style="margin-top:YYYpx;%s">
   <div class="dayheaderheader" style="height:%spx">%s class="%s" style="padding-top:%spx;%spx">%s%s</div>
   <ul class="%s" style="padding-top:10px;float:%s">
""" % ('dayheaderleft' if left else 'dayheaderright','height:'+str((len(re.findall(r'\n',l))+1)*LH+CHH)+'px' if re.search(r'^[Ll]$',self.day[k][i]) and self.backend!='m' else 'height:'+str((len(re.findall(r'\n',self.db.get(self.tech,'value','id',self.day[k][i])[0][0]))+1)*LH+CHH)+'px' if self.backend!='m' else '',CHH,'<pre' if self.mode=='agenda' or re.search(r'^[Ll]$',self.day[k][i]) else "<a name=\"main"+self.day[k][i]+"\" href=\"#chap"+str(self.day[k][i])+"\"",'dayheader',CHH/4 if not re.search(r'^[Ll]$',self.day[k][i]) else 0,'height:'+str(CHH) if not re.search(r'^[Ll]$',self.day[k][i]) else 'line-height:'+str(CHH),'     Lab' if re.search(r'[Ll]',self.day[k][i]) else '  Lecture - '+self.db.get(self.tech,'name','id',self.day[k][i])[0][0],'</pre>' if self.mode=='agenda' or re.search(r'^[Ll]$',self.day[k][i]) else '</a>','daycontent','left' if left else 'right')
    subtopiccount=0
    for le in [re.sub(r'^\n*(.*?)\n*$',r'\1',e,flags=re.DOTALL) for e in re.split(r'[*]',l if  re.search(r'^[Ll]$',self.day[k][i]) else self.db.get(self.tech,'value','id',self.day[k][i])[0][0]) if e]:
     top+="""   <li>%s%s%s</li>
""" % ('<pre>' if self.mode=='agenda' or re.search(r'^[Ll]$',self.day[k][i]) else "<a href=\"#chap"+str(self.day[k][i])+'_'+str(subtopiccount)+"\">" if self.mode=='pdf' and not re.search(r'^[Ll]$',self.day[k][i]) else '<a href=\"#chap'+self.day[k][i]+'_'+str(subtopiccount)+'\">'+'<pre>',re.sub(r'\n','<br>',le,flags=re.DOTALL) if self.mode=='pdf' and not re.search(r'^[Ll]$',self.day[k][i]) else le,'</pre>' if self.mode=='agenda' or re.search(r'^[Ll]$',self.day[k][i]) else "</a>" if self.mode=='pdf' and not re.search(r'^[Ll]$',self.day[k][i]) else '</pre></a>')
     subtopiccount+=1
    top+='''
   </ul>
  </div>
'''
    height=max(height,(len(re.findall(r'\n',l))+1)*LH+10 if re.search(r'^[Ll]$',self.day[k][i]) else (len(re.findall(r'\n',self.db.get(self.tech,'value','id',self.day[k][i])[0][0]))+1)*LH+10)#10 is ul padding top
    if re.search(r'^[Ll]$',self.day[k][i]): l=''
    left=not left
  if top:
   top=header+top
   height=height+CHG+HHH+HCG+CHH if header else height+CCG+CHH
   agendadaydata.append({'height':height,'data':top})

  if self.backend[0]=='m':
   for k in range(0,len(agendadaydata)):
    if re.search(r'XXX',agendadaydata[k]['data'],flags=re.I):
     self.htmlstr+=re.sub(r'XXX',str(CHG/2),re.sub(r'YYY',str(HCG/2),agendadaydata[k]['data'],flags=re.I),flags=re.I)
    else:
     self.htmlstr+=re.sub(r'YYY',str(CCG/2),agendadaydata[k]['data'],flags=re.I)
  else:
   self.hc+=self.BTMOFST
   boundry=hf=cf=ii=0
   for k in range(0,len(agendadaydata)):
    if k==boundry: ii=k
    while k==boundry and ii<len(agendadaydata) and (self.PH-self.hc-agendadaydata[ii]['height'])>0:
     self.hc+=agendadaydata[ii]['height']
     if re.search(r'XXX',agendadaydata[ii]['data']):
      hf+=1
     else:
      cf+=1
     ii+=1
    else:
     if re.search(r'XXX',agendadaydata[k]['data']):
      if re.search(r'height:\d+px">\n$',self.htmlstr,flags=re.DOTALL):
       agendadaydata[k]['data']=re.sub(r'XXX',str(0),agendadaydata[k]['data'])
       self.hc=self.hc-CHG
      else:
       if re.search(r'AfterNoon',agendadaydata[k]['data'],flags=re.I):
        agendadaydata[k]['data']=re.sub(r'XXX',str(CHG+(self.PH-self.hc)/hf if (self.PH-self.hc)/hf < self.PH/4 else CHG+(2*(self.PH-self.hc))/(3*hf)),agendadaydata[k]['data'])
        self.hc=self.hc+(self.PH-self.hc)/hf if (self.PH-self.hc)/hf < self.PH/4 else self.hc+(2*(self.PH-self.hc))/(3*hf)
       else:
        agendadaydata[k]['data']=re.sub(r'XXX',str(CHG+(self.PH-self.hc)/hf),agendadaydata[k]['data'])
        self.hc=self.hc+(self.PH-self.hc)/hf
      agendadaydata[k]['data']=re.sub(r'YYY',str(HCG),agendadaydata[k]['data'])
      hf=hf-1
     else:
      if re.search(r'height:\d+px">\n$',self.htmlstr,flags=re.DOTALL):
       agendadaydata[k]['data']=re.sub(r'YYY',str(0),agendadaydata[k]['data'])
       self.hc=self.hc-CCG
      else:
       if not hf:
        agendadaydata[k]['data']=re.sub(r'YYY',str(CCG+(self.PH-self.hc)/(4*cf)),agendadaydata[k]['data'])
        self.hc=self.hc+(self.PH-self.hc)/(4*cf)
       else:
        agendadaydata[k]['data']=re.sub(r'YYY',str(CCG),agendadaydata[k]['data'])
      cf=cf-1
     boundry=ii
    self.htmlstr+=agendadaydata[k]['data']
    if k+1==boundry: 
     self.pagenumber=self.pagenumber+1
     self.htmlstr+=""" <pre class="ftr">&copy www.MinhInc.com</pre><a class="pn"><img src="http://minhinc.com/image/arrow.png" width="20px" height="20px"/>%s</a>
</div>
%s
""" % ("p"+str(self.pagenumber),'<div class="pg" style="margin-top:'+str(self.TM)+'px;height:'+str(self.PH)+'px">' if (k+1)!=len(agendadaydata) else '')
     self.hc=self.BTMOFST
  self.htmlstr+='''</div>
<div style="clear:both;"></div>
'''

#
# def preparedisclaimer():
#  self.htmlstr+="""<div class="pg" style="margin-top:%spx;height:%spx">
# <pre class="slidetitle" style="margin-top:%s">%s</pre>
# <pre class="slidesubtitle">%s</pre>
# <pre class="ftr">&copy www.MinhInc.com</pre><pre class="pn">%s</pre>
#</div>
#<div class="pg" style="margin-top:%spx;height:%spx">
# <pre class="slidedisclaimer" style="margin-top:%s">%s</pre>
# <pre class="ftr">&copy www.MinhInc.com</pre><pre class="pn">%s</pre>
#</div>
#""" % (TM,PH,'30%',string.capwords(sys.argv[1])+' Essentials',string.capwords(sys.argv[1])+' Essenstials- Training Course',"p"+str(pagenumber),TM,PH,'30%',"""DISCLAIMER
#
#This document is edited on Cent OS 5 using Open Office 3.1.1 Draw Package.
#
#CentOS is freely download from centos.org/download
#Open Office 3.1.1 can be obtained through yum or through openoffice.org
#
#Text of this document is written in Bembo Std Otf(13 pt) font.
#
#Code parts are written in Consolas (10 pts) font.
#
#This training material is provided through <a style="font-family:mytwcenmt,Tw Cen MT;font-size:14pt;color:#004000;font-weight:bold" href="http://www.minhinc.com">Minh, Inc.</a>, B'lore, India
#Pdf version of this document is available at <a href="http://www.minhinc.com/training/advance-%s-slides.pdf">http://www.minhinc.com/training/advance-%s-slides.pdf</a>
#For suggestion(s) or complaint(s) write to us at <a href="mailto:training@minhinc.com">training@minhinc.com</a>
#
#Document modified on 07/2018
#
#Document contains xxxx pages.""" % (sys.argv[1],sys.argv[1]),"p"+str(pagenumber+1))
#  self.pagenumber+=2
#
 def preparecontent(self):
  LH=20;HBH=21;CH=15;HLH=10;CNTTHR=3*LH
  contentlength=headerheight=lineheight=0
  cnt=fixheader=header=code=dayhalf=""
  CCH=CSH=9.5
  LINEWIDTH=84
  CODELINEWIDTH=104
  cscount=linecount=subtopiccount=0
  self.placetopbreak()
  self.hc=self.BTMOFST
  for k in range(0,len(self.day)):
   dayhalf='Morning'
   for i in range(0,len(self.day[k])):
    if not re.search(r'^(\d+|:|l|L)$',self.day[k][i],flags=re.I):
     self.tech=self.day[k][i]
     continue
    if re.search(r'^(:|l|L)$',self.day[k][i],flags=re.I):
     if self.day[k][i]==':':
      dayhalf='Afternoon'
     continue
    cnt=self.db.get(self.tech,'content','id',self.day[k][i])[0][0]
    fixheader=re.sub(r'^\n(.*)\n$','\\1',re.sub(r'\n+','\n',''.join([re.sub(r'</?h>','\n',e) for e in re.findall(r'<h>.*?</h>',cnt,flags=re.DOTALL)])),flags=re.DOTALL)
    print("fixheader><%s<>" % fixheader)
    subtopiccount=0
    while cnt:
     #if re.search(r'^[\n\s]*<h>.*',cnt,flags=re.DOTALL):
     if self.searchtag('h',cnt):
      print("<h>")
      code,cnt=self.getcodecnt('h',cnt)
      headerheight=(len(re.findall(r'\n',fixheader))-len(re.findall(r'\n',code)))*HLH+(len(re.findall(r'\n',code))+1)*HBH+42+32 #42+32 is for header day and topic
      print("headerheight %s" % headerheight)
      header=""" %s<div class="slideheader" style="%s">
  <pre class="day">%s</pre>
  <pre class="topic">%s</pre>
  <ul class="slidecontent">
""" % ("<a name=\"chap"+self.day[k][i]+"\">&nbsp;" if subtopiccount==0 else "",'height:'+str(headerheight)+'px' if self.backend!='m' else '','Day '+str(k+1)+' '+dayhalf,'  '+str(self.day[k][i])+'. '+self.db.get(self.tech,'name','id',self.day[k][i])[0][0])
      for line in [line for line in re.split(r'('+re.escape(code)+r'\s*$)',fixheader,flags=re.M) if line]:
       line=re.sub(r'^\n*(.*)\n*$','\\1',line,flags=re.DOTALL)
       for ii in [re.sub(r'^\n*(.*)\n*$','\\1',ii,flags=re.DOTALL) for ii in re.split(r'^[*]',line,flags=re.M) if ii]:
 #       header+="""   <li class="%s"><pre>%s</pre></li>""" % ("big" if line==code else "sml",re.sub(r'\n*(.*)\n*$','\\1',ii,flags=re.DOTALL))
        header+="""   <li class="%s">%s%s%s</li>""" % ("big" if line==code else "sml",("<a name=\"chap"+str(self.day[k][i])+'_'+str(subtopiccount)+"\">") if line==code else '<pre>',re.sub(r'\n','<br>',ii,flags=re.DOTALL) if line==code else ii,"</a>" if line==code else '</pre>')
      header+="""
  </ul>
 </div>%s
""" % ('</a>' if subtopiccount==0 else '')
      subtopiccount+=1
      if (self.hc+headerheight+LH*2)>self.PH:
       self.placepagebreak(k,i);
      if self.backend=='m':
       self.placepagebreak(k,i,'header')
      self.htmlstr+=header
      self.hc+=headerheight
      if not re.search(r'^\s*<a>.*',cnt,flags=re.DOTALL):
       self.htmlstr+='''<div class="clr"></div>
'''
     elif re.search(r'^\s*<a>.*</a>',cnt):
      print("<a>")
      code,cnt=self.getcodecnt('a',cnt)
      self.htmlstr+='<pre class="slideabstract">'+re.sub(r'&lt;(pre.*?|/pre|b|/b|c|/c|cc|/cc)&gt;',r'<\1>',re.sub(r'<',r'&lt;',re.sub(r'>',r'&gt;',re.sub(r'<c>',r'<pre class="codei">',re.sub(r'</cc?>',r'</pre>',re.sub(r'<cc>',r'<pre class="codeci">',re.sub(r'<',r'&lt;',re.sub(r'>',r'&gt;',code))))))))+'</pre>\n<div class="clr"></div>\n'
     elif re.search(r'^.*<i>.*</i>',cnt):
      print("<i>")
      line,cnt=self.getcodecnt('i',cnt)
      #print("<----------line--------%s>>" % line[0:40])
      try:
       with Image.open(urllib2.urlopen(line)) as img:
        if (self.hc+img.height)>self.PH:
         self.placepagebreak(k,i);
        self.hc+=img.height
       self.htmlstr+="""%s<img class="img" src="%s" />%s
""" % ('<div><a href="'+re.sub(r'(.*)_s[.](.*)','\\1.\\2',line)+'">' if re.search(r'_s[.]',line) else '<div>' ,line,'</a></div>' if re.search(r'_s[.]',line) else '</div>')
       #except urllib3.HTTPError:
      except:
       print("HTTPError exception,line:%s" % line)
       self.htmlstr+="""<a href="%s">%s</a>""" % (line,line)
     elif self.searchtag('c',cnt):
      print("<c>")
      self.htmlstr+='<pre class="code">\n'
      code,cnt=self.getcodecnt('c',cnt)
      for line in code.split('\n'):
       if (self.hc+(int(len(re.sub(r'(<pre.*?>|<b>|</b>|</pre>|<cc>|</cc>)','',line))/CODELINEWIDTH)+1)*CH)>self.PH:
        if self.backend!='m':
         self.htmlstr+='</pre>\n'
        self.placepagebreak(k,i) 
        if self.backend!='m':
         self.htmlstr+='<pre class="code">'
       self.hc+=(int(len(re.sub(r'(<pre.*?>|<b>|</b>|</pre>|<cc>|</cc>)','',line))/CODELINEWIDTH)+1)*CH
       self.htmlstr+=re.sub(r'&lt;(pre.*?|/pre|b|/b|cc|/cc)&gt;',r'<\1>',re.sub(r'<',r'&lt;',re.sub(r'>',r'&gt;',re.sub(r'<cc>',r'<pre class="codeci">',re.sub(r'</cc>',r'</pre>',line)))))+'\n'
      self.htmlstr+='</pre>\n' 
     elif self.searchtag('cc',cnt):
      print("<cc>")
      self.htmlstr+='<pre class="codec">\n'
      code,cnt=self.getcodecnt('cc',cnt)
      for line in code.split('\n'):
       if (self.hc+(int(len(re.sub(r'(<pre.*?>|<b>|</b>|</pre>|<c>|</c>)','',line))/CODELINEWIDTH)+1)*CCH)>self.PH:
        if self.backend!='m':
         self.htmlstr+='</pre>\n'
        self.placepagebreak(k,i) 
        if self.backend!='m':
         self.htmlstr+='<pre class="codec">'
       self.hc+=(int(len(re.sub(r'(<pre.*?>|<b>|</b>|</pre>|<c>|</c>)','',line))/CODELINEWIDTH)+1)*CCH
       self.htmlstr+=re.sub(r'&lt;(pre.*?|/pre|b|/b|c|/c)&gt;',r'<\1>',re.sub(r'<',r'&lt;',re.sub(r'>',r'&gt;',re.sub(r'<c>',r'<pre class="codei">',re.sub(r'</c>',r'</pre>',line)))))+'\n'
      self.htmlstr+='</pre>\n' 
     elif self.searchtag('cs',cnt):
      print("<cs>")
      code,cnt=self.getcodecnt('cs',cnt)
      csheight=len(re.split(r'\n',code))+1
      if (self.hc+CNTTHR)>self.PH:
       self.placepagebreak(k,i) 
      colcount=1;tcount=0;thc=self.hc
      self.htmlstr+='<pre class="codes" style="clear:both;float:left;">'
      for line in code.split('\n'):
       tcount=tcount+1
       if self.backend!='m':
        if (self.hc+(int(len(re.sub(r'(<pre.*?>|<b>|</b>|</pre>|<c>|</c>)','',line))/CODELINEWIDTH)+1)*CSH)>self.PH or (tcount>csheight/2 and colcount==1 and csheight>30):
   #      print("line,self.hc,tcount,csheight %s,%s,%s,%s" % (line,hc,tcount,csheight))
         self.htmlstr+='</pre>\n'
         if colcount==1:
          colcount+=1
          self.htmlstr+='<pre class="codes" style="float:left;">'
          self.hc=thc
         # if tcount>csheight/2:
         #  tcount=0
         else: # elif tcount<csheight/2:
          self.placepagebreak(k,i) 
          thc=self.hc
          self.htmlstr+='<pre class="codes" style="clear:both;float:left;">'
          colcount=1
          csheight=csheight-tcount
          tcount=0
        self.hc+=(int(len(re.sub(r'(<pre.*?>|<b>|</b>|</pre>|<c>|</c>)','',line))/CODELINEWIDTH)+1)*CSH
       else:
        if tcount>csheight/2:
         tcount=0
         self.htmlstr+='</pre>\n'
         self.htmlstr+='<pre class="codes" style="float:left;">'
       self.htmlstr+=re.sub(r'&lt;(pre.*?|/pre|b|/b|c|/c)&gt;',r'<\1>',re.sub(r'<',r'&lt;',re.sub(r'>',r'&gt;',re.sub(r'<c>',r'<pre class="codei">',re.sub(r'</c>',r'</pre>',line)))))+'\n'
      self.htmlstr+='</pre><div style="clear:both;"></div>\n' 
     else:
      print("<>")
      self.htmlstr+='<pre class="slidecontent">\n'
      #print("<----------cnt--------%s>>" % cnt[0:40])
      #if re.search(r'[\n\s]*.+(<h>|<a>|<i>|<c>|<cc>|<cs>).*',cnt,flags=re.DOTALL):
      if re.search(r'^.*\n\s*(<h>|<a>.*</a>|<i>.*</i>|<c>|<cc>|<cs>)\s*(\n|$)',cnt,flags=re.DOTALL):
       #code,cnt=re.split(r'<><>',re.sub(r'(.+?\n*)\n\s*((<h>|<a>|<i>|<c>|<cc>|<cs>).*)$','\\1<><>\\2',cnt,flags=re.DOTALL))
       code,cnt=re.split(r'<><>',re.sub(r'^(.*?)\n[ \t]*((<h>|<a>.*</a>|<i>.*</i>|<c>|<cc>|<cs>)\s*\n?.*$)','\\1<><>\\2',cnt,flags=re.DOTALL))
      else:
       code=cnt;cnt=''
      #print("<---------code---------%s>>" % code)
      for line in re.split('\n',re.sub(r'^\s*$','',code,flags=re.DOTALL)):
       if (self.hc+(int(len(re.sub(r'(<pre.*?>|<b>|</b>|</pre>|<c>|</c>|<cc>|</cc>)','',line))/LINEWIDTH)+1)*LH)>self.PH:
        if self.backend!='m':
         self.htmlstr+='</pre>\n'
        self.placepagebreak(k,i) 
        if self.backend!='m':
         self.htmlstr+='<pre class="slidecontent">'
  #     print("(self.hc,line)%s%s" % (line,hc))
       self.hc+=(int(len(re.sub(r'(<pre.*?>|<b>|</b>|</pre>|<c>|</c>|<cc>|</cc>)','',line))/LINEWIDTH)+1)*LH
       self.htmlstr+=re.sub(r'&lt;(pre.*?|/pre|b|/b|c|/c|cc|/cc)&gt;',r'<\1>',re.sub(r'<',r'&lt;',re.sub(r'>',r'&gt;',re.sub(r'<c>',r'<pre class="codei">',re.sub(r'</cc?>',r'</pre>',re.sub(r'<cc>',r'<pre class="codeci">',line))))))+'\n'
      self.htmlstr+='</pre>\n' 
    else:
     self.placepagebreak(k,i)
  self.htmlstr+='</div>\n'
 def searchtag(self,tag,cnt):
  return re.search(r'^.*<'+tag+r'>.*',cnt) and not re.search(r'^.*</'+tag+r'>.*',cnt)
 def getcodecnt(self,tag,cnt):
  return re.split(r'<><>',re.sub(r'^\s*<'+tag+r'>\s*(.*?)\s*</'+tag+r'>.*?\n?(.*)$','\\1<><>\\2',cnt,flags=re.DOTALL))
 def preparepdf(self):
  import pdfkit
  import os
  os.environ['NO_AT_BRIDGE']=str(1)
  print("--writing to %s" % 'advance-'+sys.argv[3]+'-slides.txt')
  self.file.write(self.htmlstr);
  self.file.close()
  print("--writing to %s" % sys.argv[3]+'_pdf.html')
  with open(sys.argv[3]+"_pdf.html",'w') as file:
   file.write(re.sub(r'.*?(<div\s+class="pg".*)',r'<html>\n<head>\n<title>Minh, Inc. Software development and Outsourcing| '+sys.argv[1]+' training Bangalore India</title>\n<META http-equiv="Content-Type" content="text/html; charset=UTF-8">\n<link rel="stylesheet" type="text/css" href="../css/main.css" media="all"/>\n<link rel="stylesheet" type="text/css" href="../css/agenda.css" media="all"/>\n'+r'\1'+'</body>\n</html>',self.htmlstr,flags=re.DOTALL))
  if self.mode=='agenda':
   print("preparing local pdf...\n---please mute @font-face in ../css/main.css---")
   pdfkit.from_file(sys.argv[3]+'_pdf.html','advance-'+sys.argv[3]+'-agenda.pdf')
 def placepagebreak(self,k=0,i=0,header=''):
  if self.backend!='m':
   self.pagenumber=self.pagenumber+1
   self.htmlstr+="""<pre class="ftr">&copy www.minhinc.com</pre><a href="#main%s" class="pn"><img src="http://minhinc.com/image/arrow.png" width="20px" height="20px"/>%s</a>
</div>
<div class="pg" style="margin-top:%spx;height:%spx">
""" % (self.day[k][i],"p"+str(self.pagenumber),self.TM,self.PH)
   self.hc=self.BTMOFST
  elif header=='header':
   self.htmlstr+="""<pre class="ftr">&copy www.minhinc.com</pre><a class="pn" href="#main%s"><img src="http://minhinc.com/image/arrow.png" style="width:20px"/></a>
</div>
<div class="pg" style="margin-top:%spx;">
""" % (self.day[k][i],self.TM)
 def placetopbreak(self,top=False):
  if self.backend[0]=='m':
   if top:
    self.htmlstr+="""<div class="pg" style="margin-top:%spx">
""" % (2*self.TM)
   else:
    self.htmlstr+='''<div class="pg">
'''
  else:
   if top:
    self.htmlstr+="""<div class="pg" style="margin-top:%spx;height:%spx">
""" % (2*self.TM,self.PH-self.TM)
   else:
    self.htmlstr+="""<div class="pg" style="margin-top:%spx;height:%spx">
""" % (self.TM,self.PH)

#   
#  
#prepareheader()
#if not agenda:
# preparedisclaimer()
# preparecontent()
#preparetailer()
#if agenda or pdf:
# preparepdf()

agenda()
