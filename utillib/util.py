from PyPDF2 import PdfFileWriter, PdfFileReader, PdfFileMerger
import io,os,re
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

class Util:
 def __init__(self):
  super(Util,self).__init__()
 def concatpdf(self,dir):
  merger=PdfFileMerger()
  for count,i in enumerate(sorted([i for i in os.listdir(dir) if os.path.isfile(dir+r'/'+i) and re.search(r'[.]pdf$',i,flags=re.I)],key=str.lower)):
   print('processing i ->',i)
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
  print(r'generating '+dir+r'/output/pyreverse.pdf ...')
  if not os.path.exists(dir+r'/output'):
   os.mkdir(dir+r'/output')
  merger.write(dir+r'/output/pyreverse.pdf')
  merger.close()
  print(r'deleting all '+dir+r'/*_tmp.pdf files...')
  os.system(r'rm '+dir+r'/*_tmp.pdf')
