import os,sys;sys.path.append(os.path.expanduser('~')+r'/tmp/')
from PyPDF2 import PdfFileWriter, PdfFileReader, PdfFileMerger
import io,os,re
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
#from MISC.extra.debugwrite import print

class Util:
 def __init__(self):
  super(Util,self).__init__()
 def concatpdf(self,dir):
  merger=PdfFileMerger()
  for count,i in enumerate(sorted([i for i in os.listdir(dir) if os.path.isfile(dir+r'/'+i) and re.search(r'[.]pdf$',i,flags=re.I)],key=str.lower)):
   print('<=>Util.concatpdf processing i ->',i)
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
  print(r'<=>Util.concatpdf generating '+dir+r'/output/pyreverse.pdf ...')
  if not os.path.exists(dir+r'/output'):
   os.mkdir(dir+r'/output')
  merger.write(dir+r'/output/pyreverse.pdf')
  merger.close()
  print(r'<=>Util.concatpdf deleting all '+dir+r'/*_tmp.pdf files...')
  os.system(r'rm '+dir+r'/*_tmp.pdf')

 @staticmethod
 def getarg(arg,count=1,removehyphen=False):
  """count=0 if argument to be returned
    count=1 if argument presense is checked (True/False)
    count=2 if argument next value to be returned"""
  print(f'><Util.getarg {arg=}')
  ret=False
  index=([count for count in range(len(sys.argv)) if re.search(arg,sys.argv[count])] or [None])[0]
  print(f'<=>Util.getarg {index=}')
  '''
  if [x for x in sys.argv if re.search(arg,x)]:
   ret=sys.argv[sys.argv.index(arg)+1] if count>1 else True
   sys.argv[sys.argv.index(arg):sys.argv.index(arg)+(2 if count>=2 else 1)]=''
  '''
  if index:
   ret=sys.argv[index+1] if count>1 else re.sub(r'^(-+)','' if removehyphen else r'\1',sys.argv[index]) if count==0 else True
   sys.argv[index:index+(2 if count>=2 else 1)]=[]
  return ret

 @staticmethod
 def webpageurl(http=False):
  return (r'http://' if http else '')+r'minhinc.42web.io'

 @staticmethod
 def push(*file,dir,push=False):
  data=None
  if not hasattr(Util.push,'file'):
   Util.push.file=[]
  count=[x for x in Util.push.file if x[1]==dir]
  count[0][0].extend(file) if count else Util.push.file.append([list(file),dir])
  print(f'<=>Util.push {Util.push.file=} {push=}')
  if push:
   for dir in Util.push.file:
    data=os.popen(r'~/tmp/ftp.sh ls '+dir[1]).read()
#    outputfile=' '.join([x for x in dir[0] if not re.search(x,data) or re.sub(r'^.*?(\d+)(?:\s+\w+){3}\s+'+x+r'\s*$',r'\1',data,flags=re.DOTALL) != re.sub(r'^.*?(\d+)(\s+\w+){3}\s+'+x+r'\s*$',r'\1',os.popen(r'ls -la '+x).read(),flags=re.M)])
    outputfile=' '.join([x for x in dir[0] if not re.search(x,data)])
    print(f'data ->{data=} {dir=} {outputfile=}')
    os.system(r'~/tmp/ftp.sh mput '+dir[1]+' '+outputfile) if outputfile else None
   [[os.system(f"cp {x} {os.path.expanduser('~')}/tmp/MISC/{dir[1]}") for x in dir[0]] for dir in Util.push.file] if push else None
   Util.push.file=[]
