import sys
import re
from PIL import Image
from databasem import databasec
import json
import string
import requestm
from datetime import date
import math
import os
from selenium import webdriver
if len(sys.argv)<6 or not re.search(r'^(m|d).*',sys.argv[1],flags=re.I) or not re.search(r'^(agenda|pdf|php)$',sys.argv[2],flags=re.I):
 print(''' ---usage---
 agenda.py <backend> <mode> <tech> <company> <iddaywise>
 agenda.py mobile php qt '' "1 2 3:4 L" "4 5 6:L"
 agenda.py [desktop|mobile] [agenda|pdf|php] [c|cpp|gl|li|ldd|py|qt|qml] '' "1 2 3:4 L" "4 5 6:L qml" "1 2:3 L"
 <m>-image<c>code<cb>codebackground<cc>shortcode<cs>veryshortcode<a>abstract<n>note<rR>red(Bold)<gG>(greenBold)<lL>blue(Bold)''')
 exit(-1)
class agenda:
 def __init__(self):
  self.backend=sys.argv[1]
  self.mode=sys.argv[2]
  self.tech=sys.argv[3]
  self.company=sys.argv[4]
  if self.backend[0]=='m' and self.mode=='pdf':
   print('pdf cannot be generated in mobile backend, choose desktop,i.e python3 agenda.py desktop pdf qt')
   exit(-1)
  self.day=[]
  for i in range(5,len(sys.argv)):
   if re.search(r':',sys.argv[i]):
    self.day.append(sys.argv[i].split(':')[0].split()+[':']+sys.argv[i].split(':')[1].split())
   else:
    self.day.append(sys.argv[i].split())
  self.TM=20
  self.PH=1415-self.TM
  self.BTMOFST=20
  self.hc=0
  self.PAGEWIDTH=int(re.sub(r'^.*body\s*{\s*width\s*:\s*(\d+).*$',r'\1',open(r'../css/main.css').read(),flags=re.I|re.DOTALL))
  self.htmlstr=''
  self.file=open('advance-'+self.tech+'-slidesFULL_m.txt','w')  if self.backend[0]=='m' else open('advance-'+self.tech+'-slidesFULL.txt','w')
  self.db=databasec(False)
  self.driver=None
  self.pagenumber=0
  self.responsivesquare=None
  self.prepareagenda()
  if self.mode!='agenda':
   self.preparedisclaimer()
   self.preparecontent()
  self.preparepdf()
  self.file.close()
  self.driver.close()

 def prepareagenda(self):
  LH=22;HH=40;OFST=25#headerheight
  CHH=40;HHH=50;CHG=125;HCG=40;CCG=80#contentheaderheight,contentheadergap,headercontentgap,contentcontentgap
  tech=self.tech
  numofline=0
  top='';left=True;
  l='';header=''
  height=0
  agendadaydata=[]
  subtopiccount=0
  headerlist=None
  self.placetopbreak(True)
  self.htmlstr+=""" <pre class=title>%s</pre>
 <pre class=subtitle>%s</pre>
 <pre class=company>%s</pre>
""" % (self.db.get(self.tech,'value','name','title')[0][0],self.db.get(self.tech,'value','name','subtitle')[0][0],'('+self.company+')' if self.company else '')
#adsensee
  self.htmlstr+="<div style=\"width:100%;height:100px;\">"+self.adsensepaste(self.PAGEWIDTH,100)+"</div>"
  for data in self.db.get(self.tech,'*','name','[[:<:]]h_',orderby='id',regex=True):
   numofline=numofline+max(len(re.findall(r'\n',str(data[1])))+1,len(re.findall(r'\n',str(data[2])))+1)
  for data in self.db.get(self.tech,'*','name','[[:<:]]h_',orderby='id',regex=True):
   if not re.search(r'h_hr',data[1]):
    self.htmlstr+=""" <div style="height:%spx;">
  <div class="headerleft"> <pre>%s</pre>
  </div>
  <div class="headerright"> <pre>%s</pre>
  </div>
 </div>
""" % (max(len(re.findall(r'\n',data[1]))+1,len(re.findall(r'\n',data[2]))+1)*LH+int((50*OFST)/numofline),re.sub(r'^h_','',data[1]),data[2])
   else:
    self.htmlstr+=''' <hr>
'''
  self.placepagebreak(header='noarrow')
  self.hc=0
  for data in self.db.get(self.tech,'*','name','[[:<:]]h2_',orderby='id',regex=True):
   self.htmlstr+=""" <div class="header2" style="margin-top:%spx;">
  <pre class="header" style="line-height:%spx">%s</pre>
  <pre class="content" style="height:%spx">%s</pre>
 </div>
""" % (0 if not self.hc and self.backend[0]!='m' else OFST*5,HH,re.sub(r'^h2_','',data[1]),len(re.findall(r'\n',data[2]))*LH+OFST,data[2])
   self.hc=HH+(len(re.findall(r'\n',data[2]))+1)*LH+OFST if not self.hc else self.hc+5*OFST+HH+(len(re.findall(r'\n',data[2]))+1)*LH+OFST
  
  tmpstr='';tmphc=0;dayheight=0
  tech=self.tech
  techchange=False
  for k in range(0,len(self.day)):
   for i in range(0,len(self.day[k])):
    if re.search(r'^\d+[Ll]$',self.day[k][i],flags=re.I):
     l=self.db.get(tech,'lab','id',self.day[k][i][:-1])[0][0] if l=='' else l+('\n'+self.db.get(tech,'lab','id',self.day[k][i][:-1])[0][0] if self.db.get(tech,'lab','id',self.day[k][i][:-1])[0][0] else '')
#    elif not re.search(r'^(\d+|[Ll]|:)',self.day[k][i],flags=re.I):
#     tech=self.day[k][i]
    elif re.search(r'^\d+[Tt]?$',self.day[k][i],flags=re.I) or re.search(r'^[Ll]$',self.day[k][i],flags=re.I) or self.day[k][i]==':' or not re.search(r'^(\d+|[Ll]|:)',self.day[k][i],flags=re.I):
     if i==0 or self.day[k][i]==':':
      tmpstr+=""" <div class="dayheader" style="margin-top:%spx;height:%spx"><pre>Day %s %s</pre><hr></div>
 """ % (str(CHG)+'YYY',str(HHH),k+1,"Afternoon" if self.day[k][i]==':' else "Morning")
      tmphc+=HHH+CHG
      if self.day[k][i]==':':
       continue
     if not re.search(r'^(\d+|[Ll]|:)',self.day[k][i],flags=re.I):
       tech=self.day[k][i]
       techchange=True
       continue;
     if re.search(r'^[Ll]$',self.day[k][i]):
      data=l;l=""
     else:
      if self.day[k][i].isdecimal():
       l=self.db.get(tech,'lab','id',self.day[k][i])[0][0] if l=='' else l+('\n'+self.db.get(tech,'lab','id',self.day[k][i])[0][0] if self.db.get(tech,'lab','id',self.day[k][i])[0][0] else '')
      self.day[k][i]=re.sub(r'^(\d+)[Tt]$',r'\1',self.day[k][i],flags=re.I)
#      data=self.db.get(tech,'value','id',self.day[k][i])[0][0]
      data=re.sub(r'^\n(.*)\n$','\\1',re.sub(r'\n+','\n',''.join([re.sub(r'</?h>','\n',e) for e in re.findall(r'<h>.*?</h>',self.db.get(tech,'content','id',self.day[k][i])[0][0],flags=re.DOTALL)])),flags=re.DOTALL)
     tmpstr+=""" <div class=%s style="margin-top:%spx;%s">
  <div class="%s" style="height:%spx">%s class="%s" style="padding-top:%spx;%spx">%s%s  </div>
  <ul class="daycontent" style="padding-top:10px;">
""" % ('"dayheaderright"' if re.search(r'dayheaderleft',tmpstr,flags=re.I) else '"dayheaderleft"',HCG if re.search(r'YYY',tmpstr,flags=re.I) else str(CCG)+'XXX','height:'+str((len(re.findall(r'\n',data))+1)*LH+CHH)+'px;' if self.backend[0]!='m' else '','dayheaderheaderlab' if re.search(r'[Ll]',self.day[k][i]) else 'dayheaderheadertechchange' if techchange else 'dayheaderheader',CHH,'<pre' if self.mode=='agenda' or re.search(r'^[Ll]$',self.day[k][i]) else "<a name=\"main"+self.day[k][i]+"\" href=\"#chap"+str(self.day[k][i])+"\"",'dayheader',CHH/4 if not re.search(r'^[Ll]$',self.day[k][i]) else 0,'height:'+str(CHH) if not re.search(r'^[Ll]$',self.day[k][i]) else 'line-height:'+str(CHH),'     Lab' if re.search(r'[Ll]',self.day[k][i]) else '  Lecture - '+self.db.get(tech,'name','id',self.day[k][i])[0][0]+('    ( '+tech+' )' if techchange else ''),'</pre>' if self.mode=='agenda' or re.search(r'^[Ll]$',self.day[k][i]) else '</a>')
     subtopiccount=0
     techchange=False
     for headerindex in (re.findall(r'\s*([*].*?)\s*(?=[*]|$)',data,flags=re.I|re.DOTALL) if re.search(r'^[Ll]$',self.day[k][i]) else re.findall(r'<h>\s*(.*?)\s*</h>',self.db.get(tech,'content','id',self.day[k][i])[0][0],flags=re.I|re.DOTALL)):
      for le in [re.sub(r'^\n*(.*?)\n*$',r'\1',e,flags=re.DOTALL) for e in re.split(r'[*]',headerindex) if e]:
       tmpstr+="""   <li>%s%s%s</li>
 """ % ('<pre>' if self.mode=='agenda' or re.search(r'^[Ll]$',self.day[k][i]) else "<a href=\"#chap"+str(self.day[k][i])+'_'+str(subtopiccount)+"\">" if self.mode!='php' and not re.search(r'^[Ll]$',self.day[k][i]) else '<a href=\"#chap'+self.day[k][i]+'_'+str(subtopiccount)+'\">'+'<pre>',re.sub(r'\n','<br>',le,flags=re.DOTALL) if self.mode!='php' and not re.search(r'^[Ll]$',self.day[k][i]) else le,'</pre>' if self.mode=='agenda' or re.search(r'^[Ll]$',self.day[k][i]) else "</a>" if self.mode=='pdf' and not re.search(r'^[Ll]$',self.day[k][i]) else '</pre></a>')
      subtopiccount+=1
     tmpstr+='''  </ul>
 </div>
'''
     dayheight=max(dayheight,self.lineheightnhtml(re.sub(r'^.*(<div\s*class="dayheader(?:left|right)")\s*style=".*?"(.*)$',r'\1\2',tmpstr,flags=re.I|re.DOTALL),re.sub(r'^.*(<div\s*class="dayheader(?:left|right)").*$',r'\1>',tmpstr,flags=re.I|re.DOTALL),addtag=False,skipconversion=True)[0]['height'] + (HCG if re.search(r'YYY',tmpstr,flags=re.I) else CCG))
     tmpstr=re.sub(r'^(?P<id>.*<div\s*class="dayheader(?:left|right)".*?height:)\d+(?P<id1>.*)$',lambda m:m.group('id')+str(self.lineheightnhtml(re.sub(r'^.*(<div\s*class="dayheader(?:left|right)")\s*style=".*?"(.*)$',r'\1\2',tmpstr,flags=re.I|re.DOTALL),re.sub(r'^.*(<div\s*class="dayheader(?:left|right)").*$',r'\1>',tmpstr,flags=re.I|re.DOTALL),addtag=False,skipconversion=True)[0]['height'])+m.group('id1'),tmpstr,flags=re.I|re.DOTALL) if self.backend[0]!='m' else tmpstr
     if re.search(r'dayheaderright',tmpstr,re.I) or i==(len(self.day[k])-1) or self.day[k][i+1]==':' or not re.search(r'^(\d+|[Ll]|:)',self.day[k][i+1],flags=re.I):
      tmphc+=dayheight
      dayheight=0
     if ((self.hc+tmphc)>self.PH and dayheight==0) or (k==len(self.day)-1 and i==len(self.day[k])-1):
      if (self.hc+tmphc)>self.PH:
       if self.backend[0] != 'm': self.pagenumber+=1
       self.htmlstr+=""" %s
</div>
%s
""" % ('<pre class="ftr">&copy www.MinhInc.com</pre><a class="pn">p'+str(self.pagenumber)+'</a>' if self.backend[0]!='m' else '','<div class="pg" style="margin-top:'+str(self.TM)+'px;'+('height:'+str(self.PH)+'px' if self.backend[0]!='m' else '')+'">'+'\n'+re.sub(r'\d+(YYY|XXX)',r'0' if self.backend[0]!='m' else str(self.TM*4),tmpstr,flags=re.I))
       if re.search(r'YYY',tmpstr,flags=re.I): 
        tmphc-=CHG
       elif re.search(r'XXX',tmpstr,flags=re.I): 
        tmphc-=CCG
       if k==len(self.day)-1 and i==len(self.day[k])-1:
        self.htmlstr+='\n</div>'
       print("self.hc {}, self.PH {}".format(self.hc,self.PH))
       self.hc=self.hc+(self.PH-self.hc)*0.40
      else: 
       if self.backend[0] != 'm': self.pagenumber+=1
       self.htmlstr+=tmpstr+""" %s
</div>
""" % ('<pre class="ftr">&copy www.MinhInc.com</pre><a class="pn">p'+str(self.pagenumber)+'</a>' if self.backend[0]!='m' else '')
       self.hc+=tmphc
       self.hc=self.hc+(self.PH-self.hc)*0.85
      headermorningcount=len(re.findall(r'YYY.*?Morning',self.htmlstr,flags=re.I))
      headerafternooncount=len(re.findall(r'YYY.*?Afternoon',self.htmlstr,flags=re.I))
      daycount=len(re.findall(r'dayheaderleft.*?XXX',self.htmlstr,flags=re.I))
      if headermorningcount+headerafternooncount+daycount:
       self.htmlstr=re.sub(r'(?P<id>\d+)YYY(?P<id1>.*?Morning)',lambda m: str(int(m.group('id'))+int(6*(self.PH-self.hc)/(6*headermorningcount+2*headerafternooncount+daycount)))+m.group('id1'),self.htmlstr,flags=re.I)
       self.htmlstr=re.sub(r'(?P<id>\d+)YYY(?P<id1>.*?Afternoon)',lambda m: str(int(m.group('id'))+int(2*(self.PH-self.hc)/(6*headermorningcount+2*headerafternooncount+daycount)))+m.group('id1'),self.htmlstr,flags=re.I)
       self.htmlstr=re.sub(r'(?P<id>\d+)XXX',lambda m: str(int(m.group('id'))+int((self.PH-self.hc)/(6*headermorningcount+2*headerafternooncount+daycount))),self.htmlstr,flags=re.I)
      self.hc=tmphc
      tmpstr='';tmphc=0
     elif dayheight==0:
      self.htmlstr+=tmpstr if self.backend[0]!='m' else re.sub(r'\d+(YYY|XXX)',str(self.TM*4),tmpstr,flags=re.I)
      self.hc+=tmphc
      tmpstr='';tmphc=0
    
  self.htmlstr+='''
<div style="clear:both;"></div>
''' 

  self.hc=0

 def preparedisclaimer(self):
  self.placetopbreak()
  self.htmlstr+="""<pre class="slidetitle">%s</pre><pre class="slidesubtitle">%s</pre><pre class="slidecompanytitle">%s</pre><pre class="slidedisclaimer">%s</pre>
</div>
""" % (re.sub(r'(.*) Training',r'\1',json.loads(self.db.get('headername','content','name',self.tech)[0][0])['title'])+' Essentials',re.sub(r'(.*) Training',r'\1',json.loads(self.db.get('headername','content','name',self.tech)[0][0])['title'])+' Essenstials- Training Course','Minh, Inc.',"""DISCLAIMER

Text of this document is written in Bembo Std Otf(13 pt) font.

Code parts are written in Consolas (10 pts) font.

This training material is provided through <a style="font-family:mytwcenmt,Tw Cen MT;font-size:10pt;color:#004000;font-weight:bold" href="http://www.minhinc.com">Minh, Inc.</a>, B'lore, India
Pdf version of this document is available at <a href="http://www.minhinc.com/training/advance-%s-slides.pdf">http://www.minhinc.com/training/advance-%s-slides.pdf</a>
For suggestion(s) or complaint(s) write to us at <a href="mailto:sales@minhinc.com">sales@minhinc.com</a>

Document modified on %s 

Document contains XXPAGEXX pages.""" % (self.tech,self.tech,date.today().strftime("%b-%d-%Y")) if self.backend[0]!='m' else '')
#  self.pagenumber+=1

 def preparecontent(self):
  LH=20
  cnt=fixheader=header=code=dayhalf=""
  cscount=linecount=subtopiccount=0
  XOFFSET=10
  self.placetopbreak()
  self.hc=self.BTMOFST
  youtubesize=(480,210 if self.backend[0]=='m' else 270)
  tmpvar1=tmpvar2=tmpcode=None
  htmltag=''
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
     if self.searchtag('h',cnt):
      print("<h>",self.hc)
      code,cnt=self.getcodecnt('h',cnt)
      header="""%s<div class="slideheader">
  <pre class="day">%s</pre>
  %s<pre class="topic">%s</pre>%s
   <ul class="slidecontent">
""" % ("<a name=\"chap"+self.day[k][i]+"\">&nbsp;" if subtopiccount==0 else "",'Day '+str(k+1)+' '+dayhalf,"<h1>" if subtopiccount==0 else '','  '+str(self.day[k][i])+'. '+self.db.get(self.tech,'name','id',self.day[k][i])[0][0],"</h1>" if subtopiccount==0 else '')
      for line in [line for line in re.split(r'('+re.escape(code)+r'\s*$)',fixheader,flags=re.M) if line]:
       line=re.sub(r'^\n*(.*)\n*$','\\1',line,flags=re.DOTALL)
       for ii in [re.sub(r'^\n*(.*)\n*$','\\1',ii,flags=re.DOTALL) for ii in re.split(r'^[*]',line,flags=re.M) if ii]:
        header+="""   <li class="%s">%s%s%s</li>""" % ("big" if line==code else "sml",'<h2>'+("<a name=\"chap"+str(self.day[k][i])+'_'+str(subtopiccount)+"\">") if line==code else '<pre>',"<br>".join([re.sub(r'^[ ]?([ ]*)(.*)',re.sub(r'[ ]',r'&nbsp;',re.sub(r'^[ ]?([ ]*).*',r'\1',iii))+r'\2',iii) for iii in re.split(r'\n',ii)]) if line==code else ii,"</a>"+'</h2>' if line==code else '</pre>')
      header+="""
   </ul>
</div>%s
""" % ('</a>' if subtopiccount==0 else '')
      subtopiccount+=1
      tmpcode=self.lineheightnhtml(header,r'<div class="slideheader">',addtag=False,skipconversion=True)
      if (self.hc+tmpcode[0]['height']+LH)>self.PH:
       self.placepagebreak(k,i);
      if self.backend[0]=='m':
       self.placepagebreak(k,i,'header')
      header=re.sub(r'^(.*?class="slideheader")(.*)$',r'\1{}\2'.format(' style="height:'+str(tmpcode[0]['height'])+'px;width:'+str(tmpcode[0]['width'])+'px;"' if self.backend[0]!='m' else ''),header,flags=re.I|re.DOTALL)
      self.htmlstr+=header
      self.hc+=tmpcode[0]['height']
      if not re.search(r'^\s*<a>.*',cnt,flags=re.DOTALL):
       self.htmlstr+='''<div class="clr"></div>
'''
     elif re.search(r'^\s*<a>.*?</a>',cnt,flags=re.I|re.DOTALL):
      print("<a>")
      code,cnt=self.getcodecnt('a',cnt)
      self.htmlstr+='<pre class="slideabstract">'+self.lineheightnhtml(code,'<pre class="slideabstract">')[1]+'</pre>\n<div class="clr"></div>\n'
     elif re.search(r'^.*<m>.*</m>',cnt):
      print("<m>",self.hc)
      line,cnt=self.getcodecnt('m',cnt)
      try:
       if re.search(r'youtube',line,flags=re.I):
        print('youtube,hc,line',self.hc,line)
        tmpvar1=requestm.youtubeimage(re.sub(r'^.*embed/(.*)$',r'\1',line,flags=re.I)) if self.mode!='php' else None
        if (self.hc+(youtubesize[1]+30 if self.mode=='php' else tmpvar1[1][1]))>self.PH:
         self.placepagebreak(k,i);
        tmpvar2=self.adsensepaste(self.PAGEWIDTH-youtubesize[0]-XOFFSET,youtubesize[1]+30,stylecode=('float:right;' if self.backend[0]!='m' and self.mode=='php' else ''))
        self.htmlstr+="<div style=\""+("float:left;" if re.search('float:right',tmpvar2,flags=re.DOTALL) and self.backend[0]!='m' and self.mode=='php' else "")+"background-color:#888888;"+("width:"+str(youtubesize[0])+'px;height:'+str(youtubesize[1]+30)+'px;' if self.backend[0]!='m' else '')+"\"><pre style=\"text-align:center;color:#ffffff;font-weight:bold;font-family:mybembo;font-size:16pt\">YouTube Video</pre><iframe style=\"margin-bottom:2px;width:"+(str(youtubesize[0])+'px;' if self.backend[0]!='m' else '100%')+";height:"+str(youtubesize[1])+"px;\" src=\""+line+"?enablejsapi=1&controls=1&autoplay=1&vq=hd240\" frameborder=\"0\"></iframe></div>"+tmpvar2+"\n" if self.mode=='php' else r'<div style="position:relative;width:'+str(tmpvar1[1][0])+r';height:'+str(tmpvar1[1][1])+r';"><a style="position:absolute;margin-left:25%;" '+r'href="https://www.youtube.com/watch?v='+re.sub(r'^.*embed/(.*)$',r'\1',line,flags=re.I)+'"><img src="'+tmpvar1[0]+'"/></a></div>'
        self.hc+=(youtubesize[1]+30 if self.mode=='php' else tmpvar1[1][1])
       else:
        with Image.open(requestm.gets(line,get=True,stream=True)) as img:
         if (self.hc+img.height)>self.PH:
          self.placepagebreak(k,i);
         print("hc img",self.hc,img.width,img.height)
         tmpvar2=self.adsensepaste(self.PAGEWIDTH-img.width-XOFFSET,img.height,stylecode=('float:right;' if self.backend[0]!='m' and self.mode=='php' else ''))
#         self.htmlstr+="<div"+(' style="height:'+str(img.height)+'px;' if self.backend[0]!='m' else '')+("float:left;" if self.backend[0]!='m' and self.mode=='php' else "")+"\">"+("<a href=\""+re.sub(r'(.*)_s[.](.*)','\\1.\\2',line)+"\">" if re.search(r'_s[.]',line) else '')+"<img class=\"img\" src=\""+line+"\" />"+("</a></div>" if re.search(r'_s[.]',line) else '</div>')+tmpvar2
         self.htmlstr+="<div"+(' style="float:left;"' if self.backend[0]!='m' and self.mode=='php' else "")+">"+("<a href=\""+re.sub(r'(.*)_s[.](.*)','\\1.\\2',line)+"\">" if re.search(r'_s[.]',line) else '')+"<img class=\"img\" src=\""+line+"\" />"+("</a></div>" if re.search(r'_s[.]',line) else '</div>')+tmpvar2
         self.hc+=img.height
      except Exception as e:
       print("HTTPError exception,hc,line:{}".format(self.hc,line,e.__class__.__name__))
       tmpvar1=self.lineheightnhtml(line,'<pre class="code">')
       self.htmlstr+="""<a href="%s">%s</a>""" % (line,line)
       if (self.hc+tmpvar1[0]['height'])>self.PH:
        self.placepagebreak(k,i)
       self.hc+=tmpvar1[0]['height']
     elif self.searchtag('cs',cnt):
      print("<cs>")
      tmpvar2=0
      code,cnt=self.getcodecnt('cs',cnt)
      tmpcode=self.lineheightnhtml(code,'<pre class="codes">')
      tmpcode=self.pagedivider(tmpcode[1],'<pre class="codes">',tmpcode[0]['height']/2 if tmpcode[0]['height']/2+self.hc < self.PH else None,skipconversion=True)
      while tmpcode[1][0] or tmpcode[1][1]:
       if tmpcode[1][0]:
        self.htmlstr+=r' <pre class="codes" style="float:left;'+('height:'+str(tmpcode[0]['height'])+'px;' if self.backend[0]!='m' else '')+'">'+tmpcode[1][0]+' </pre>\n'+('<div class="clr"></div>' if tmpvar2 and (self.backend[0]=='m' or self.mode!='php') else '')+(self.adsensepaste(self.PAGEWIDTH-tmpvar1['width']-tmpcode[0]['width']-XOFFSET,max(tmpvar1['height'],tmpcode[0]['height']),stylecode=('float:right;' if self.backend[0]!='m' else '')) if tmpvar2 else "")
        if tmpvar2:
         self.hc+=tmpcode[0]['height']
        else:
         tmpvar1=tmpcode[0]
       if tmpcode[1][1]:
        if tmpvar2:
         self.placepagebreak(k,i)
         tmpcode=self.lineheightnhtml(tmpcode[1][1],'<pre class="codes">',skipconversion=True)
         tmpcode=self.pagedivider(tmpcode[1],'<pre class="codes">',tmpcode[0]['height']/2 if tmpcode[0]['height']/2+self.hc < self.PH else None,skipconversion=True)
        else:
         tmpcode=self.pagedivider(tmpcode[1][1],'<pre class="codes">',skipconversion=True)
       else:
        break
       tmpvar2=(tmpvar2+1)%2
     else:
      if self.searchtag('cb?',cnt) or self.searchtag('cc',cnt):
       print("<cb|c|cc>",self.hc)
       htmltag='<pre class="code">' if self.searchtag('c',cnt) else '<pre class="codeb">' if self.searchtag(r'cb',cnt) else '<pre class="codec">'
       code,cnt=self.getcodecnt('c',cnt) if self.searchtag('c',cnt) else self.getcodecnt('cb',cnt) if self.searchtag(r'cb',cnt) else self.getcodecnt('cc',cnt)
      else:
       print("<>")
       if re.search(r'(\s*<h>[ \t]*\n.*\n?[ \t]*</h>|\s*<a>.*?</a>|\s*<cb?>[ \t]*\n.*\n?[ \t]*</cb?>|\s*<cc>[ \t]*\n.*\n?[ \t]*</cc?>|\s*<cs>[ \t]*\n.*\n?[ \t]*</cs>|\s*<m>.*?</m>)',cnt,flags=re.DOTALL):
        code,cnt=re.split(r'<><>',re.sub(r'^(.*?)\n?((?:[ \t]*<h>[ \t]*\n.*\n?[ \t]*</h>|[ \t]*<a>.*?[ \t]*</a>|[ \t]*<cb?>[ \t]*\n.*\n?[ \t]*</cb?>|<cc>[ \t]*\n.*\n?[ \t]*</cc?>|[ \t]*<cs>[ \t]*\n.*\n?[ \t]*</cs>|[ \t]*<m>.*?</m>).*)$',r'\1<><>\2',cnt,flags=re.DOTALL))
       else:
        code=cnt;cnt=''
       htmltag='<pre class="slidecontent">'
      tmpcode=self.pagedivider(code,htmltag)
      while tmpcode[1][0] or tmpcode[1][1]:
       if tmpcode[1][0]:
        tmpvar1=self.adsensepaste(self.PAGEWIDTH-tmpcode[0]['width']-XOFFSET,tmpcode[0]['height'],stylecode=('float:right;' if self.backend[0]!='m' else '')) if self.mode=='php' else ''
        self.htmlstr+=' '+re.sub(r'(class=)',r'{} \1'.format(('style="height:'+str(tmpcode[0]['height'])+'px;' if self.backend[0]!='m' else '')+('float:left;"' if re.search('float:right',tmpvar1,flags=re.DOTALL) and self.backend[0]!='m' and self.mode=='php' else '"')),htmltag,flags=re.I)+tmpcode[1][0]+' </pre>\n'+tmpvar1
        self.hc+=tmpcode[0]['height']
       else:
        self.placepagebreak(k,i)
       if not tmpcode[1][1]:
        break
       tmpcode=self.pagedivider(tmpcode[1][1],htmltag,skipconversion=True)
    else:
     self.placepagebreak(k,i)
  if self.backend[0]=='m': self.placepagebreak(k,[j for j in range(i,-1,-1) if re.search(r'^\d+$',self.day[k][j])][0],header)
  self.htmlstr+='''<a href="http://www.minhinc.com" target="_blank" class="logo"><pre><span>&copy</span>www.minhinc.com</pre></a>
</div>\n'''

 def searchtag(self,tag,cnt):
  return re.search(r'^[ \t]*<'+tag+r'>[ \t]*\n',cnt,flags=re.I|re.DOTALL)

 def getcodecnt(self,tag,cnt):
  return re.split(r'<><>',re.sub(r'^[ \t]*<'+tag+r'>[ \t]*\n?(.*?)\n?[ \t]*</'+tag+r'>[ \t]*\n?(.*)$','\\1<><>\\2',cnt,flags=re.DOTALL))

 def lineheightnhtml(self,line,htmlcode,addtag=True,skipconversion=False):
  '''calculate line height and html string for line
   line - multiline for which height and html needs to be calculated
   htmlcode - tag added to test.html fed to selenium webdriver. i.e. '<div class="code">'''
  filedata=r''
  htmltag=re.sub(r'^\s*<\s*(\w+).*$',r'\1',htmlcode,flags=re.I)
  htmlselector=re.sub(r'^\s*<\s*(\w+).*?class\s*=\s*"?(\w+).*$',r'\1.\2',htmlcode,flags=re.I)
  line='\n'.join([x if x else ' ' for x in line.split('\n')]) if not skipconversion else line
#  print("><hc,line,htmlcode,addtag,skipconversion,htmltag,htmlselector:{}:{}:{}:{}:{}:{}:{}".format(self.hc,line,htmlcode,addtag,skipconversion,htmltag,htmlselector))
  if not self.driver:
#   self.driver=webdriver.Firefox()
   self.driver=webdriver.Chrome()
   self.driver.minimize_window()
   open(r'./test.html','w').write(filedata)
   self.driver.get(r'file:///'+re.sub(r'/?$','',os.getcwd())+r'/test.html')
  line=re.sub(r'&lt;(pre.*?|/pre|i|/i|b|/b|c|/c|span.*?|/span|cc|/cc)&gt;',r'<\1>',re.sub(r'<',r'&lt;',re.sub(r'>',r'&gt;',re.sub(r'<r>',r'<span style="color:#ff0000;">',re.sub(r'<g>',r'<span style="color:#004000;">',re.sub(r'<l>',r'<span style="color:#0055cf;">',re.sub(r'<R>',r'<span style="color:#ff0000;font-weight:bold">',re.sub(r'<G>',r'<span style="color:#004000;font-weight:bold">',re.sub(r'<L>',r'<span style="color:#0055cf;font-weight:bold">',re.sub(r'</[rglRGL]>',r'</span>',re.sub(r'<n>',r'<pre class="note">',re.sub(r'</n>',r'</pre>',re.sub(r'<c>',r'<pre class="codei">',re.sub(r'</cc?>',r'</pre>',re.sub(r'<cc>',r'<pre class="codeci">',line,flags=re.I|re.DOTALL))))))))))))))) if not skipconversion else line
  with open(r'./test.html','w') as file:
   file.write('<html>\n<head>\n<link rel="stylesheet" type="text/css" href="../css/main.css" media="all"/>\n<link rel="stylesheet" type="text/css" href="../css/agenda.css" media="all"/>\n</head>\n<body>\n<div class="pg">\n'+(htmlcode if addtag else '')+line+('</'+htmltag+'>\n' if addtag else '')+'</div>\n</body>\n</html>')
  self.driver.refresh()
  return (self.driver.find_element_by_css_selector(htmlselector).size,line)
 
 def pagedivider(self,code,htmlselector,height=None,skipconversion=False):
  '''partition code to before page end and after page end
   code - code to analysed
   htmlselector - ie. '<pre class="slidecontent">'
   height - to be calcaluted for height i.e '<pre class="codes">'
   skipconversion - to be passed to lineheightnhtml
   returns ((codeheight,codewidth),(prepagecode,postpagecode))'''
  
  tmpcode=tmpvar1=tmpvar2=None
  tmpcode=self.lineheightnhtml(code,htmlselector,skipconversion=skipconversion)
  height=min(self.PH-self.hc,tmpcode[0]['height'],(max(self.PH-self.hc,tmpcode[0]['height']) if not height else height))
  if height == tmpcode[0]['height']:
   return (tmpcode[0],(tmpcode[1],None))
  tmpvar1=tmpcode[1].split('\n')
  tmpvar2=int(((len(tmpvar1)-1)*height)/tmpcode[0]['height'])
  tmpcode=self.lineheightnhtml('\n'.join(tmpvar1[:(tmpvar2+1)]),htmlselector,skipconversion=True)
  while tmpvar2<len(tmpvar1) and tmpcode[0]['height']<height:
   tmpvar2+=1
   tmpcode=self.lineheightnhtml('\n'.join(tmpvar1[:(tmpvar2+1)]),htmlselector,skipconversion=True)
  while tmpvar2 and tmpcode[0]['height']>height:
   tmpvar2=tmpvar2-1
   tmpcode=self.lineheightnhtml('\n'.join(tmpvar1[:(tmpvar2+1)]),htmlselector,skipconversion=True)
  if not tmpvar2:
   return (tmpcode[0],(None,'\n'.join(tmpvar1)))
  return (tmpcode[0],('\n'.join(tmpvar1[:tmpvar2+1]),'\n'.join(tmpvar1[tmpvar2+1:])))

 def preparepdf(self):
  import pdfkit
  os.environ['NO_AT_BRIDGE']=str(1)
  print("--writing to %s" % 'advance-'+sys.argv[3]+'-slidesFULL'+('_m' if self.backend[0]=='m' else '')+'.txt')
  self.htmlstr=re.sub('XXPAGEXX',str(self.pagenumber),self.htmlstr);
  self.file.write(self.htmlstr);

  if self.mode == 'php':
   matchobj=re.match(r'(.*)(<div class="pg".*)$',re.sub(r'^(.*)\n<div class="pg".*$',r'\1',re.sub(r'^(.*?)name="chap\d+.*$',r'\1',self.htmlstr,flags=re.I|re.DOTALL),flags=re.DOTALL),flags=re.I|re.DOTALL)
   header,preface=matchobj.group(1),matchobj.group(2)

#add adsense header
   def settle(m):
    stt=self.adsensepaste(self.PAGEWIDTH,int(m.group('id1')),stylecode='clear:both;')
    return ('' if re.search(r'<div\s*class\s*=\s*"dayheaderright"',m.group('id'),flags=re.I) else stt)+m.group('id')+(str(0) if stt else m.group('id1'))
   header=re.sub(r'(?P<id><div\s*class="dayheader(?:left|right)?"\s*style=".*?margin-top:)(?P<id1>\d+)',lambda m:settle(m),header,flags=re.I|re.DOTALL) if self.mode == 'php' else header
   headerlist=list(re.findall(r'<div class\s*=\s*"dayheader(?:left|right).*?</ul>.*?</div>',header,flags=re.I|re.DOTALL))
   for i in range(len(headerlist)):
    if re.search(r'dayheaderleft',headerlist[i],flags=re.I|re.DOTALL) and ((i+1<len(headerlist)-1 and re.search(r'dayheaderleft',headerlist[i+1],flags=re.I|re.DOTALL)) or i==len(headerlist)-1):
     header=re.sub(r'^(.*)('+re.escape(headerlist[i])+r')(.*)$',r'\1\2{}\3'.format(self.adsensepaste(int(self.PAGEWIDTH*0.495),self.lineheightnhtml(headerlist[i],'<div class="dayheaderleft">',addtag=False,skipconversion=True)[0]['height'],stylecode=re.sub(r'^.*?(margin-top\s*:\s*\d+).*$',r'\1px;{}'.format('float:right;' if self.backend[0]!='m' else ''),headerlist[i],flags=re.I|re.DOTALL)) if self.backend[0]!='m' and self.mode=='php' else ''),header,flags=re.I|re.DOTALL)

   cnt=re.split(re.escape(preface),self.htmlstr,flags=re.I|re.DOTALL)[1]
   content=re.findall(r'(name="chap\d+".*?)(?=name="chap\d+"|$)',cnt,flags=re.I|re.DOTALL)
   header=re.sub(r'href="#(chap)(\d+)(_\d+)?"',r'href="./advance-'+sys.argv[3]+r'-slides.php?\1=\2#\1\2\3"',header,flags=re.I|re.DOTALL)
   idbase=re.sub(r'^.*?name\s*=\s*"main(\d+)".*$',r'\1',header,flags=re.I|re.DOTALL)
   for count,i in enumerate(re.findall(r'name\s*=\s*"main(\d+)"',header,flags=re.I|re.DOTALL)):
    with open('advance-'+sys.argv[3]+r'-slides'+('-chap'+str(i) if i!=idbase else '')+('_m' if self.backend[0]=='m' else '')+'.txt','w') as file:
     print('writing to file',file.name)
     file.write(re.sub(r'(href="./advance-'+sys.argv[3]+r'-slides.php)\?chap='+str(idbase)+r'#',r'\1#',re.sub(r'href="./advance-'+sys.argv[3]+r'-slides.php\?chap='+str(i)+r'(#chap'+str(i)+r'(?:_\d+)?)"',r'href="\1"',re.sub(r'^(.*(?<=style="))(.*?)(name="main'+str(i)+r'".*)$',r'\1background-color:#f38502;\2\3',header,flags=re.I|re.DOTALL),flags=re.I|re.DOTALL),flags=re.I|re.DOTALL)+preface+re.sub(r'^(.*</div>).*$',r'<div class="pg" style="margin-top:'+str(self.TM)+'px;{}'.format('height:'+str(self.PH)+'px;' if self.backend[0]!='m' else '')+r'">\n<a \1',content[count],flags=re.I|re.DOTALL))

  if self.mode != 'php':
   print("--writing to %s" % sys.argv[3]+'_pdf.html')
   with open(sys.argv[3]+"_pdf.html",'w') as file:
    open('tmp.css','w').write('div.pg pre.slidecontent, div.pg pre.code,div.pg codeb,  div.pg pre.codec {display:block;}\ndiv.pg pre.slidetitle{margin-top:20%},div.pg pre.slidedisclaimer {margin-top:20%;}')
    file.write(re.sub(r'.*?(<div\s+class="pg".*)',r'<html>\n<head>\n<title>Minh, Inc. Software development and Outsourcing| '+sys.argv[3]+' training Bangalore India</title>\n<META http-equiv="Content-Type" content="text/html; charset=UTF-8">\n<link rel="stylesheet" type="text/css" href="../css/main.css" media="all"/>\n<link rel="stylesheet" type="text/css" href="../css/agenda.css" media="all"/>\n<link rel="stylesheet" type="text/css" href="./tmp.css" media="all"/>\n'+r'\1'+'</body>\n</html>',self.htmlstr,flags=re.DOTALL))
   print('creating pdf ... advance-'+sys.argv[3]+'-'+('agenda' if self.mode == 'agenda' else 'slides')+'.pdf crateated')
#   pdfkit.from_file(sys.argv[3]+'_pdf.html','advance-'+sys.argv[3]+'-'+('agenda' if self.mode == 'agenda' else 'slides')+'.pdf')
   os.system('wkhtmltopdf --enable-local-file-access '+sys.argv[3]+'_pdf.html advance-'+sys.argv[3]+'-'+('agenda' if self.mode == 'agenda' else 'slides')+'.pdf')

 def placepagebreak(self,k=0,i=0,header='',border=''):
  if self.backend[0]!='m':
   self.pagenumber=self.pagenumber+1
   self.htmlstr+="""<pre class="ftr">&copy www.minhinc.com</pre><a href="#main%s" class="pn">%s%s</a>
</div>
<div class="pg" style="margin-top:%spx;height:%spx;%s">
""" % (self.day[k][i],'<img src="http://minhinc.com/image/arrow.png" width="20px" height="20px"/>' if header!='noarrow' else '',"p"+str(self.pagenumber),self.TM,self.PH,"border:"+border if border else '')
#   self.hc=self.BTMOFST
  elif header:
    self.htmlstr+="""<br><pre class="ftr">&copy www.minhinc.com</pre><a class="pn" href="#main%s">%s</a>
</div>
<div class="pg" style="margin-top:%spx;">
""" % (self.day[k][i],'<img src="http://minhinc.com/image/arrow.png" style="width:20px"/>' if header!='noarrow' else '',self.TM)
  self.hc=self.BTMOFST

 def placetopbreak(self,top=False,border=''):
  if self.backend[0]=='m':
   if top:
    self.htmlstr+="""<div class="pg" style="margin-top:%spx">
""" % (2*self.TM)
   else:
    self.htmlstr+='''<div class="pg">
'''
  else:
   if top:
    self.htmlstr+="""<div class="pg" style="margin-top:%spx;height:%spx;%s">
""" % (2*self.TM,self.PH-self.TM,"border:"+border if border else '')
   else:
    self.htmlstr+="""<div class="pg" style="margin-top:%spx;height:%spx;%s">
""" % (self.TM,self.PH,"border:"+border if border else '')

 def adsensepaste(self,width,height,stylecode='',factor=0.2):
  rightdiv=''
  tmpstr=''
  if not self.responsivesquare:
   self.responsivesquare=[self.db.get('adsense','value','name','responsivesquare')[0][0],False]
   print('responsivesquare',self.responsivesquare)
  if self.backend[0]=='m':
   if self.hc+height<=self.PH/2 or self.responsivesquare[1]:
    height=height if width == self.PAGEWIDTH else int(height/4)
    tmpstr=re.sub(r'\s*data-ad-format="auto".*responsive="true"',r'',re.sub(r'(class="adsbygoogle)',r'\1 adslot_1',re.sub(r'display:block',r'display:inline-block;height:'+str(height)+'px;',self.responsivesquare[0],flags=re.I|re.DOTALL),flags=re.I|re.DOTALL),flags=re.I|re.DOTALL) if height >= 50 else ''
#    rightdiv+="<div style=\"width:100%;height:"+str(height)+"px;\"><div align=\"center\" style=\"width:100%;height:"+str(height)+"px;"+stylecode+"\">"+tmpstr+r'</div></div>' if tmpstr else ''
    rightdiv+="<div align=\"center\" style=\"width:100%;height:"+str(height)+"px;"+stylecode+"\">"+tmpstr+r'</div>' if tmpstr else ''
  else:
   tmpstr=''.join(requestm.adsenserect(width,height,criteria=('.*desktop.*'),factor=factor))
   rightdiv=("<div style=\"width:"+str(int(width))+"px;height:"+str(height)+"px;position:relative;"+stylecode+"\" align=\"center\">"+tmpstr+r'</div>' if tmpstr and self.mode=='php' else '')+(r'<div class="clr"></div>' if re.search(r'float\s*:\s*right',stylecode,flags=re.I) and self.mode=='php' else '')
  if self.hc<=self.PH/2 and self.responsivesquare[1]:
   self.responsivesquare[1]=False
  if self.hc+height>self.PH/2 and not self.responsivesquare[1]:
   rightdiv+="<div align=\"center\" style=\"width:100%;\""+self.responsivesquare[0]+r'</div>' if self.mode=='php' else ''
   self.responsivesquare[1]=True
  return rightdiv

agenda()
