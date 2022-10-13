import re
import os
import magic
from PySide6.QtCore import QObject, Slot, Property#, QEnum, QFlag
#from enum import Enum, Flag

class Re(QObject):
 """
 @QFlag
 class Variant(Flag):
  Default,Dark,HighContrast=(re.I,re.DOTALL,re.MULTILINE)
 """
 def __init__(self,parent=None):
  super(Re,self).__init__(parent)
#  if not os.path.isdir('ffmpegtest'):
# os.mkdir('ffmpegtest')
# os.system(r'cp ../../MISC/ffmpeg/test/*.py ./ffmpegtest')

 @Property(int)
 def DOTALL(self):
  return re.DOTALL

 @Property(int)
 def MULTILINE(self):
  return re.MULTILINE

 @Property(int)
 def I(self):
  return re.I

 @Slot(str,str,str,result=str)
 @Slot(str,str,str,int,result=str)
 def sub(self,a,b,c,f=0):
#  print('a,b,c,f',a,b,c,f)
  return re.sub(a,b,c,flags=f)

 @Slot(str,str,result=bool)
 @Slot(str,str,int,result=bool)
 def search(self,a,b,f=0):
#  print('><Re.search a,b,f',a,b,f)
  retval=re.search(a,b,flags=f)
#  print('<Re.search> retval',retval)
  return True if retval else False
#  return re.search(a,b,flags=f)

 @Slot(str,result=str)
 def filetype(self,filename):
#  print('filetype ->',filename)
  print('file type->',magic.from_file(filename,mime=True) if os.path.isfile(filename) else 'nofile')
  return magic.from_file(filename,mime=True) if os.path.isfile(filename) else 'nofile'

 @Slot(str,result=str)
 def newfilename(self,path):
#  print('Rem.newfilename',path)
  return path+'/example'+str(max([int(re.sub(r'^\w+?(?P<id>\d+).*',lambda m:str(int(m.group('id'))+1),i) if re.search(r'\d+[.]py$',i,flags=re.I) else 1) for i in os.listdir(path) if os.path.isfile(path+r'/'+i) and re.search(r'example(\d+)?[.]py',i,flags=re.I)] or ['']))+'.py'

 @Slot(list,result=list)
 def sortfile(self,filelist):
  return sorted([x.toString() for x in filelist],key=lambda m:0.0 if not re.search(r'^.*?[\d+.]+[.][^.]+$',m) else float(re.sub(r'^.*?([\d+.]+)[.][^.]+$',r'\1',m)))
