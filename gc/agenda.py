import os,sys;sys.path.append(os.path.expanduser('~')+r'/tmp')
import random
import re
from PIL import Image,ImageDraw,ImageFont
import json
import string
import MISC.utillib.requestm as requestm
from MISC.utillib.databasem import databasec
from datetime import date
import math
from selenium import webdriver
from MISC.utillib.util import Util
from MISC.ffmpeg.libm import libc
from MISC.extra.debugwrite import print
if len(sys.argv)<4:
 print(''' ---usage---
 Note:-[Ll]->lab [Tt]->Theory
 agenda.py [--browser firefox] --tech [c|cpp|gl|li|ldd|py|qt|qml|ml] --company '' "(((1,2,3),(4,L)),((4 5 6),(L,qml1)),((2,),(4T 3 L)))"
 =agenda.py --tech [c|cpp|gl|li|ldd|py|qt|qml] --company '' "(((1,2,3),(4,L)),((4 5 6),(L,qml1)),((2,),(4T 3 L)))"
 agenda.py --tech qt --company '' "(((1,2,3),(4,L)),((4,5,6),(L,)))"
 agenda.py --tech qt --company 'ABC Company' "(1,2,4,5,3)"
 ---- tags ----
 <m> - image - http://minhinc.42web.io/image/logo.png OR ../../image/logo.png
  <mb> - bigimage for article format (would come on next page)
 <c> - code
  <cb> - code with gray background
  <cc> - shortcode
  <cs> - veryshortcode multicolumn, for article format would appear on next page
 <a> - abstract in italics
 <n> - notes
 <d[12..]> - bullet dot size 1 or 2 or ..
 <[rgl]> - red/green/blue font
  <[R|G|L]> - bold red/green/blue font''')
 exit(-1)

class format:
 DELIMITER='!ABS SBA!'
 #PH -> Page Height Maximum TM->Top Margin BTMOFST->Bottom Offset/Margin PDFOFST->pdf version extra less calculated page height
# PH,TM,BTMOFST=1415,20,60
 PH,TM,BTMOFST=1402,20,60
 ADIMAGEHEIGHT=200
 def __init__(self):
  super(format,self).__init__()
  self.libi=libc()
  self.browser,self.tech,self.company=Util.getarg('--browser',2),Util.getarg('--tech',2).lower(),Util.getarg('--company',2)
  self.day=[]
  self.day.extend([[[x for x in re.split(r'\s+',y) if x] for y in re.split(':',i)] for i in sys.argv[1:]])
#  self.newlinehtmltag=['h','m','a','c','cb','cc','cs']
  self.inlinehtmltag=dict((('<i>',r'<span style="font-style:Italic">'),(r'<d(\d+)?>',r'<span style="background-color:#000" class="dot\1"></span>'),('<r>',r'<span style="color:#ff0000;">'),('<g>',r'<span style="color:#004000;">'),('<l>',r'<span style="color:#0055cf;">'),('<R>',r'<span style="color:#ff0000;font-weight:bold">'),(r'<G>',r'<span style="color:#004000;font-weight:bold">'),(r'<L>',r'<span style="color:#0055cf;font-weight:bold">'),(r'</[irglRGL]>',r'</span>'),(r'<n>',r'<pre class="note">'),(r'</n>',r'</pre>'),(r'<c>',r'<pre class="codei">'),(r'</c.?>',r'</pre>'),(r'<cc>',r'<pre class="codeci">'),('<b>','<b>'),('<pre>','<pre>'),('<div>','<div>'),('<p>','<p>')))
  self.PAGEWIDTH=int(re.sub(r'^.*body\s*{\s*width\s*:\s*(\d+).*$',r'\1',open(r'../css/main.css').read(),flags=re.I|re.DOTALL))
  self.htmlstr=''
  self.db=databasec(False)
  self.driver=None
  self.pagenumber=0
  print(f'<=>format.__init__ self.tech={self.tech} self.company={self.company} self.day={self.day} sys.argv={sys.argv}')
  self.fileheader=(f'<html>\n<head>\n<title>Minh, Inc. Software development and Outsourcing| {self.tech} training Bangalore India</title>\n<META http-equiv="Content-Type" content="text/html; charset=UTF-8">\n<link rel="stylesheet" type="text/css" href="../css/main.css" media="all"/>\n<link rel="stylesheet" type="text/css" href="../css/agenda.css" media="all"/>\n</head>\n<body>\n',re.sub(r'.*(<div class="pg".*?Intentionally.*)$',r'\1',self.htmlstr,flags=re.DOTALL),'</body>\n</html>')
  os.mkdir(r'logdir') if not os.path.exists('logdir') else None
  self.preparedisclaimer()
  self.prepareheader()
  self.preparecontent()
  self.prepareoutfile()
  self.driver.close()

 def placepagebreak(self,side,topicnumber=0,arrow=False,topoffset=0,updatehc=True):
  '''\
  pagebreak - top or/and bottom, if header == None no break for mobile
  side='top'/'bottom'/'all'
  topicnumber - self.day[k][j][i]
  arrow -> 'arrow'/'noarrow' - no top arrow button icon
  topoffset -> offset from the top, In main page it is required
  '''
  print(f'><placepagebreak {side=} {topicnumber=} {arrow=} {topoffset=} {updatehc=}')
  if side in ['bottom','all']:
   self.pagenumber=self.pagenumber+1
   self.htmlstr+=f"""\n <pre class="ftr">&copy {Util.webpageurl()}</pre><a href="#main{topicnumber}" class="pn">{'<img src="../http://{Util.webpageurl()}/image/arrow.png" width="20px" height="20px"/>' if arrow else ''}{"p"+str(self.pagenumber)}</a>\n</div>"""
  if side in ['top','all']:
   self.htmlstr+='\n'+rf'<div class="pg" style="height:{self.PH}px;"><div class="topcolor" style="height:{self.TM}px;margin-bottom:{topoffset}px;"></div>'
  self.hc=self.BTMOFST+self.TM+topoffset if updatehc else self.hc

 def lineheightnhtml(self,htmlcode,covertag,skipconversion=False,cssselector=None):
  '''\
  <-  ({'height':,'width':} convertedhtmlcode)
  ->
  htmlcode - htmlcode for conversion i.e. <pre class="articlecontentmaintopic">Descriptor in Python</pre>
  covertag - covertag over htmlcode i.e. '<div class='articleleft'>' 
   this would be converted to <div class="pg"><div class='articleleft'>htmlcode</div></div>
  cssselector - div.pg is default cssselector if this argument is None
  skipconversion - skip the conversion raw htmlcode fed to selenium with expanding custom tags, i.e. <m>,<a>,<cc><cs>...
  '''
  elementdata=None
  print(f'><lineheightnhtml htmlcode={htmlcode} covertag={covertag} skipconversion={skipconversion} {cssselector=}')
  covertag='<div class="pg">'+covertag
  htmlcode='\n'.join([x if x else ' ' for x in htmlcode.split('\n')]) if not skipconversion else htmlcode
  if not self.driver:
   if str(self.browser).lower()=='firefox':
    self.driver=webdriver.Firefox(executable_path=os.path.expanduser('~')+r'/nottodelete/geckodriver')
   else:
    self.driver=webdriver.Chrome()
   self.driver.maximize_window()
   with open(r'test.html','w') as file:
    file.write(r'')
   self.driver.get(r'file:///'+re.sub(r'/?$','',os.getcwd())+r'/test.html')
  htmlcode=eval(','.join(r"re.sub(r'"+x+"',r'"+self.inlinehtmltag[x]+"'" for x in self.inlinehtmltag)+r",re.sub(r'(?P<id>&lt;/?)(?P<id2>\w+)&gt;',lambda m:re.sub(r'&lt;','<',m.group('id'))+m.group('id2')+'>' if [x for x in self.inlinehtmltag if re.search(x,'<'+m.group('id2')+'>')] else m.group('id')+m.group('id2')+r'&gt;',re.sub(r'<',r'&lt;',re.sub(r'>',r'&gt;',htmlcode,flags=re.M),flags=re.M),flags=re.M)"+')'*len(self.inlinehtmltag),{"self":self,"re":re},{"htmlcode":htmlcode}) if not skipconversion else htmlcode
  htmlcode=re.sub(r'&lt;m&gt;(?P<id>.*?)&lt;/m&gt;',lambda m:r'<a href="'+re.sub(r'(http.*)',r'\1',m.group('id'))+r'">'+re.sub(r'^(.*)http.*',r'\1',m.group('id'))+r'</a>',htmlcode,flags=re.M)
  with open(r'test.html','w') as file:
#   file.write('<html>\n<head>\n<link rel="stylesheet" type="text/css" href="../css/main.css" media="all"/>\n<link rel="stylesheet" type="text/css" href="../css/agenda.css" media="all"/>\n</head>\n<body>\n'+(covertag if not type(covertag)==tuple else covertag[0])+htmlcode+(re.sub(r'^\s*<\s*(\w+).*',r'</'+r'\1'+'>',covertag) if not type(covertag)==tuple else covertag[1])+'\n</body>\n</html>')
#   file.write('<html>\n<head>\n<link rel="stylesheet" type="text/css" href="../css/main.css" media="all"/>\n<link rel="stylesheet" type="text/css" href="../css/agenda.css" media="all"/>\n<link rel="stylesheet" type="text/css" href="../css/tmp.css" media="all"/>\n</head>\n<body>\n'+(covertag if not type(covertag)==tuple else covertag[0])+htmlcode+(''.join(r'</'+x+'>' for x in reversed(re.findall(r'<\s*(\w+)',covertag if not type(covertag)==tuple else covertag[1]))))+'\n</body>\n</html>')
   file.write(self.fileheader[0]+(covertag if not type(covertag)==tuple else covertag[0])+htmlcode+(''.join(r'</'+x+'>' for x in reversed(re.findall(r'<\s*(\w+)',covertag if not type(covertag)==tuple else covertag[1]))))+self.fileheader[1])
  self.driver.refresh()
  elementdata=self.driver.find_element_by_css_selector(re.sub(r'.*<\s*(\w+).*?class=\s*[\'"]\s*(\w+).*',r'\1'+r'.'+r'\2',(covertag if not type(covertag)==tuple else covertag[0]),flags=re.DOTALL) if not cssselector else cssselector)
  print(f'''<>lineheightnhtml cssselector=''',re.sub(r'.*<\s*(\w+).*?class=\s*[\'"]\s*(\w+).*',r'\1'+r'.'+r'\2',(covertag if not type(covertag)==tuple else covertag[0]),flags=re.DOTALL) if not cssselector else cssselector,f''' {elementdata.size=} {elementdata.value_of_css_property('margin-top')=} {elementdata.value_of_css_property('margin-bottom')=} {open("test.html").read()=}''')
  return ({'height':elementdata.size['height']+int(re.sub(r'^\s*(\d+).*$',r'\1',elementdata.value_of_css_property('margin-top')))+int(re.sub(r'^\s*(\d+).*$',r'\1',elementdata.value_of_css_property('margin-bottom'))),'width':elementdata.size['width']},htmlcode)
 
# def codedivider(self,htmlcode,height=None,covertag='<div class="pg">',skipconversion=False):
 def codedivider(self,htmlcode,covertag='<div class="pg">',height=None,skipconversion=False,cssselector=None):
  '''\
  partition the code of height 'height'/self.PH-self.hc and the rest
  htmlcode - code to analysed, include tag begin and tag end
  height - first half height
  covertag - to be passed to lineheightnhtml
  skipconversion - to be passed to lineheightnhtml
  returns ((codeheight,codewidth),(prepagecode,postpagecode))'''
  
  print(f'><codedivider htmlcode={htmlcode} height={height} covertag={covertag} skipconversion={skipconversion} {self.PH=} {self.hc=}')
  tmpcode=tmpvar1=tmpvar2=None
  tmpcode=self.lineheightnhtml(htmlcode,covertag,skipconversion=skipconversion,cssselector=cssselector)
  height=height or min(self.PH-self.hc,tmpcode[0]['height'])
  if height >= tmpcode[0]['height']:
   return (tmpcode[0],(tmpcode[1],''))
  tmpvar1=tmpcode[1].split('\n')
  tmpvar2=int(((len(tmpvar1)-1)*height)/tmpcode[0]['height'])
  tmpcode=self.lineheightnhtml('\n'.join(tmpvar1[:(tmpvar2+1)]),covertag,skipconversion=True,cssselector=cssselector)
  while tmpvar2<len(tmpvar1) and tmpcode[0]['height']<height:
   tmpvar2+=1
   tmpcode=self.lineheightnhtml('\n'.join(tmpvar1[:(tmpvar2+1)]),covertag,skipconversion=True,cssselector=cssselector)
  while tmpvar2 and tmpcode[0]['height']>height:
   tmpvar2=tmpvar2-1
   tmpcode=self.lineheightnhtml('\n'.join(tmpvar1[:(tmpvar2+1)]),covertag,skipconversion=True,cssselector=cssselector)
  if not tmpvar2 and tmpcode[0]['height']>height:
   return (tmpcode[0],('','\n'.join(tmpvar1)))
  return (tmpcode[0],('\n'.join(tmpvar1[:tmpvar2+1]),'\n'.join(tmpvar1[tmpvar2+1:])))

 def searchtag(self,tag,cnt):
  return re.search(r'^[ \t]*<'+tag+r'>[ \t]*\n',cnt,flags=re.I|re.DOTALL)

 def getcodecnt(self,tag,cnt):
#  print(f'><getcodecnt {tag=} {cnt=}')
  if tag:
#   return re.split(self.DELIMITER,re.sub(r'^\s*<'+tag+r'>\s*?\n(.*?)\n\s*</'+tag+r'>\s*(.*)$',r'\1'+self.DELIMITER+r'\2',cnt,flags=re.DOTALL))
   return re.split(self.DELIMITER,re.sub(r'^\s*<'+tag+r'>\s*(.*?)\s*</'+tag+r'>\s*(.*)$',r'\1'+self.DELIMITER+r'\2',cnt,flags=re.DOTALL))
  else:
#   return re.split(self.DELIMITER,re.sub(r'^(.*?)\s*((?:'+r'|'.join(r'<'+x+r'>((?!<'+x+r'>).)+\n[ \t]*</'+x+r'>' for x in self.newlinehtmltag)+r'|$).*)',r'\1'+self.DELIMITER+r'\2',cnt,flags=re.DOTALL))
   if re.search(r'\n('+'|'.join(r'\s*<'+x+r'>[ \t]*\n.*\n?[ \t]*</'+x+'>' for x in ['h','a','c','cb','cc','cs'])+r'|[ \t]*<m>[^\n]+</m>)',cnt,flags=re.DOTALL):
    return re.split(self.DELIMITER,re.sub(r'^(.*?)\n((?:'+'|'.join(r'[ \t]*<'+x+'>[ \t]*\n.*\n?[ \t]*</'+x+'>' for x in ['h','a','c','cb','cc','cs'])+r'|[ \t]*<m>[^\n]+</m>).*)$',r'\1'+self.DELIMITER+r'\2',cnt,flags=re.DOTALL))
   else:
    return cnt,''
#  return re.split(r'<><>',re.sub(r'^[ \t]*<'+tag+r'>[ \t]*\n?(.*?)\n?[ \t]*</'+tag+r'>[ \t]*\n?(.*)$','\\1<><>\\2',cnt,flags=re.DOTALL))

 def adsense(self,height):
  if not hasattr(format.adsense,'tech'):
   format.adsense.tech=[]
#  print(f'TEST adsense {height=} {format.adsense.tech=}')
  height-=int(self.TM*1.2)
  format.adsense.tech=[x[0] for x in self.db.get('tech','name') if x[0]!=self.tech and os.path.exists(os.path.expanduser('~')+r'/tmp/MISC/image/'+x[0]+'traininglogo.gif')] if not format.adsense.tech else format.adsense.tech
  basetech=format.adsense.tech[random.randint(0,len(format.adsense.tech)-1)]
  format.adsense.tech[format.adsense.tech.index(basetech):format.adsense.tech.index(basetech)+1]=[]
  img=Image.open(os.path.expanduser('~')+r'/tmp/MISC/image/'+f'{basetech}traininglogo.gif')
  heightl=(height*img.width)/img.height > self.PAGEWIDTH*0.95 and int((self.PAGEWIDTH*0.95*img.height)/img.width) or height
  print(f'TEST2 adsense {basetech=} {format.adsense.tech=} {height=} {heightl=}')
  return '\n<div class="clr"></div>'+f'<a style="display:block" href="{"http://"+Util.webpageurl()+"/training/"+basetech}"><img style="margin:{heightl<height and (height-heightl)//2 or self.TM//2}px 0 {heightl<height and (height-heightl)//2 or self.TM//2}px {(self.PAGEWIDTH-(heightl*img.width)//img.height)//2}px;height:{heightl}px;" src=http://{Util.webpageurl()}/image/{basetech}traininglogo.gif /></a>'+'<div class="clr"></div>\n'

class trainingformat(format):
 def __init__(self):
  super(trainingformat,self).__init__()
 def prepareheader(self):
  LH=22;HH=40;OFST=25#headerheight
#  CHH=40;HHH=50;CHG=125;HCG=40;CCG=80#contentheaderheight,contentheadergap,headercontentgap,contentcontentgap
  CHH=40;HHH=50;CHG=155;HCG=40;CCG=100#contentheaderheight,contentheadergap,headercontentgap,contentcontentgap
  numofline=0
  top='';left=True;
  labstr='';header=''
  height=0
  agendadaydata=[]
  subtopiccount=0
  headerlist=None
  tech=self.tech
  day=self.day.copy()
  tmpstr=''
#  self.placepagebreak(side='top',topoffset=2*self.TM)
  self.placepagebreak(side='top')
  tmpstr=""" <pre class=title>%s</pre>
 <pre class=subtitle>%s</pre>
 <pre class=company>%s</pre>
""" % (self.db.get(self.tech,'content','name','title')[0][0],self.db.get(self.tech,'content','name','subtitle')[0][0],'('+self.company+')' if self.company else '')
  tmpstr+="<div style=\"width:100%;height:100px;\"></div>"
  numofline=sum(max(len(re.findall(r'\n',str(data[1])))+1,len(re.findall(r'\n',str(data[3])))+1) for data in self.db.get(self.tech,'*','name','^h_',orderby='id',regex=True))
  for data in self.db.get(self.tech,'*','name','^h_',orderby='id',regex=True):
   if not re.search(r'h_hr',data[1]):
    tmpstr+=""" <div style="height:%spx;">
  <div class="headerleft"> <pre>%s</pre>
  </div>
  <div class="headerright"> <pre>%s</pre>
  </div>
 </div>
""" % (max(len(re.findall(r'\n',data[1]))+1,len(re.findall(r'\n',data[3]))+1)*LH+int((50*OFST)/numofline),re.sub(r'^h_','',data[1]),data[3])
   else:
    tmpstr+=''' <hr>
'''
  self.htmlstr+=re.sub(r'(class=title)',r'\1'+f' style="margin-top:{int((self.PH-self.TM-self.BTMOFST-self.lineheightnhtml(tmpstr,covertag="",skipconversion=True)[0]["height"])*0.3)}"',tmpstr,flags=re.DOTALL)
  self.placepagebreak('all')
  for count,data in enumerate(self.db.get(self.tech,'*','name','^h2_',orderby='id',regex=True)):
   tmpstr=f""" <div class="header2" style="margin-top:{0 if not count else OFST*5}px;margin-bottom:{0 if not count else 5*OFST}px;">
  <pre class="header" style="line-height:{HH}px">{re.sub(r'^h2_','',data[1])}</pre>
  <pre class="content" style="height:"""+str(len(re.findall(r'\n',data[3]))*LH+OFST)+f"""px">{data[3]}</pre>
 </div>
"""
   self.htmlstr+=tmpstr
   self.hc+=self.lineheightnhtml(tmpstr,covertag='',skipconversion=True,cssselector='div.header2')[0]['height']
#   print(f'TEST header {self.hc=}')
#""" % (0 if not count else OFST*5,HH,re.sub(r'^h2_','',data[1]),len(re.findall(r'\n',data[3]))*LH+OFST,data[3])
#   self.hc+=HH+(len(re.findall(r'\n',data[3]))+1)*LH+OFST if not count else self.hc+5*OFST+HH+(len(re.findall(r'\n',data[3]))+1)*LH+OFST
#   self.hc+=HH+(len(re.findall(r'\n',data[3]))+1)*LH+OFST if not count else 5*OFST+HH+(len(re.findall(r'\n',data[3]))+1)*LH+OFST
#  print(f'self.htmlstr={self.htmlstr}')
  
  tmpstr='';tmphc=0;dayheight=0
  basevalue=0
#  tech=self.tech
#  day=self.day.copy()
  techchange=False
  for k in range(len(day)):#each day
   for i in range(len(day[k])):#morning and evening
    for j in range(len(day[k][i])):#each topic
     if re.search(r'\d+',day[k][i][j]):
      if re.search(r'^[a-z]+\d+',day[k][i][j],flags=re.I):
       tech=re.sub(r'^([a-z]+)\d+.*$',r'\1',day[k][i][j])
       day[k][i][j]=re.sub(r'[a-z]+(\d+.*)',r'\1',day[k][i][j])
       techchange=True
      if re.search(r'\d+[Tt]$',day[k][i][j],flags=re.I):
       day[k][i][j]=re.sub(r'^(\d+).*',r'\1',day[k][i][j])
      else:#elif  re.search(r'\d+(?![Tt])$',day[k][i][j],flags=re.I):
#       print(f'TEST lab {(k,i,j)=}')
       labstr=labstr+('\n' if labstr else '')+'\n'.join([self.db.get(tech,'lab','id',day[k][i][j])[0][0]])
      data=re.sub(r'^\n(.*)\n$','\\1',re.sub(r'\n+','\n',''.join([re.sub(r'</?h>','\n',e) for e in re.findall(r'<h>.*?</h>',self.db.get(tech,'content','id',day[k][i][j])[0][0],flags=re.DOTALL)])),flags=re.DOTALL)
     elif re.search(r'^[Ll]$',day[k][i][j]):
      data=labstr;labstr=''
     if j==0:
      tmpstr+=f""" <div class="dayheader" style="margin-top:{str(CHG)+'YYY'}px;height:{HHH}px"><pre>Day {k+1} {"Afternoon" if i!=0 else "Morning"}</pre><hr></div>\n"""
      tmphc+=HHH+CHG
     print(f'k,i,j={(k,i,j)} data={data} labstr={labstr} tmphc={tmphc} tmpstr={tmpstr}')
     tmpstr+=""" <div class=%s style="margin-top:%spx;%s">
   <div class="%s" style="height:%spx">%s class="%s" style="padding-top:%spx;%spx">%s%s  </div>
    <ul class="daycontent" style="padding-top:10px;">
 """ % ('"dayheaderright"' if re.search(r'dayheaderleft',tmpstr,flags=re.I) else '"dayheaderleft"',HCG if re.search(r'YYY',tmpstr,flags=re.I) else str(CCG)+'XXX','height:'+str((len(re.findall(r'\n',data))+1)*LH+CHH)+'px;','dayheaderheaderlab' if re.search(r'^[Ll]$',day[k][i][j]) else 'dayheaderheadertechchange' if techchange else 'dayheaderheader',CHH,'<pre' if re.search(r'^[Ll]$',day[k][i][j]) else "<a name=\"main"+day[k][i][j]+"\" href=\"#chap"+str(day[k][i][j])+"\"",'dayheader',CHH/4 if not re.search(r'^[Ll]$',day[k][i][j]) else 0,'height:'+str(CHH) if not re.search(r'^[Ll]$',day[k][i][j]) else 'line-height:'+str(CHH),'     Lab' if re.search(r'^[Ll]$',day[k][i][j]) else '  Lecture - '+self.db.get(tech,'name','id',day[k][i][j])[0][0]+('    ( '+tech+' )' if techchange else ''),'</pre>' if re.search(r'^[Ll]$',day[k][i][j]) else '</a>')
     subtopiccount=0
     techchange=False
     for headerindex in (re.findall(r'\s*([*].*?)\s*(?=[*]|$)',data,flags=re.I|re.DOTALL) if re.search(r'^[Ll]$',day[k][i][j]) else re.findall(r'<h>\s*(.*?)\s*</h>',self.db.get(tech,'content','id',day[k][i][j])[0][0],flags=re.I|re.DOTALL)):
      for le in [re.sub(r'^\n*(.*?)\n*$',r'\1',e,flags=re.DOTALL) for e in re.split(r'[*]',headerindex) if e]:
       tmpstr+="""   <li>%s%s%s</li>
  """ % ('<pre>' if re.search(r'^[Ll]$',day[k][i][j]) else '<a name="main'+str(day[k][i][j])+'_'+str(subtopiccount)+'" href="#chap'+str(day[k][i][j])+'_'+str(subtopiccount)+'"<pre>',re.sub(r'\n','<br>',le,flags=re.DOTALL),'</pre>' if re.search(r'^[Ll]$',day[k][i][j]) else '</pre></a>')
#  """ % ('<pre>' if re.search(r'^[Ll]$',day[k][i][j]) else "<a href=\"#chap"+str(day[k][i][j])+'_'+str(subtopiccount)+"\">" if not re.search(r'^[Ll]$',day[k][i][j]) else '<a href=\"#chap'+day[k][i][j]+'_'+str(subtopiccount)+'\">'+'<pre>',re.sub(r'\n','<br>',le,flags=re.DOTALL) if not re.search(r'^[Ll]$',day[k][i][j]) else le,'</pre>' if re.search(r'^[Ll]$',day[k][i][j]) else "</a>" if not re.search(r'^[Ll]$',day[k][i][j]) else '</pre></a>')
       subtopiccount+=1
     tmpstr+='''  </ul>
  </div>
 '''
#     dayheight=max(dayheight,self.lineheightnhtml(re.sub(r'^.*(<div\s*class="dayheader(?:left|right)")\s*style=".*?"(.*)$',r'\1\2',tmpstr,flags=re.I|re.DOTALL),re.sub(r'^.*(<div\s*class="dayheader(?:left|right)").*$',r'\1>',tmpstr,flags=re.I|re.DOTALL),skipconversion=True)[0]['height'] + (HCG if re.search(r'YYY',tmpstr,flags=re.I) else CCG))
     dayheight=max(dayheight,self.lineheightnhtml(re.sub(r'^.*(<div\s*class="dayheader(?:left|right)")\s*style=".*?"(.*)$',r'\1\2',tmpstr,flags=re.I|re.DOTALL),covertag='',skipconversion=True,cssselector='div.dayheader'+re.sub(r'^.*<div\s*class="dayheader(left|right)".*$',r'\1',tmpstr,flags=re.I|re.DOTALL))[0]['height'] + (HCG if re.search(r'YYY',tmpstr,flags=re.I) else CCG))
#     tmpstr=re.sub(r'^(?P<id>.*<div\s*class="dayheader(?:left|right)".*?height:)\d+(?P<id1>.*)$',lambda m:m.group('id')+str(self.lineheightnhtml(re.sub(r'^.*(<div\s*class="dayheader(?:left|right)")\s*style=".*?"(.*)$',r'\1\2',tmpstr,flags=re.I|re.DOTALL),re.sub(r'^.*(<div\s*class="dayheader(?:left|right)").*$',r'\1>',tmpstr,flags=re.I|re.DOTALL),skipconversion=True)[0]['height'])+m.group('id1'),tmpstr,flags=re.I|re.DOTALL)
     tmpstr=re.sub(r'^(?P<id>.*<div\s*class="dayheader(?:left|right)".*?height:)\d+(?P<id1>.*)$',lambda m:m.group('id')+str(self.lineheightnhtml(re.sub(r'^.*(<div\s*class="dayheader(?:left|right)")\s*style=".*?"(.*)$',r'\1\2',tmpstr,flags=re.I|re.DOTALL),covertag='',skipconversion=True,cssselector='div.dayheader'+re.sub(r'^.*<div\s*class="dayheader(left|right)".*$',r'\1',tmpstr,flags=re.I|re.DOTALL))[0]['height'])+m.group('id1'),tmpstr,flags=re.I|re.DOTALL)
     if re.search(r'dayheaderright',tmpstr,re.I) or j==(len(day[k][i])-1):
      tmphc+=dayheight
      dayheight=0
     print(f'TEST {(k,i,j)=} {self.hc=} {self.hc+tmphc=} {dayheight}')
     def fixextragap(self):
      headermorningcount=len(re.findall(r'YYY.*?Morning',self.htmlstr,flags=re.I))
      headerafternooncount=len(re.findall(r'YYY.*?Afternoon',self.htmlstr,flags=re.I))
      daycount=len(re.findall(r'dayheaderleft.*?XXX',self.htmlstr,flags=re.I))
      basevalue=int((self.PH-self.hc)/(6*headermorningcount+2*headerafternooncount+daycount)) if headermorningcount+headerafternooncount+daycount>0 else 0
      print(f'TEST {(headermorningcount,headerafternooncount,daycount)=} {basevalue=} {(k,i,j)=} {self.hc=}\n',self.htmlstr if (k,i,j)==(3,0,1) else '')
      if headermorningcount+headerafternooncount+daycount:
       self.htmlstr=re.sub(r'(<div class="dayheader".*?YYY.*?Morning)',self.adsense(6*basevalue+CHG)+r'\1',self.htmlstr,flags=re.M) if headermorningcount and (6*basevalue+CHG)>= self.ADIMAGEHEIGHT else self.htmlstr
       self.htmlstr=re.sub(r'(<div class="dayheader".*?YYY.*?Afternoon)',self.adsense(2*basevalue+CHG)+r'\1',self.htmlstr,flags=re.M) if headerafternooncount and (2*basevalue+CHG)>= self.ADIMAGEHEIGHT else self.htmlstr
       self.htmlstr=re.sub(r'(<div class="dayheaderleft".*?XXX)',self.adsense(basevalue+CCG)+r'\1',self.htmlstr,flags=re.M) if daycount and (basevalue+CCG)>= self.ADIMAGEHEIGHT else self.htmlstr
       self.htmlstr=re.sub(r'(?P<id>\d+)YYY(?P<id1>.*?Morning)',lambda m: str(int(m.group('id'))+6*basevalue if (6*basevalue+CHG)<self.ADIMAGEHEIGHT else 0)+m.group('id1'),self.htmlstr,flags=re.I)
       self.htmlstr=re.sub(r'(?P<id>\d+)YYY(?P<id1>.*?Afternoon)',lambda m: str(int(m.group('id'))+2*basevalue if (2*basevalue+CHG)<self.ADIMAGEHEIGHT else 0)+m.group('id1'),self.htmlstr,flags=re.I)
       self.htmlstr=re.sub(r'(?P<id>\d+)XXX',lambda m: str(int(m.group('id'))+basevalue if (basevalue+CCG)<self.ADIMAGEHEIGHT else 0),self.htmlstr,flags=re.I)
     if ((self.hc+tmphc)>=self.PH and dayheight==0) or (k==len(day)-1 and i==len(day[k])-1 and j==len(day[k][i])-1):
      if (self.hc+tmphc)>=self.PH:
#       self.pagenumber+=1
       self.placepagebreak('all',day[k][i][j],updatehc=False)
#       print("self.hc {}, self.PH {}".format(self.hc,self.PH))
#       self.hc=self.hc+(self.PH-self.hc)*0.40
       fixextragap(self)
       self.htmlstr+='\n'+re.sub(r'\d+(YYY|XXX)',r'0',tmpstr,flags=re.I)
       if re.search(r'YYY',tmpstr,flags=re.I): 
        tmphc-=CHG
       elif re.search(r'XXX',tmpstr,flags=re.I): 
        tmphc-=CCG
       if k==len(day)-1 and i==len(day[k])-1 and j==len(day[k][i])-1:
        self.htmlstr+=self.adsense(self.PH-tmphc-self.TM-self.BTMOFST)
        self.placepagebreak('bottom',day[k][i][j])
      else: 
#       print(f'TEST 1')
#       self.pagenumber+=1
       self.htmlstr+=tmpstr
       self.hc+=tmphc
       fixextragap(self)
       self.placepagebreak('bottom',day[k][i][j],updatehc=False)
#       self.hc=self.hc+(self.PH-self.hc)*0.85
#       self.htmlstr+='''
#       <div style="clear:both;"></div>
#       ''' 
      self.hc=self.TM+self.BTMOFST+tmphc
      tmpstr='';tmphc=0
     elif dayheight==0:
      self.htmlstr+=tmpstr
      self.hc+=tmphc
      tmpstr='';tmphc=0
    

  self.hc=0
#  print(f'self.htmlstr={self.htmlstr}')

 def preparedisclaimer(self):
  self.placepagebreak(side='top')
  img=Image.open(os.path.expanduser('~')+r'/tmp/imageglobe/resource/booktitlepage.png').convert('RGBA')
  img=img.resize((((self.PH-self.TM-self.BTMOFST)*img.width)//img.height,self.PH-self.TM))
  self.libi.system(r'python3 tex.py "'+self.db.get('tech','content','name',self.tech)[0][0].title()+r'" 1')
  img2=Image.open(re.sub(r'[\s/]+','',self.db.get('tech','content','name',self.tech)[0][0].lower())+'.png').convert('RGBA')
  img.paste(img2,((img.width-img2.width)//2,(img.height-img2.height)//2),img2)
  draw=ImageDraw.Draw(img)
#  draw.text((img.width//2,img.height//18),self.db.get('tech','content','name',self.tech)[0][0].title()+' Training',font=self.libi.getfont((self.db.get('tech','content','name',self.tech)[0][0].title()+' Training',),0.8,os.path.expanduser('~')+r'/.fonts/urwbookman-light.otf',False,img.size),anchor='mt',fill=(6,21,90,255))
  draw.text((img.width//2,img.height//18),self.db.get('tech','content','name',self.tech)[0][0].title()+' Training',font=self.libi.getfont((self.db.get('tech','content','name',self.tech)[0][0].title()+' Training',),0.8,os.path.expanduser('~')+r'/.fonts/ufonts.com_tw-cen-mt.ttf',False,img.size),anchor='mt',fill=(0,60,0,255))
#  draw.text((img.width//2,img.height//18+self.libi.getfont((self.db.get('tech','content','name',self.tech)[0][0].title()+' Training',),0.8,os.path.expanduser('~')+r'/.fonts/urwbookman-light.otf',False,img.size).getsize(self.tech.title()+' Training')[1]),'Essentials',font=self.libi.getfont((self.db.get('tech','content','name',self.tech)[0][0].title()+' Training',),0.6,os.path.expanduser('~')+r'/.fonts/urwbookman-light.otf',False,img.size),anchor='mt',fill=(6,21,90,255))
  draw.text((img.width//2,img.height//18+self.libi.getfont((self.db.get('tech','content','name',self.tech)[0][0].title()+' Training',),0.8,os.path.expanduser('~')+r'/.fonts/ufonts.com_tw-cen-mt.ttf',False,img.size).getsize(self.tech.title()+' Training')[1]),'Essentials',font=self.libi.getfont((self.db.get('tech','content','name',self.tech)[0][0].title()+' Training',),0.6,os.path.expanduser('~')+r'/.fonts/urwbookman-light.otf',False,img.size),anchor='mt',fill=(0,60,0,255))
  draw.text((img.width//4,(img.height*8.9)//10),'Minh, Inc.',font=ImageFont.truetype(os.path.expanduser('~')+r'/.fonts/ufonts.com_tw-cen-mt.ttf',40),anchor='mt',fill=(0,0,0,255))
  draw.text((img.width//4,(img.height*8.9)//10+ImageFont.truetype(os.path.expanduser('~')+r'/.fonts/ufonts.com_tw-cen-mt.ttf',40).getsize('Minh')[1]),r'https://youtube.com/@minhinc',font=ImageFont.truetype(os.path.expanduser('~')+r'/.fonts/urwbookman-light.otf',25),anchor='mt',fill=(0,0,0,255))
  img.save('advance-'+self.tech+'-slides_front.png')
  self.htmlstr+=f'\n<img src="http://{Util.webpageurl()}/image/advance-{self.tech}-slides_front.png" style="display:block;margin:auto"/>'
  self.placepagebreak(side='all')
  self.htmlstr+=f'<img src="http://{Util.webpageurl()}/image/honeybee.png" style="width:{self.PAGEWIDTH//3}px;margin-top:100px;margin-left:{self.PAGEWIDTH//3}px;margin-bottom:400px;"/>'
  self.htmlstr+=fr"""<pre style="font-family:Liberation Serif;font-size:12pt;width:80%;color:#222222;margin:auto">The {self.db.get('tech','content','name',self.tech)[0][0]} Training journal is published online by Minh, Inc. and is available at http://minhinc.42web.io/training/{self.tech}<br><br>For submission guildelines please visit http://minhinc.42.web.io. Enquiries should be addressed to tominhinc@gmail.com or WhatsApp +91 9483160610.<br><br>Copyright &copy Minh, Inc. Bangalore, India. Author(s) retain copyright and grant journal right of first publication with the work simultaneously licensed under a creative Commons Attribution License that allows others to share the work with an acknowledgement of the work’s authorship and initial publication in this journal. Author(s) are able to enter into separate, additional contractual agreements for the non–exclusive distribution of the journal’s published version of the work (e.g. post it to an institutional repository or publish it in a book), with an acknowledgement of its initial publication in this journal.</p>"""
  self.placepagebreak(side='all')
  self.htmlstr+=fr"""<pre style="line-height:{self.TM*4}px;text-align:center;font-family:mytwcenmt;font-size:26pt;color:#222222">Acknowledgements</pre>"""
  self.placepagebreak(side='bottom')
  Util.push('advance-'+self.tech+'-slides_front.png',dir='image')

 def preparecontent(self):
  LH=20
  cnt=fixheader=header=code=""
  cscount=linecount=subtopiccount=0
  XOFFSET=10
  self.hc=self.BTMOFST
  tmpvar1=tmpvar2=tmpcode=None
  htmltag=''
  tech=self.tech
  day=self.day.copy()
  for k in range(len(day)):
   for i in range(len(day[k])):
    for j in [x for x in range(len(day[k][i])) if not re.search(r'^[Ll]$',day[k][i][x])]:
     if re.search(r'^\w+\d+[Tt]?$',day[k][i][j]):
      tech,day[k][i][j]=re.sub(r'^(\w+)\d+.*',r'\1',day[k][i][j]),re.sub(r'^.*?(\d+).*$',r'\1',day[k][i][j])
     cnt=self.db.get(self.tech,'content','id',day[k][i][j])[0][0]
     fixheader=re.sub(r'^\n(.*)\n$','\\1',re.sub(r'\n+','\n',''.join([re.sub(r'</?h>','\n',e) for e in re.findall(r'<h>.*?</h>',cnt,flags=re.DOTALL)])),flags=re.DOTALL)
     print("fixheader><%s<>" % fixheader)
     subtopiccount=0
     self.placepagebreak(side='top')
     while cnt:
      if self.searchtag('h',cnt):
       print("<=><h>",self.hc)
       code,cnt=self.getcodecnt('h',cnt)
       header="""<div class="slideheader">
   %s<pre class="day">%s</pre></a>
   %s<pre class="topic">%s</pre>%s
    <ul class="slidecontent">
 """ % ('\n <a style="display:block;" href="#main'+str(day[k][i][j])+'" '+('name="chap'+day[k][i][j]+'"' if subtopiccount==0 else '')+r'>','Day '+str(k+1)+' '+('Afternoon' if i!=0 else 'Morning'),"<h1>" if subtopiccount==0 else '','  '+str(day[k][i][j])+'. '+self.db.get(self.tech,'name','id',day[k][i][j])[0][0],"</h1>" if subtopiccount==0 else '')
# """ % ("\n <a "+"href=\"#main"+str(day[k][i][j])+('_'+str(subtopiccount) if subtopiccount else '')+"\" name=\"chap"+day[k][i][j]+"\">&nbsp;",'Day '+str(k+1)+' '+('Afternoon' if i!=0 else 'Morning'),"<h1>" if subtopiccount==0 else '','  '+str(day[k][i][j])+'. '+self.db.get(self.tech,'name','id',day[k][i][j])[0][0],"</h1>" if subtopiccount==0 else '')
# """ % ("\n <a "+"href=\"#main"+str(day[k][i][j])+"\" name=\"chap"+day[k][i][j]+"\">&nbsp;" if subtopiccount==0 else "",'Day '+str(k+1)+' '+('Afternoon' if i!=0 else 'Morning'),"<h1>" if subtopiccount==0 else '','  '+str(day[k][i][j])+'. '+self.db.get(self.tech,'name','id',day[k][i][j])[0][0],"</h1>" if subtopiccount==0 else '')
       for line in [line for line in re.split(r'('+re.escape(code)+r'\s*$)',fixheader,flags=re.M) if line]:
        line=re.sub(r'^\n*(.*)\n*$','\\1',line,flags=re.DOTALL)
        for ii in [re.sub(r'^\n*(.*)\n*$','\\1',ii,flags=re.DOTALL) for ii in re.split(r'^[*]',line,flags=re.M) if ii]:
         header+="""   <li class="%s">%s%s%s</li>""" % ("big" if line==code else "sml",'<h2>'+("<a href=\"#main"+str(day[k][i][j])+"\" name=\"chap"+str(day[k][i][j])+'_'+str(subtopiccount)+"\">") if line==code else '<pre>',"<br>".join([re.sub(r'^[ ]?([ ]*)(.*)',re.sub(r'[ ]',r'&nbsp;',re.sub(r'^[ ]?([ ]*).*',r'\1',iii))+r'\2',iii) for iii in re.split(r'\n',ii)]) if line==code else ii,"</a>"+'</h2>' if line==code else '</pre>')
       header+="""
    </ul>
 </div>%s
 """ % ('</a>' if subtopiccount==0 else '')
       subtopiccount+=1
#       tmpcode=self.lineheightnhtml(header,r'<div class="slideheader">',skipconversion=True)
       tmpcode=self.lineheightnhtml(header,'',skipconversion=True,cssselector=r'div.slideheader')
       if (self.hc+tmpcode[0]['height']+LH)>self.PH:
        self.placepagebreak('all',day[k][i][j]);
       header=re.sub(r'^(.*?class="slideheader")(.*)$',r'\1{}\2'.format(' style="height:'+str(tmpcode[0]['height'])+'px;width:'+str(tmpcode[0]['width'])+'px;"'),header,flags=re.I|re.DOTALL)
       self.htmlstr+=header
       self.hc+=tmpcode[0]['height']
       self.htmlstr+=f'\n<div class="clr"></div>' if not re.search(r'^\s*<a>',cnt,flags=re.DOTALL) else ''
      elif re.search(r'^\s*<a>.*?</a>',cnt,flags=re.I|re.DOTALL):
       print("<a>")
       code,cnt=self.getcodecnt('a',cnt)
       self.htmlstr+='\n<pre class="slideabstract">'+self.lineheightnhtml(code,'<pre class="slideabstract">')[1]+'</pre>\n<div class="clr"></div>'
      elif re.search(r'^\s*<m>[^\n]+</m>',cnt):
       print("<m>",self.hc)
       code,cnt=self.getcodecnt('m',cnt)
       code=Util.webpageurl(http=True)+r'/image/'+code if not re.search(r'/',code) else code
       tmpvar1=re.sub(r'^.*(?:embed/|\?v=)(.*)$',r'\1',code) if re.search('youtube',code,flags=re.I) else ''
       code=requestm.youtubeimage(re.sub(r'^.*(?:embed/|\?v=)(.*)$',r'\1',code),pushonserver=True)[0] if re.search(r'youtube',code,flags=re.I) else code
       try:
        with Image.open(os.path.expanduser('~')+r'/tmp/MISC/image/'+re.sub(r'^.*/','',code)) as img:
         if self.hc+(img.height if img.width<=self.PAGEWIDTH else (self.PAGEWIDTH//2*img.height)//img.width)>self.PH:
          self.htmlstr+=self.adsense(self.PH-self.hc) if self.PH-self.hc>self.ADIMAGEHEIGHT else ''
          self.placepagebreak('all',day[k][i][j])
         self.hc+=img.height if img.width<=self.PAGEWIDTH//2 else (self.PAGEWIDTH//2*img.height)//img.width
         self.htmlstr+='\n'+("  <a style=\"display:block;\" href=\""+(re.sub(r'(.*)_s[.](.*)','\\1.\\2',code) if not tmpvar1 else r'https://youtube.com/watch?v='+tmpvar1)+"\">" if re.search(r'_s[.]',code) or tmpvar1 else '')+f'<img style="margin-left:{(self.PAGEWIDTH-img.width)//2}" class="img" src="{code}" />'+("</a>" if re.search(r'_s[.]',code) or tmpvar1 else "")+f'''<div class="clr"></div>'''
       except Exception as e:
        if self.hc+LH>self.PH:
         self.placepagebreak('all',day[k][i][j])
        self.hc+=LH
        self.htmlstr+="""\n <a href="{line}">{line}</a>"""
      elif self.searchtag('cs',cnt):
       print("<cs>")
       tmpvar2=0#0->first half 1->second half
       code,cnt=self.getcodecnt('cs',cnt)
       tmpcode=self.lineheightnhtml(code,'<pre class="codes">')
       tmpcode=self.codedivider(tmpcode[1],'<pre class="codes">',tmpcode[0]['height']/2 if tmpcode[0]['height']/2+self.hc < self.PH else None,skipconversion=True)
       while tmpcode[1][0] or tmpcode[1][1]:
        if tmpcode[1][0]:
#         self.htmlstr+='\n <pre class="codes" style="float:left;'+('height:'+str(tmpcode[0]['height'])+'px;')+'">'+tmpcode[1][0]+' </pre>\n'+('<div class="clr"></div>' if tmpvar2 else "")
         self.htmlstr+='\n <pre class="codes" style="'+('height:'+str(tmpcode[0]['height'])+'px;')+'">'+tmpcode[1][0]+' </pre>\n'+('<div class="clr"></div>' if tmpvar2 else "")
         if tmpvar2:
          self.hc+=tmpcode[0]['height']
        if tmpcode[1][1]:
         if tmpvar2:
          self.placepagebreak('all',day[k][i][j])
          tmpcode=self.lineheightnhtml(tmpcode[1][1],'<pre class="codes">',skipconversion=True)
          tmpcode=self.codedivider(tmpcode[1],'<pre class="codes">',tmpcode[0]['height']/2 if tmpcode[0]['height']/2+self.hc < self.PH else None,skipconversion=True)
         else:
          tmpcode=self.codedivider(tmpcode[1][1],'<pre class="codes">',skipconversion=True)
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
#        if re.search(r'(\s*<h>[ \t]*\n.*\n?[ \t]*</h>|\s*<a>.*?</a>|\s*<cb?>[ \t]*\n.*\n?[ \t]*</cb?>|\s*<cc>[ \t]*\n.*\n?[ \t]*</cc?>|\s*<cs>[ \t]*\n.*\n?[ \t]*</cs>|\s*<m>.*?</m>)',cnt,flags=re.DOTALL):
#         code,cnt=re.split(r'<><>',re.sub(r'^(.*?)\n?((?:[ \t]*<h>[ \t]*\n.*\n?[ \t]*</h>|[ \t]*<a>.*?[ \t]*</a>|[ \t]*<cb?>[ \t]*\n.*\n?[ \t]*</cb?>|<cc>[ \t]*\n.*\n?[ \t]*</cc?>|[ \t]*<cs>[ \t]*\n.*\n?[ \t]*</cs>|[ \t]*<m>.*?</m>).*)$',r'\1<><>\2',cnt,flags=re.DOTALL))
        code,cnt=self.getcodecnt('',cnt)
#        else:
#         code=cnt;cnt=''
        htmltag='<pre class="slidecontent">'
       tmpcode=self.codedivider(code,htmltag)
       while tmpcode[1][0] or tmpcode[1][1]:
        if tmpcode[1][0]:
         self.htmlstr+='\n '+re.sub(r'>$','',htmltag)+f' style="height:{tmpcode[0]["height"]}px;">{tmpcode[1][0]}\n </pre>'
         self.hc+=tmpcode[0]['height']
        else:
         self.placepagebreak('all',day[k][i][j])
        if not tmpcode[1][1]:
         break
        tmpcode=self.codedivider(tmpcode[1][1],htmltag,skipconversion=True)
     else:
      self.htmlstr+=self.adsense(self.PH-self.hc) if self.PH-self.hc>self.ADIMAGEHEIGHT else ''
      self.placepagebreak('bottom',day[k][i][j])

 def prepareoutfile(self):
#  import pdfkit
#  os.environ['NO_AT_BRIDGE']=str(1)
  filedatadesktop=None
  self.placepagebreak(side='top')
  self.htmlstr+=fr'''<pre style="line-height:{self.PH-self.TM}px;text-align:center;font-weight:bold;font-size:30pt;color:#000000;font-family:Liberation Serif;">Intentionally Left Blank</pre>'''
  self.placepagebreak(side='all')
  img=Image.open(os.path.expanduser('~')+r'/tmp/imageglobe/resource/booktitlepagebottom.png').convert('RGBA')
  img=img.resize((((self.PH-self.TM-self.BTMOFST)*img.width)//img.height,self.PH-self.TM))
  self.libi.system(r'python3 tex.py "'+self.db.get('tech','content','name',self.tech)[0][0].title()+r'" 2')
  img2=Image.open(re.sub(r'[\s/]+','',self.db.get('tech','content','name',self.tech)[0][0].lower())+'.png').convert('RGBA')
  img.paste(img2,((img.width-img2.width)//2,int(img.height*0.64)-img2.height//2),img2)
  draw=ImageDraw.Draw(img)
  draw.text((img.width//16,img.height//16),'MINH, INC.',font=ImageFont.truetype(os.path.expanduser('~')+r'/.fonts/ufonts.com_tw-cen-mt.ttf',30),anchor='lt',fill=(9,21,90,255))
  draw.line((img.width//16,img.height//16+ImageFont.truetype(os.path.expanduser('~')+r'/.fonts/ufonts.com_tw-cen-mt.ttf',30).getsize('MINH')[1]+4,(img.width*11)//12,img.height//16+ImageFont.truetype(os.path.expanduser('~')+r'/.fonts/ufonts.com_tw-cen-mt.ttf',30).getsize('MINH')[1]+4),fill=(6,21,90,255),width=6)
  draw.line((img.width//16,img.height//16+ImageFont.truetype(os.path.expanduser('~')+r'/.fonts/ufonts.com_tw-cen-mt.ttf',30).getsize('MINH')[1]+12,(img.width*11)//12,img.height//16+ImageFont.truetype(os.path.expanduser('~')+r'/.fonts/ufonts.com_tw-cen-mt.ttf',30).getsize('MINH')[1]+12),fill=(6,21,90,255),width=4)
  draw.multiline_text((img.width//16,img.height//16+ImageFont.truetype(os.path.expanduser('~')+r'/.fonts/ufonts.com_tw-cen-mt.ttf',30).getsize('MINH')[1]+44),'Minh, Inc. was established in Mid 2015 as research and developement center in software\ntechnologies like Device Drivers, Embedded OpengGL 3D graphics, Machine Learning and\nArtificial Intelligence. Company provides training in various technolgies. Visit \nhttp://minhinc.42web.io/training\n\nPlease follow at https://youtube.com/@minhinc',font=ImageFont.truetype(os.path.expanduser('~')+r'/.fonts/timesnewromanbold.ttf',20),spacing=8,fill=(9,21,90,255))
  draw.multiline_text((img.width//16,img.height//16+ImageFont.truetype(os.path.expanduser('~')+r'/.fonts/ufonts.com_tw-cen-mt.ttf',30).getsize('MINH')[1]+440),f'''"Tell me I'll forget, show me and I may remember,\ninvolve me and I'll understand."\n{"-Chinese Proverb":>90}''',font=ImageFont.truetype(os.path.expanduser('~')+r'/.fonts/timesnewromanbold.ttf',28),spacing=8,fill=(9,21,90,255))
  draw.text((img.width//4,(img.height*8.9)//10),'Minh, Inc.',font=ImageFont.truetype(os.path.expanduser('~')+r'/.fonts/ufonts.com_tw-cen-mt.ttf',40),anchor='mt',fill=(0,0,0,255))
  draw.text((img.width//4,(img.height*8.9)//10+ImageFont.truetype(os.path.expanduser('~')+r'/.fonts/ufonts.com_tw-cen-mt.ttf',40).getsize('Minh')[1]),r'https://youtube.com/@minhinc',font=ImageFont.truetype(os.path.expanduser('~')+r'/.fonts/urwbookman-light.otf',25),anchor='mt',fill=(0,0,0,255))
  img.save('advance-'+self.tech+'-slides_bottom.png')
  self.htmlstr+=f'''<img src="http://{Util.webpageurl()}/image/advance-{self.tech+'-slides_bottom.png'}" style="display:block;margin:auto"/>'''
  self.placepagebreak(side='bottom')
  Util.push(f'advance-{self.tech}-slides_bottom.png',dir='image',push=True)

  open('../css/tmp.css','w').write('div.pg pre.slidecontent, div.pg pre.code,div.pg pre.codeb,  div.pg pre.codec {display:block;}')
  disclaimer2=re.sub(r'.*(<div class="pg".*?Intentionally.*)$',r'\1',self.htmlstr,flags=re.DOTALL)
  content=[re.sub(r'^.*(<div class="pg".*)$',r'\1',re.split(re.escape(x),self.htmlstr)[0],flags=re.DOTALL)+re.sub(r'^(.*)<div class="pg".*$',r'\1',x,flags=re.DOTALL) for x in re.findall(r'(name="chap\d+".*?)(?=name="chap\d+"|Intentionally Left Blank)',self.htmlstr,flags=re.I|re.DOTALL)]

  #destop Firefox and Chrome
  for count in range(len(content)):
   daycount=re.sub(r'.*?name="chap(\d+)".*$',r'\1',content[count],flags=re.DOTALL)
   with open(f"logdir/advance-{self.tech}-slides{'-chap'+daycount if count else ''}{'_f' if str(self.browser).lower()=='firefox' else ''}.txt",'w') as file:
    print(f'writing to file firefox {file.name=} {daycount=} {count=}')
#    filedatadesktop=re.sub(r'-slides.php\?chap='+self.day[0][0][0]+'#',r'-slides.php#',re.sub(r'(?P<id>style=")?(?P<id2>.*?href="#chap.*?")',lambda m:(m.group('id')+'background-color:#f38502;' if m.group('id') and re.search('"#chap'+daycount+'"',m.group('id2')) else m.group('id') if m.group('id') else '')+re.sub(r'#chap(\d+)(_\d+)?',r'http://'+Util.webpageurl()+r'/training/'+self.tech+r'/advance-'+self.tech+r'-slides.php?chap='+r'\1'+'#chap'+r'\1\2',m.group('id2')),re.split(re.escape(content[0]),self.htmlstr)[0]+'\n'+content[count],flags=re.M),flags=re.M)+disclaimer2
    filedatadesktop=re.sub(r'-slides.php\?chap='+self.day[0][0][0]+'#',r'-slides.php#',re.sub(r'(?P<id>.*?)(?P<id2>href="#chap.*?")',lambda m:(re.sub(r'(style=")',r'\1'+'background-color:#f38502;',m.group('id')) if re.search('"#chap'+daycount+'"',m.group('id2')) else m.group('id'))+re.sub(r'#chap(\d+)(_\d+)?',r'http://'+Util.webpageurl()+r'/training/'+self.tech+r'/advance-'+self.tech+r'-slides.php?chap='+r'\1'+'#chap'+r'\1\2',m.group('id2')),re.split(re.escape(content[0]),self.htmlstr)[0]+'\n'+content[count],flags=re.M),flags=re.M)+disclaimer2
    file.write(filedatadesktop)
   #Mobile Chrome
   if not str(self.browser).lower()=='firefox':
    with open(f"logdir/advance-{self.tech}-slides{'-chap'+daycount+'_m' if count else '_m'}.txt",'w') as file:
     print(f'writing to file firefox {file.name=} {daycount=} {count=}')
     file.write(re.sub('(<pre .*?)font-size:\d+pt(.*?Intentionally.*)$',r'\1\2',re.sub('(?P<id><div class="dayheader".*?style="margin-top\s*:\s*)(?P<id2>\d+)',lambda m:m.group('id')+('40' if int(m.group('id2'))>40 else m.group('id2')),re.sub(r'(<div class="pg".*?)style="height:.*?"(.*)$',r'\1\2',re.sub(r'(<img .*?)style=".*?"(.*)$',r'\1'+'class="img" '+r'\2',re.sub(r'<pre.*?class="ftr.*','',re.sub(r'(<div class="(?:dayheaderleft|dayheaderright)".*?)style=".*?"(.*)',r'\1'+' style="margin-top:20px;margin-bottom:40px;"'+r'\2',re.sub(r'(<div class="slideheader".*?)style=".*?"(.*)$',r'\1'+'style="margin-top:20px;margin-bottom:10px;"'+r'\2',re.sub(r'(<(?:pre|div) class="(?:code.*?|slidecontent)".*?)style=".*?"(.*)$',r'\1\2',filedatadesktop,flags=re.M),flags=re.M),flags=re.M),flags=re.M),flags=re.M),flags=re.M),flags=re.M),flags=re.M))

  #Desktop single file
  print(f"--writing to {self.tech}_pdf{'_f' if str(self.browser).lower()=='firefox' else ''}.html")
  open(f"logdir/{self.tech}_pdf{'_f' if str(self.browser).lower()=='firefox' else ''}.html",'w').write(re.sub(r'(\n</head>)',r'\n<link rel="stylesheet" type="text/css" href="../css/tmp.css" media="all"/>'+r'\1',self.fileheader[0],flags=re.DOTALL)+self.htmlstr+self.fileheader[1])

  #PDF file generation
  open('logdir/tmp.html','w').write(re.sub(r'http://minhinc.42web.io/image/',r'file://'+os.path.expanduser('~')+r'/tmp/MISC/image/',re.sub(r'[.][.]/css/',r'../../css/',re.sub(r'(\n</head>)',r'\n<link rel="stylesheet" type="text/css" href="../css/tmp.css" media="all"/>'+r'\1',self.fileheader[0],flags=re.DOTALL),flags=re.DOTALL)+self.htmlstr+self.fileheader[1],flags=re.DOTALL))
  print(f'creating pdf ... advance-{self.tech}-slides.pdf')
  os.system(f'wkhtmltopdf --enable-local-file-access logdir/tmp.html logdir/advance-{self.tech}-slides.pdf')

trainingformat()
