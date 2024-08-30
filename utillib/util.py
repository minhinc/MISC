import os,sys;sys.path.append(os.path.expanduser('~')+r'/tmp/')
import builtins
import traceback
from PyPDF2 import PdfFileWriter, PdfFileReader, PdfFileMerger,PdfMerger,PdfReader
import io,os,re
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import datetime
from pathlib import Path
from MISC.extra.debugwrite import print

class utilc:
 kwargc=dict( \
  customtag=['<h[yor]?>','<m>','<a>','<c>','<cb>','<cc>','<cs>'], \
  delimiter='!ABS SBA!', \
  round=3, \
  fps=15 \
 )
 moduleclassc=(('MISC.utillib.seleniumrequest','seleniumrequestc()'),('MISC.utillib.databaserequest','databaserequestc()'),('MISC.utillib,machinelearningrequest','machinelearningrequestc()'),('MISC.utillib.database','databasec(False)'))
 def __init__(self):
  super(utilc,self).__init__()
 def concatpdf(self,dir):
  merger=PdfFileMerger()
  for count,i in enumerate(sorted([i for i in os.listdir(dir) if os.path.isfile(dir+r'/'+i) and re.search(r'[.]pdf$',i,flags=re.I)],key=str.lower)):
   print(f'M Util.concatpdf processing i ->',i)
   classname=re.sub(r'^(.*?)[.]pdf',r'\1',i)
   packet = io.BytesIO()
   existing_pdf = PdfFileReader(open(dir+r'/'+i, "rb"))
   can = canvas.Canvas(packet, pagesize=letter)
   can.setFont('Helvetica-Bold', 8)
  # can.drawString((existing_pdf.getPage(0).mediaBox[2]-4*len(classname))//2, 10, r'<'+classname+r'>')
   can.drawString((existing_pdf.getPage(0).mediaBox[2]-4*len(classname))//2, 10, r'<'+classname+r'>'+('_0_' if os.path.isfile(dir+r'/'+classname+'_1_.pdf') else ''))
   can.setFontSize(4)
   can.drawString(existing_pdf.getPage(0).mediaBox[2]-2*(len(str(count+1))+1),5,str(count+1))
   can.showPage()
   can.save()
   packet.seek(0)
   new_pdf = PdfFileReader(packet)
   output = PdfFileWriter()
   page = existing_pdf.getPage(0)
   page.mergePage(new_pdf.getPage(0))
   output.addPage(page)
   outputStream = open(dir+r'/'+classname+r'_tmp.pdf', "wb")
   output.write(outputStream)
   outputStream.close()
   merger.append(PdfFileReader(open(dir+r'/'+classname+'_tmp.pdf','rb')))
  print(f'M Util.concatpdf generating '+dir+r'/output/pyreverse.pdf ...')
  if not os.path.exists(dir+r'/output'):
   os.mkdir(dir+r'/output')
  merger.write(dir+r'/output/pyreverse.pdf')
  merger.close()
  print(f'M Util.concatpdf deleting all '+dir+r'/*_tmp.pdf files...')
  os.system(r'rm '+dir+r'/*_tmp.pdf')

 def concatpdffiles(self,*files):
  merger=PdfMerger()
  for count,i in enumerate(files):
   print(f'I {i} {count+1}/{len(files)}')
   merger.append(PdfReader(open(i, "rb")))
  merger.write(re.sub(r'\s+','',files[0][:10]).lower()+'_'+"{dd.year}_{dd.month}_{dd.day}_{dd.hour}_{dd.minute}_{dd.second}.pdf".format(dd=datetime.datetime.now()))
  merger.close()
  

 def getarg(self,arg,count=1,removehyphen=False,removearg=True):
  """count=0 if argument to be returned
    count=1 if argument presense is checked (True/False)
    count=2 if argument next value to be returned
    count=-1 if agument till next -- or till end to be returned
    removehyphen - if count=0 then hyphen should be removed?"""
  print(f'E Util.getarg {arg=}')
  ret=None
  index=([count for count in range(len(sys.argv)) if re.search(r'^'+arg+r'$',sys.argv[count])] or [None])[0]
  print(f'M Util.getarg {index=}')
  '''
  if [x for x in sys.argv if re.search(arg,x)]:
   ret=sys.argv[sys.argv.index(arg)+1] if count>1 else True
   sys.argv[sys.argv.index(arg):sys.argv.index(arg)+(2 if count>=2 else 1)]=''
  '''
  if index:
   if count>=0:
    ret=sys.argv[index+1] if count>1 else re.sub(r'^(-+)','' if removehyphen else r'\1',sys.argv[index]) if count==0 else True
    if removearg:
     sys.argv[index:index+(2 if count>=2 else 1)]=[]
   else:
    ret=sys.argv[index+1:([x for x in range(index+1,len(sys.argv)) if re.search(r'^--',sys.argv[x])] or [len(sys.argv)])[0]]
    if removearg:
     sys.argv[index:([x for x in range(index+1,len(sys.argv)) if re.search(r'^--',sys.argv[x])] or [len(sys.argv)])[0]]=[]
  return ret

 def webpageurl(self,http=False):
  return (r'http://' if http else '')+r'minhinc.42web.io'

 def push(self,*file,dir,push=False):
  data=None
  retry=2
  if not hasattr(Util.push,'file'):
   Util.push.file=[]
  count=[x for x in Util.push.file if x[1]==dir]
  count[0][0].extend(file) if count else Util.push.file.append([list(file),dir])
  print(f'M Util.push {Util.push.file=} {push=}')
  if push:
   for dir in Util.push.file:
    os.mkdir(os.path.expanduser('~')+r'/tmp/imageglobe/'+dir[1]) if not os.path.exists(os.path.expanduser('~')+r'/tmp/imageglobe/'+dir[1]) else None
    [os.system(f"cp {x} {os.path.expanduser('~')}/tmp/imageglobe/{dir[1]}/") for x in dir[0]]
    while retry:
     data=os.popen(r'~/tmp/ftp.sh ls '+dir[1]).read()
     if data and not re.search(r'not connected',data,flags=re.I):
      break
     retry-=1
    else:
     print('C Util.push Could Not Connect')
     return None
#    outputfile=' '.join([x for x in dir[0] if not re.search(x,data) or re.sub(r'^.*?(\d+)(?:\s+\w+){3}\s+'+x+r'\s*$',r'\1',data,flags=re.DOTALL) != re.sub(r'^.*?(\d+)(\s+\w+){3}\s+'+x+r'\s*$',r'\1',os.popen(r'ls -la '+x).read(),flags=re.M)])
    outputfile=' '.join([x for x in dir[0] if not re.search(x,data)])
    print(f'D Util.push data ->{dir[1]=} {outputfile=}')
    os.system('cd ~/tmp/imageglobe/'+dir[1]+';'+r'~/tmp/ftp.sh '+'mput '+dir[1]+' '+outputfile) if outputfile else None
#   [[os.system(f"cp {x} {os.path.expanduser('~')}/tmp/imageglobe/{dir[1]}") for x in dir[0]] for dir in Util.push.file] if push else None
   Util.push.file=[]

 def searchhtmltag(self,htmltaglist,htmlstr):
  htmltaglist=[re.sub(r'^<(.*)>$',r'\1',x) for x in htmltaglist]
  resulttag={}
  for i in re.findall(r'<(\w+)',htmlstr,flags=re.DOTALL):
   if [x for x in htmltaglist if re.search(r'^'+x+r'$',i)]:
    resulttag[i]=1 if i not in resulttag else resulttag[i]+1
  print(f'I --------- HTML TAG DETECTED ----------')
  print(resulttag)
  print(f'I ---------------------------')

 '''
 @staticmethod
 def gethtmltagdescripancy(htmltaglist,htmlstr):
  htmltaglist=[re.sub(r'^<(.*)>$',r'\1',x) for x in htmltaglist]
  resulttag={}
  for i in re.split(r'(\n|\\n)',htmlstr):
   for x in [x for x in re.findall(r'(?<!<)</?(\w+)',i) if [k for k in htmltaglist if re.search(r'^'+k+r'$',x)]]:
    if re.search(r'</?'+x+r'[^>]+(<|$)',i):
     if i not in resulttag:
      resulttag[i]=[1,x]
     else:
      resulttag[i][0]+=1
      resulttag[i].append(x) if x not in resulttag[i] else None
  print(f'I ---------- HTML TAG DISCREPENCY FOUND ----------')
  print(resulttag)
  print(f'---------------------------')
 '''

 def usertagdescripancy(self,tech):
  mismatchdict=dict()
  for count,i in enumerate(re.split('\n',os.popen(f'python3 ../gc/seed.py print {tech}').read())):
   for j in __class__.customtag:
    count1=len(re.findall(r'(?<!\\)'+j,re.sub(r'\\n','\n',i),flags=re.M))
    count2=len(re.findall(r'(?<!\\)'+re.sub('^<','</',j),re.sub(r'\\n','\n',i),flags=re.M))
    if count1!=count2:
     print(f'{count} {i[:20]} {j} {count1} {count2}')
     mismatchdict[j]=(count,i[:20],j,count1,count2)
  return mismatchdict

 def mysqldump(self):
  open(f'dbname{datetime.datetime.today():%Y_%m_%d}.sql','w').write(re.sub('utf8mb4_0900_ai_ci','utf8mb4_general_ci',os.popen('mysqldump -p -u root epiz_30083730_minhinc').read()))

 def ftp(self,mode,dir,*filelist,localdir='.'):
  print(f'E Util.ftp {mode=} {dir=} {filelist=} {localdir=}')
  filelist=[re.sub(r'^.*/(.*)$',r'\1',x) for x in filelist]
  retrycount=2
  while retrycount:
   data=os.popen('cd '+localdir+';~/tmp/ftp.sh '+(mode=='get' and 'mget' or mode=='put' and 'mput' or mode)+' '+dir+' '+' '.join(filelist)).read()
   if data and re.search('^Connected to',data,flags=re.M):
    break
   retrycount-=1
  return retrycount if not retrycount else data
 def gettable(self):
  return {i[1]:re.findall(r'(\w+)\s+(\w*(?:CHAR|INT|TEXT|BLOB))',i[2]) for i in re.findall('^(.*?)CREATE TABLE.*?(\w+)\s*\(\s*(.*?)"\s*\)',open(os.path.expanduser('~')+r'/tmp/MISC/utillib/'+'database.py').read(),flags=re.M) if not re.search('#',i[0])}

 def converttolatin1(self,strpar):
  return strpar.encode('latin1').decode('latin1')

 '''
 @staticmethod
 def syncimagedir():
  filelistremote=[i for i in re.findall(r'^(?:[d-]rw.*?)(\S+)$',Util.ftp('ls','image',''),flags=re.M) if not i=='.' and not i=='..']
  filelistlocal=os.listdir(os.path.expanduser('~')+'/tmp/imageglobe/image/')
  Util.ftp('put','image',*[i for i in filelistlocal if i not in filelistremote],localdir='~/tmp/imageglobe/image')
  Util.ftp('get','image',*[i for i in filelistremote if i not in filelistlocal],localdir='~/tmp/imageglobe/image')
 @staticmethod
 def diffindirectory(dir1,dir2):
  dir1file=[i for i in os.listdir(dir1) if not i=='.' and not i=='..']
  dir2file=[i for i in os.listdir(dir2) if not i=='.' and not i=='..']
  [print(dir1+'/'+i) for i in dir1file if i not in dir2file]
  [print(dir2+'/'+i) for i in dir2file if i not in dir1file]
  for i in [i for i in dir1file if i in dir2file]:
   print(i,end=' ') if open(dir1+'/'+i).read()!=open(dir2+'/'+i).read() else None
 @staticmethod
 def resizeimagesize(referencesize,imagesize,ratio):
  width,height=0,0
  ratio=float(ratio/100) if ratio>1 else ratio
  if imagesize[0]/imagesize[1]>=referencesize[0]/referencesize[1]:
   width=int(referencesize[0]*ratio)
   height=(width*imagesize[1])//imagesize[0]
  else:
   height=int(referencesize[1]*ratio)
   width=(height*imagesize[0])//imagesize[1]
  return (width,height) if width<imagesize[0] else imagesize
 '''

 def scaledwidthheight(self,imagesize,scalesize=None,referencesize=None,libi=None):
  '''\
  ---------------------------------------
  |         <referencesize>/<windowsize>|
  |    ----------------------------     |
  |    |             <scalesize>  |     |
  |    |  ----------------        |     |
  |    |  |              |        |     |
  |    |  |              |        |     |
  |    |  |<imagesize>   |        |     |
  |    |  |              |        |     |
  |    |  ----------------        |     |
  |    |                          |     |
  |    ----------------------------     |
  ---------------------------------------
  '''
  width=height=None
  print(f'E Util.scaledwidthheight {imagesize=} {scalesize=} {referencesize=} {libi=}')
  if type(imagesize)==str and not re.search(r'^\d+x\d+$',imagesize):
   imagesize=[int(x) for x in libi.videoattribute(imagesize)[0]]
  elif re.search(r'^\d+x\d+$',imagesize):
   imagesize=[int(x) for x in re.split('x',imagesize)]
  if scalesize==None:
   scalesize=(libi.videowidth,libi.videoheight)
  if referencesize==None:
   referencesize=(libi.videowidth,libi.videoheight)
  print(f'M Util.scaledwidthheight {imagesize=} {scalesize=} {referencesize=} {libi=}')
  if abs(scalesize[0]-imagesize[0])//imagesize[0]<=abs(scalesize[1]-imagesize[1])//imagesize[1]:
   width,height=scalesize[0],(scalesize[0]*imagesize[1])//imagesize[0]
   if height>referencesize[1]:
    height=referencesize[1]
    width=(height*imagesize[0])//imagesize[1]
  else:
   width,height=(scalesize[1]*imagesize[0])//imagesize[1],scalesize[1]
   if width>referencesize[0]:
    width=referencesize[0]
    height=(width*imagesize[1])//imagesize[0]
  return (2*(width//2),2*(height//2))

 def pprint(self,*a):
  print(f'I {"":-^40}')
  for i in a:
   print(f'I {str(i):^40}')
  print(f'I {"":-^40}')

 def getlist(self,url):
#  print(f'E Util.getlist {url=}')
  if type(url)==list or type(url)==tuple:
   return [x for x in (url[0] if type(url)==tuple and len(url)==1 else url)]
  else:
   return [] if not url else [url] if not typeof(url)==dict else [url[count] for count in range(len(url))] if not [x for x in url if not type(x)==int] else url.values()

 def getdict(self,url):
#  print(f'util.getdict {url=} {starb=}')
  if type(url)==list or type(url)==tuple:
   return {count:x for count,x in enumerate(url[0] if type(url)==tuple and len(url)==1 else url)}
  else:
   return {} if not url else {0:url} if [x for x in url if not type(x)==int] else url

 def exec(self,arg):
  self.arg=arg
  return self.arg

 def usage(self,*arg,count=1):
  if len(sys.argv)<=count:
   print(f'--- usage ---')
   [print(i) for i in arg]
   sys.exit(-1)

 def print(self,args):
  print(args[0],f' {traceback.extract_stack(None,2)[0][1]} {traceback.extract_stack(None,2)[0][2]} ',args[2:])
 '''
 def moduleclassinstance(self,modulename,classobj):
  return sys.modules[__name__].moduleclassinstance(modulename,classobj)
 def populatemodulefunc(self,*moduleclass):
  print(f'E utilc.populatemodulefunc {moduleclass=}')
  sys.modules[__name__].populatemodulefunc(*moduleclass)
 '''


class utildict(builtins.dict):
 def append(self,value):
  self[len(self)]=value if not type(value)==dict else value.values()[0]
 def extend(self,*value):
  [self.append(x if not type(x)==dict else x.values()[0]) for x in value]
 def index(self,item):
  itemt=tuple(item) if type(item)==list else item.items()[0] if type(item)==dict else item
  return [count for count,item in enumerate(self.items()) if item==itemt][0]

print(f'C ****** WELCOME TO UTIL MODULE *****')
def cmc(*moduleclass):#create module class
 print(f'E util.cmc {moduleclass=}')
 '''
 if [x for x in moduleclass if not type(x)==str]:
  print(f'C util.populatemodulefunc module name and class name must be string. exiting..')
  sys.exit(-1)
 createdmoduletmp=[xx for xx in sys.modules if hasattr(sys.modules[xx],'__file__') and hasattr(sys.modules[xx],'__name__')  and not sys.modules[xx].__name__ == sys.modules[moduleclass[0]].__name__ and str(Path(str(sys.modules[xx].__file__)).resolve())==str(Path(str(sys.modules[moduleclass[0]].__file__)).resolve())]
 [setattr(sys.modules[moduleclass[0]],re.sub(r'^\s*(\S+)(?=[\s(]).*',r'\1',x)+'m',eval(moduleclass[0]+'.'+x) if not createdmoduletmp else getattr(sys.modules[createdmoduletmp[0]],re.sub(r'^\s*(\S+)(?=[\s(]).*',r'\1',x)+'m')) for x in moduleclass[1:]]
 '''
 [setattr(sys.modules[moduleclass[0]],x.__class__.__name__+'m',x) for x in moduleclass[1:]]

def mce(modulename,classobj):#module class exists?
 moduleloadedtmp=[sys.modules[xx] for xx in sys.modules if hasattr(sys.modules[xx],'__file__') and hasattr(sys.modules[xx],'__name__')  and not sys.modules[xx].__name__ == sys.modules[modulename].__name__ and str(Path(str(sys.modules[xx].__file__)).resolve())==str(Path(str(sys.modules[modulename].__file__)).resolve())]
 print(f'C util.mce object {getattr(moduleloadedtmp[0],classobj.__name__+"m")} already loaded "{modulename}:{sys.modules[modulename].__file__}" -> "{moduleloadedtmp[0].__name__}:{moduleloadedtmp[0].__file__}"...') if moduleloadedtmp else None
 return moduleloadedtmp and getattr(moduleloadedtmp[0],classobj.__name__+'m') or moduleloadedtmp

cmc(__name__,mce(__name__,utilc) or utilc())
'''
#populatemodulefunc(__name__,dictc())
for i in utilc.moduleclassc:
 exec('import '+i[0])
 createdmoduletmp=[xx for xx in sys.modules if hasattr(sys.modules[xx],'__file__') and hasattr(sys.modules[xx],'__name__')  and not sys.modules[xx].__name__ == sys.modules[i[0]].__name__ and str(Path(str(sys.modules[xx].__file__)).resolve())==str(Path(str(sys.modules[i[0]].__file__)).resolve())]
 setattr(sys.modules[i[0]],re.sub(r'^(.*?)\(.*',r'\1',i[1])+'m',getattr(sys.modules[createdmoduletmp[0]],re.sub(r'^(.*?)\(.*',r'\1',i[1])+'m') if createdmoduletmp else eval(i[0]+'.'+i[1]))
 print('M util module initialized the module -> {i=}')
'''
__all__=['utilcm','utildict','print']
