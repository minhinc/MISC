from collections import OrderedDict
import re,os,sys
import shlex
import subprocess
import glob
def usage():
 print(f'''\
  --- usage ---
  Note - execute in 'package' parent directory,i.e. 'abc' if package='tkinter' /home/pi/tmp/.../abc/tkinter/..
  python3 pyreverse.py [--fix|--modify] <file|directory> [classname]
  python3 pyreverse.py [--fix|--modify] kivy/uix
  python3 pyreverse.py [--fix|--modify] kivy/uix/widget.py
  python3 pyreverse.py [--fix|--modify] kivy/uix/widget.py Widget\
''')
 sys.exit(-1)
usage() if len(sys.argv)==1 else None
fixarg=modifyarg=True
if [x for x in sys.argv if re.search(r'--fix',x)]:
 fixarg=True
 modifyarg=False
 sys.argv[sys.argv.index(r'--fix'):sys.argv.index(r'--fix')+1]=''
if [x for x in sys.argv if re.search(r'--modify',x)]:
 fixarg=False
 modifyarg=True
 sys.argv[sys.argv.index(r'--modify'):sys.argv.index(r'--modify')+1]=''
class fix:
 def __init__(self):
  super(fix,self).__init__()
  if len(sys.argv)>2:
   print(f'<=>fix.__init__ sys.argv={sys.argv}\n----only one argument supported in fix-----\n',usage())
  print(f'------- FIX has been initiated at dir {sys.argv[1]} --------')
  DELIMITER='!ABS SBA!'
  mode=''
  data=''
  filedata=''
  backspace=None
  file=[]
  if re.search(r'[.](pyx|pxi)$',sys.argv[1]):
   file.extend(sys.argv[1:])
  else:
   for i in os.walk(sys.argv[1]):
    for j in i[2]:
     file.append(i[0]+r'/'+j) if re.search(r'[.](pyx|pxi)?$',j) else None
  for k in file:
   with open(k) as file:
    filedata=re.sub(r'\n+',r'\n',re.sub(r'^\s*(#.*|)$',r'',(re.sub(DELIMITER,r"'''",re.sub(r'(?:^|\n)[ \t]*(\'\'\'|""").*?\1','',re.sub(r'((?:^|\n)[ \t]*\w+[^\n]*?)(?:\'\'\'|""")(.*?)(?:\'\'\'|""")',r'\1'+DELIMITER+r'\2'+DELIMITER,file.read(),flags=re.I|re.DOTALL),flags=re.I|re.DOTALL),flags=re.I|re.DOTALL) if re.search(r'[.](pyx|pxi)$',k,flags=re.I) else file.read()),flags=re.I|re.M),flags=re.I|re.DOTALL)
   if re.search(r'.*[.](pyx|pxi)$',k):
    for i in re.findall(r'(?:^|\n)([ \t]*(?:cp?)?def(?:[ \t]\w+)+[ \t]*\([^)]*?\)[^\n:]*?:)',filedata,flags=re.DOTALL):
     if not re.search(r'^\s*cp?def\s+class\s+',i):
      j=','.join(re.findall(r'('+(r'[*]*' if not re.search(r'^\s*cp?def\s+',i) else '')+r'\w+)(?:=.*?)?[),]',re.sub(r'\n+','',i,flags=re.DOTALL)))
      j=re.sub(r'^(\s*)((?:cp?)?def).*?(\w+)\s*\(.*',r'\1def \3'+(r'_'+r'\2' if re.search(r'^\s*cp?def\s+',i) else '')+r'('+j+r'):pass',i,flags=re.DOTALL)
      filedata=re.sub(re.escape(i)+r'[^\n]*(\n|$)',j+r'\1',filedata,flags=re.DOTALL)
    filedata=re.sub(r'(?P<id1>^|\n)(?P<id2>(?:c?import\s+|from\s+)[^\n]+\n(?:\s+[^\n]+\n)+)',lambda m:m.group('id1')+re.sub('\n+','',m.group('id2'),flags=re.DOTALL)+'\n',filedata,flags=re.DOTALL)
    filedata=re.sub(r'(?P<id1>^|\n)(?:cp?def\s+)?(?P<id2>class\s+[^:]+:[^\n]*)',lambda m:m.group('id1')+re.sub('\n+','',m.group('id2'),flags=re.DOTALL)+r'pass' if not re.search(r':\s*pass\s*',m.group('id2'),flags=re.DOTALL) and re.search(re.escape(m.group('id2'))+r'(?=\n(\S|\s+pass))',filedata,flags=re.DOTALL) else m.group('id1')+re.sub('\n+','',m.group('id2'),flags=re.DOTALL),filedata,flags=re.DOTALL)
    filedata=re.sub(r'(?P<id>^|\n)(?P<id2>\s*@[^\n(]+\([^)]+\)[^\n]*)(?=\n)',lambda m:m.group('id')+re.sub(r"'\s*'",r'',re.sub(r'\n+','',m.group('id2'),flags=re.DOTALL)),filedata,flags=re.DOTALL)
    for i in re.split('\n',filedata):
     if not re.search(r'^\s+',i) and re.search(r'\bclass\s+[^\n]+\n$',data,flags=re.DOTALL) and not re.search(r':pass\n$',data,flags=re.DOTALL):
      data=re.sub('\n$','pass\n',data,flags=re.DOTALL)
     if re.search(r'^(c?import|(?:cp?def\s+)?class\s+|from\s+)',i):
      data+=re.sub(r'cimport','import',i)+'\n'
     elif re.search(r'^\s*def\s+',i):
      if re.search(r'(^|\n)class\s+[^\n]+\n$',data,flags=re.DOTALL) and not re.search(r':\s*pass[^\n]*\n$',data,flags=re.DOTALL):
       mode=re.sub(r'^(\s*).*',r'\1',i)
      if re.sub(r'^(\s*).*',r'\1',i)==mode:#definition signature
       data+=i+'\n'
     elif re.sub(r'^(\s*)@.*',r'\1',i)==mode or re.search(r'^@',i):
      data+=i+'\n'
     elif not re.search(r'^\s+',i):
      mode=re.sub(r'^(\s*).*',r'\1',i)
    mode=''
   elif re.search(r'.*[.]py$',k):
    for i in re.split('\n',filedata):
     if re.search(r'=\s*\w+\s*\(\s*["\']\w+["\']\s*,\s*\(.*?\).*?{.*?}.*\)',i):
      base=re.sub(r'^\s*(.*?)\s*=\s*(.*?)\s*\(\s*["\']\s*(\w+)\s*["\']\s*,\s*\((.*?)[, ]*\).*$',r'\1'+DELIMITER+r'\2'+DELIMITER+r'\3'+DELIMITER+r'\4',i)
      data+='class '+re.split(DELIMITER,base)[0]+r'('+re.split(DELIMITER,base)[3]+r',metaclass='+re.split(DELIMITER,base)[1]+r'):pass'+'\n'
     else:
      data+=i+'\n'
   with open(re.sub(r'^(.*[.])(pyx|pxi)$',r'\1'+'py',k),'w') as file:
    file.write(data)
   data=''
   print(k,re.sub(r'^(.*[.])(pyx|pxi)$',r'\1'+'py',k))
  print(f'---- FIX FINIESHED dir={sys.argv[1]} ------')

class modify:
 def __init__(self):
  print(f'---- MODIFY INITIATED dir={sys.argv[1:]} ----')
  DELIMITER='!ABS SBA!'
  wrongfile=open('wrongfile.txt','w')
  file=filek=[]
  data=datak=tarray=None
  package=None
  baseclassnumber=classnumber=None
  deriveclass={}
  DELIMITER='!ABS SBA!'
  def classname(filename,hint=None):
   if hint==None:
    return re.findall(r'^class\s+(.+?)\b.*:\s*(?:pass\s*|#.*)?$',open(filename).read(),flags=re.M)
   else:
    return re.findall(r'^class\s+('+hint+r')\b.*:\s*$',open(filename).read(),flags=re.I|re.M)
  if re.search(r'[.]py$',sys.argv[1]):
   if len(sys.argv)==3 and not re.search(r'[.]py$',sys.argv[2]):
    file=[(sys.argv[1],sys.argv[2])] if sys.argv[2]!='=' else [(sys.argv[1],classname(sys.argv[1],re.sub(r'.*/(.*?)[.]py$',r'\1',sys.argv[1]))[0])]
   else:
    for i in sys.argv[1:]:
     for k in classname(i):
      file.append((i,k))
  else:
   for i in os.walk(sys.argv[1]):
    for j in [j for j in i[2] if re.search(r'[.]py$',j)]:
     for k in classname(i[0]+r'/'+j,re.sub(r'(.*?)[.]py$',r'\1',j) if len(sys.argv)==3 and sys.argv[2]=='=' else None):
      file.append((i[0]+r'/'+j,k))
  filek=file
  file=[i for i in file if not os.path.exists(r'./'+re.sub(r'/+',r'.',re.sub(r'(.*?)(?:/?__init__)?[.]py$',r'\1',i[0]))+r'.'+i[1]+'.dot')]
  print(f'list of file,class to be processed (.dot file do not exists)={file}')
  for count,i in enumerate(file):
   print(fr'file,class={i} {count+1}/{len(file)}')
   if subprocess.call(shlex.split('pyreverse3 -f ALL '+i[0]+r' -ASmy -c '+i[1])):
    wrongfile.write(rf'{i}'+'\n');wrongfile.flush()
    continue 
   data=open(i[1]+r'.dot').read()
   classdata=re.sub(r'.*label="{('+re.sub(r'/+',r'.',re.sub(r'(?:/?__init__)?[.]py$','',i[0]))+r'.'+i[1]+r'\b.*?)}".*',r'\1',data,flags=re.I|re.DOTALL)
  # classnumber=re.sub(r'.*\n("\d+")\s+\[label="{'+re.sub(r'/+',r'.',re.sub(r'(?:/?__init__)?[.]py$','',i[0]))+r'.'+i[1]+r'\b.*',r'\1',data,flags=re.I|re.DOTALL)
  # print(f'classnumber={classnumber}')
  # data=re.sub('\n+','\n',re.sub(r'^\s*"\d+"\s*->\s*'+classnumber+r'\s*\[arrowhead="empty".*$',r'',data,flags=re.I|re.M),flags=re.DOTALL)
   data=re.sub(r'^(.*label="){(.*?)\|.*}(".*)',r'\1\2\3',data,flags=re.I|re.M)
   print(f'classdata={classdata}')
   data=re.sub(r'^(.*label=)"('+re.split(r'\|',classdata)[0]+r')\b.*?"(, shape=.*)$',r'\1'+r'<<TABLE border="0" cellborder="0"><TR><TD colspan="2">'+r'\2'+r'</TD></TR><TR><TD valign="top">'+(r'<FONT POINT-SIZE="4"><BR />'+r'<BR ALIGN="LEFT" />'.join(re.split(r'\\l',re.split(r'\|',classdata)[1]))+r'</FONT>' if ''.join(re.split(r'\\l',re.split(r'\|',classdata)[1])) else '')+r'</TD><TD valign="top">'+(r'<FONT POINT-SIZE="4">'+r'<BR ALIGN="LEFT" />'.join(re.split(r'\\l',re.split(r'\|',classdata)[2]))+r'</FONT>' if ''.join(re.split(r'\\l',re.split(r'\|',classdata)[2])) else '')+r'</TD></TR></TABLE>>'+r',color="red"'+r'\3',data,flags=re.I|re.DOTALL)
  # print(f'data2 data={data}')
   for property in re.findall(r'^\s*("\d+")\s+\[label="kivy[.]properties[.]',data,flags=re.I|re.M):
    data=re.sub(r'\n+','\n',re.sub(fr'^{property}\s+->\s+"\d+"\s+\[arrowhead="diamond".*$',r'',data,flags=re.I|re.M),flags=re.I|re.DOTALL)
    if not re.search(fr'^\s*({property}\s+->\s+"\d+"|"\d+"\s+->\s+{property})\s+\[arrowhead="empty"',data,flags=re.I|re.M) or not re.search(r'^kivy[.]properties',re.sub(r'/+','.',re.sub(r'[.]py$','',i[0])+r'/'+i[1])):
     data=re.sub(r'\n+','\n',re.sub(fr'^(|.*?\s+->)\s*{property}.*$',r'',data,flags=re.I|re.M),flags=re.I|re.DOTALL)
   open(i[1]+'.dot','w').write('\n'.join(list(OrderedDict.fromkeys(re.split('\n',data)))))
  # os.rename(i[1]+'.dot',re.sub(r'/+',r'.',re.sub(r'(.*)[.]py$',r'\1',i[0]))+r'.'+i[1]+'.dot')
   os.rename(i[1]+'.dot',re.sub(r'/+',r'.',re.sub(r'(.*?)(?:/?__init__)?[.]py$',r'\1',i[0]))+r'.'+i[1]+'.dot')
  wrongfile.close()
  def fixderiveclass(package):
   nonlocal deriveclass
   tarray=[]
   datak=''
   if not package in deriveclass:
    for k in [k for k in re.split('\n',os.popen(r'egrep -le "\[label=\"'+package+r'\"" *.dot').read()) if k]:
     datak=open(k).read()
     if re.search(r'\n"\d+"\s+\[label="'+package+r'"',datak,flags=re.I|re.DOTALL):
      baseclassnumber=re.sub(r'.*\n("\d+")\s+\[label="'+package+r'".*',r'\1',datak,flags=re.I|re.DOTALL)
      classnumber,classname=re.split(DELIMITER,re.sub(r'.*\n("\d+")\s+\[label=<<TABLE.*?<TD.*?>(.*?)</TD>.*',r'\1'+DELIMITER+r'\2',datak,flags=re.I|re.DOTALL))
      if re.search(r'.*\n'+classnumber+'\s+->\s+'+baseclassnumber+'\s+\[arrowhead="empty".*',datak,flags=re.I|re.DOTALL):
       tarray.append(re.sub(r'(.*)[.]dot',r'\1',k))
       fixderiveclass(re.sub(r'(.*)[.]dot',r'\1',k))
    if tarray:
     deriveclass[package]=tarray
  for count,i in enumerate(filek):
   print(f'fixing subclass i={i} {count+1}/{len(filek)}')
  # package=re.sub(r'/+',r'.',re.sub(r'(.*)[.]py$',r'\1',i[0]))+r'.'+i[1]
   package=re.sub(r'/+',r'.',re.sub(r'(.*?)(?:/?__init__)?[.]py$',r'\1',i[0]))+r'.'+i[1]
   tarray=[]
   datak=''
   fixderiveclass(package)
  print(f'deriveclass={deriveclass}')
  def deriveclassrecursivestring(package,space):
   derivestring=''
   for k in deriveclass[package]:
     derivestring+=r'<BR ALIGN="LEFT" /><FONT POINT-SIZE="'+str(max(2,6-len(space)))+r'"'+(r' COLOR="red">' if k in deriveclass else '>')+space*int(6/max(3,6-len(space))+0.5)+k+r'</FONT>'
     if k in deriveclass:
      derivestring+=deriveclassrecursivestring(k,space+'  ')
   return derivestring
  for count,i in enumerate(filek):
  # package=re.sub(r'/+',r'.',re.sub(r'(.*)[.]py$',r'\1',i[0]))+r'.'+i[1]
   package=re.sub(r'/+',r'.',re.sub(r'(.*?)(?:/?__init__)?[.]py$',r'\1',i[0]))+r'.'+i[1]
   if not os.path.exists(r'./'+package+r'.dot'):
    continue
   print(fr'writing to file {package}.dot_ {count+1}/{len(filek)}')
   with open(package+'.dot') as fp:
    data=fp.read()
   if package in deriveclass:
    data=re.sub(r'(.*)}\s*$',r'\1',data,flags=re.I|re.DOTALL)
    biggestnumber=str(max(int(x) for x in re.findall(r'^"(\d+)"\s+\[.*?label=["<]',data,flags=re.I|re.M))+1)
    classnumber=re.sub(r'.*\n"(\d+)"\s+\[label=<<TABLE.*',r'\1',data,flags=re.I|re.DOTALL)
    data+='\n'+r'"'+biggestnumber+r'" [label=<<TABLE border="0"><TR><TD>'+deriveclassrecursivestring(package,"")+r'<BR ALIGN="LEFT" /></TD></TR></TABLE>>, shape="record"];'
    data+='\n'+r'"'+biggestnumber+r'" -> "'+classnumber+r'" [arrowhead="empty", arrowtail="none"];'+'\n}'
   with open(package+r'.dot_','w') as fp:
    fp.write(data)
   subprocess.call(shlex.split(r'dot -Tpdf '+package+'.dot_ -o '+package+'.pdf'))
  print(f'---- MODIFY FINISHED dir={sys.argv[1:]}')
fix() if fixarg else None
modify() if modifyarg else None
