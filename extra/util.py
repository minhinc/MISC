import json,re
class _jsonc:
 def __init__(self,*args,**kwargs):
  super(_jsonc,self).__init__(*args,**kwargs)

 def loads(self,str_):
  return json.loads(re.sub(r'(?P<id>\n\s*".*?"\s*:\s*")(?P<id2>.*?)(?="\s*(?:,\s*\n|\]|}))',lambda m:m.group('id')+r'\n'.join(re.split('\n',m.group('id2'))),str_,flags=re.DOTALL))

import sys,os;sys.path.append(os.path.expanduser('~')+'/tmp') if not os.path.expanduser('~')+'/tmp' in sys.path else None
from MISC.extra.config import _configi as print
from MISC.extra.config import _configi
class _helpc:
 tabspace='    '

 def hash2str(self,hashd_,sep_=''):
#  print(f'>< hash2str {hashd_=}')
  if not type(hashd_)==dict:
   return
  if sep_=='':
   _helpc.hash2str.rets=''
  for i in hashd_:
   _helpc.hash2str.rets+=('\n' if not _helpc.hash2str.rets=='' else '')+sep_+i+(str(_helpc.tabspace+hashd_[i]) if not _configi.type(hashd_[i])=='sequence' and not type(hashd_[i])==dict else '')
   self.hash2str(hashd_[i],sep_+_helpc.tabspace)
#  print(f'<> {_helpc.hash2str.rets=}')
  return _helpc.hash2str.rets

 def str2hash(self,str_):
  '''help string to hash'''
  str_=os.popen('python3 '+str_).read() if os.path.isfile(str_) else str_
  str_=re.sub(r'^(?:\s*\n)?(.*?)(?:\n\s*)?$',r'\1',str_,flags=re.DOTALL)
  str_=re.sub(r'^'+re.sub(r'^(\s*).*',r'\1',str_,flags=re.DOTALL),'',str_,flags=re.M)
#  print(f'><_helpc.str2hash {str_=}')
  hashl=[dict()]
  tabspace=''
  for i in [i for i in re.split(r'\n',str_) if not re.search(r'^\s*$',i)]:
   key=re.sub(r'^\s*','',i)
   initialspace=re.sub(r'^(\s*).*$',r'\1',i)
#   print(f'<=> {key=} {i=} {initialspace=} {tabspace=} {hashl=}')
   if re.search(r'^\s*--',i):
    [hashl.pop() for l in range(max(0,(len(tabspace)-len(initialspace))//len(_helpc.tabspace)))]
    hashl[-1][key]=dict()
    hashl.append(hashl[-1][key])
   elif re.search(r'^\s*-[^-]',i):
    hashl[-1][re.sub(r'(.*?)\s+.*',r'\1',key)]=re.sub(r'.*?\s+(.*)$',r'\1',key)
   tabspace=initialspace
  return hashl[0]

 def removetype(self,hashd_):
  if not type(hashd_)==dict:
   return hashd_
  return {re.sub(r'\(\S+\)$',r'',key):self.removetype(hashd_[key]) for key in hashd_}

 def cmd2list(self,refhash_,argv_):
  '''refhash_(dict) reference command line help
'|--' is for looking one level up in the helpstring'''
  print(f'>< {refhash_=} {argv_=}')
  tabspace=_helpc.tabspace
  jsonstr='{'
  '''
  if not type(refhash_)==dict:
   refhash_=self.removetype(self.str2hash(refhash_))
  '''
  if type(refhash_)==str:
   refhash_=self.str2hash(os.popen('python3 '+refhash_).read() if os.path.isfile(refhash_) else refhash_)
  hashtmpl=[[refhash_,0]]
  argv_=' '.join(argv_) if not type(argv_)==str else argv_
  print(f'<=> _helpi.cmd2hash {refhash_=} {argv_=}')
  while not re.search(r'^\s*$',argv_):
   key=re.sub(r'^\s*(\S+).*$',r'\1',argv_)
   argv_=re.sub(r'^\s*'+key+'(.*)$',r'\1',argv_)
   if re.search(r'^[|]*--',key):
    while re.search(r'^[|]',key):
     key=re.sub(r'^[|](.*)$',r'\1',key)
     hashtmpl.pop()
     tabspace=re.sub(r'^'+_helpc.tabspace,'',tabspace)
     jsonstr+='\n'+tabspace+'}'
    while key not in [re.sub(r'\(\S+\)$','',x) for x in hashtmpl[-1][0]]:
     hashtmpl.pop()
     tabspace=re.sub(r'^'+_helpc.tabspace,'',tabspace)
     jsonstr+='\n'+tabspace+'}'
    jsonstr+=(',' if hashtmpl[-1][1]>=1 else '')+'\n'+tabspace+f'"{key}"'+' : {'
    hashtmpl[-1][1]+=1
    tabspace+=_helpc.tabspace
    hashtmpl.append([hashtmpl[-1][0][key],0])
   elif re.search(r'^\s*-',key):
    value=re.sub(r'^\s*(.*?(?=\s+-|\s*$)).*$',r'\1',argv_)
    argv_=re.sub(r'^\s*'+value+'(.*)',r'\1',argv_)
    if hashtmpl[-1][1]>=1:
     jsonstr=re.sub('$',',',jsonstr,flags=re.DOTALL)
    print(f'<=> cmd2str {key=} {value=} {jsonstr=}')
    jsonstr+='\n'+tabspace+f'"{key}"'+' : '+f'"{value}"'
    hashtmpl[-1][1]+=1

#   if re.search('^[|]*--',re.sub(r'^\s*(\S+).*$',r'\1',argv_)) and not jsonstr=='{':
   for dk in [dk for dk in hashtmpl[-1][0] if re.search(r'\(\S+\)$',hashtmpl[-1][0][dk]) and not re.search(re.sub(r'^-(.*?)\(\S+\)$',r'\1',dk)+r'"\s*:',re.sub(r'^.*{(.*)',r'\1',jsonstr, flags=re.DOTALL), flags=re.DOTALL) and not re.search(re.sub(r'\(\S+\)$',r'',dk)+r'\s+',re.sub(r'^(.*?)(?=(?:[|]*--|\s*$))',r'\1',argv_))]:
    argv_=re.sub(r'\(\S+\)$','',dk)+' '+re.sub(r'.*\((\S+)\)$',r'\1',hashtmpl[-1][0][dk])+' '+argv_
    print(f'{dk=} {argv_=}')
  while hashtmpl:
   tabspace=re.sub(r'^'+_helpc.tabspace,'',tabspace)
   jsonstr+='\n'+tabspace+'}'
   hashtmpl.pop()
  print(f'<> _configc.cmd2hash jsonstr=\n')
  print(jsonstr)
  print(f'<=> {json.loads(jsonstr,object_pairs_hook=lambda o:o)=}')
  return json.loads(jsonstr,object_pairs_hook=lambda o:o)

 def sortlist(self,listl_,sortcriteriahash_):
  print(f'>< {listl_=} {sortcriteriahash_=}')
  i=0
  for k in sortcriteriahash_:
   print(f'D {i=} {k=}')
   listl_=listl_[0:i]+sorted(listl_[i:],key=lambda m:not m[0]==re.sub(r'\(\S+\)$','',k))
   print(f'D {listl_}=')
   i=([count for count in range(len(listl_)) if listl_[count][0]==re.sub(r'\(\S+\)$','',k)] or [0])[0]+1
  print(f'<> {listl_=}')
  return listl_

