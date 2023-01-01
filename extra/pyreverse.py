from collections import OrderedDict
import re,os,sys
import shlex
import subprocess
sys.path.append(os.path.expanduser('~')+r'/tmp')
import MISC.ffmpeg.libm
libi=MISC.ffmpeg.libm.libc()
fileextension='py|pyx|pxd|pxi|pyi'
def convert2localdir(file):
 localdir=re.sub(r'^.*?[.].*$','.',re.sub(r'^[./]*(.*?)(/[^/]+)?$',r'\1',file))
 localdirfile=localdir+r'/'+re.sub(r'^(?:.*/)?(.*)[.][^.]+$',r'\1'+'.py',file)
 return (localdir,localdirfile)
def getarg(arg,count=1):
 ret=False
 if [x for x in sys.argv if re.search(arg,x)]:
  ret=sys.argv[sys.argv.index(arg)+1] if count>1 else True
  sys.argv[sys.argv.index(arg):sys.argv.index(arg)+(2 if count>=2 else 1)]=''
 return ret
def usage():
 print(f'''\
  --- usage ---
  Note - directory /usr/lib/python3//dist-packages package sklearn modulefile sklearn/base.py
  python3 pyreverse.py --fix <directory> <[package|modulefile]> [modulefile]...
  python3 pyreverse.py --modify <package|modulefile> [classname] [classname]...
  python3 pyreverse.py --exclude <class>
  python3 pyreverse.py --timeout <sec>
  python3 pyreverse.py --association <level>
  python3 pyreverse.py --ancestor <level>
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
print(f'TEST {excludeclass=} {timeout=} {colorized=} {association=} {ancestor=}')

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
  print(f'{file=}')
  for k in file:
   with open(k) as file:
    filedata=re.sub(r'\n+',r'\n',re.sub(r'^\s*(#.*|)$',r'',re.sub(r"(^|\n)[^\n]*?'''.*?'''[^\n]*",'',re.sub(r'(^|\n)[^\n]*?""".*?"""[^\n]*','',file.read(),flags=re.DOTALL),flags=re.DOTALL),flags=re.M),flags=re.DOTALL) if re.search(r'[.](pyx|pxd|pxi)$',k,flags=re.I) else file.read()
   if re.search(r'.*[.](pyx|pxd|pxi)$',k):
    filedata=re.sub(r'(?P<id1>^|\n)(?P<id2>(?:c?import\s+|from\s+|__all__\s+).*?)(?=\n[^) \t]|$)',lambda m:m.group('id1')+re.sub(r'(?:\\+[ \t]*)?\n+',' ',m.group('id2'),flags=re.DOTALL),filedata,flags=re.DOTALL)
    filedata=re.sub(r'(?P<id>^|\n)(?P<id2>\s*cp?def\s+)?(?P<id3>class\s+.*?)(?=:|\n\S*def|class|\S*import|from|__all__|:\s*pass)',lambda m:m.group('id')+re.sub(r'(?:\\+\s*)?\n+',' ',m.group('id3'),flags=re.DOTALL),filedata,flags=re.DOTALL)
    filedata=re.sub(r'(?P<id>^|\n)(?P<id2>\s*(?:async\s+)?(?:cp?)?def\s+(?!class)[^#\n]*?\S+?\s*\()(?P<id3>.*?)(?:\)[^)]*?)(?=:[^\n]*|\n)',lambda m:m.group('id')+re.sub(r'^(?P<id11>\s*).*?def\s+.*?(?P<id12>\S+\s*\()$',lambda m:m.group('id11')+'def '+re.sub(r'[^a-zA-Z0-9_( ]','_',m.group('id12')),m.group('id2'),flags=re.M)+','.join(re.sub(r'^.*(\**\b[a-zA-Z0-9_]+).*$',r'\1',re.sub(r'(=|:).*','',x)) for x in re.split(',',re.sub(r'\n+',' ',re.sub(r'(\[.*?\]|\(.*?\)|{.*?}|\.)','',m.group('id3')))) if not re.search(r'^\s*\d',x) and re.search(r'^[a-zA-Z0-9_* ]+$',re.sub(r'(=|:).*','',x)))+r'):pass',filedata,flags=re.I|re.DOTALL)
#    print(f'TEST BEFORE {k=}')
#    print(filedata)
    filedata=re.sub(r'(?P<id>^|\n)(?P<id2>\s*@.*?)(?=\n\s*(@|async|def|class))',lambda m:m.group('id')+re.sub(r'(?:\\+[ \t]*)?\n+','',m.group('id2'),flags=re.DOTALL),filedata,flags=re.DOTALL)
    for i in re.split('\n',filedata):
     if not re.search(r'^\s+',i) and re.search(r'\bclass\s+[^\n]+\n$',data,flags=re.DOTALL) and not re.search(r':\s*pass\s*\n$',data,flags=re.DOTALL):
      data=re.sub('\n$',(':pass\n' if not re.search(r':\s*$',data,flags=re.DOTALL) else 'pass\n'),data,flags=re.DOTALL)
     if re.search(r'^(c?import|(?:cp?def\s+)?class\s+|from\s+|__all__\s+)',i):
      data+=re.sub(r'cimport','import',i)+'\n'
     elif re.search(r'^\s*def\s+',i):
      if re.search(r'(^|\n)class\s+[^\n]+\n$',data,flags=re.DOTALL) and not re.search(r':\s*pass[^\n]*\n$',data,flags=re.DOTALL):
       mode=re.sub(r'^(\s*).*',r'\1',i)
      if re.search(r'^\s*def\s+(?!class)\S+?\s*\([^()]*\):',i) and not re.search(r'\b\d+\b',i) and re.sub(r'^(\s*).*',r'\1',i)==mode:#definition signature
       data+=re.sub(r'\)\s*:pass.*$','):pass',i)+'\n'
     elif re.sub(r'^(\s*)@.*',r'\1',i)==mode or re.search(r'^@',i):
      data+=i+'\n'
      mode='' if re.search(r'^@',i) else mode
     elif not re.search(r'^\s+',i):
      mode=re.sub(r'^(\s*).*',r'\1',i)
    mode=''
   elif re.search(r'.*[.](py|pyi)$',k):
    filedata=re.sub(r'(?P<id>^|\n)(?P<id2>\s*)def(?P<id3>\s+[^(]+\()(?P<id4>[^#]*?)(?=\)[^\)]*:)',lambda m:m.group('id')+m.group('id2')+'def'+re.sub(r'[^a-zA-Z0-9_( ]','_',m.group('id3'))+','.join(re.sub(r'^.*?(\**\b[a-zA-Z0-9_]+).*$',r'\1',x) for x in re.split(',',re.sub(r'\n+',' ',re.sub(r'(\[.*?\]||\(.*?\)|{.*?}|\.)','',m.group('id4'),flags=re.DOTALL),flags=re.DOTALL)) if not re.search(r'^\s*\d',x) and re.search(r'^[a-zA-Z0-9_* ]+$',re.sub(r'(=|:).*','',x))),filedata,flags=re.DOTALL)
    for i in re.split('\n',filedata):
     if re.search(r'^w+\s*=\s*\w+\s*\(\s*["\']\w+["\']\s*,\s*\(.*?\).*?{.*?}.*?\)',i) and not re.search(r').*?\(\)\s*$',i):
      base=re.sub(r'^\s*(.*?)\s*=\s*(.*?)\s*\(\s*["\']\s*(\w+)\s*["\']\s*,\s*\((.*?)[, ]*\).*$',r'\1'+DELIMITER+r'\2'+DELIMITER+r'\3'+DELIMITER+r'\4',i)
      data+='class '+re.split(DELIMITER,base)[0]+r'('+(re.split(DELIMITER,base)[3]+r',' if not re.search(r'^\s*$',re.split(DELIMITER,base)[3]) else '')+r'metaclass='+re.split(DELIMITER,base)[1]+r'):pass'+'\n'
     else:
      data+=i+'\n'
   tmp=r'/'+re.sub(r'^'+sys.argv[1]+r'/*','',k)
   if not os.path.exists(convert2localdir(tmp)[0]):
    os.makedirs(convert2localdir(tmp)[0])
   if os.path.exists(convert2localdir(tmp)[1]):
#    print(f'TEST exists {k=}')
#    print(data)
    filedata1=open(convert2localdir(tmp)[1]).read()
    filedata2=''
    for i in re.split('\n',data):
     if not re.search(r'^\s*$',i) and not re.search(r'\b(import|__all__)\b',i):
      break
     filedata2+=i+'\n'
    filedata1=filedata2+'\n'+filedata1
    for i in re.findall(r'^class\s+(\w+)\b.*$',data,flags=re.M):
     if re.search(r'^class\s+'+i+r'\b.*$',filedata1,flags=re.M) and not re.search(r'(^|\n)class\s+'+i+r'(\b[^:]*:\s*pass)',data,flags=re.DOTALL):
      filedata1=re.sub(r'(?:^|\n)class\s+'+i+r'\b[^:]*:[^\n]*\n(?:\s*pass\s*\n)?',re.sub(r'^.*?((?:^|\n)class\s+'+i+r'\b.*?)(?:\n\S.*$|$)',r'\1'+'\n',data,flags=re.DOTALL),filedata1,flags=re.DOTALL)
      tmp2=re.sub(r'(?:^|\n)class\s+'+i+r'\b[^:]*:.*?\n([ \t]+)\S+.*$',r'\1',flags=re.DOTALL) if os.path.exists(convert2localdir(tmp)[1]) and re.search(r'(?:^|\n)class\s+'+i+r'\b[^:]*:\s*(?!pass)',convert2localdir(tmp)[1]) else '    '
#      filedata1=re.sub(r'(?P<id>(?:^|\n)class\s+[^\n]*?\n)(?P<id2>.*?)(?=\n\S|$)',lambda m:m.group('id')+re.sub(r'^\s+','    ',m.group('id2'),flags=re.M),filedata1,flags=re.DOTALL)
      print(f'TEST {k=} {tmp2=}')
      filedata1=re.sub(r'(?P<id>(?:^|\n)class\s+'+i+r'[^\n]*?\n)(?P<id2>.*?)(?=\n\S|$)',lambda m:m.group('id')+re.sub(r'^\s+',tmp2,m.group('id2'),flags=re.M),filedata1,flags=re.DOTALL)
     elif not re.search(r'^class\s+'+i+r'\b.*$',filedata1,flags=re.M):
      filedata1+='\n'+re.sub(r'(?:^|^.*?\n)(class\s+'+i+r'\b.*?)(?:\n\S.*$|$)',r'\1',data,flags=re.DOTALL)
    open(convert2localdir(tmp)[1],'w').write(filedata1)
   else:
    with open(convert2localdir(tmp)[1],'w') as file:
     file.write(data)
   data=''
   print(k,convert2localdir(tmp)[1])
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
    return re.findall(r'^class\s+(.+?)\b.*:\s*(?:pass\s*|#.*)?$',open(filename).read(),flags=re.M)
   else:
    return re.findall(r'^class\s+('+hint+r')\b.*:\s*$',open(filename).read(),flags=re.I|re.M)
  if re.search(r'[.]py$',sys.argv[1]):
   if len(sys.argv)>=3 and not re.search(r'[.]py$',sys.argv[2]):
    file=[(sys.argv[1],self.dirpathtopackage(sys.argv[1])+'.'+i) for i in sys.argv[2:]]
   else:
    for i in sys.argv[1:]:
     for k in classname(i):
      file.append((i,self.dirpathtopackage(i)+r'.'+k))
  else:
   for i in [y for k in sys.argv[1:] for y in os.walk(k)]:
    for j in [j for j in i[2] if re.search(r'[.]py$',j)]:
     for k in classname(i[0]+r'/'+j):
      file.append((re.sub(r'/+$','',i[0])+r'/'+j,self.dirpathtopackage(i[0]+r'/'+j)+'.'+k))
  filek=file
  file=[i for i in file if not os.path.exists(r'./'+i[1]+'.dotx')]
  print(f'list of file,class to be processed (.dot file do not exists)={file}')
  for count,i in enumerate(file):
   print(fr'package={i} {count+1}/{len(file)}')
   try:
    if subprocess.call(shlex.split('pyreverse -f ALL '+i[0]+(' --colorized ' if colorized else '')+(r' -A' if ancestor==False else ' -a '+ancestor+' ')+('S' if association==False else ' -s '+association+' -')+'my --show-builtin -c '+i[1]),timeout=timeout):
     wrongfile.write(rf'{i}'+'\n');wrongfile.flush()
     del filek[[count for count in range(len(filek)) if filek[count][1]==i[1]][0]]
     continue 
   except subprocess.TimeoutExpired:
    print(f"Timedout file={i[0]} class={i[1]}")
    print(f'trying with -A -s 1 -my -c new')
    if subprocess.call(shlex.split('pyreverse -f ALL '+i[0]+(r' -A' if ancestor==False else ' -a '+ancestor+' ')+' -s 1 -my -c '+i[1])):
     wrongfile.write(rf'{i}'+'\n');wrongfile.flush()
     del filek[[count for count in range(len(filek)) if filek[count][1]==i[1]][0]]
     continue
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
   for y in [y for x in set(re.findall(r'^\s*(.*?)\s+\[.*?arrowhead="diamond".*$',data,flags=re.M)) for y in re.findall(r'^(\s*'+x+r'\s+\[.*?arrowhead="diamond".*)$',data,flags=re.M)[1:]]:
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
    tmp2=[y for y in re.findall(r'^\s*("[^"]+")\s+->\s+'+x+r'\s+\[.*?arrowhead="diamond".*$',data,flags=re.M) if not re.search(r'^\s*'+y+r'\s+->\s+(?!(?:'+y+r'|'+x+'))"[^"]+"\s+\[.*$',data,flags=re.M) and not re.search(r'^\s*(?!'+y+r')"[^"]+"\s+->\s+'+y+r'\s+\[.*$',data,flags=re.M) and not y=='"'+i[1]+'"']
    if len(tmp2)>2:
     for y in tmp2:
      tmp+=r'<BR ALIGN="LEFT" /><FONT POINT-SIZE="6" COLOR="black">'+' '*6+y+r'</FONT>'
      data=re.sub(r'^\s*'+y+r'\s+->\s+'+x+r'\s+\[.*?arrowhead="diamond".*$','',data,flags=re.M)
      data=re.sub(r'^\s*'+y+r'\s+\[.*$','',data,flags=re.M)
      data=re.sub(r'^\s*'+y+r'\s+->\s+'+y+r'\s+\[.*$','',data,flags=re.M)
     if tmp:
      data=re.sub(r'(.*)}\s*$',r'\1',data,flags=re.I|re.DOTALL)
      data+='\n'+r'"'+re.sub(r'"([^"]+)"',r'\1',x)+'.aggregation'+r'" [color="yellow",label=<<TABLE border="0"><TR><TD>'+tmp+r'<BR ALIGN="LEFT" /></TD></TR></TABLE>>, shape="record",style="solid"];'
      data+='\n'+r'"'+re.sub(r'"([^"]+)"',r'\1',x)+'.aggregation'+r'" -> '+x+r' [arrowhead="diamond", arrowtail="none"];'+'\n}'
   data=re.sub(r'\n+','\n',data,flags=re.DOTALL)
   open(i[1]+'.dotx','w').write('\n'.join(list(OrderedDict.fromkeys(re.split('\n',data)))))
  wrongfile.close()
  def insertintofile(file,line):
   data=open(file).read()
   with open(file,'w') as tmpfile:
    tmpfile.write(re.sub(r'}\s*$',line+'\n}\n',data,flags=re.DOTALL))
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
  return re.sub(r'/+',r'.',re.sub(r'(.*?)(?:/*__init__)?[.][^.]+$',r'\1',i))
if getarg('--fix'):
 fix()
elif getarg('--modify'):
 modify()
