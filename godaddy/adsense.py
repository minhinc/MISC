import re
import os
import sys
sys.path.append('..')
from utillib import requestm
for i in [i for i in os.listdir() if re.search(r'[.]php$',i) and re.search(r'<py>.*</py>',open(i).read(),flags=re.DOTALL)]:
 data=open(i).read()
 funclist=re.findall(r'<py>(.*?)</py>',data,flags=re.I)
 for func in funclist:
  data=re.sub(r'<py>'+re.escape(func)+r'</py>',eval(func),data,flags=re.I|re.DOTALL)
 with open(i+'.py','w') as file:
  print('writing ->',i+'.py')
  file.write(data)
