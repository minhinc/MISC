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
for i in os.walk(sys.argv[1]):
 for j in i[2]:
  file.append(i[0]+r'/'+j) if re.search(r'[.]pyx?$',j) else None
#for i in file:
# print(i)
for k in file:
 with open(k) as file:
  filedata=re.sub(r'\n+',r'\n',re.sub(r'^\s*(#.*|)$',r'',(re.sub(DELIMITER,r"'''",re.sub(r'(?:^|\n)[ \t]*(\'\'\'|""").*?\1','',re.sub(r'((?:^|\n)[ \t]*\w+[^\n]*?)(?:\'\'\'|""")(.*?)(?:\'\'\'|""")',r'\1'+DELIMITER+r'\2'+DELIMITER,file.read(),flags=re.I|re.DOTALL),flags=re.I|re.DOTALL),flags=re.I|re.DOTALL) if re.search(r'[.]pyx$',k,flags=re.I) else file.read()),flags=re.I|re.M),flags=re.I|re.DOTALL)
#  filedata=re.sub(r'\n+',r'\n',re.sub(r'^\s*(#.*|)$',r'',file.read(),flags=re.I|re.M),flags=re.I|re.DOTALL)
 if re.search(r'.*[.]pyx$',k):
  for i in re.split('\n',filedata):
   if re.search(r'^(cdef\s+)?class\s+.*:\s*(?:pass|#.*)?\s*$',i):
    data+=(' pass\n' if mode=='class' else '')+re.sub(r'^cdef ','',i)+'\n'
    if not re.search(r':\s*pass\s*$',i):
     mode='class'
   elif re.search(r'^\s*(cp?)?def\s+\w+\s*\(.*',i) and not re.search(r'^\s*(?:cdef\s+)?class\s+\w+',i) and not re.search(r'\s+except\s+',i) or re.search(r'^\s*def',mode):
    if mode=='class':
     if not re.search(r'^\s+',i):#global function
      data+=' pass\n'
     mode=re.sub(r'^(\s*).*',r'\1',i)
    elif not re.search(r'^\s+',i) and not re.search(r'^\s*def',mode):#global function
     mode=re.sub(r'^(\s*).*',r'\1',i)
    if re.sub(r'^(\s*).*',r'\1',i)==mode:#definition signature
     i=re.sub(r'^(\s*)(cp?def)(\s+\w+)(.*:?).*',r'\1'+r'def\3'+r'_'+r'\2\4',i)
     i=re.sub(r':\s*#.*$',r':',i)
     data+=re.sub(r'([(,]\s*)([\w*]+)\s+[\w*]+',r'\1\2',i)
     if re.search(r'\(',i) and not re.search(r'\)',i):
      mode+='def'
     else:
      data+='pass'
     data+='\n'
    elif re.search(r'^\s*def',mode):#mulitiline definition nextline
     if re.search(r'\)\s*:\s*($|#)',i):
      i=re.sub(r'^(.*:).*',r'\1',i)
      data+=re.sub(r'([\w*]+)\s+[\w*]+',r'\1',i)+'pass'+'\n'
      mode=re.sub(r'^(\s*)def',r'\1',mode)
     elif not re.search(r'^\s*(cp?)?def\s+\w+\s*\(',i):
      data+=re.sub(r'([\w*]+)\s+[\w*]+',r'\1',i)+'\n'
   elif mode=='tuple' or re.search(r'^c?import\s+',i) or re.search(r'^from\s+\S+\s+c?import',i):
    if mode=='class':
     data+=' pass\n'
    data+=re.sub(r'cimport','import',i)+'\n'
    if re.search(r'\(',i) and not re.search(r'\)',i):
     mode='tuple'
    elif mode=='tuple' and re.search(r'\)',i):
     mode=''
   elif re.search(r'^\s*@',i):
    if mode=='class' and not re.search(r'^\s+',i):#global decorator following class
     data+=' pass\n'
     mode=re.sub(r'^(\s*)@.*',r'\1',i)
    data+=i+'\n'
   elif re.search(r'@[^\n]+\n$',data,re.I|re.DOTALL):
    data=re.sub(r'(.*)\s*@.*',r'\1',data)
  mode=''
  data=re.sub(r'\b(class|def)(\s+[^\n]+:)\s*$',r'\1\2'+'pass',data,flags=re.I|re.DOTALL)
 elif re.search(r'.*[.]py$',k):
  for i in re.split('\n',filedata):
#   adjustemptytag(i)
   if re.search(r'=\s*\w+\s*\(\s*["\']\w+["\']\s*,\s*\(.*?\).*?{.*?}.*\)',i):
#    base=re.sub(r'^.*?=\s*(.*?)\s*\(\s*["\']\s*(\w+)\s*["\']\s*,\s*\((.*?)[, ]*\).*$',r'\1'+DELIMITER+r'\2'+DELIMITER+r'\3',i)
    base=re.sub(r'^\s*(.*?)\s*=\s*(.*?)\s*\(\s*["\']\s*(\w+)\s*["\']\s*,\s*\((.*?)[, ]*\).*$',r'\1'+DELIMITER+r'\2'+DELIMITER+r'\3'+DELIMITER+r'\4',i)
#    data+='class '+re.split(DELIMITER,base)[1]+r'('+re.split(DELIMITER,base)[2]+r',metaclass='+re.split(DELIMITER,base)[0]+r'):pass'+'\n'
    data+='class '+re.split(DELIMITER,base)[0]+r'('+re.split(DELIMITER,base)[3]+r',metaclass='+re.split(DELIMITER,base)[1]+r'):pass'+'\n'
   else:
    data+=i+'\n'
 with open(re.sub(r'^(.*[.])pyx$',r'\1'+'py',k),'w') as file:
  file.write(data)
 data=''
 print(k,re.sub(r'^(.*[.])pyx$',r'\1'+'py',k))
