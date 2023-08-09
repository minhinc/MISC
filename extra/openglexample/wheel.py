import sys,os;sys.path.append(os.path.expanduser('~')+'/tmp')
from MISC.extra.shader import shader
class wheel(shader):
 def __init__(self,*arg,**kwarg):
  super().__init__(**dict({'objfile':'wheel.obj'},**kwarg))
 '''
 def display(self,**kwarg):
#  print(f"><wheel.display {kwarg=} {kwarg['parent'].children[kwarg['count']]['fixtransformation']=}")
  nearwheel=kwarg['parent'].children[kwarg['count']]['fixtransformation'] and kwarg['parent'].children[kwarg['count']]['fixtransformation'][0][2]>0
  rotationangle=kwarg['key']==b'y' and nearwheel and (10,0,0,-1) or kwarg['key']==b'Y' and nearwheel and (10,0,0,1) or kwarg['key']==b'y' and not nearwheel and (10,0,0,1) or (10,0,0,-1)
  if kwarg['active'] and 'key' in kwarg and kwarg['key'] and shader.utili.mode!='grand':
   if kwarg['key']==b'n':
    shader.utili.keyboard(b'y',kwarg['parent'].children[kwarg['count']]['fixtransformation'])
    if [x for x in kwarg['parent'].children[kwarg['count']]['fixtransformation'] if len(x)==4 and not type(x[0])==str and abs(x[3])==1]:
     [kwarg['parent'].children[kwarg['count']]['fixtransformation'].remove(x) for x in kwarg['parent'].children[kwarg['count']]['fixtransformation'][:] if len(x)==4 and not type(x[0])==str and abs(x[3])==1]
     kwarg['parent'].children[kwarg['count']]['fixtransformation'][-1:]=[]
   elif kwarg['key']==b'f':
    shader.utili.keyboard(b'Y',kwarg['parent'].children[kwarg['count']]['fixtransformation'])
   elif kwarg['key']==b'y' or kwarg['key']==b'Y':
    tmp=None
    if abs(kwarg['parent'].children[kwarg['count']]['fixtransformation'][-1][2])==1:
     tmp=kwarg['parent'].children[kwarg['count']]['fixtransformation'].pop(-1)
    shader.utili.keyboard(kwarg['key']==b'y' and nearwheel and b'Z' or kwarg['key']==b'Y' and nearwheel and b'z' or kwarg['key']==b'y' and not nearwheel and b'z' or b'Z',kwarg['parent'].children[kwarg['count']]['fixtransformation'])
    kwarg['parent'].children[kwarg['count']]['fixtransformation'][-1][0]=max(min(kwarg['parent'].children[kwarg['count']]['fixtransformation'][-1][0],20),-20)
    if tmp:
     kwarg['parent'].children[kwarg['count']]['fixtransformation'].append(tmp)
    shader.utili.mode=tmp
#   kwarg['parent'].children[kwarg['count']]['fixtransformation'].append(rotationangle)
  super().display(**kwarg)
 '''
 def display(self,**kwarg):
  if hasattr(shader.keyboard,'key') and kwarg['active'] and shader.utili.mode!='grand':
   if not hasattr(self,'extratransformation'):
    setattr(self,'extratransformation',[])
   mode=shader.utili.mode
   shader.utili.mode='grand'
   if shader.keyboard.key in 'nf':
    self.extratransformation=[x for x in self.extratransformation if not x[3]==1]
    shader.utili.keyboard(shader.keyboard.key=='n' and b'y' or b'Y',self.extratransformation)
   elif shader.keyboard.key in 'yY':
    print(f'TEST wheel {self.extratransformation=}')
    if self.orientation=='left':
     shader.utili.keyboard(shader.keyboard.key=='y' and b'Z' or b'z',self.extratransformation) if -30<sum([x[0] for x in self.extratransformation if x[3]==1])+(-10 if shader.keyboard.key=='y' else 10)<30 else None
    elif self.orientation=='right':
     shader.utili.keyboard(shader.keyboard.key=='y' and b'z' or b'Z',self.extratransformation) if -30<sum([x[0] for x in self.extratransformation if x[3]==1])+(-10 if shader.keyboard.key=='Y' else 10)<30 else None
    print(f'TEST wheel {sum([x[0] for x in self.extratransformation if x[3]==1])=}')
   shader.utili.mode=mode
  super().display(**kwarg)
