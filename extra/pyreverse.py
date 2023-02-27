from collections import OrderedDict
import re,os,sys,glob
import shlex
import subprocess
sys.path.append(os.path.expanduser('~')+r'/tmp')
import MISC.ffmpeg.libm
libi=MISC.ffmpeg.libm.libc()
fileextension='py|pyx|pxd|pxi|pyi'
import re
def remcurly(filedata):
 def clean(i,count):
  i=re.sub(r'\\[()]','',re.sub(r'\'.*?[()]+.*?(?=\')','',re.sub(r'".*?[()]+.*?(?=")','',re.sub(r'[\[{].*?[()]+.*?(?=[\]}])','',i))))
  count+=len(re.findall(r'\(',i))
  count-=len(re.findall(r'\)',i))
  return (i,count)
 DELIMITER=r'!ABS SBA!'
 filedata=re.sub(r'\\n',DELIMITER,filedata,flags=re.DOTALL)
 filedata=uncomment(filedata)
 buff=''
 count=0
 for i in re.split('\n',filedata):
  if re.search(r'^(\s*(cp?)?def\s+.*?\w+\(|\s*((cp?)?def\s+)?class\s+|\s*async\s+|\s*from\s+|\s*import\s+|\s*for\s+|\s*while\s+|\s*try\s+|\s*except\s+|\s*finally\s+|\s*with\s+|\s*@|\s*__)',i):
   if re.search(r'\n',buff):
    filedata=re.sub(r'(?P<id>'+re.escape(buff)+')',lambda m:re.sub(r'\n','',m.group('id'),flags=re.DOTALL),filedata,flags=re.DOTALL)
   buff=i
   count=0
   i,count=clean(i,count)
   if not count:
    buff=''
  elif not buff=='':
   buff+='\n'+i
   i,count=clean(i,count)
   if count==0:
    if re.search(r'\n',buff):
     filedata=re.sub(r'(?P<id>'+re.escape(buff)+')',lambda m:re.sub(r'\n','',m.group('id'),flags=re.DOTALL),filedata,flags=re.DOTALL)
    buff=''
 return re.sub(DELIMITER,r'\\n',filedata,flags=re.DOTALL)
def convert2localdir(file):
 localdir=re.sub(r'^.*?[.].*$','.',re.sub(r'^[./]*(.*?)(/[^/]+)?$',r'\1',file))
 localdirfile=localdir+r'/'+re.sub(r'^(?:.*/)?(.*)[.][^.]+$',r'\1'+'.py',file)
 return (localdir,localdirfile)

def insertintofile(file,line):
 print(f'><insertintfile {file=} {line=}')
 data=open(file).read()
 with open(file,'w') as tmpfile:
  tmpfile.write(re.sub(r'}\s*$',line+'\n}\n',data,flags=re.DOTALL))

def getarg(arg,count=1):
 ret=False
 index=[[count for count in range(len(sys.argv)) if re.search(re.escape(arg),sys.argv[count])] or [None]][0]
 '''
 if [x for x in sys.argv if re.search(arg,x)]:
  ret=sys.argv[sys.argv.index(arg)+1] if count>1 else True
  sys.argv[sys.argv.index(arg):sys.argv.index(arg)+(2 if count>=2 else 1)]=''
 '''
 if index:
  ret=sys.argv[index+1] if count>1 else True
  sys.argv[index:index+(2 if count>=2 else 1)]=[]
 return ret
def usage():
 print(f'''\
  --- usage ---
  Note - directory /usr/lib/python3//dist-packages package sklearn modulefile sklearn/base.py
  python3 pyreverse.py --fix <directory> <[package|modulefile]> [modulefile]...
  python3 pyreverse.py --modify <package|modulefile> [classname] [classname]...
  python3 pyreverse.py [--exclude <class>| --timeout <sec> | --association <level>| --ignore <dir> | --ancestor <level>]
  python3 pyreverse.py --fix /usr/local/lib/python3.7/dist-packages kivy
  python3 pyreverse.py --fix /usr/local/lib/python3.7/dist-packages kivy/uix/widget.py kivy/uix/button.py
  python3 pyreverse.py --modify kivy --exclude 'kivy.properties'
  python3 pyreverse.py --modify kivy/uix/widget.py Widget WidgetBase
  python3 pyreverse.py --modify kivy/uix kivy/tools
''')
 sys.exit(-1)
usage() if len(sys.argv)==1 else None
excludeclass=[re.sub(r'[.]',r'[.]',x) for x in libi.str2tuple(getarg(r'--exclude',2) or '')+(r'builtins.',)]
timeout=int(getarg(r'--timeout',2)) or 30
colorized=getarg(r'--colorized') or True
association=getarg(r'--association',2)
ancestor=getarg(r'--ancestor',2)
ignore=getarg(r'--ignore',2)
print(f'TEST {excludeclass=} {timeout=} {colorized=} {association=} {ancestor=} {ignore=}')

def uncomment(text):
 return re.sub(r'\n+',r'\n',re.sub(r'(#.*|^\s*)$',r'',re.sub(r"(^|\n)[^\n]*?'''.*?'''[^\n]*",'',re.sub(r'(^|\n)[^\n]*?""".*?"""[^\n]*','',text,flags=re.DOTALL),flags=re.DOTALL),flags=re.M),flags=re.DOTALL)
class fix:
 def __init__(self):
  super(fix,self).__init__()
  if len(sys.argv)<3:
   usage()
  print(f'------- FIX has been initiated at dir {sys.argv[1]} for package {sys.argv[2]} --------')
  DELIMITER='!ABS SBA!'
  mode=''
  data=''
  filedata=''
  backspace=None
  file=[]
  tmp=tmp2=None
#  os.system(r'cd '+sys.argv[1]+';find '+sys.argv[2]+' -name "*.py" | cpio -pdm '+os.getcwd())
  if re.search(fr'[.]({fileextension})$',sys.argv[1]+r'/'+sys.argv[2]):
   file.extend([sys.argv[1]+r'/'+x for x in sys.argv[2:]])
  else:
   for i in os.walk(sys.argv[1]+r'/'+sys.argv[2]):
    for j in i[2]:
     file.append(i[0]+r'/'+j) if re.search(fr'[.]({fileextension})?$',j) else None
  file=[x for x in file if re.search(r'[.]pyi',x) or not re.sub(r'[.][^.]*$',r'.pyi',x) in file]
  file.sort(key=lambda m:re.search(r'[.](py|pyi)$',m) and r'.' or re.search(r'[.]pyx$',m) and r'..' or m)
  print(f'{file=}')
  for k in file:
   print(f'processing -> {k=}')
   with open(k) as file:
    filedata=file.read()
   if re.search(r'[.](pyx|pxi|pxd)$',k):
#    filedata=re.sub(r'\n+','\n',re.sub(r'^(?!\s*@|\s*class.*:|\s*from|\s*__all__|\s*import|\s*def.*?\().*$','',re.sub(r'^(\s*def\s+).*?(\S+\(.*\)).*$',r'\1\2',re.sub(r'^(\s*)def\s+class\s+',r'\1'+'class ',re.sub(r'cp?(import|class|def)',r'\1', re.sub(r'(?P<id>\(|,)(?P<id2>.*?)\s*(?=[),])',lambda m:m.group('id')+(re.sub(r'.*?(\w+)$',r'\1',m.group('id2')) if re.search(r'\w+.*?[*]',m.group('id2')) else re.sub(r'.*?(\S+)$',r'\1',m.group('id2')))   ,re.sub(r'(?P<id>\(.*?\))',lambda m:re.sub(r'\n+','',m.group('id')),   re.sub(r'(?::[^:\n]+)?=\s*(?:\[.*?\]|{.*?}|\(.*?\)|\'.*?\'|".*?"|.*?(?=\)|,|$))\s*','',re.sub(r'(\[.*?\]|{.*})','',re.sub(r'\\[ \t]*\n',r' ',re.sub(r'(#.*|^\s*)$',r'',re.sub(r"(^|\n)[^\n]*?'''.*?'''[^\n]*",'',re.sub(r'(^|\n)[^\n]*?""".*?"""[^\n]*','',filedata,flags=re.DOTALL),flags=re.DOTALL),flags=re.M),flags=re.DOTALL),flags=re.DOTALL),flags=re.DOTALL),  flags=re.DOTALL), flags=re.M),flags=re.M),flags=re.M),flags=re.M),flags=re.M),flags=re.DOTALL)
#    filedata=re.sub(r'\n+','\n',re.sub(r'^\s*$','',re.sub(r'^(?!\s*@|\s*class.*:|__all__|from|import|\s*def\s+\w+\().*$','',re.sub(r'^(\s*@.*?,).*$',r'\1'+')',re.sub(r'^(\s*def\s+).*?(\S+\(.*?\)).*$',r'\1\2',re.sub(r'^(\s*)def\s+class\s+',r'\1'+'class ',re.sub(r'cp?(import|class|def)',r'\1', re.sub(r'(?P<id>\(|,)(?P<id2>.*?)\s*(?=[),])',lambda m:m.group('id')+(re.sub(r'.*?(\w+)$',r'\1',m.group('id2')) if re.search(r'\w+.*?[*]',m.group('id2')) else re.sub(r'.*?(\S+)$',r'\1',m.group('id2')))   ,re.sub(r'(?P<id>\(.*?\))',lambda m:re.sub(r'\n+','',m.group('id')), re.sub(r'(?P<id>(?::[^:\n]+)?=\s*(?:\[.*?\].*?\S|{.*?}.*?\S|\(.*?\).*?\S|\'.*?\'.*?\S|".*?".*\S|.*?(?=\)|,|$)))',lambda m:m.group('id') if re.search(r'=\s*\((.*[^)]$|$)',m.group('id')) else '',re.sub(r'(?P<id>.*?)(?P<id2>\[.*?\]|{.*?})', lambda m:m.group('id')+m.group('id2') if  re.search(r'=',m.group('id')) else m.group('id'),re.sub(r'\\[ \t]*\n',r' ',re.sub(r'(#.*|^\s*)$',r'',re.sub(r"(^|\n)[^\n]*?'''.*?'''[^\n]*",'',re.sub(r'(^|\n)[^\n]*?""".*?"""[^\n]*','',filedata,flags=re.DOTALL),flags=re.DOTALL),flags=re.M),flags=re.DOTALL),flags=re.M),flags=re.M),  flags=re.DOTALL), flags=re.M),flags=re.M),flags=re.M),flags=re.M),flags=re.M),flags=re.M),flags=re.M),flags=re.DOTALL)
    filedata=remcurly(re.sub(r'\n+','\n',re.sub(r'^\s*$','',re.sub(r'\\[ \t]*\n',r' ',re.sub(r'(#.*|^\s*)$',r'',re.sub(r"(^|\n)[^\n]*?'''.*?'''[^\n]*",'',re.sub(r'(^|\n)[^\n]*?""".*?"""[^\n]*','',filedata,flags=re.DOTALL),flags=re.DOTALL),flags=re.M),flags=re.DOTALL),flags=re.M),flags=re.DOTALL))
#    print(f'FIRST PROCESSED {k=} nfiledata=\n',filedata)
    filedata=re.sub(r'\n+','\n',re.sub(r'^\s*$','',re.sub(r'^(?!\s*class.*?:|from\s+|import\s+|__all__|\s*def\s+\w+\(|\s*@).*$','',re.sub(r'^(?P<id>\s*)(cp?)?(?P<idx>def\s+|@).*?(?P<id2>\S+?)(?P<id3>\(.*\)).*$',lambda m:m.group('id')+m.group('idx')+m.group('id2')+''.join(y for y in re.findall(r'[(,].*?(?=[),])',re.sub(r'(?P<id10>[(,].*?)(?::.*?)?(=.*?)?(?=[,)])',lambda m:re.sub(r'^(?P<id20>[(,])(?:\s*\S+\s+.*?(?P<id21>\w+)|.*?(?P<id22>\S+))\s*$',lambda m:m.group('id20')+''.join(x for x in (m.group('id21'),m.group('id22')) if x),m.group('id10')),m.group('id3'))) if re.search(r'^[(,][*\w\s]+$',y) and not re.search(r'^[(,\s\d]+$',y))+')',re.sub(r'^(\s*)(cp?)?def\s+class\s+',r'\1'+'class ',re.sub(r'cimport','import',filedata,flags=re.M),flags=re.M),flags=re.M),flags=re.M),flags=re.M),flags=re.DOTALL)
    previouscapture=None
#    print(f'><MODIFIED {k=} nfiledata=\n',filedata)
    for i in re.findall(r'([ \t]*)(class[^\n]+|def[^\n]+|@[^\n]+)\n([ \t]*)',filedata):
     i=list(i)
     i[0]=previouscapture if previouscapture!=None else i[0]
#     print(f'MODIFIED0 {k=} {i=}')
     if re.search(r'(\bdef|\bclass)\s+\w+',i[1]) and not re.search(r':[^)]*$',i[1]):
      filedata=re.sub(r'^'+i[0]+re.escape(i[1])+r'$',i[0]+i[1]+':',filedata,flags=re.M)
#      print(f'MODIFIED01 {k=} {i=}')
     if re.search(r'(\bdef|\bclass)\s+\w+',i[1]) and len(i[0])>=len(i[2]) and not re.search(r':pass',i[1]):
      filedata=re.sub(r'^('+i[0]+re.escape(re.sub(r':$','',i[1]))+r'.*:)$',r'\1'+'pass',filedata,flags=re.M,count=1)
#      print(f'MODIFIED02 {k=} {i=}')
     elif re.search(r'(\bdef|\bclass)\s+\w+',i[1]):
      filedata=re.sub(r'^('+i[0]+re.escape(re.sub(r':$','',i[1]))+r':)$',r'\1'+DELIMITER,filedata,flags=re.M,count=1)
#      print(f'MODIFIED03 {k=} {i=}')
     previouscapture=i[2]
    filedata=re.sub(DELIMITER+r'$','',filedata,flags=re.M)
#    print(f'<>MODIFIED {k=} {i=} nfiledata=\n',filedata)
    if re.search(r'.*[*].*?,.*(?==)',filedata,flags=re.M):
     filedata=re.sub(r'(?P<id>.*[*])(?P<id2>.*?)(?P<id3>\).*)$',lambda m:m.group('id')+re.sub(r'(,[\w\s]+)',r'\1'+r'=""',m.group('id2'))+m.group('id3'),filedata,flags=re.M)
#   elif re.search(r'[.]pyi$',k):
#    filedata=re.sub(r'\n+','\n',re.sub(r'(?P<id>\(.*?\))',lambda m:re.sub(r'\n+','',m.group('id')),re.sub(r'\\[ \t]*\n',r' ',re.sub(r'(#.*|^\s*)$',r'',re.sub(r"(^|\n)[^\n]*?'''.*?'''[^\n]*",'',re.sub(r'(^|\n)[^\n]*?""".*?"""[^\n]*','',filedata,flags=re.DOTALL),flags=re.DOTALL),flags=re.M),flags=re.DOTALL),flags=re.DOTALL),flags=re.DOTALL)
   for i in re.split('\n',filedata):
    if re.search(r'^w+\s*=\s*\w+\s*\(\s*["\']\w+["\']\s*,\s*\(.*?\).*?{.*?}.*?\)',i) and not re.search(r').*?\(\)\s*$',i):
     base=re.sub(r'^\s*(.*?)\s*=\s*(.*?)\s*\(\s*["\']\s*(\w+)\s*["\']\s*,\s*\((.*?)[, ]*\).*$',r'\1'+DELIMITER+r'\2'+DELIMITER+r'\3'+DELIMITER+r'\4',i)
     data+='class '+re.split(DELIMITER,base)[0]+r'('+(re.split(DELIMITER,base)[3]+r',' if not re.search(r'^\s*$',re.split(DELIMITER,base)[3]) else '')+r'metaclass='+re.split(DELIMITER,base)[1]+r'):pass'+'\n'
    else:
     data+=i+'\n'
   tmp=r'/'+re.sub(r'^'+sys.argv[1]+r'/*','',k)
   os.makedirs(convert2localdir(tmp)[0]) if not os.path.exists(convert2localdir(tmp)[0]) else None
   if os.path.exists(convert2localdir(tmp)[1]):
    filedata1=open(convert2localdir(tmp)[1]).read()
    filedata1=re.sub(r'\n+','\n',re.sub(r'^(?!import\s+|from\s+|__).*$','',data,flags=re.M),flags=re.DOTALL)+'\n'+filedata1
    print(f'FILE EXISTS {k=}')
    for i in re.findall(r'^class\s+(\w+)\b.*$',data,flags=re.M):
     if re.search(r'^class\s+'+i+r'\b.*$',filedata1,flags=re.M) and not re.search(r'(^|\n)class\s+'+i+r'(\b[^:]*:\s*(?:pass|[.][.][.]))',uncomment(data),flags=re.DOTALL):
      if re.search(r'(?:^|\n)class\s+'+i+r'\b[^:]*:\s*(?!pass|[.][.][.])',uncomment(filedata1),flags=re.DOTALL):
       tmp2=re.sub(r'^.*(?:^|\n)class\s+'+i+r'\b[^:]*:.*?\n([ \t]+)\S+.*$',r'\1',data,flags=re.DOTALL)
       tmp3=re.sub(r'^.*(?:^|\n)class\s+'+i+r'\b[^:]*:.*?\n([ \t]+)\S+.*$',r'\1',filedata1,flags=re.DOTALL)
       if tmp2!=tmp3:
        print(f'EXIST {k=} {i=} {tmp2=} {tmp3=}')
#        data=re.sub(r'(?P<id>(?:^|\n)class\s+'+i+r'\b.*?)(?!\n[ \t]*#)(?=\n\S|$)',lambda m:m.group('id')+re.sub(r'^'+tmp2,tmp3,m.group('id2'),flags=re.M),data,flags=re.DOTALL)
        data=re.sub(r'(?P<id>(?:^|\n)class\s+'+i+r'[^\n]*?\n)(?P<id2>.*?)(?=\n\S|$)',lambda m:m.group('id')+re.sub(r'^'+tmp2,tmp3,m.group('id2'),flags=re.M),data,flags=re.DOTALL)
      data=re.sub(r'\\n',DELIMITER,data,flags=re.DOTALL)
      filedata1=re.sub(r'(?:^|\n)class\s+'+i+r'\b[^:]*:[^\n]*\n(?:\s*(?:pass|[.][.][.])\s*\n)?',re.sub(r'^.*?((?:^|\n)class\s+'+i+r'\b.*?)'+'(?:\n\S.*$|$)','\n'+r'\1'+'\n',data,flags=re.DOTALL),filedata1,flags=re.DOTALL)
      filedata1=re.sub(DELIMITER,r'\\n',filedata1,flags=re.DOTALL)
     elif not re.search(r'^class\s+'+i+r'\b.*$',filedata1,flags=re.M):
      filedata1+='\n'+re.sub(r'(?:^|^.*?\n)(class\s+'+i+r'\b.*?)(?:\n\S.*$|$)',r'\1',data,flags=re.DOTALL)
#    print(f'TEST exist2 {k=} {filedata1=}')
     open(convert2localdir(tmp)[1],'w').write(filedata1)
   else:
    with open(convert2localdir(tmp)[1],'w') as file:
     file.write(data)
   data=''
#   print(k,convert2localdir(tmp)[1])
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
  tmp=tmp2=None
  def classname(filename,hint=None):
   if hint==None:
    return re.findall(r'^class\s+(.+?)\b.*:\s*(?:pass\s*|#.*|->.*|[.][.][.].*)?$',remcurly(uncomment(open(filename).read())),flags=re.M)
   else:
    return re.findall(r'^class\s+('+hint+r')\b.*:\s*$',open(filename).read(),flags=re.I|re.M)
  if len(sys.argv)>=3 and not re.search(r'(/|[.]py$)',sys.argv[2]):
   file=[(sys.argv[1],self.dirpathtopackage(sys.argv[1])+'.'+i,'package') for i in sys.argv[2:]]
   [os.remove(y) for x in file for y in glob.glob(x[1]+r'.*')]
  else:
   if re.search(r'[.]py$',sys.argv[1]):
#   if len(sys.argv)>=3 and not re.search(r'[.]py$',sys.argv[2]):
#    file=[(sys.argv[1],self.dirpathtopackage(sys.argv[1])+'.'+i) for i in sys.argv[2:]]
#    file=[(sys.argv[1],self.dirpathtopackage(sys.argv[1])+'.'+i,'package') for i in sys.argv[2:]]
#   else:
     for i in sys.argv[1:]:
      for k in classname(i):
       file.append((i,self.dirpathtopackage(i)+r'.'+k))
   else:
    for i in [y for k in sys.argv[1:] for y in os.walk(k) if not ignore or not re.search(r'/'+ignore,y[0])]:
     for j in [j for j in i[2] if re.search(r'[.]py$',j)]:
      for k in classname(i[0]+r'/'+j):
       file.append((re.sub(r'/+$','',i[0])+r'/'+j,self.dirpathtopackage(i[0]+r'/'+j)+'.'+k))
  filek=file
  file=[i for i in file if not os.path.exists(r'./'+i[1]+'.dotx')]
  print(f'list of file,class to be processed (.dot file do not exists)={file}')
  for count,i in enumerate(file):
   print(fr'package={i} {count+1}/{len(file)}')
   try:
    if subprocess.call(shlex.split('pyreverse -f ALL '+i[0]+(' --colorized ' if colorized else '')+(r' -A' if ancestor==False else ' -a '+ancestor+' ')+('S' if association==False else ' -s '+association+' -')+'my --show-builtin '+(r' --ignore '+ignore+' ' if ignore else '')+(r'-c '+i[1] if len(i)<=2 else '')),timeout=timeout):
     wrongfile.write(rf'{i}'+'\n');wrongfile.flush()
     del filek[[count for count in range(len(filek)) if filek[count][1]==i[1]][0]]
     continue 
   except subprocess.TimeoutExpired:
    print(f"Timedout file={i[0]} class={i[1]}")
    print(f'trying with -A -s 1 -my -c')
#    if subprocess.call(shlex.split('pyreverse -f ALL '+i[0]+(r' -A' if ancestor==False else ' -a '+ancestor+' ')+' -s 1 -my '+(r'-c '+i[1] if len(i)<=2 else ''))):
    try:
     if subprocess.call(shlex.split('pyreverse -f ALL '+i[0]+(' --colorized ' if colorized else '')+(r' -A' if ancestor==False else ' -a '+ancestor+' ')+' -s 1 -my --show-builtin '+(r' --ignore '+ignore+' ' if ignore else '')+(r'-c '+i[1] if len(i)<=2 else '')),timeout=timeout*4):
      wrongfile.write(rf'{i}'+'\n');wrongfile.flush()
      del filek[[count for count in range(len(filek)) if filek[count][1]==i[1]][0]]
      continue
    except subprocess.TimeoutExpired:
     print(f'Timedout2 file={i[0]} class={i[1]}\nskipping...')
     del filek[[count for count in range(len(filek)) if filek[count][1]==i[1]][0]]
     continue
   os.rename('classes.dot',i[1]+r'.dot') if len(i)>2 else None
#   [insertintofile(i[1]+'.dot','"'+y+'" [color="black", label="'+y+'", shape="record", style="solid"];\n"'+re.sub(r'.*[.]','',i[1])+'" -> "'+y+'" [arrowhead="empty",arrowtail="none"];') for x in re.findall(r'^class\s+'+re.sub(r'^.*[.]','',i[1])+r'(.*?):',remcurly(uncomment(open(re.sub(r'^(.*)[.].*',r'\1'+'.py',re.sub(r'[.]',r'/',re.sub(r'([.]py|/)$','',i[0])+'.'+i[1]))).read())),flags=re.M)[0] for y in re.split(r'[(),]',re.sub(r'[ \t]*','',x)) if not re.search(re.sub(r'^.*[.]','',i[1])+r'\s+->\s+'+y+r'\s*\[',open(i[1]+'.dot').read(),flags.M)]
   [insertintofile(i[1]+'.dot','"'+y+'" [color="black", label="'+y+'", shape="record", style="solid"];\n"'+i[1]+'" -> "'+y+'" [arrowhead="empty",arrowtail="none"];') for x in re.findall(r'^class\s+'+re.sub(r'^.*[.]','',i[1])+r'\b(.*?):',remcurly(uncomment(open(re.search(r'[.]py$',i[0]) and i[0] or re.sub(r'[.]',r'/',re.sub(r'[.][^.]+$','',i[1]))+'.py').read())),flags=re.M) for y in re.split(r'[(),]',re.sub(r'[ \t]*','',x)) if y and re.search(r'^[ \t\w]+$',y) and not re.search('"'+i[1]+r'"\s+->\s+".*?[.]'+y+r'"\s*\[',open(i[1]+'.dot').read(),flags=re.M)]
   data=open(i[1]+r'.dot').read()
   if not re.search(r'label="{'+i[1]+r'\b.*?}"',data,flags=re.I|re.DOTALL) and len([x for x in re.findall(r'label="{(.*?)\b\|.*?}"',data,flags=re.I|re.DOTALL) if re.search(re.escape(x)+r'$',i[1])])==1:
    data=re.sub([x for x in re.findall(r'label="{(.*?)\b\|.*?}"',data,flags=re.I|re.DOTALL) if re.search(re.escape(x)+r'$',i[1])][0]+r'\b',i[1],data,flags=re.DOTALL)
   classdata=re.sub(r'.*label="{('+i[1]+r'\b.*?)}".*',r'\1',data,flags=re.I|re.DOTALL)
   if data==classdata:
    print(f'data==classdata {classdata=}\n{data=}')
    wrongfile.write(rf'{i}'+'\n');wrongfile.flush()
    del filek[[count for count in range(len(filek)) if filek[count][1]==i[1]][0]]
    continue
   data=re.sub(r'^(.*label="){(.*?)\|.*}(".*)',r'\1\2\3',data,flags=re.I|re.M)
   data=re.sub(r'\n+','\n',re.sub(r'^.*?"builtins[.]object"\s+.*$',r'',data,flags=re.I|re.M),flags=re.I|re.DOTALL)
   print(f'classdata={classdata}')
   data=re.sub(r'^(.*label=)"('+re.split(r'\|',classdata)[0]+r')\b.*?"(, shape=.*)$',r'\1'+r'<<TABLE border="0" cellborder="0"><TR><TD colspan="2">'+r'\2'+r'</TD></TR><TR><TD valign="top">'+(r'<FONT POINT-SIZE="4"><BR />'+r'<BR ALIGN="LEFT" />'.join(re.split(r'\\l',re.split(r'\|',classdata)[1]))+r'<BR ALIGN="LEFT" /></FONT>' if ''.join(re.split(r'\\l',re.split(r'\|',classdata)[1])) else '')+r'</TD><TD valign="top">'+(r'<FONT POINT-SIZE="4">'+r'<BR ALIGN="LEFT" />'.join([re.sub(r'^','    ',y) if count else y for x in re.split(r'\\l',re.split(r'\|',classdata)[2]) for count,y in enumerate(re.findall(r'(.{,50})',x)[:-1])])+r'<BR ALIGN="LEFT" /></FONT>' if ''.join(re.split(r'\\l',re.split(r'\|',classdata)[2])) else '')+r'</TD></TR></TABLE>>'+r',color="red"'+r'\3',data,flags=re.I|re.DOTALL)
   data='\n'.join(list(OrderedDict.fromkeys(re.split(r'\n',data))))
   data=re.sub(r'^(?P<id>.*)$',lambda m:m.group(1) if re.search(r'^"builtins[.]',m.group(1)) or not re.search(r'^.*?\[.*?style="[^"]+".*?\].*$',m.group(1)) else re.sub(r'^(.*?\bcolor=")[^"]+(.*?style=")[^"]+(.*)$',r'\1'+'black'+r'\2'+'solid'+r'\3',m.group(1)),data,flags=re.I|re.M)
   for y in [y for x in set(re.findall(r'^\s*(.*?)\s+\[.*?arrowhead="diamond".*$',data,flags=re.M)) for y in re.findall(r'^(\s*'+x+r'\s+\[.*?arrowhead="diamond".*)$',data,flags=re.M)[4:]]:
    data=re.sub(r'^\s*'+re.escape(y)+r'$','',data,count=1,flags=re.M)
   parentclass=list(set(re.findall(fr'^"((?!(?:'+'|'.join(x for x in excludeclass if not re.search(r'^'+x,i[1]))+r'))[^"]+)"\s+\[.*',data,flags=re.I|re.M)))
   while True:
    tmp=len(parentclass)
    for y in parentclass[:]:
     [parentclass.append(x) for x in re.findall(r'^"'+y+r'"\s+->\s+"([^"]+)"\s+\[.*?arrowhead="empty".*$',data,flags=re.I|re.M) if x not in parentclass]
    if tmp==len(parentclass):
     break
   print(f'TEST {parentclass=} {excludeclass=}')
   data=re.sub(r'\n+','\n',re.sub(fr'^(?P<id>"(?:'+'|'.join(x for x in excludeclass if not re.search(r'^'+x,i[1]))+r')[^"]+"\s+)(->\s+"[^"]+"\s+)?(\[.*)$',lambda m:'' if not re.sub(r'^"([^"]+)".*$',r'\1',m.group(1)) in parentclass or m.group(2) and re.search(r'^[^"]+"builtins[.]',m.group(2)) and not re.sub(r'^[^"]+"([^"]+)".*$',r'\1',m.group(2)) in parentclass or re.sub(r'.*arrowhead="([^"]+)".*$',r'\1',m.group(3))=='diamond' else ''.join(x if x else '' for x in m.groups()),data,flags=re.I|re.M),flags=re.I|re.DOTALL)
   for x in set([re.sub(r'^.*?->\s+("[^"]+").*$',r'\1',x) for x in re.findall(r'^(".*?")\s+\[.*?arrowhead="diamond".*$',data,flags=re.M)]):
    tmp=''
    tmp2=[y for y in re.findall(r'^\s*("[^"]+")\s+->\s+'+x+r'\s+\[.*?arrowhead="diamond".*?label="(.*?)".*$',data,flags=re.M) if not re.search(r'^\s*'+y[0]+r'\s+->\s+(?!(?:'+y[0]+r'|'+x+'))"[^"]+"\s+\[.*$',data,flags=re.M) and not re.search(r'^\s*(?!'+y[0]+r')"[^"]+"\s+->\s+'+y[0]+r'\s+\[.*$',data,flags=re.M) and not y[0]=='"'+i[1]+'"']
    print(f'{x=} {tmp2=}')
    if len(tmp2)>2:
     for y in tmp2:
      tmp+=r'<BR ALIGN="LEFT" /><FONT POINT-SIZE="6" COLOR="black">'+' '*6+y[0]+r'</FONT>'
      data=re.sub(r'^\s*'+y[0]+r'\s+->\s+'+x+r'\s+\[.*?arrowhead="diamond".*$','',data,flags=re.M)
      data=re.sub(r'^\s*'+y[0]+r'\s+\[.*$','',data,flags=re.M)
      data=re.sub(r'^\s*'+y[0]+r'\s+->\s+'+y[0]+r'\s+\[.*$','',data,flags=re.M)
     if tmp:
      data=re.sub(r'(.*)}\s*$',r'\1',data,flags=re.I|re.DOTALL)
      data+='\n'+r'"'+re.sub(r'"([^"]+)"',r'\1',x)+'.aggregation'+r'" [color="yellow",label=<<TABLE border="0"><TR><TD>'+tmp+r'<BR ALIGN="LEFT" /></TD></TR></TABLE>>, shape="record",style="solid"];'
      data+='\n'+r'"'+re.sub(r'"([^"]+)"',r'\1',x)+'.aggregation'+r'" -> '+x+r' [arrowhead="diamond", arrowtail="none", fontcolor="green", label="'+r'\l'.join([xx[1] for xx in tmp2][:4])+r'", style="solid"];'+'\n}'
   data=re.sub(r'\n+','\n',data,flags=re.DOTALL)
   open(i[1]+'.dotx','w').write('\n'.join(list(OrderedDict.fromkeys(re.split('\n',data)))))
  wrongfile.close()
  for count,i in enumerate(filek):
   tmp=[x for x in re.findall(r'^\s*("[^"]+")\s+\[.*$',open(i[1]+'.dotx').read(),flags=re.M) if not re.search(r'(^'+x+r'\s+->|\s+->\s+'+x+')',open(i[1]+'.dotx').read(),flags=re.M)]
   for x in tmp:
    [insertintofile(i[1]+'.dotx',y) for y in set(y for y in re.split('\n',os.popen(fr'egrep -he "^\s*\"[^\"]+\"\s+->\s+\"[^\"]+\".*$" *.dotx').read()) for x in re.findall(r'^\s*("[^"]+")\s+->\s+("[^"]+").*$',y) if x[0] in tmp and x[1] in tmp)]
   print(f'fixing subclass i={i} {count+1}/{len(filek)}')
   if not i[1] in deriveclass:
    deriveclass[i[1]]=[]
   [deriveclass[i[1]].append(re.sub(r'^"(.*?)"$',r'\1',k)) for k in re.split('\n',os.popen(fr'egrep -he "^\s*\"[^\"]+?\"\s+->\s+\"{i[1]}\"\s+\[.*?arrowhead=\"empty\"" *.dotx|egrep -o -e "^\"[^\"]+\""').read()) if k and not k=='"'+i[1]+'"' and re.sub(r'(^"|"$)','',k) not in deriveclass[i[1]]]
   if not deriveclass[i[1]]:
    del deriveclass[i[1]]
  print(f'deriveclass={deriveclass}')
  def deriveclassrecursivestring(package,space):
   derivestring=''
   for k in deriveclass[package]:
     derivestring+=r'<BR ALIGN="LEFT" /><FONT POINT-SIZE="'+str(max(2,6-len(space)))+r'"'+(r' COLOR="red">' if k in deriveclass else '>')+space*int(6/max(3,6-len(space))+0.5)+k+r'</FONT>'
     if k in deriveclass:
      derivestring+=deriveclassrecursivestring(k,space+'  ')
   return derivestring
  for count,i in enumerate(filek):
   if not os.path.exists(r'./'+i[1]+r'.dotx'):
    continue
   print(fr'writing to file {i[1]}.dot_ {count+1}/{len(filek)}')
   with open(i[1]+'.dotx') as fp:
    data=fp.read()
   if i[1] in deriveclass:
    data=re.sub(r'(.*)}\s*$',r'\1',data,flags=re.I|re.DOTALL)
    data+='\n'+r'"'+i[1]+'.derived'+r'" [color="green",label=<<TABLE border="0"><TR><TD>'+deriveclassrecursivestring(i[1],"")+r'<BR ALIGN="LEFT" /></TD></TR></TABLE>>, shape="record",style="solid"];'
    data+='\n'+r'"'+i[1]+'.derived'+r'" -> "'+i[1]+r'" [arrowhead="empty", arrowtail="none"];'+'\n}'
   with open(i[1]+r'.dot_','w') as fp:
    fp.write(data)
   os.remove(i[1]+'.pdf') if os.path.exists(i[1]+'.pdf') else None
   subprocess.call(shlex.split(r'dot -Tpdf '+i[1]+'.dot_ -o '+i[1]+'.pdf'))
  sys.path.append(os.path.expanduser('~')+r'/tmp')
  from MISC.utillib.util import Util
  Util().concatpdf('.')
  print(f'---- MODIFY FINISHED dir={sys.argv[1:]}')
 def dirpathtopackage(self,i):#/tkinter/filedialog/FileDialog -> tkinter.filedialog.FileDialog
#  return re.sub(r'/+',r'.',re.sub(r'(.*?)(?:/*__init__)?[.]py$',r'\1',i[0]))+r'.'+i[1]
#  return re.sub(r'/+',r'.',re.sub(r'(.*?)(?:/*__init__)?[.][^.]+$',r'\1',i))
  return re.sub(r'/+',r'.',re.sub(r'(.*?)(?:/*__init__)?[.][^.]+$',r'\1',re.sub(r'/*$','',i)))
if getarg('--fix'):
 fix()
elif getarg('--modify'):
 modify()
