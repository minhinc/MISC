import os,re,sys
import magic
if len(sys.argv)==1:
 print(f'diff <originaldir> <changeddir>\ndiff MISC MISC_mod')
 sys.exit(-1)
source=[x for x in re.split('\n',os.popen(f'find '+sys.argv[1]+r' -name "*.*"').read()) if x and not os.path.isdir(x) and re.search(r'text',magic.from_file(x,mime=True),flags=re.I)]
target=[x for x in re.split('\n',os.popen(f'find '+sys.argv[2]+r' -name "*.*"').read()) if x and not os.path.isdir(x) and re.search(r'text',magic.from_file(x,mime=True),flags=re.I)]

for i in target:
 tmp=[x for x in source if re.sub(r'^.*/([^/]+)/(.*$)',r'\1'+r'/'+r'\2',i) in x]
# print(f'TEST i={i} tmp={tmp}')
 if not tmp or tmp and not open(i).read() == open(tmp[0]).read():
  print(i)
