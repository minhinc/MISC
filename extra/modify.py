from collections import OrderedDict
import re,os,sys
import shlex
import subprocess
import glob
if len(sys.argv)==1:
 print(f'usage \n \
python3 modify.py <file|directory> [classname] \n \
python3 modify.py kivy/uix/widget.py Widget \n \
python3 modify.py kivy/uix = \n \
python3 modify.py kivy/uix')
 sys.exit(-1)
wrongfile=open('wrongfile.txt','w')
file=filek=[]
data=datak=tarray=None
package=None
baseclassnumber=classnumber=None
deriveclass={}
DELIMITER='!ABS SBA!'
def classname(filename,hint=None):
# print(f'filename={filename} hint={hint}')
 if hint==None:
#  return re.findall(r'^class\s+(.+?)\b.*:\s*(?:pass\s*)?$',open(filename).read(),flags=re.I|re.M)
  return re.findall(r'^class\s+(.+?)\b.*:\s*(?:pass\s*|#.*)?$',open(filename).read(),flags=re.M)
 else:
  return re.findall(r'^class\s+('+hint+r')\b.*:\s*$',open(filename).read(),flags=re.I|re.M)
if re.search(r'[.]py$',sys.argv[1]):
 if len(sys.argv)==3:
  file=[(sys.argv[1],sys.argv[2])] if sys.argv[2]!='=' else [(sys.argv[1],classname(sys.argv[1],re.sub(r'.*/(.*?)[.]py$',r'\1',sys.argv[1]))[0])]
 else:
  for k in classname(sys.argv[1]):
   file.append((sys.argv[1],k))
else:
 for i in os.walk(sys.argv[1]):
  for j in [j for j in i[2] if re.search(r'[.]py$',j)]:
   for k in classname(i[0]+r'/'+j,re.sub(r'(.*?)[.]py$',r'\1',j) if len(sys.argv)==3 and sys.argv[2]=='=' else None):
    file.append((i[0]+r'/'+j,k))
filek=file
file=[i for i in file if not os.path.exists(r'./'+re.sub(r'/+',r'.',re.sub(r'(.*)[.]py$',r'\1',i[0]))+r'.'+i[1]+'.dot')]
print(f'file={file}')
for count,i in enumerate(file):
 print(fr'i={i} {count+1}/{len(file)}')
 if subprocess.call(shlex.split('pyreverse3 -f ALL '+i[0]+r' -ASmy -c '+i[1])):
  wrongfile.write(rf'{i}'+'\n');wrongfile.flush()
  continue 
 data=open(i[1]+r'.dot').read()
 classdata=re.sub(r'.*label="{('+re.sub(r'/+',r'.',re.sub(r'(?:/?__init__)?[.]py$','',i[0]))+r'.'+i[1]+r'\b.*?)}".*',r'\1',data,flags=re.I|re.DOTALL)
 data=re.sub(r'^(.*label="){(.*?)\|.*}(".*)',r'\1\2\3',data,flags=re.I|re.M)
 print(f'classdata={classdata}')
# subprocess.call(shlex.split('pyreverse3 -f ALL '+i[0]+r' -ASmy -c '+i[1]+r' -k'))
 data=re.sub(r'^(.*label=)"('+re.split(r'\|',classdata)[0]+r')\b.*?"(, shape=.*)$',r'\1'+r'<<TABLE border="0" cellborder="0"><TR><TD colspan="2">'+r'\2'+r'</TD></TR><TR><TD valign="top">'+(r'<FONT POINT-SIZE="4"><BR />'+r'<BR ALIGN="LEFT" />'.join(re.split(r'\\l',re.split(r'\|',classdata)[1]))+r'</FONT>' if ''.join(re.split(r'\\l',re.split(r'\|',classdata)[1])) else '')+r'</TD><TD valign="top">'+(r'<FONT POINT-SIZE="4">'+r'<BR ALIGN="LEFT" />'.join(re.split(r'\\l',re.split(r'\|',classdata)[2]))+r'</FONT>' if ''.join(re.split(r'\\l',re.split(r'\|',classdata)[2])) else '')+r'</TD></TR></TABLE>>'+r',color="red"'+r'\3',data,flags=re.I|re.DOTALL)
 for property in re.findall(r'^\s*("\d+") \[label="kivy[.]properties[.]',data,flags=re.I|re.M):
  data=re.sub(r'\n+','\n',re.sub(fr'^(|.*?\s+->)\s*{property}.*$',r'',data,flags=re.I|re.M),flags=re.I|re.DOTALL)
 open(i[1]+'.dot','w').write('\n'.join(list(OrderedDict.fromkeys(re.split('\n',data)))))
 os.rename(i[1]+'.dot',re.sub(r'/+',r'.',re.sub(r'(.*)[.]py$',r'\1',i[0]))+r'.'+i[1]+'.dot')
wrongfile.close()
def fixderiveclass(package):
 global deriveclass
 tarray=[]
 datak=''
 if not package in deriveclass:
  for k in [k for k in re.split('\n',os.popen(r'egrep -le "\[label=\"'+package+r'\"" *.dot').read()) if k]:
   datak=open(k).read()
   if re.search(r'\n"\d+"\s+\[label="'+package+r'"',datak,flags=re.I|re.DOTALL):
    baseclassnumber=re.sub(r'.*\n("\d+")\s+\[label="'+package+r'".*',r'\1',datak,flags=re.I|re.DOTALL)
    classnumber,classname=re.split(DELIMITER,re.sub(r'.*\n("\d+")\s+\[label=<<TABLE.*?<TD.*?>(.*?)</TD>.*',r'\1'+DELIMITER+r'\2',datak,flags=re.I|re.DOTALL))
    if re.search(r'.*\n'+classnumber+'\s+->\s+'+baseclassnumber+'\s+\[.*',datak,flags=re.I|re.DOTALL):
#     print(f'package={package} k={k} classnumber={classnumber} classname={classname}')
     tarray.append(re.sub(r'(.*)[.]dot',r'\1',k))
     fixderiveclass(re.sub(r'(.*)[.]dot',r'\1',k))
  if tarray:
   deriveclass[package]=tarray
for count,i in enumerate(filek):
 print(f'fixing subclass i={i} {count+1}/{len(filek)}')
 package=re.sub(r'/+',r'.',re.sub(r'(.*)[.]py$',r'\1',i[0]))+r'.'+i[1]
 tarray=[]
 datak=''
 '''
 for k in [k for k in re.split('\n',os.popen(r'egrep -le "\[label=\"'+package+r'\"" *.dot').read()) if k]:
  datak=open(k).read()
  if re.search(r'\n"\d+"\s+\[label="'+package+r'"',datak,flags=re.I|re.DOTALL):
   baseclassnumber=re.sub(r'.*\n("\d+")\s+\[label="'+package+r'".*',r'\1',datak,flags=re.I|re.DOTALL)
   classnumber=re.sub(r'.*\n("\d+")\s+\[label=<<TABLE.*',r'\1',datak,flags=re.I|re.DOTALL)
   if re.search(r'.*\n'+classnumber+'\s+->\s+'+baseclassnumber+'\s+\[.*',datak,flags=re.I|re.DOTALL):
    tarray.append(re.sub(r'(.*)[.]dot',r'\1',k))
 if tarray:
  deriveclass[package]=tarray
 '''
 fixderiveclass(package)
print(f'deriveclass={deriveclass}')
def settlederiveclass(package,classnumber,createnode=False):
# print(f'settlederiveclass package={package} classnumber={classnumber}createnode={createnode}')
 global deriveclass,data
 if createnode:
  biggestnumber=str(max(int(x) for x in re.findall(r'^"(\d+)"\s+\[.*?label=["<]',data,flags=re.I|re.M))+1)
  data+='\n'+r'"'+biggestnumber+r'" [label=<<TABLE border="0"><TR><TD>'+package+r'</TD></TR></TABLE>>,shape="record"];'
  data+='\n'+r'"'+biggestnumber+r'" -> "'+classnumber+r'" [arrowhead="empty", arrowtail="none"];'
 if [x for x in deriveclass[package] if not x in deriveclass]:
  biggestnumber=str(max(int(x) for x in re.findall(r'^"(\d+)"\s+\[.*?label=["<]',data,flags=re.I|re.M))+1)
  data+='\n'+r'"'+biggestnumber+r'" [label=<<TABLE border="0"><TR><TD><FONT POINT-SIZE="4"><BR />'+r'<BR ALIGN="LEFT" />'.join((r'<FONT COLOR="red">'+x+r'</FONT>' if x in deriveclass else x for x in deriveclass[package]))+r'<BR ALIGN="LEFT" /></FONT></TD></TR></TABLE>>, shape="record"];'
  data+='\n'+r'"'+biggestnumber+r'" -> "'+(classnumber if createnode==False else str(int(biggestnumber)-1))+r'" [arrowhead="empty", arrowtail="none"];'
 for k in [k for k in deriveclass[package] if k in deriveclass]:
  settlederiveclass(k,classnumber if createnode==False else str(int(biggestnumber)-(1 if [x for x in deriveclass[package] if not x in deriveclass] else 0)),createnode=True)
def deriveclassrecursivestring(package,space):
 derivestring=''
 for k in deriveclass[package]:
   derivestring+=r'<BR ALIGN="LEFT" /><FONT POINT-SIZE="'+str(max(2,6-len(space)))+r'"'+(r' COLOR="red">' if k in deriveclass else '>')+space*int(6/max(3,6-len(space))+0.5)+k+r'</FONT>'
   if k in deriveclass:
    derivestring+=deriveclassrecursivestring(k,space+'  ')
 return derivestring
for count,i in enumerate(filek):
 package=re.sub(r'/+',r'.',re.sub(r'(.*)[.]py$',r'\1',i[0]))+r'.'+i[1]
 if not os.path.exists(r'./'+package+r'.dot'):
  continue
 print(fr'writing to file {package}.dot_ {count+1}/{len(filek)}')
 with open(package+'.dot') as fp:
  data=fp.read()
 if package in deriveclass:
  data=re.sub(r'(.*)}\s*$',r'\1',data,flags=re.I|re.DOTALL)
  biggestnumber=str(max(int(x) for x in re.findall(r'^"(\d+)"\s+\[.*?label=["<]',data,flags=re.I|re.M))+1)
  classnumber=re.sub(r'.*\n"(\d+)"\s+\[label=<<TABLE.*',r'\1',data,flags=re.I|re.DOTALL)
#  data+='\n'+r'"'+biggestnumber+r'" [label=<<TABLE border="0"><TR><TD><FONT POINT-SIZE="4"><BR />'+r'<BR ALIGN="LEFT" />'.join((r'<FONT COLOR="red">'+x+r'</FONT>' if x in deriveclass else x for x in deriveclass[package]))+r'<BR ALIGN="LEFT" /></FONT></TD></TR></TABLE>>, shape="record"];'
#  settlederiveclass(package,classnumber,createnode=False)
#  print(f'{deriveclassrecursivestring(package,"")}')
  data+='\n'+r'"'+biggestnumber+r'" [label=<<TABLE border="0"><TR><TD>'+deriveclassrecursivestring(package,"")+r'<BR ALIGN="LEFT" /></TD></TR></TABLE>>, shape="record"];'
  data+='\n'+r'"'+biggestnumber+r'" -> "'+classnumber+r'" [arrowhead="empty", arrowtail="none"];'+'\n}'
#  data+='\n'+r'"'+biggestnumber+r'" -> '+classnumber+r' [arrowhead="empty", arrowtail="none"];'+'\n}'
#  data+='\n}'
#  print(f'data={data}')
 with open(package+r'.dot_','w') as fp:
  fp.write(data)
 subprocess.call(shlex.split(r'dot -Tpdf '+package+'.dot_ -o '+package+'.pdf'))
# [os.remove(x) for x in glob.glob(r'*.dot_*')]
