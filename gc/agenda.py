import os,sys;sys.path.append(os.path.expanduser('~')+r'/tmp')
import random
import re
from PIL import Image,ImageDraw,ImageFont
import datetime
import math
from selenium import webdriver
import PyPDF2
import MISC.utillib.requestm as requestm
from MISC.utillib.databasem import databasec
from MISC.utillib.util import Util
from MISC.ffmpeg.libm import libc
from MISC.extra.debugwrite import print
if len(sys.argv)<4:
 print(''' ---usage---
 Note:-[Ll]->lab [Tt]->Theory
 agenda.py --tech [c|cpp|gl|li|ldd|py|qt|qml|ml] --company '' "(((1,2,3),(4,L)),((4 5 6),(L,qml1)),((2,),(4T 3 L)))"
 =agenda.py --tech [c|cpp|gl|li|ldd|py|qt|qml] --company '' "(((1,2,3),(4,L)),((4 5 6),(L,qml1)),((2,),(4T 3 L)))"
 agenda.py --tech qt --company '' "(((1,2,3),(4,L)),((4,5,6),(L,)))"
 agenda.py --tech qt --company 'ABC Company' "(1,2,4,5,3)"
 ---- tags ----
 <m> - image - <m>http://minhinc.42web.io/image/logo.png</m>  OR logot.png for href images
   <m> can be inline also
  <mb> - bigimage for article format (would come on next page)
 <c> - code
  <cb> - code with gray background
  <cc> - shortcode
  <cs> - veryshortcode multicolumn, for article format would appear on next page
 <a> - abstract in italics
 <n> - notes
 <d[1..]> - bullet dot size 1 or 2 or ..
 <[rgl]> - red/green/blue font
  <[R|G|L]> - bold red/green/blue font''')
 exit(-1)

class format:
 DELIMITER='!ABS SBA!'
 #PH -> Page Height Maximum TM->Top Margin
# PH,TM=1402,20
 TM=20
 ADIMAGEHEIGHT=200
 TESTFILE='test.html'
 TESTPDF='test.pdf'
 LEFTBLANK='Intentionally Left Blank'
 def __init__(self):
  super(format,self).__init__()
  self.libi=libc()
  self.tech,self.company=Util.getarg('--tech',2).lower(),Util.getarg('--company',2)
  if Util.usertagdescripancy(self.tech):
   print(f'-------- USER TAG DESCRIPANCY TAG FOUND --------')
   print(f'------------------------------------------------')
   sys.exit(-1)
  self.day=[]
  self.day.extend([[[x for x in re.split(r'\s+',y) if x] for y in re.split(':',i)] for i in sys.argv[1:]])
  self.inlinehtmltaglist=Util.customtag
  self.inlinehtmltag=dict((('<i>',r'<span style="font-style:Italic">'),(r'<d(\d+)?>',r'<span style="background-color:#000" class="dot\1"></span>'),('<r>',r'<span style="color:#ff0000;">'),('<g>',r'<span style="color:#004000;">'),('<l>',r'<span style="color:#0055cf;">'),('<R>',r'<span style="color:#ff0000;font-weight:bold">'),(r'<G>',r'<span style="color:#004000;font-weight:bold">'),(r'<L>',r'<span style="color:#0055cf;font-weight:bold">'),(r'</[irglRGL]>',r'</span>'),(r'<n>',r'<pre class="note">'),(r'</n>',r'</pre>'),(r'<c>',r'<pre class="codei">'),(r'</c.?>',r'</pre>'),(r'<cc>',r'<pre class="codeci">'),('<(a|abbr|acronym|address|applet|area|article|aside|audio|b|base|basefont|bb|bdo|big|blockquote|body|br|button|canvas|caption|center|cite|code|col|colgroup|command|datagrid|datalist|dd|del|details|dfn|dialog|dir|div|dl|dt|em|embed|eventsource|fieldset|figcaption|figure|font|footer|form|frame|frameset|h[1-6]?|head|header|hgroup|hr|html|i|iframe|img|input|ins|isindex|kbd|keygen|label|legend|li|link|map|mark|menu|meta|meter|nav|noframes|noscript|object|ol|optgroup|option|output|p|param|pre|progress|q|rp|rt|ruby|s|samp|script|section|select|small|source|span|strike|strong|style|sub|sup|table|tbody|td|textarea|tfoot|th|thead|time|title|tr|track|tt|u|ul|var|video|wbr)>','EMPTY')))
  self.inlinehtmltag_nofrequentlyused=dict((('<(abbr|acronym|address|applet|area|article|aside|audio|base|basefont|bb|bdo|big|blockquote|button|canvas|caption|center|cite|col|colgroup|command|datagrid|datalist|dd|del|details|dfn|dialog|dir|eventsource|fieldset|figcaption|figure|footer|hgroup|input|ins|isindex|kbd|keygen|label|legend|link|map|mark|menu|meta|meter|nav|noframes|noscript|object|optgroup|option|output|param|progress|q|rp|rt|ruby|s|samp|script|section|select|small|source|strike|strong|style|sub|sup|tfoot|thead|time|track|tt|var|wbr)>','EMPTY'),))
  self.PAGEWIDTH=int(re.sub(r'^.*body\s*{\s*width\s*:\s*(\d+).*$',r'\1',open(r'../css/main.css').read(),flags=re.I|re.DOTALL))
  self.htmlstr=''
  self.db=databasec(False)
  self.driver={'firefox':None,'chrome':None}
  self.pagenumber=0
  print(f'<=>format.__init__ self.tech={self.tech} self.company={self.company} self.day={self.day} sys.argv={sys.argv}')
  self.fileheader=(f'<html>\n<head>\n<title>Minh, Inc. Software development and Outsourcing| {self.tech} training Bangalore India</title>\n<META http-equiv="Content-Type" content="text/html; charset=UTF-8">\n<link rel="stylesheet" type="text/css" href="../css/main.css" media="all"/>\n<link rel="stylesheet" type="text/css" href="../css/agenda.css" media="all"/>\n</head>\n<body>\n','\n</body>\n</html>')
  os.mkdir(r'logdir') if not os.path.exists('logdir') else None
  self.PH=int(open('logdir/ph.txt').read()) if os.path.exists('logdir/ph.txt') else 1390
  Image.new('RGBA',(self.PAGEWIDTH//2,self.PH),color=(255,0,0,255)).save('logdir/ding.png')
  while self.lineheightnhtml(f'<img src="logdir/ding.png" style="height:{self.PH}px;"/>')[2]>=2:
   self.PH-=1
  while self.lineheightnhtml(f'<img src="logdir/ding.png" style="height:{self.PH}px;"/>')[2]==1:
   self.PH+=1
  self.PH-=1
  open('logdir/ph.txt','w').write(f'{self.PH}')
  self.preparedisclaimer()
  self.prepareheader()
  self.preparecontent()
  self.preparedisclaimer2()
  self.prepareoutfile()
#  os.remove(self.TESTFILE)
  self.driver['firefox'].close()
  self.driver['chrome'].close()

 def placepagebreak(self,side,topicnumber=0,arrow=True):
  '''\
  pagebreak - top or/and bottom, if header == None no break for mobile
  side='top'/'bottom'/'all'
  topicnumber - self.day[k][j][i]
  arrow -> 'arrow'/'noarrow' - no top arrow button icon
  '''
  print(f'><placepagebreak {side=} {topicnumber=} {arrow=}')
  tmpstr=''
  if side in ['bottom','all']:
   self.pagenumber=self.pagenumber+1 if arrow else self.pagenumber
#   tmpstr+=(f'\n <pre class="ftr">&copy {Util.webpageurl()}</pre><a href="#main{topicnumber}" class="pn">{"p"+str(self.pagenumber)}</a>' if arrow else '')+'\n</div>'
   tmpstr+=(f'\n <a class="ftr" style="display:block" href="{Util.webpageurl(http=True)}">&copy {Util.webpageurl()}</a><a class="pn" href="#main{topicnumber}">p{self.pagenumber}</a>' if arrow else '')+'\n</div>'
  if side in ['top','all']:
#   tmpstr+='\n'+rf'<div class="pg" style="height:{self.PH}px;"><div class="topcolor" style="height:{self.TM}px;"></div>'
   tmpstr+='\n'+rf'<div class="pg" style="height:{self.PH}px;"><div class="topcolor" style="height:{self.TM}px;"></div>'
  self.htmlstr+=tmpstr if arrow else ''
  return tmpstr

 def lineheightnhtml(self,htmlcode,makepdf=True,driver='chrome'):
  '''\
  <-  ({'height':,'width':} convertedhtmlcode)
  ->
  htmlcode - htmlcode for conversion i.e. <pre class="articlecontentmaintopic">Descriptor in Python</pre>
    latter it would be fed to browser as <div style="overflow:auto">htmlcode</div>
    cssselector as div.pg
  '''
  elementdata=None
  print(f'><lineheightnhtml htmlcode={htmlcode}')
#  covertag='<div class="pg" style="overflow:auto;">'
  htmlcode='\n'.join([x if x else ' ' for x in htmlcode.split('\n')])
  if not self.driver[driver]:
   if driver=='firefox':
    self.driver[driver]=webdriver.Firefox(executable_path=os.path.expanduser('~')+r'/nottodelete/geckodriver')
   else:
    self.driver[driver]=webdriver.Chrome()
   self.driver[driver].maximize_window()
   with open(self.TESTFILE,'w') as file:
    file.write(r'')
   self.driver[driver].get(r'file:///'+re.sub(r'/?$','',os.getcwd())+r'/'+self.TESTFILE)
  htmlcode=eval(','.join(r"re.sub(r'"+x+"',r'"+self.inlinehtmltag[x]+"' if '"+self.inlinehtmltag[x]+"'!='EMPTY' else '<'+r'\\1'+'>'" for x in self.inlinehtmltag)+r",re.sub(r'(?P<id>\\?&lt;/?)(?P<id2>\w+)(?P<id3>((?!&lt;).)*?&gt;)',lambda m:re.sub(r'&lt;','<',m.group('id'))+m.group('id2')+re.sub(r'&gt;','>',m.group('id3')) if not re.search(r'^\\',m.group('id')) and [x for x in self.inlinehtmltag if re.search(x,'<'+m.group('id2')+'>',flags=re.I)] else re.sub(r'\\&lt;','&lt;',m.group('id'))+m.group('id2')+m.group('id3'),re.sub(r'<',r'&lt;',re.sub(r'>',r'&gt;',htmlcode,flags=re.M),flags=re.M),flags=re.M)"+',flags=re.I|re.M)'*len(self.inlinehtmltag),{"self":self,"re":re},{"htmlcode":htmlcode})
#  htmlcode=re.sub(r'&lt;m&gt;(?P<id>.*?)&lt;/m&gt;',lambda m:r'<a href="'+re.sub(r'^.*(http.*)',r'\1',m.group('id'))+r'">'+re.sub(r'^(.*)(http.*)',r'\1' or r'\2',m.group('id'))+r'</a>',htmlcode,flags=re.M)
  htmlcode=re.sub(r'&lt;m&gt;(?P<id>.*?)&lt;/m&gt;',lambda m:r'<a href="'+re.sub(r'^.*(http.*)',r'\1',m.group('id'))+r'">'+re.sub(r'^(?P<id2>.*)(?P<id3>http.*)',lambda m:m.group('id2') or m.group('id3'),m.group('id'))+r'</a>',htmlcode,flags=re.M)
  with open(self.TESTFILE,'w') as file:
   file.write(self.fileheader[0]+'<div class="pg" style="overflow:auto;">'+htmlcode+'</div>'+self.fileheader[1])
  self.driver[driver].refresh()
  elementdata=self.driver[driver].find_element_by_css_selector('div.pg')
  height=elementdata.size['height']+int(re.sub(r'^\s*(\d+).*$',r'\1',elementdata.value_of_css_property('margin-top')))+int(re.sub(r'^\s*(\d+).*$',r'\1',elementdata.value_of_css_property('margin-bottom')))
  os.system('wkhtmltopdf --enable-local-file-access '+self.TESTFILE+' '+self.TESTPDF+' > /dev/null 2>&1') if makepdf and height>self.PH*0.75 else None
  print(f'''<>lineheightnhtml {elementdata.size=} {elementdata.value_of_css_property('margin-top')=} {elementdata.value_of_css_property('margin-bottom')=} {open(self.TESTFILE).read()=} numpages={PyPDF2.PdfFileReader(open(self.TESTPDF,'rb')).numPages if makepdf and height>self.PH*0.75 else 1}''')
  return ({'height':elementdata.size['height']+int(re.sub(r'^\s*(\d+).*$',r'\1',elementdata.value_of_css_property('margin-top')))+int(re.sub(r'^\s*(\d+).*$',r'\1',elementdata.value_of_css_property('margin-bottom'))),'width':elementdata.size['width']},htmlcode,PyPDF2.PdfFileReader(open(self.TESTPDF,'rb')).numPages if makepdf and height>self.PH*0.75 else 1)
 
 def searchtag(self,tag,cnt,getcode=False,getall=False,includetag=False):
#  return re.search(r'^[ \t]*<'+tag+r'>[ \t]*\n',cnt,flags=re.I|re.DOTALL)
  reg=r'(?:^|^\n[ \t]*)<'+tag+r'>[ \t]*\n(.*?)\n[ \t]*</'+tag+r'>(?=(?:[ \t]*\n|$))'
  reg2=r'(?:^|^\n[ \t]*)(<'+tag+r'>[ \t]*\n.*?\n[ \t]*</'+tag+r'>)(?=(?:[ \t]*\n|$))'
#  print(f'><format.searchtag {tag=} {cnt=} {getcode=} {getall=} {includetag=}')
  if not getcode and not getall:
   return re.search(reg,cnt,flags=re.DOTALL)
  elif getcode and not getall:
   if tag:
    return re.findall((reg if not includetag else reg2)+r'(.*)',cnt,flags=re.DOTALL)[0]
   else:
    return re.findall(r'(?:^\n?)(.*?)(?=\n(?:'+'|'.join(self.inlinehtmltaglist)+')|$)(.*)',cnt,flags=re.DOTALL)[0]
  elif getall:
   return re.findall(re.sub('|\^','',reg if not includetag else reg2),cnt,flags=re.DOTALL)

 '''
 def getcodecnt(self,tag,cnt):
#  print(f'><getcodecnt {tag=} {cnt=}')
  if tag:
   return re.split(self.DELIMITER,re.sub(r'^\s*<'+tag+r'>[ \t]*\n?(?P<id>.*?)\n?[ \t]*</'+tag+r'>(?P<id2>.*)$',lambda m:m.group('id')+self.DELIMITER+(re.sub(r'^[ \t]*\n','',m.group('id2'),flags=re.DOTALL) if m.group('id2') else ''),cnt,flags=re.DOTALL))
  else:
   if re.search(r'\n('+'|'.join(r'\s*<'+x+r'>[ \t]*\n.*\n?[ \t]*</'+x+'>' for x in ['h','a','c','cb','cc','cs'])+r'|[ \t]*<m>[^\n]+</m>)',cnt,flags=re.DOTALL):
    return re.split(self.DELIMITER,re.sub(r'^(.*?)\n((?:'+'|'.join(r'[ \t]*<'+x+'>[ \t]*\n.*\n?[ \t]*</'+x+'>' for x in ['h','a','c','cb','cc','cs'])+r'|[ \t]*<m>[^\n]+</m>).*)$',r'\1'+self.DELIMITER+r'\2',cnt,flags=re.DOTALL))
   else:
    return cnt,''

 '''
 def adsense(self,height=None,width=None,imageurl=None):
  basetech=youtube=None
  if not hasattr(format.adsense,'tech'):
   format.adsense.tech=[]
  if not imageurl:
   format.adsense.tech=[x[0] for x in self.db.search2('tech','name','name','R','.*',mode='get') if x[0]!=self.tech and os.path.exists(os.path.expanduser('~')+r'/tmp/imageglobe/image/'+x[0]+'traininglogo.gif')] if not format.adsense.tech else format.adsense.tech
   basetech=format.adsense.tech[random.randint(0,len(format.adsense.tech)-1)]
   format.adsense.tech[format.adsense.tech.index(basetech):format.adsense.tech.index(basetech)+1]=[]
   imageurl=f'{basetech}traininglogo.gif'
  else:
   youtube=True if re.search('youtube',imageurl,flags=re.I) else False
   imageurl=re.sub('.*/(.*)$',r'\1',imageurl)
  img=Image.open(os.path.expanduser('~')+r'/tmp/imageglobe/image/'+imageurl)
  if width:
   widthl=width if img.width>=width else img.width
   heightl=(widthl*img.height)//img.width
  if height:
   heightl=height if img.height >= height else img.height
   widthl=(heightl*img.width)//img.height
   if widthl>self.PAGEWIDTH:
    widthl=self.PAGEWIDTH
    heightl=(widthl*img.height)//img.width
  print(f'<=>adsense adsense {(width,height)=} {(widthl,heightl)=} {(youtube,imageurl)=} {format.adsense.tech=}')
  return '\n<div class="clr"></div>'+f'<a style="display:block" href="'+(f'https://youtube.com/watch?v={imageurl}' if youtube else Util.webpageurl(http=True)+"/image/"+imageurl if not basetech else Util.webpageurl(http=True)+"/training/"+basetech)+f'"><img style="height:{heightl}px;margin:{((height and height or heightl)-heightl)//2}px {(self.PAGEWIDTH-widthl)//2}px" src="http://{Util.webpageurl()}/image/{imageurl}" /></a>'+'<div class="clr"></div>\n'

class trainingformat(format):
 def __init__(self):
  super(trainingformat,self).__init__()
 def prepareheader(self):
  HH=40;#headerheight
#  CHH=40;HHH=50;CHG=125;HCG=40;CCG=80#contentheaderheight,contentheadergap,headercontentgap,contentcontentgap
  CHH=40;HHH=50;CHG=155;HCG=40;CCG=100#contentheaderheight,contentheadergap,headercontentgap,contentcontentgap
  tmpstr=''
  labstr=[]
  tech=self.tech
  day=self.day.copy()
#  self.placepagebreak(side='top',topoffset=2*self.TM)
  self.placepagebreak(side='top')
  self.htmlstr+=""" <pre class="title">%s</pre>
 <pre class="subtitle">%s</pre>
 <pre class="company">%s</pre>
""" % (self.db.search2(self.tech,'content','name','=','title',mode='get')[0][0],self.db.search2(self.tech,'content','name','=','subtitle',mode='get')[0][0],'('+self.company+')' if self.company else '')
  self.htmlstr+="<div style=\"width:100%;height:100px;\"></div>"
  for data in self.db.search2(self.tech,'*','name','ROid','^h_',mode='get'):
   if not re.search(r'h_hr',data[1]):
    tmpstr=f"""
  <div class="headerleft"> <pre>{data[1]}</pre></div>
  <div class="headerright"> <pre>"""+re.sub(r'\n','<br>',data[3],flags=re.DOTALL)+"""</pre>  </div>\n <div class="clr"></div>"""
   else:
    tmpstr=''' <hr>
'''
   self.htmlstr+=re.sub(r'^(?P<id>.*?<div.*?class="header(?:left|right)")(?P<id2>.*)$',lambda m:m.group('id')+' style="height:'+str(self.lineheightnhtml(tmpstr)[0]['height'])+'px;"'+m.group('id2'),tmpstr,flags=re.M)
  tmpstr=int(max(0,(self.PH*0.70-self.lineheightnhtml(self.getpage())[0]['height'])//len(re.findall(r'<div\s+class="headerleft"',self.getpage(),flags=re.M))))
  self.htmlstr=re.sub(r'(?P<id><div\s+class="header(?:left|right)".*?style="height:)(?P<id2>\d+)(?P<id3>.*)$',lambda m:m.group('id')+str(eval(m.group('id2'))+tmpstr)+m.group('id3'),self.htmlstr,flags=re.M)
  self.htmlstr=re.sub(r'(class="title")',r'\1'+f' style="margin-top:{int((self.PH-self.lineheightnhtml(self.getpage())[0]["height"])*0.3)}"',self.htmlstr,flags=re.DOTALL)
  self.placepagebreak('all')
  for count,data in enumerate(self.db.search2(self.tech,'*','name','ROid','^h2_',mode='get')):
   tmpstr=f"""
 <div class="header2" style="margin-top:{0 if not count else self.PH//10}px;margin-bottom:{0 if not count else self.PH//10}px;">
  <pre class="header" style="line-height:{HH}px">{re.sub(r'^h2_','',data[1])}</pre>
  <pre class="content" >{data[3]}</pre>
 </div>"""
   self.htmlstr+=tmpstr
  
  tmpstr='';
  for k in range(len(day)):#each day
   for i in range(len(day[k])):#morning and evening
    for j in range(len(day[k][i])):#each topic
     if re.search(r'\d+',day[k][i][j]):
      if re.search(r'^[a-z]+\d+',day[k][i][j],flags=re.I):
       tech=re.sub(r'^([a-z]+)\d+.*$',r'\1',day[k][i][j])
       day[k][i][j]=re.sub(r'[a-z]+(\d+.*)',r'\1',day[k][i][j])
      if re.search(r'\d+[Tt]$',day[k][i][j],flags=re.I):
       day[k][i][j]=re.sub(r'^(\d+).*',r'\1',day[k][i][j])
      else:#elif  re.search(r'\d+(?![Tt])$',day[k][i][j],flags=re.I):
       labstr.extend([(x,day[k][i][j],count) for count,x in enumerate(self.searchtag('h[or]',self.db.search2(tech,'lab','id','=',day[k][i][j],mode='get')[0][0],getall=True,includetag=True))])
     if j==0:
      tmpstr+=f"""\n <div class="dayheader" style="margin-top:{str(CHG)+'YYY'}px;height:{HHH}px"><pre>Day {k+1} {"Afternoon" if i!=0 else "Morning"}</pre><hr></div>"""
     tmpstr+="""\n  <div class=%s style="margin-top:%spx;">
   <div class="%s" style="height:%spx">%s class="%s" style="padding-top:%spx;%spx">%s%s  </div>
    <ul class="daycontent" style="padding-top:10px;"> """ % ('"dayheaderright"' if re.search(r'dayheaderleft',tmpstr,flags=re.I) else '"dayheaderleft"',HCG if re.search(r'YYY',tmpstr,flags=re.I) else str(CCG)+'XXX','dayheaderheaderlab' if re.search(r'^[Ll]$',day[k][i][j]) else 'dayheaderheadertechchange' if not tech==self.tech else 'dayheaderheader',CHH,'<pre' if re.search(r'^[Ll]$',day[k][i][j]) else "<a name=\"main"+day[k][i][j]+"\" href=\"#chap"+str(day[k][i][j])+"\"",'dayheader',CHH/4 if not re.search(r'^[Ll]$',day[k][i][j]) else 0,'height:'+str(CHH) if not re.search(r'^[Ll]$',day[k][i][j]) else 'line-height:'+str(CHH),'     Lab' if re.search(r'^[Ll]$',day[k][i][j]) else '  Lecture - '+self.db.search2(tech,'name','id','=',day[k][i][j],mode='get')[0][0]+('    ( '+tech+' )' if not tech==self.tech else ''),'</pre>' if re.search(r'^[Ll]$',day[k][i][j]) else '</a>')
     for count,header in enumerate([(re.sub(r'^.*?<h(.*?)>.*',r'\1',x,flags=re.DOTALL),re.sub(r'^.*?<h.*?>.*?\n(.*?)\n</h.*$',r'\1',x,flags=re.DOTALL)) for x in ([x[0] for x in labstr] if re.search(r'^[Ll]$',day[k][i][j]) else self.searchtag('h',self.db.search2(tech,'content','id','=',day[k][i][j],mode='get')[0][0],getall=True,includetag=True))]):
#      print(f'TEST {count=} {labstr=} {labcount=} {day[k][i][j]=}')
      tmpstr+="""\n   <li>%s%s%s</li>""" % (f'''<a {'class="'+header[0]+'"' if header[0] else ""}'''+(f''' name="lab{labstr[count][1]}_{labstr[count][2]}" href="#chaplab{labstr[count][1]}_{labstr[count][2]}"''' if re.search(r'^[Ll]$',day[k][i][j]) else f''' name="main{day[k][i][j]}_{count}" href="#chap{day[k][i][j]}_{count}"''')+'>',f'<pre>{header[1]}</pre>','</a>')
     tmpstr+='''\n  </ul>
  </div>
 '''
#     print(f'TEST {(k,i,j)=} {tmpstr=}')
     labstr.clear() if re.search(r'^[Ll]$',day[k][i][j]) else None
     def fixextragap(self,factor=1.0):
      tmphtmlstr=self.htmlstr
      headermorningcount=len(re.findall(r'YYY.*?Morning',self.htmlstr,flags=re.I))
      headerafternooncount=len(re.findall(r'YYY.*?Afternoon',self.htmlstr,flags=re.I))
      daycount=len(re.findall(r'dayheaderleft.*?XXX',self.htmlstr,flags=re.I))
      basevalue=int(factor*(self.PH-self.lineheightnhtml(re.sub(r'(YYY|XXX)','',self.getpage(),flags=re.DOTALL))[0]['height'])/(6*headermorningcount+2*headerafternooncount+daycount)) if headermorningcount+headerafternooncount+daycount>0 else 0
#      print(f'TEST {(headermorningcount,headerafternooncount,daycount)=} {basevalue=} {(k,i,j)=}')
      if headermorningcount+headerafternooncount+daycount:
       self.htmlstr=re.sub(r'(<div class="dayheader".*?YYY.*?Morning)',self.adsense(6*basevalue+CHG)+r'\1',self.htmlstr,flags=re.M) if headermorningcount and (6*basevalue+CHG)>= self.ADIMAGEHEIGHT else self.htmlstr
       self.htmlstr=re.sub(r'(<div class="dayheader".*?YYY.*?Afternoon)',self.adsense(2*basevalue+CHG)+r'\1',self.htmlstr,flags=re.M) if headerafternooncount and (2*basevalue+CHG)>= self.ADIMAGEHEIGHT else self.htmlstr
       self.htmlstr=re.sub(r'(<div class="dayheaderleft".*?XXX)',self.adsense(basevalue+CCG)+r'\1',self.htmlstr,flags=re.M) if daycount and (basevalue+CCG)>= self.ADIMAGEHEIGHT else self.htmlstr
       self.htmlstr=re.sub(r'(?P<id>\d+)YYY(?P<id1>.*?Morning)',lambda m: str(int(m.group('id'))+6*basevalue if (6*basevalue+CHG)<self.ADIMAGEHEIGHT else 0)+m.group('id1'),self.htmlstr,flags=re.I)
       self.htmlstr=re.sub(r'(?P<id>\d+)YYY(?P<id1>.*?Afternoon)',lambda m: str(int(m.group('id'))+2*basevalue if (2*basevalue+CHG)<self.ADIMAGEHEIGHT else 0)+m.group('id1'),self.htmlstr,flags=re.I)
       self.htmlstr=re.sub(r'(?P<id>\d+)XXX',lambda m: str(int(m.group('id'))+basevalue if (basevalue+CCG)<self.ADIMAGEHEIGHT else 0),self.htmlstr,flags=re.I)
      while self.lineheightnhtml(self.getpage())[2]>=2:
       self.htmlstr=tmphtmlstr
       fixextragap(self,factor=factor-0.1)
#     if (re.search(r'class="dayheaderright"',tmpstr,flags=re.DOTALL) or j==(len(day[k][i])-1)) and self.lineheightnhtml(re.sub(r'(YYY|XXX)','',self.getpage(tmpstr),flags=re.DOTALL))[0]['height']>(self.PH-self.PDFOFST):
     if (re.search(r'class="dayheaderright"',tmpstr,flags=re.DOTALL) or j==(len(day[k][i])-1)) and self.lineheightnhtml(re.sub(r'(YYY|XXX)','',self.getpage(tmpstr),flags=re.DOTALL))[2]>=2:
      fixextragap(self)
      self.placepagebreak('all',day[k][i][j])
      self.htmlstr+='\n'+re.sub(r'\d+(YYY|XXX)',r'0',tmpstr,flags=re.I)
      tmpstr=''
     if k==len(day)-1 and i==len(day[k])-1 and j==len(day[k][i])-1:
      self.htmlstr+=tmpstr
      tmpstr=''
      fixextragap(self)
#      self.htmlstr+=self.adsense(self.PH-self.lineheightnhtml(self.getpage())[0]['height']) if (self.PH-self.lineheightnhtml(self.getpage())[0]['height']) >=self.ADIMAGEHEIGHT else ''
      self.htmlstr+=self.adjustimage(self.PH-self.lineheightnhtml(self.getpage())[0]['height']) if (self.PH-self.lineheightnhtml(self.getpage())[0]['height']) >=self.ADIMAGEHEIGHT else ''
      self.placepagebreak('bottom',day[k][i][j])
     if (re.search(r'class="dayheaderright"',tmpstr,flags=re.DOTALL) or j==(len(day[k][i])-1)):
      self.htmlstr+=tmpstr
      tmpstr=''
#  print(f'self.htmlstr={self.htmlstr}')

 '''
 def getheadertag(self,data):
  return re.findall(r'(?:^|\n[ \t]*)<h[yor]?>[ \t]*\n.*?</h>(?=(?:[ \t]*\n|$))',data,flags=re.DOTALL)
 '''
 def adjustimage(self,height):
  count=0
  while(self.lineheightnhtml(self.getpage()+self.adsense(height=int(height-math.sqrt(height)*count)))[2]>=2):
   count+=1
  return self.adsense(int(height-math.sqrt(height)*count))
 def preparedisclaimer(self):
  self.placepagebreak(side='top')
  img=Image.open(os.path.expanduser('~')+r'/tmp/imageglobe/resource/booktitlepage.png').convert('RGBA')
  img=img.resize((((self.PH-self.TM)*img.width)//img.height,self.PH-self.TM))
  self.libi.system(r'python3 tex.py "'+self.db.search2('tech','content','name','=',self.tech,mode='get')[0][0].title()+r'" 1')
  img2=Image.open(r'logdir/tex_'+re.sub(r'[\s/]+','',self.db.search2('tech','content','name','=',self.tech,mode='get')[0][0].lower())+'.png').convert('RGBA')
  img.paste(img2,((img.width-img2.width)//2,(img.height-img2.height)//2),img2)
  draw=ImageDraw.Draw(img)
#  draw.text((img.width//2,img.height//18),self.db.search2('tech','content','name',self.tech)[0][0].title()+' Training',font=self.libi.getfont((self.db.search2('tech','content','name',self.tech)[0][0].title()+' Training',),0.8,os.path.expanduser('~')+r'/.fonts/urwbookman-light.otf',False,img.size),anchor='mt',fill=(6,21,90,255))
  draw.text((img.width//2,img.height//18),self.db.search2('tech','content','name','=',self.tech,mode='get')[0][0].title()+' Training',font=self.libi.getfont((self.db.search2('tech','content','name','=',self.tech,mode='get')[0][0].title()+' Training',),0.8,os.path.expanduser('~')+r'/.fonts/ufonts.com_tw-cen-mt.ttf',False,img.size),anchor='mt',fill=(0,60,0,255))
#  draw.text((img.width//2,img.height//18+self.libi.getfont((self.db.search2('tech','content','name',self.tech)[0][0].title()+' Training',),0.8,os.path.expanduser('~')+r'/.fonts/urwbookman-light.otf',False,img.size).getsize(self.tech.title()+' Training')[1]),'Essentials',font=self.libi.getfont((self.db.search2('tech','content','name',self.tech)[0][0].title()+' Training',),0.6,os.path.expanduser('~')+r'/.fonts/urwbookman-light.otf',False,img.size),anchor='mt',fill=(6,21,90,255))
  draw.text((img.width//2,img.height//18+self.libi.getfont((self.db.search2('tech','content','name','=',self.tech,mode='get')[0][0].title()+' Training',),0.8,os.path.expanduser('~')+r'/.fonts/ufonts.com_tw-cen-mt.ttf',False,img.size).getsize(self.tech.title()+' Training')[1]),'Essentials',font=self.libi.getfont((self.db.search2('tech','content','name','=',self.tech,mode='get')[0][0].title()+' Training',),0.6,os.path.expanduser('~')+r'/.fonts/urwbookman-light.otf',False,img.size),anchor='mt',fill=(0,60,0,255))
  draw.text((img.width//4,(img.height*8.9)//10),'Minh, Inc.',font=ImageFont.truetype(os.path.expanduser('~')+r'/.fonts/ufonts.com_tw-cen-mt.ttf',40),anchor='mt',fill=(0,0,0,255))
  draw.text((img.width//4,(img.height*8.9)//10+ImageFont.truetype(os.path.expanduser('~')+r'/.fonts/ufonts.com_tw-cen-mt.ttf',40).getsize('Minh')[1]),r'https://youtube.com/@minhinc',font=ImageFont.truetype(os.path.expanduser('~')+r'/.fonts/urwbookman-light.otf',25),anchor='mt',fill=(0,0,0,255))
  img.save('advance-'+self.tech+'-slides_front.png')
  self.htmlstr+=f'\n<img src="http://{Util.webpageurl()}/image/advance-{self.tech}-slides_front.png" style="display:block;margin:auto"/>'
  self.placepagebreak(side='all')
  self.htmlstr+=f'<img src="http://{Util.webpageurl()}/image/honeybee.png" style="width:{self.PAGEWIDTH//3}px;margin-top:100px;margin-left:{self.PAGEWIDTH//3}px;margin-bottom:400px;"/>'
  self.htmlstr+=fr"""<pre style="font-family:myliberationserif;font-size:12pt;width:80%;color:#222222;margin:auto">The {self.db.search2('tech','content','name','=',self.tech,mode='get')[0][0]} Training journal is published online by Minh, Inc. and is available at http://minhinc.42web.io/training/{self.tech}<br><br>For submission guildelines please visit http://minhinc.42.web.io. Enquiries should be addressed to tominhinc@gmail.com or WhatsApp +91 9483160610.<br><br>Copyright &copy Minh, Inc. Bangalore, India. Author(s) retain copyright and grant journal right of first publication with the work simultaneously licensed under a creative Commons Attribution License that allows others to share the work with an acknowledgement of the work’s authorship and initial publication in this journal. Author(s) are able to enter into separate, additional contractual agreements for the non–exclusive distribution of the journal’s published version of the work (e.g. post it to an institutional repository or publish it in a book), with an acknowledgement of its initial publication in this journal.</pre>"""
  self.placepagebreak(side='all')
  self.htmlstr+=fr"""<pre style="line-height:{self.TM*4}px;text-align:center;font-family:mytwcenmt;font-size:26pt;color:#222222">Acknowledgements</pre>"""
  self.placepagebreak(side='bottom')
  Util.push('advance-'+self.tech+'-slides_front.png',dir='image')

 def getpage(self,htmlcode=''):
  return re.sub(r'^.*<div class="pg".*?>(.*)$',r'\1',self.htmlstr+htmlcode,flags=re.DOTALL)

 def preparecontent(self,content='content'):
  cnt=code=tmpcode=""
  tmpvar1=tmpvar2=None
  tech=self.tech
  day=self.day.copy()
  subtopiccount=0
  fixheader=[]
  for k in range(len(day)):
   for i in range(len(day[k])):
    for j in [x for x in range(len(day[k][i])) if not re.search(r'^[Ll]$',day[k][i][x])]:
     if re.search(r'^\w+\d+[Tt]?$',day[k][i][j]):
      tech,day[k][i][j]=re.sub(r'^(\w+)\d+.*',r'\1',day[k][i][j]),re.sub(r'^.*?(\d+).*$',r'\1',day[k][i][j])
     cnt=self.db.search2(self.tech,content,'id','=',day[k][i][j],mode='get')[0][0]
     fixheader=self.searchtag('h[yor]?',cnt,getall=True,includetag=True)
     print("fixheader><%s<>" % fixheader)
     self.placepagebreak(side='top')
     while cnt:
#      print(f'TEST {(k,i,j)=} {day=} {cnt=}')
      if self.searchtag('h[yor]?',cnt):
       print("<=><h>")
       code,cnt=self.searchtag('h[yor]?',cnt,getcode=True)
       if content=='lab' and not subtopiccount or content=='content':
        tmpcode="""\n <div class="slideheader">
  %s<pre class="day">%s</pre></a>
  %s<pre class="topic">%s</pre>%s
  %s """ % (f'<a name="{"chap" if content=="content" else "chaplab"}{day[k][i][j]}{"_"+str(subtopiccount) if subtopiccount else ""}" href="#{"main" if content=="content" else "lab"}{day[k][i][j]}{"_"+str(subtopiccount) if subtopiccount else ""}">','Day '+str(k+1)+' '+('Afternoon' if i!=0 else 'Morning'),"<h1>" if subtopiccount==0 else '','  '+str(day[k][i][j])+'. '+self.db.search2(self.tech,'name','id','=',day[k][i][j],mode='get')[0][0],"</h1>" if subtopiccount==0 else '','</div><div class="clr"></div>' if content=='lab' else '')
       if content=='lab':
        tmpcode+='\n <div class="slideheader">'
       tmpcode+='\n  <ul class="slidecontent">'
       for count,line in enumerate([(re.sub(r'^.*?<h(.*?)>.*',r'\1',x,flags=re.DOTALL),re.sub(r'^.*?<h.*?>.*?\n(.*?)\n</h.*$',r'\1',x,flags=re.DOTALL)) for x in fixheader]):
        if content=='lab' and count==subtopiccount or content=='content':
#         tmpcode+='\n   <li class='+('"sml"' if count!=subtopiccount else '"big"')+'>'+(f'''<h2><a {'class="'+line[0]+'"' if line[0] else ""} href="#{"main" if content=="content" else "lab"}{day[k][i][j]}_{count}" name="{"chap" if content=="content" else "chaplab"}{day[k][i][j]}_{count}">''' if count==subtopiccount else '<pre>')+f'<pre>{line[1]}</pre>'+('</a></h2>' if count==subtopiccount else '</pre>')+'</li>'
#         tmpcode+='\n   <li class='+('"sml"' if count!=subtopiccount else '"big"')+'>'+(f'''<h2><a {'class="'+line[0]+'"' if line[0] else ""} href="#{"main" if content=="content" else "lab"}{day[k][i][j]}_{count}" name="{"chap" if content=="content" else "chaplab"}{day[k][i][j]}_{count}">''' if count==subtopiccount else '')+f'<pre>{line[1]}</pre>'+('</a></h2>' if count==subtopiccount else '')+'</li>'
         tmpcode+='\n   <li class='+('"sml"' if count!=subtopiccount else '"big"')+'>'+(f'''<a {'class="'+line[0]+'"' if line[0] else ""} href="#{"main" if content=="content" else "lab"}{day[k][i][j]}_{count}" name="{"chap" if content=="content" else "chaplab"}{day[k][i][j]}_{count}">''' if count==subtopiccount else '')+f'<pre>{line[1]}</pre>'+('</a>' if count==subtopiccount else '')+'</li>'
       tmpcode+="""\n  </ul>
 </div>"""
#       if self.lineheightnhtml(self.getpage('\n'+tmpcode))[0]['height']>=self.PH-self.PDFOFST:
       if self.lineheightnhtml(self.getpage('\n'+tmpcode))[2]>=2:
        self.placepagebreak('all',day[k][i][j]);
       self.htmlstr+=tmpcode
       self.htmlstr+=f'\n <div class="clr"></div>' if not re.search(r'^\s*<a>',cnt,flags=re.DOTALL) else ''
       subtopiccount+=1
       tmpcode=''
      elif re.search(r'^\s*<a>.*?</a>',cnt,flags=re.I|re.DOTALL):
       print("<a>")
       code,cnt=self.searchtag('a',cnt,getcode=True)
       self.htmlstr+='\n'+self.lineheightnhtml('<pre class="slideabstract">'+code+'</pre>')[1]+'\n<div class="clr"></div>'
#      elif re.search(r'^\s*<m>[^\n]+</m>',cnt):
#      elif self.searchtag('obj[yor]?',cnt):
#       code,cnt=self.searchtag('obj[yor]?',cnt,getcode=True,includetag=True)
#       self.htmlstr+='\n <pre class="obj'+re.sub('^.*?<obj(.*?)>.*',r'\1',code)+'">'+re.sub(r'^.*?<obj.*?>[ \t]*\n(.*?)\n[ \t]*</obj>',r'\1',code)+'</pre>'
      elif self.searchtag('m',cnt):
       print("<m>")
       code,cnt=self.searchtag('m',cnt,getcode=True)
       '''
       code=Util.webpageurl(http=True)+r'/image/'+code if not re.search(r'/',code) else code
       '''
#       tmpvar1=re.sub(r'^.*(?:embed/|\?v=)(.*)$',r'\1',code) if re.search('youtube',code,flags=re.I) else ''
       code=requestm.youtubeimage(re.sub(r'^.*(?:embed/|\?v=)(.*)$',r'\1',code),pushonserver=True)[0] if re.search(r'youtube',code,flags=re.I) else code
#       code='file://'+os.path.expanduser('~')+'/tmp/imageglobe/image/'+code if not re.search(r'/',code) else re.sub(Util.webpageurl(http=True)+r'/image/','file://'+os.path.expanduser('~')+'/tmp/imageglobe/image/',code)
       try:
#        with Image.open(os.path.expanduser('~')+r'/tmp/imageglobe/image/'+re.sub(r'^.*/','',code)) as img:
#         tmpvar1='\n'+("  <a style=\"display:block;\" href=\""+(re.sub(r'(.*)_s[.](.*)','\\1.\\2',code) if not tmpvar1 else r'https://youtube.com/watch?v='+tmpvar1)+"\">" if re.search(r'_s[.]',code) or tmpvar1 else '')+f'<img class="img" style="margin-left:{(self.PAGEWIDTH-img.width)//2 if self.PAGEWIDTH>img.width*2 else self.PAGEWIDTH//4}px;" src="{code}" />'+("</a>" if re.search(r'_s[.]',code) or tmpvar1 else "")+f'''<div class="clr"></div>'''
         tmpvar1=self.adsense(width=re.search(r'youtube',code) and (self.PAGEWIDTH*4)//10 or (self.PAGEWIDTH*6)//10,imageurl=code)
#         tmpcode=self.lineheightnhtml(self.getpage('\n'+tmpvar1))
#         if tmpcode[0]['height']>=self.PH-self.PDFOFST:
         if self.lineheightnhtml(self.getpage('\n'+tmpvar1))[2]>=2:
          self.htmlstr+=self.adjustimage(self.PH-self.lineheightnhtml(self.getpage())[0]['height']) if self.PH-self.lineheightnhtml(self.getpage())[0]['height']>self.ADIMAGEHEIGHT else ''
          self.placepagebreak('all',day[k][i][j])
         self.htmlstr+=tmpvar1
       except Exception as e:
        print(f'<=>preparecontent exception {code=}')
        tmpvar1=f'\n <a style="display:block" href="{code}">{code}</a>'
#        if self.lineheightnhtml(self.getpage('\n'+tmpvar1))[0]['height']>=self.PH-self.PDFOFST:
        if self.lineheightnhtml(self.getpage('\n'+tmpvar1))[2]>=2:
         self.placepagebreak('all',day[k][i][j])
        self.htmlstr+=tmpvar1
      else:
       if self.searchtag('c[sbc]?',cnt):
        print("<cb|c|cc|cs>")
        htmltag='<pre class="code">' if self.searchtag('c',cnt) else '<pre class="codeb">' if self.searchtag(r'cb',cnt) else '<pre class="codec">' if self.searchtag(r'cc',cnt) else '<pre class="codes">'
        code,cnt=self.searchtag('c',cnt,getcode=True) if self.searchtag('c',cnt) else self.searchtag('cb',cnt,getcode=True) if self.searchtag(r'cb',cnt) else self.searchtag('cc',cnt,getcode=True) if self.searchtag(r'cc',cnt) else self.searchtag('cs',cnt,getcode=True)
       else:
        print("<>")
        code,cnt=self.searchtag('',cnt,getcode=True)
        htmltag='<pre class="slidecontent">'
#       def gettagheight(self=self,htmltag=htmltag):
#        return min(self.lineheightnhtml(self.getpage())[0]['height']+self.lineheightnhtml('<pre class="codes">\n'+code+'</pre>')[0]['height']//2+self.PDFOFST,self.PH-self.PDFOFST) if re.search(r'"codes"',htmltag) else self.PH-self.PDFOFST
       tmpvar2=False if re.search(r'"codes"',htmltag) else True
       maxindex=len(re.split('\n',code))
       print(f'<=>preparecontent {htmltag=} {maxindex=}')
       code=' ' if code=='' else code
#       tmpvar1=gettagheight()
       while code:
        if re.search('"codes"',htmltag) and not tmpvar2 and max(self.lineheightnhtml(self.getpage()+'\n'+htmltag+'\n'+'\n'.join(re.split('\n',code)[:maxindex//2])+'</pre>')[2],self.lineheightnhtml(self.getpage()+'\n'+htmltag+'\n'+'\n'.join(re.split('\n',code)[maxindex//2:])+'</pre>')[2])==1:
         self.htmlstr+='\n'+htmltag+'\n'.join(re.split('\n',code)[:maxindex//2])+'</pre>'+'\n'+htmltag+'\n'.join(re.split('\n',code)[maxindex//2:])+'</pre>\n<div class="clr"></div>'
         code=''
#        print(f'TEST {tmpvar1=} {tmpvar2=} {maxindex=} {htmltag=} {code=}')
#        if self.lineheightnhtml(self.getpage('\n '+htmltag+'\n'+'\n'.join(re.split('\n',code)[:maxindex])+'</pre>'))[0]['height']<=tmpvar1:
        elif self.lineheightnhtml(self.getpage('\n '+htmltag+'\n'+'\n'.join(re.split('\n',code)[:maxindex])+'</pre>'))[2]==1:
         if maxindex==len(re.split('\n',code)):
          self.htmlstr+='\n '+htmltag+'\n'+code+'</pre>'+('\n <div class="clr"></div>' if tmpvar2 and re.search('"codes"',htmltag)  or not tmpvar2 and maxindex==len(re.split('\n',code)) else '')
         else:
          jumpcodeindex=max(1,int(math.sqrt(maxindex*2)))
#          while self.lineheightnhtml(self.getpage('\n '+htmltag+'\n'+'\n'.join(re.split('\n',code)[:maxindex])+'</pre>'))[0]['height']<=tmpvar1:
          while self.lineheightnhtml(self.getpage('\n '+htmltag+'\n'+'\n'.join(re.split('\n',code)[:maxindex])+'</pre>'))[2]==1:
           maxindex+=jumpcodeindex
#          while self.lineheightnhtml(self.getpage('\n '+htmltag+'\n'+'\n'.join(re.split('\n',code)[:maxindex])+'</pre>'))[0]['height']>tmpvar1:
          while self.lineheightnhtml(self.getpage('\n '+htmltag+'\n'+'\n'.join(re.split('\n',code)[:maxindex])+'</pre>'))[2]>=2:
           maxindex=maxindex-1
          self.htmlstr+='\n '+htmltag+'\n'+'\n'.join(re.split('\n',code)[:maxindex])+'</pre>'+('\n <div class="clr"></div>' if tmpvar2 and re.search('"codes"',htmltag)  or not tmpvar2 and maxindex==len(re.split('\n',code)) else '')
#          self.placepagebreak('all',self.day[k][i][j]) if tmpvar1==(self.PH-self.PDFOFST) and tmpvar2 else None
          self.placepagebreak('all',self.day[k][i][j]) if tmpvar2 else None
         code='\n'.join(re.split('\n',code)[maxindex:])
         maxindex=len(re.split('\n',code))
         tmpvar2=not tmpvar2 if re.search('"codes"',htmltag) else True
#         tmpvar1=gettagheight()
        else:
         maxindex=maxindex//2
         if not maxindex:
          self.placepagebreak('all',day[k][i][j])
          tmpvar2=False
          maxindex=len(re.split('\n',code))
#          tmpvar1=gettagheight()
     else:
      subtopiccount=0
      self.htmlstr+=self.adjustimage(self.PH-self.lineheightnhtml(self.getpage())[0]['height']) if self.PH-self.lineheightnhtml(self.getpage())[0]['height']>self.ADIMAGEHEIGHT else ''
#      self.htmlstr+=self.adsense(self.PH-self.hc) if self.PH-self.hc>self.ADIMAGEHEIGHT else ''
      self.placepagebreak('bottom',day[k][i][j])
#  self.htmlstr=self.lineheightnhtml(self.htmlstr)[1]
  self.htmlstr=self.lineheightnhtml(re.sub(r'\\</pre>$',r'\ </pre>',self.htmlstr,flags=re.M))[1]

#  import pdfkit
#  os.environ['NO_AT_BRIDGE']=str(1)
 def placeemptypage(self,text=format.LEFTBLANK):
  tmpstr=self.placepagebreak(side='top',arrow=False)
#  tmpstr+=fr'''<pre style="margin-top:{(self.PH-ImageFont.truetype(os.path.expanduser('~')+r'/tmp/MISC/misc/LiberationSerif-Regular.ttf',30).getsize(text)[1])//2}px;text-align:center;font-weight:bold;font-size:30pt;color:#000000;font-family:myliberationserif;">{text}</pre>'''
  tmpstr+=fr'''<pre style="margin:{(self.PH-ImageFont.truetype(os.path.expanduser('~')+r'/tmp/MISC/misc/LiberationSerif-Regular.ttf',30).getsize(text)[1])//2}px auto;text-align:center;font-weight:bold;font-size:30pt;color:#000000;font-family:myliberationserif;">{text}</pre>'''
  tmpstr+=self.placepagebreak(side='bottom',arrow=False)
  return tmpstr
 def preparedisclaimer2(self):
  filedatadesktop=None
  self.htmlstr+=self.placeemptypage()
  self.placepagebreak(side='top')
  img=Image.open(os.path.expanduser('~')+r'/tmp/imageglobe/resource/booktitlepagebottom.png').convert('RGBA')
  img=img.resize((((self.PH-self.TM)*img.width)//img.height,self.PH-self.TM))
  self.libi.system(r'python3 tex.py "'+self.db.search2('tech','content','name','=',self.tech,mode='get')[0][0].title()+r'" 2')
  img2=Image.open(r'logdir/tex_'+re.sub(r'[\s/]+','',self.db.search2('tech','content','name','=',self.tech,mode='get')[0][0].lower())+'.png').convert('RGBA')
  img.paste(img2,((img.width-img2.width)//2,int(img.height*0.64)-img2.height//2),img2)
  draw=ImageDraw.Draw(img)
  draw.text((img.width//16,img.height//16),'MINH, INC.',font=ImageFont.truetype(os.path.expanduser('~')+r'/.fonts/ufonts.com_tw-cen-mt.ttf',30),anchor='lt',fill=(9,21,90,255))
  draw.line((img.width//16,img.height//16+ImageFont.truetype(os.path.expanduser('~')+r'/.fonts/ufonts.com_tw-cen-mt.ttf',30).getsize('MINH')[1]+4,(img.width*11)//12,img.height//16+ImageFont.truetype(os.path.expanduser('~')+r'/.fonts/ufonts.com_tw-cen-mt.ttf',30).getsize('MINH')[1]+4),fill=(6,21,90,255),width=6)
  draw.line((img.width//16,img.height//16+ImageFont.truetype(os.path.expanduser('~')+r'/.fonts/ufonts.com_tw-cen-mt.ttf',30).getsize('MINH')[1]+12,(img.width*11)//12,img.height//16+ImageFont.truetype(os.path.expanduser('~')+r'/.fonts/ufonts.com_tw-cen-mt.ttf',30).getsize('MINH')[1]+12),fill=(6,21,90,255),width=4)
  draw.multiline_text((img.width//16,img.height//16+ImageFont.truetype(os.path.expanduser('~')+r'/.fonts/ufonts.com_tw-cen-mt.ttf',30).getsize('MINH')[1]+44),'Minh, Inc. was established in Mid 2015 as research and developement center in software\ntechnologies like Device Drivers, Embedded OpengGL 3D graphics, Machine Learning and\nArtificial Intelligence. Company provides training in various technolgies. Visit \nhttp://minhinc.42web.io/training\n\nPlease follow at https://youtube.com/@minhinc',font=ImageFont.truetype(os.path.expanduser('~')+r'/.fonts/timesnewromanbold.ttf',20),spacing=8,fill=(9,21,90,255))
  draw.multiline_text((img.width//16,img.height//16+ImageFont.truetype(os.path.expanduser('~')+r'/.fonts/ufonts.com_tw-cen-mt.ttf',30).getsize('MINH')[1]+440),f'''"Tell me I'll forget, show me and I may remember,\ninvolve me and I'll understand."\n{"-Chinese Proverb":>90}''',font=ImageFont.truetype(os.path.expanduser('~')+r'/.fonts/timesnewromanbold.ttf',28),spacing=8,fill=(9,21,90,255))
  draw.text((img.width//4,(img.height*8.9)//10),'Minh, Inc.',font=ImageFont.truetype(os.path.expanduser('~')+r'/.fonts/ufonts.com_tw-cen-mt.ttf',40),anchor='mt',fill=(0,0,0,255))
  draw.text((img.width//4,(img.height*8.9)//10+ImageFont.truetype(os.path.expanduser('~')+r'/.fonts/ufonts.com_tw-cen-mt.ttf',40).getsize('Minh')[1]),r'https://youtube.com/@minhinc',font=ImageFont.truetype(os.path.expanduser('~')+r'/.fonts/urwbookman-light.otf',25),anchor='mt',fill=(0,0,0,255))
  draw.text((img.width,img.height-ImageFont.truetype(os.path.expanduser('~')+r'/.fonts/urwbookman-light.otf',14).getsize('Generated')[1]*2),f'Generated on {datetime.datetime.now():%Y-%m-%d %H:%M:%S}',align="left",anchor='rt',fill=(0,0,0,255),font=ImageFont.truetype(os.path.expanduser('~')+r'/.fonts/urwbookman-light.otf',14),stroke_width=1,stroke_fill=(255,0,0,255))
  img.save('advance-'+self.tech+'-slides_bottom.png')
  self.htmlstr+=f'''<img src="http://{Util.webpageurl()}/image/advance-{self.tech+'-slides_bottom.png'}" style="display:block;margin:auto"/>'''
  self.placepagebreak(side='bottom')
  Util.push(f'advance-{self.tech}-slides_bottom.png',dir='image',push=True)

 def prepareoutfile(self):
#  open('../css/tmp.css','w').write('div.pg pre.slidecontent, div.pg pre.code,div.pg pre.codeb,  div.pg pre.codec {display:block;}')
  tmpstr=tmpstr2=tmpcode=''
  count=0
  print(f'{"":-^40}\n{"OUTPUT GENERATION":-^40}\n{"":-^40}')
  for i in self.driver:
   for j in re.findall(r'(<div\s+class="pg"\s+style=".*?)(?=<div\s+class="pg"\s+style="|$)',self.htmlstr,flags=re.DOTALL):
    tmpstr+=re.sub(r'(?P<id><div\s+class="pg".*?style="height:)\d+(?P<id2>.*)',lambda m:m.group('id')+str(max(self.lineheightnhtml(re.sub(r'^.*?<div\s+class="pg".*?>(.*)</div>',r'\1',j,flags=re.DOTALL),makepdf=False,driver=i)[0]['height'],self.PH)+(i=='firefox' and 20 or 10))+m.group('id2'),j,flags=re.DOTALL)
   open(f'logdir/tmp{self.tech}{"_f" if i=="firefox" else ""}.html','w').write(re.sub('([.][.]/css/)','../'+r'\1',self.fileheader[0])+'\n'+tmpstr+'\n'+self.fileheader[1])
   tmpstr=re.sub('file://'+os.path.expanduser('~')+r'/tmp/imageglobe/image/',Util.webpageurl(http=True)+r'/image/',tmpstr,flags=re.DOTALL)
   disclaimer2=re.sub(r'.*(<div class="pg".*?'+self.LEFTBLANK+'.*)$',r'\1',tmpstr,flags=re.DOTALL)
   content=[re.sub(r'^.*(<div class="pg".*)$',r'\1',re.split(re.escape(x),tmpstr)[0],flags=re.DOTALL)+re.sub(r'^(.*)<div class="pg".*$',r'\1',x,flags=re.DOTALL) for x in re.findall(r'(name="chap\d+".*?)(?=name="chap\d+"|'+self.LEFTBLANK+')',tmpstr,flags=re.I|re.DOTALL)]

   #desktop
   for count in range(len(content)):
    daycount=re.sub(r'.*?name="chap(\d+)".*$',r'\1',content[count],flags=re.DOTALL)
    with open(f"logdir/advance-{self.tech}-slides{'-chap'+daycount if count else ''}{'_f' if i=='firefox' else ''}.txt",'w') as file:
     print(f'writing to file firefox {file.name=} {daycount=} {count=}')
     filedatadesktop=re.sub(r'-slides.php\?chap='+self.day[0][0][0]+'#',r'-slides.php#',re.sub(r'(?P<id>.*?)(?P<id2>href="#chap.*?")',lambda m:(re.sub(r'(style=")',r'\1'+'background-color:#f38502;',m.group('id')) if re.search('"#chap'+daycount+'"',m.group('id2')) else m.group('id'))+re.sub(r'#chap(\d+)(_\d+)?',r'http://'+Util.webpageurl()+r'/training/'+self.tech+r'/advance-'+self.tech+r'-slides.php?chap='+r'\1'+'#chap'+r'\1\2',m.group('id2')),re.split(re.escape(content[0]),tmpstr)[0]+'\n'+content[count],flags=re.M),flags=re.M)+disclaimer2
     file.write(filedatadesktop)
   #Mobile Chrome
    if not i=='firefox':
     with open(f"logdir/advance-{self.tech}-slides{'-chap'+daycount+'_m' if count else '_m'}.txt",'w') as file:
      print(f'writing to file firefox {file.name=} {daycount=} {count=}')
      file.write(re.sub('(<pre .*?)font-size:\d+pt(.*?'+self.LEFTBLANK+'.*)',r'\1\2',re.sub(r'(?P<id><div class="header2".*?margin-top:)(?P<id2>\d+)',lambda m:m.group('id')+('40' if int(m.group('id2'))==0 else m.group('id2')),re.sub(r'(?P<id><div class="dayheader".*?style="margin-top\s*:\s*)(?P<id2>\d+)',lambda m:m.group('id')+('40' if int(m.group('id2'))>40 else m.group('id2')),re.sub(r'(<div class="pg".*?)style="height:.*?"',r'\1',re.sub(r'(<img .*?)style=".*?"',r'\1'+'class="img" ',re.sub(r'^.*?<a.*?class="ftr.*','',re.sub(r'(<div class="(?:dayheaderleft|dayheaderright)".*?)style=".*?"',r'\1'+' style="margin-top:20px;margin-bottom:40px;"',re.sub(r'(<div class="slideheader".*?)style=".*?"',r'\1'+'style="margin-top:20px;margin-bottom:10px;"',re.sub(r'(<pre class="(?:code.*?|slidecontent)".*?)style=".*?"',r'\1',filedatadesktop,flags=re.M),flags=re.M),flags=re.M),flags=re.M),flags=re.M),flags=re.M),flags=re.M),flags=re.M),flags=re.M))
#     file.write(re.sub(r'(<div class="pg".*?)style=".*?"',r'\1',re.sub(r'(<pre class="(?:code.*?|slidecontent)".*?)style=".*?"',r'\1',re.sub(r'(<div class="slideheader".*style=".*?)width:\d+px',r'\1',re.sub(r'(<img .*style=".*?)margin-left:\d+px',r'\1'+'max-width:100%',filedatadesktop,flags=re.M),flags=re.M),flags=re.M),flags=re.M))
   tmpstr=''

  Util.searchhtmltag(self.inlinehtmltag_nofrequentlyused,self.htmlstr)

  #PDF file generation
  print(f"creating pdf... logdir/advance-{self.tech}-slides.pdf")
#  open('logdir/pdf'+self.tech+'.html','w').write(re.sub(Util.webpageurl(http=True)+r'/image/',r'file://'+os.path.expanduser('~')+r'/tmp/imageglobe/image/',re.sub(r'[.][.]/css/',r'../../css/',self.fileheader[0]+'\n'+self.htmlstr+'\n'+self.fileheader[1],flags=re.M),flags=re.M))
  open('logdir/pdf'+self.tech+'.html','w').write(re.sub('(<img\s+.*?src=")'+Util.webpageurl(http=True)+r'/image/',r'\1'+r'file://'+os.path.expanduser('~')+r'/tmp/imageglobe/image/',re.sub(r'[.][.]/css/',r'../../css/',self.fileheader[0]+'\n'+self.htmlstr+'\n'+self.fileheader[1],flags=re.M),flags=re.M))
  os.system(f"wkhtmltopdf --page-size A4 --enable-local-file-access logdir/pdf{self.tech}.html logdir/advance-{self.tech}-slides.pdf")

  offset=0;tmpday=''
  for count,i in enumerate(re.findall(r'(<div\s+class="pg"\s+style=".*?)(?=<div\s+class="pg"\s+style="|$)',self.htmlstr,flags=re.DOTALL)):
   if re.search(r'<pre\s+class="title".*?<pre\s+class="subtitle"',i,flags=re.DOTALL) and not (count+1+offset)%2:
    tmpstr+=self.placeemptypage()+'\n'+i
    offset=(offset+1)%2
   elif re.search(r'<div\s+class="slideheader".*?Day\s+\d+\s+(?:Morning|Afternoon)',i,flags=re.DOTALL):
    x=re.findall(r'<pre\s+class="topic".*?(\d+)',i,flags=re.DOTALL)[0]
    if not (count+1+offset)%2 and x!=tmpday:
     tmpstr+=self.placeemptypage()+'\n'+i
     offset=(offset+1)%2
    elif (count+1+offset)%2 and x!=tmpday:
     tmpstr+=self.placeemptypage()+'\n'+self.placeemptypage()+'\n'+i
    else:
     tmpstr+=i
    tmpday=x
   elif re.search(f'<img .*advance-{self.tech}-slides_bottom',i,flags=re.DOTALL) and (count+1+offset)%2:
    tmpstr+=self.placeemptypage()+'\n'+i
   else:
    tmpstr+=i
  open(f'logdir/pdf{self.tech}_print.html','w').write(re.sub('(<img\s+.*?src=")'+Util.webpageurl(http=True)+r'/image/',r'\1'+r'file://'+os.path.expanduser('~')+r'/tmp/imageglobe/image/',re.sub(r'[.][.]/css/',r'../../css/',self.fileheader[0]+'\n'+tmpstr+'\n'+self.fileheader[1],flags=re.M),flags=re.M))
  print(f"creating pdf... logdir/advance-{self.tech}-slides_print.pdf")
  os.system(f"wkhtmltopdf --page-size A4 --enable-local-file-access logdir/pdf{self.tech}_print.html logdir/advance-{self.tech}-slides_print.pdf")
  tmpstr=''

  #image storage
  tmpcode+=self.placepagebreak('top',arrow=False)
  for x in re.findall(r'(?:<pre\s+class="topic".*?>(.*?)</pre>|<li\s+class="big".*?>.*?<pre>(.*?)<\/pre>|<img\s+(?:(?!src).)*?src="(.*?)")',self.htmlstr,flags=re.DOTALL):
   tmpstr=x[0] if not re.search(r'^\s*$',x[0]) else tmpstr
   tmpstr2=x[1] if not re.search(r'^\s*$',x[1]) else tmpstr2
   print(f'IMAGE {tmpstr=} {tmpstr2=} {x[2]=}')
   if not re.search('(^\s*$|https?://.*?youtube|traininglogo[.]gif|advance-'+self.tech+'-slides_(front|bottom)[.])',x[2]) and Image.open(re.sub(r'^.*/(.*)$',os.path.expanduser('~')+'/tmp/imageglobe/image/'+r'\1',x[2])).width > self.PAGEWIDTH*0.6:
    if self.lineheightnhtml(re.sub(r'^.*<div\s+class="pg".*?>(.*)$',r'\1',tmpcode,flags=re.DOTALL)+'\n'+self.adsense(imageurl=x[2],width=self.PAGEWIDTH*0.9)+'\n<pre style="text-align:center;margin-bottom:20px">'+tmpstr+'    '+tmpstr2+'    '+re.sub(r'.*/(.*)$',r'\1',x[2])+'</pre>')[2]>=2:
     tmpcode+='\n'+self.placepagebreak('all',arrow=False)
    tmpcode+='\n'+self.adsense(imageurl=x[2],width=self.PAGEWIDTH*0.9)+'\n<pre style="text-align:center;margin-bottom:20px">'+tmpstr+'    '+tmpstr2+'    '+re.sub(r'.*/(.*)$',r'\1',x[2])+'</pre>'
  tmpcode+=self.placepagebreak('bottom',arrow=False)
  open(f'logdir/pdf{self.tech}_image.html','w').write(re.sub(Util.webpageurl(http=True)+r'/image/',r'file://'+os.path.expanduser('~')+r'/tmp/imageglobe/image/',re.sub(r'[.][.]/css/',r'../../css/',self.fileheader[0]+'\n'+tmpcode+'\n'+self.fileheader[1],flags=re.M),flags=re.M))
  print(f'creating pdf... logdir/advance-{self.tech}-slides_image.pdf')
  os.system(f"wkhtmltopdf --page-size A4 --enable-local-file-access logdir/pdf{self.tech}_image.html logdir/advance-{self.tech}-slides_image.pdf")
  tmpcode=tmpstr=tmpstr2=''

  self.htmlstr+='\n'+self.placeemptypage('#########\n  LAB SESSION  \n##########')+'\n'+self.placeemptypage()
  self.preparecontent('lab')
  print(f"creating pdf ... logdir/advance-{self.tech}-slides_lab.pdf")
  open('logdir/lab'+self.tech+'.html','w').write(re.sub(Util.webpageurl(http=True)+r'/image/',r'file://'+os.path.expanduser('~')+r'/tmp/imageglobe/image/',re.sub(r'[.][.]/css/',r'../../css/',self.fileheader[0]+'\n'+re.sub(r'<ul class="slidecontent">','<ul class="slidecontent" style="width:140%">',re.sub(f'.*advance-{self.tech}-slides_bottom.png.*?(<div\s+class="pg".*)$',r'\1',self.htmlstr,flags=re.DOTALL),flags=re.M)+'\n'+self.fileheader[1],flags=re.M),flags=re.M))
  os.system('wkhtmltopdf --page-size A4 --enable-local-file-access logdir/lab'+self.tech+f".html logdir/advance-{self.tech}-slides_lab.pdf")

  tmpcode='\n'+self.placeemptypage('#########\n  OBJECTIVE TYPE\nQuestions \n##########')+'\n'+self.placeemptypage()
  tmpcode+=self.placepagebreak('top',arrow=False)
#  for i in re.findall(r'(<div\s+class="slideheader"(?:(?!"slideheader").)*?(?:<a\s+class="y"|\n[ \t]*a[.]\s+.*?\bb[.]\s+).*?</div>)',self.htmlstr,flags=re.DOTALL):
  for x in re.findall(r'(?:<pre\s+class="topic".*?>(.*?)</pre>|(<div\s+class="slideheader(?:(?!slideheader).)*?(?:<a\s+class="y"|\n[ \t]*a[.]\s+.*?\bb[.]\s+).*?<\/div>))',open('logdir/labpy.html').read(),flags=re.DOTALL):
   tmpstr=x[0] if not re.search(r'^\s*$',x[0]) else tmpstr
#   print(f'TEST image {count=} {x=} {tmpcode=} {tmpstr=} {tmpstr2=}')
   if not re.search(r'^\s*$',x[1]):
    if tmpstr!=tmpstr2:
     tmpcode+='\n'+self.placepagebreak('all',arrow=False) if not tmpstr2=='' else ''
     count=0
    tmpstr2='<div class="slideheader">\n<h1><pre class="topic">'+tmpstr+'</pre></h1></div>\n<div class="clr"></div>\n'+x[1]
    if self.lineheightnhtml(re.sub('^.*<div\s+class="pg".*?</div>(.*)',r'\1',tmpcode,flags=re.DOTALL)+'\n'+tmpstr2)[2]>=2 and count<10:
     tmpcode+='\n'+self.placepagebreak('all',arrow=False) 
    tmpcode+='\n'+tmpstr2 if count<10 else ''
    tmpstr2=tmpstr
    count+=1
  tmpcode+=self.placepagebreak('bottom',arrow=False)
  open(r'logdir/obj.html','w').write(re.sub(Util.webpageurl(http=True)+r'/image/',r'file://'+os.path.expanduser('~')+r'/tmp/imageglobe/image/',re.sub(r'[.][.]/css/',r'../../css/',self.fileheader[0]+'\n'+tmpcode+'\n'+self.fileheader[1],flags=re.M),flags=re.M))
  print(f"creating pdf ... logdir/advance-{self.tech}_slides_objective.pdf")
  os.system(f"wkhtmltopdf --page-size A4 --enable-local-file-access logdir/obj.html logdir/advance-{self.tech}-slides_objective.pdf")
  tmpcode=tmpstr=tmpstr2=''


trainingformat()
