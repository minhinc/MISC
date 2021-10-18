import re,os,sys,subprocess
from PyPDF2 import PdfFileWriter, PdfFileReader, PdfFileMerger
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
if len(sys.argv)<2:
 print('-----usage-----\npython3 class.py [qt|qml]')
 sys.exit(-1)

qmllist=list();qmldict=dict()
outputfile='pyreverse'
merger=PdfFileMerger()
classesdotfile=None
for i in [i for i in os.listdir('.') if os.path.isfile(i) and re.search(r'[.]txt$',i,flags=re.I)]:
 if sys.argv[1]=='qml':
  value=re.sub(r'^.*\n\s*-\s*(\w+)\s*QML\s*.*?\n\s*Contents\s*\n.*',r'\1',open(i).read(),flags=re.I|re.DOTALL)
 else:
  value=re.sub(r'^.*?\n[ \-]*(\w+)\n.*?\n\s*Contents\s*\n.*',r'\1',open(i).read(),flags=re.I|re.DOTALL)
 if value in qmldict:
  print('duplicate ->',[x['file'] for x in qmldict[value]],i,value)
 else:
  qmldict[value]=list()
 donkey=dict()
 if re.search('^.*?------.*?\n(.*?)--------\+?\n\n.*',open(i).read(),flags=re.I|re.DOTALL):
  for x in [re.sub(r'^\s*(.*?)\s*$',r'\1',x) for x in re.split('\n',re.sub('^.*?------.*?\n(.*?)--------\+?\n\n.*',r'\1',open(i).read(),flags=re.I|re.DOTALL)) if not re.search(r'^[ \-\+]+$',x) and re.search(r'^(\s+|\|\s+)\w+:',x)]:
   key,keyvalue=[re.sub(r'^(?:\s|\|)*(.*?)(?:\s|\|)*$',r'\1',ii) for ii in re.split(r':\s',x) if ii]
   donkey.__setitem__(key,[re.sub(r'^\s*(\w+).*',r'\1',re.sub(r'^.*::(.*)$',r'\1',x)) for x in re.split(r'(?:,|\sand)',keyvalue) if x])
  qmldict[value].append(donkey)
  if sys.argv[1]=='qml':
   qmldict[value][-1]['properties']=r'<FONT POINT-SIZE="2"><BR />'+r'<BR ALIGN="LEFT" />'.join(re.split('\n',re.sub('\n[\s|\-\+]*\n','\n',re.sub(r'\|',r'\|',re.sub(r'<',r'&lt;',re.sub(r'>',r'&gt;',re.sub(r'&',r'&amp;',re.sub(r'^.*?\n[ \-]*List of all members, including inherited members\n(.*?)\n[ \-]*Detailed Description.*',r'\1',open(i).read(),flags=re.I|re.DOTALL))))),flags=re.MULTILINE)))+r'</FONT>>' if re.search(r'^.*?\n[ -]*List of all members, including inherited members\n.*?\n[ \-]*Detailed Description.*$',open(i).read(),flags=re.I|re.DOTALL) else ''
  else:
   qmldict[value][-1]['properties']=r'<FONT POINT-SIZE="2"><BR />'+r'<BR ALIGN="LEFT" />'.join(re.split('\n',re.sub('\n[\s|\-\+]*\n','\n',re.sub(r'\|',r'\|',re.sub(r'<',r'&lt;',re.sub(r'>',r'&gt;',re.sub(r'&',r'&amp;',re.sub(r'^.*?\n(Properties\n.*?\w+.*?)\n[ ]*\n.*',r'\1',open(i).read(),flags=re.DOTALL))))),flags=re.MULTILINE)))+r'</FONT>>' if re.search(r'^.*?\nProperties\n.*.*$',open(i).read(),flags=re.DOTALL) else ''
  qmldict[value][-1]['file']=i
  
qmllist=list(qmldict.keys())
for key in qmldict:
 def getdeplist(key):
  for y in (y for x in qmldict.get(key,[]) for y in x.get('Inherits',[])):
   if y in qmllist:
    if qmllist.index(key)<qmllist.index(y):
     qmllist.remove(y)
     qmllist.insert(qmllist.index(key),y)
   else:
    qmllist.insert(qmllist.index(key),y)
  [getdeplist(y) for x in qmldict.get(key,[]) for y in x.get('Inherits',[])]
 getdeplist(key)
with open(outputfile+sys.argv[1]+'.py','w') as file:
 if sys.argv[1]=='qml':
  os.environ['PYTHONPATH']=os.getcwd()+r'/../qt/'
  file.write('from '+outputfile+'qt import *\n')
 for key in qmllist:
  if key not in qmldict:
   file.write('class '+key+':\n pass\n')
   continue
  for count in range(len(qmldict[key])):
   addstring='' if not count else r'_'+str(count)+r'_'
   baseclass=[ x+(r'_'+str(count1)+r'_' if count1 else '') for x in qmldict[key][count].get('Inherits',[]) for count1 in range(len(qmldict.get(x,[])))]
#   print('key,baseclass->',key,baseclass) if len(baseclass)>1 else ''
   file.write('class '+key+addstring+('('+','.join(baseclass)+')' if baseclass else '')+':\n '+('Instantiates='+','.join(qmldict[key][count]['Instantiates']) if sys.argv[1]=='qml' and 'Instantiates' in qmldict[key][count] else 'pass')+'\n')

print('deleting ./image/ dir. generating ./image/*.dot files ...')
os.system(r'rm -rf image')
os.makedirs(os.getcwd()+r'/image/',exist_ok=True)
subprocess.run(r'pyreverse '+outputfile+sys.argv[1]+'.py -ASmn -k',shell=True, cwd = os.getcwd(), env=os.environ)
classesdotfile=open(r'classes.dot').read()
subprocess.run(r'pyreverse ../'+outputfile+sys.argv[1]+'.py -ASmn -c '+' -c '.join([x+(r'_'+str(count)+r'_' if count else '') for x in qmllist for count in range(len(qmldict.get(x,['junk'])))])+' -k',shell=True, cwd=os.getcwd()+r'/image/',env=os.environ)

print('generating ./image/*.pdf files...')
for i in [i for i in os.listdir(r'./image/') if os.path.isfile(r'./image/'+i) and re.search(r'[.]dot$',i,flags=re.I)]:
 filedata=open(r'./image/'+i).read()
 key=re.sub(r'^(.*?)(?:_\d_+)?[.]dot$',r'\1',i)
 count=int(re.sub(r'^.*?_(\d+)_[.]dot$',r'\1',i)) if re.search(r'_\d+_[.]dot$',i) else 0
# print('i,key,count->',i,key,count)
######## BEGIN subclass printing #######
 classname=re.sub(r'^(.*?)[.]dot$',r'\1',i)
 keynumber=re.findall(r'"(\d+)"[ ]*.*?label="'+classname+r'"',classesdotfile)[0]
 depnumber=re.findall(r'"(\d+)"[ ]*->[ ]*"'+keynumber+r'"[ ]*\[arrowhead="empty"',classesdotfile) or []
 depclass=[re.findall(r'"'+x+r'"[ ]*\[.*?label="(.*?)"',classesdotfile)[0] for x in depnumber]
 keynumber=re.findall(r'"(\d+)"[ ]*.*?label="'+classname+r'"',filedata)[0]
 lastnumber=re.sub(r'^.*\n\s*"(\d+)"[ ]*\[.*?label=".*?".*$',r'\1',filedata,flags=re.DOTALL)
 filedata=re.sub(r'^(?P<id>.*shape="record"];\n)',lambda m:m.group('id')+'"'+str(int(lastnumber)+1)+r'" [label=<<FONT POINT-SIZE="2"><BR />'+r'<BR ALIGN="LEFT" />'.join(depclass)+r'<BR ALIGN="LEFT" /></FONT>>, shape="record"];'+'\n"'+str(int(lastnumber)+1)+r'" -> "'+str(keynumber)+r'" [arrowhead="empty", arrowtail="none"];'+'\n',filedata,flags=re.DOTALL) if depclass else filedata
 print('classname,depnumber,depclass,keynumber,lastnumber',classname,depnumber,depclass,keynumber,lastnumber)
############ END ###########
 propertiesdata=r'<'+re.sub(r'^(.*?)[.]dot$',r'\1',i)+qmldict[key][count]['properties'] if key in qmldict and qmldict[key][count]['properties'] else r'"'+re.sub(r'^(.*?)[.]dot$',r'\1',i)+r'"'
 filedata=re.sub(r'^(?P<id1>.*?label=)"(?P<id2>'+re.sub(r'^(.*?)[.]dot$',r'\1',i)+r')"(?P<id3>.*?)(?P<id4>\];\n.*)$',lambda m:m.group('id1')+propertiesdata+m.group('id3')+', color="red"'+m.group('id4'),filedata,flags=re.I|re.DOTALL)
 with open(r'./image/'+i,'w') as file:
  file.write(filedata)
 subprocess.run(r'dot -Tpdf '+i+' -o '+re.sub(r'^(.*?)[.]dot$',r'\1',i)+'.pdf',shell=True, cwd=os.getcwd()+r'/image/')

print('processing ./image/*.pdf file ...')
for count,i in enumerate(sorted([i for i in os.listdir(r'./image/') if os.path.isfile(r'./image/'+i) and re.search(r'[.]pdf$',i,flags=re.I)],key=str.lower)):
 print('processing i ->',i)
 classname=re.sub(r'^(.*?)[.]pdf',r'\1',i)
 packet = io.BytesIO()
 existing_pdf = PdfFileReader(open(r'./image/'+i, "rb"))
 can = canvas.Canvas(packet, pagesize=letter)
 can.setFont('Helvetica-Bold', 8)
# can.drawString((existing_pdf.getPage(0).mediaBox[2]-4*len(classname))//2, 10, r'<'+classname+r'>')
 can.drawString((existing_pdf.getPage(0).mediaBox[2]-4*len(classname))//2, 10, r'<'+classname+r'>'+('_0_' if os.path.isfile(r'./image/'+classname+'_1_.pdf') else ''))
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
 outputStream = open(r'./image/'+classname+r'_tmp.pdf', "wb")
 output.write(outputStream)
 outputStream.close()
 merger.append(PdfFileReader(open(r'./image/'+classname+'_tmp.pdf','rb')))
print(r'generating ./image/'+outputfile+sys.argv[1]+'.pdf ...')
merger.write(r'./image/'+outputfile+sys.argv[1]+'.pdf')
merger.close()
print('deleting all ./image/*.dot ./image/*_tmp.pdf files...')
#os.system(r'rm ./image/*.dot')
os.system(r'rm ./image/*_tmp.pdf')
