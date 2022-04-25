import sys
import re
import os
DELIMITER='!ABS SBA!'
mode=''
data=''
filedata=''
backspace=None
file=[]
if len(sys.argv)==1:
 print(f'usage \npython3 fix <directory>\npython3 fix kivy/kivy/uix\npython3 fix kivy')
 sys.exit(-1)
if re.search(r'[.]pyx$',sys.argv[1]):
 file.extend(sys.argv[1:])
else:
 for i in os.walk(sys.argv[1]):
  for j in i[2]:
   file.append(i[0]+r'/'+j) if re.search(r'[.]pyx?$',j) else None
for k in file:
 with open(k) as file:
  filedata=re.sub(r'\n+',r'\n',re.sub(r'^\s*(#.*|)$',r'',(re.sub(DELIMITER,r"'''",re.sub(r'(?:^|\n)[ \t]*(\'\'\'|""").*?\1','',re.sub(r'((?:^|\n)[ \t]*\w+[^\n]*?)(?:\'\'\'|""")(.*?)(?:\'\'\'|""")',r'\1'+DELIMITER+r'\2'+DELIMITER,file.read(),flags=re.I|re.DOTALL),flags=re.I|re.DOTALL),flags=re.I|re.DOTALL) if re.search(r'[.]pyx$',k,flags=re.I) else file.read()),flags=re.I|re.M),flags=re.I|re.DOTALL)
 if re.search(r'.*[.]pyx$',k):
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
 with open(re.sub(r'^(.*[.])pyx$',r'\1'+'py',k),'w') as file:
  file.write(data)
 data=''
 print(k,re.sub(r'^(.*[.])pyx$',r'\1'+'py',k))
