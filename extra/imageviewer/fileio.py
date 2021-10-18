import os
from PySide6.QtCore import Signal, QObject, Property, Slot, QFile, QIODevice
import re
import subprocess
from threading  import Thread
import shlex,signal

class FileIO(QObject):
 sourceChanged = Signal()
 threaddataChanged = Signal(str)
 def __init__(self,parent=None):
  super(FileIO,self).__init__(parent)
  self._source=None
  self._stopthread=False

 @Property(str, notify=sourceChanged)
 def source(self):
  return self._source

 @source.setter
 def source(self,value):
  self._source=re.sub(r'^file://','',value)
  self.sourceChanged.emit()

 @Property(bool)
 def stopthread(self):
  return self._stopthread

 @stopthread.setter
 def stopthread(self,value):
  self._stopthread=value
  if self._stopthread==True:
   self.t.join()
   print('><FileIO.stopfire')

 @Slot(str,result=str)
 @Slot(result=str)
 def filestring(self,filename=None):
#  return open(self._source if not filename else filename).read()
  if not os.path.isfile(filename):
   print(f'fileio.getstring {filename} does not exists, creating new')
   with open(filename,'x') as file:
    pass
  return open(filename).read()

 @Slot(str,str)
 def save(self,file,text):
  print('fileio.save file',file)
#  open(self._source,'w').write(text)
  open(file,'w').write(text)

 def threadfunc(self,filename):
  print('threadfunc',filename)
#  proc = subprocess.Popen(["python3","/home/minhinc/tmp/MISC/ffmpeg/test/test.py"], shell=False, bufsize=1, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
  proc = subprocess.Popen(shlex.split(rf'python3 {filename}'), preexec_fn=os.setsid, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
  print('proc pid, process group pid',proc.pid,os.getpgid(proc.pid))
  while self._stopthread==False and proc.poll() is None:
   self.threaddataChanged.emit(proc.stdout.readline().decode('utf-8'))
  else:
   if self._stopthread==True:
    self.threaddataChanged.emit("---- INTERRUPTED -----")
    print('proc.pid, killing process group',proc.pid,os.getpgid(proc.pid))
    os.killpg(os.getpgid(proc.pid),signal.SIGTERM)
#    proc.terminate()
    proc.wait()
  proc.stdout.close()
  self._stopthread=False
  print('thread exited')

 @Slot(str)
 def fire(self,testfile):
  self.t=Thread(target=self.threadfunc,args=(testfile,))
  self.t.daemon=True
  self.t.start()

 @Slot(str,result=str)
 def cachefile(self,file):
  print(f'FileIO cachefile{file=}')
  if not os.path.isdir(os.path.expanduser('~')+r'/tmp/cacheimage'):
   os.makedirs(os.path.expanduser('~')+r'/tmp/cacheimage')
  os.system('cp '+file+' '+os.path.expanduser('~')+r'/tmp/cacheimage/'+re.sub(r'^.*/(.+)$',r'\1',file,flags=re.I))
  return os.path.expanduser('~')+r'/tmp/cacheimage/'+re.sub(r'^.*/(.+)$',r'\1',file,flags=re.I)
