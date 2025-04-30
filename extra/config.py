import builtins,sys,os,re,configparser,inspect,pathlib
import sys;sys.path.append(os.path.expanduser('~')+'/tmp') if not os.path.expanduser('~')+'/tmp' in sys.path else None
import json
import traceback

class _configc:
 configfilepath=os.path.expanduser('~')+'/minh.ini'
 def __init__(self,**kwarg):
#  _configc.cmc=self.createmoduleclassinstance
  self.config=configparser.ConfigParser()
  if not os.path.exists(_configc.configfilepath):
   '''
   write to config file 'minh.ini' as
   debug level 0 1 2-> "FUNCTION ENTRY/MIDDLE/OUT [EMO]" "INFO [I]"/"TODELETE [D]" "CRITICAL [C]"
   ######## minh.ini ########
   [debug]
    level=0
   #######
   '''
   self.config.add_section('debug');self.config['debug']['level']='0'
   with open(_configc.configfilepath,'w') as configfile:
    self.config.write(configfile)
   builtins.print(f"{'':#^40}\n{'~/minh.ini missing':#^40}\n{'...created':#^40}")
  self.config.read(_configc.configfilepath)

 def shortname(self,*,instance_,keyvaluepair_):
  for k in keyvaluepair_:
   setattr(instance_.__class__,k,getattr(instance_,keyvaluepair_[k]))

 def checkmandatoryhashkeyword(self,hash_,keywordt_):
  '''check if extra keyword, other than in keywordt_ must not be available in hash_'''
  extrakeywords=[x for x in hash_ if x not in keywordt_]
  if extrakeywords:
   raise Exception(f'<=> checkmandatoryhashkeyword keywords {extrakeywords=} is not part of permitted keywords')

 def checkattributecollision(self,instance_,attributet_):
  '''
  if re.search(r'checkattributecollision',traceback.extract_stack(None,3)[0][2]):#break cycle
   print(f'I cycle detected {traceback.extract_stack(None,3)[0][2]} -> {traceback.extract_stack(None,3)[1][2]} -> {traceback.extract_stack(None,3)[2][2]}')
   return
  if hasattr(instance_,'__mro__'):
   instance_=instance_()
  for i in instance_.__class__.mro():
   for j in attributet_:
    if hasattr(i(),j):
     raise Exception(f'C attribute {j} found in class {i}')
  '''
  for i in attributet_:
   if hasattr(instance_,i):
    raise Exception(f'C attribute {i} already found in {instance_.__class__=}')

 def __getitem__(self,items_):
  return self.config[items_]

 def setconfig(self, section, key, value):
  '''\
  set key=value in section 'section' of configuration file ~/minh.ini
  section : str -> section name ,i.e. debug
  key : str -> key under section 'section' ,i.e level
  value : [int|str|float|complex] -> key value under section 'section' key ,i.e [debug][level]

  setconfig('debug','level','1.0') # sets float 1.0 to ['debug']['level']
  setconfig('debug','level','"1.0"') # set string "1.0" to ['debug']['level']
  -> None\
  '''
  self.config[section][key]=value
  with open(_configc.configfilepath,'w') as configfile:
   self.config.write(configfile)
  self.config.read(self.configfilepath)
  print(f'I written to {_configc.configfilepath} ,new value {config[section][key]=}')

 def __call__(self, *arg,**kwarg):
  '''\
  custom printing at certain print level 0-2
  *arg - comma seperated arguments to print
  **kwarg - keyword arguments in print, i.e end= etc..
  Note : debug level in ~/minh.ini mappings
         2 -> [Ee]/<> [Mm]/<=> [Oo]/<>
         1 -> [Ii]/^ [Dd]/=
         0 -> [Cc] <

  from MISC.extra.config import _config as print
  print(f'E print does custom printing at certain debug level')
  print(f'>< print does custom printing at certain debug level')
  print(f'C system down')
  print('< system down')
  -> None\
  '''
  arg=list(arg)
  printdebugstr=r'[Ee]\s+|><\s*|[Mm]\s+|<=>\s*|[Oo]\s+|<>\s*|[Dd]\s+|=\s*|[Ii]\s+|\^\s*|[Cc]\s+|<\s*'
  printlevels=re.sub(r'\s+$','',re.sub(r'^\s*('+printdebugstr+').*',r'\1',arg[0])) if re.search(r'^\s*('+printdebugstr+')',arg[0]) else 'E'
  arg[0]=re.sub(r'^\s*('+printlevels+')\s*',r'\1'+(f' {inspect.stack()[1][0].f_locals["self"].__class__.__name__}' if "self" in inspect.stack()[1][0].f_locals else " ")+f'.{inspect.stack()[1][0].f_code.co_name} ',arg[0],flags=re.DOTALL)
#  builtins.print(f'_configc.__call_ {printlevels=} {arg[0]=}')
  if int(self.config['debug']['level'])==2 or int(self.config['debug']['level'])==1 and not re.search('^(Ee|><|Mm|<=>|Oo|<>)$',printlevels) or int(self.config['debug']['level'])==0 and not re.search('^(Ee|><|Mm|<=>|Oo|<>|Dd|=|Ii|\^)$',printlevels):
   builtins.print(*arg, **kwarg)

 def createmoduleclassinstance(self,modulename,classobj,*arg,**kwarg):
  '''\
  creates module level classobj instance and assign it to sys[modulename][classobj[c]_i] attribute
  modulename:str -> name of module,i.e. generally passed as __name__ from the module
  classobj:class -> class object for which instance has to be created and tied to module
  *arg:list -> list of non keyword arguments, would be passed as it is to class __init__ constructor
  **kwarg:dict -> dict of keyword argumetns, would be passed as it is to class __init__ constructor
  -> None
  '''
#  print(f'><_configc.createmoduleclassinstance {modulename=} {classobj=} {arg=} {kwarg=}')
  classinstancename=re.sub('c$','',classobj.__name__)+'i'
#  print(f'I _configc.createmoduleclassinstance {modulename=} available {dir(sys.modules[modulename])=}') if modulename in sys.modules else print(f'I _configc.createmoduleclassinstance {modulename=} not avilable')
  alreadyloadedmodule=[sys.modules[xx] for xx in sys.modules if hasattr(sys.modules[xx],'__file__') and hasattr(sys.modules[xx],'__name__')  and not sys.modules[xx].__name__ == sys.modules[modulename].__name__ and str(pathlib.Path(str(sys.modules[xx].__file__)).resolve())==str(pathlib.Path(str(sys.modules[modulename].__file__)).resolve())]
  setattr(sys.modules[modulename],classinstancename,getattr(alreadyloadedmodule[0],classinstancename) if alreadyloadedmodule else classobj(*arg,**kwarg))
 def type(self,arg_):
  if tuple==type(arg_) or list==type(arg_):
   return 'sequence'
  else:
   return type(arg_)

 def getcallinginstance(self):
  '''\
   returns the name of class instance calling the calling function of this function'''
  return inspect.stack()[2][0].f_locals["self"]

 def disablemultitouch(self):#remove red on right click
  '''remove red dot on moush right click'''
  from kivy.config import Config
  Config.set('input','mouse','mouse,disable_multitouch')
  Config.remove_option('input',r'%(name)s')
 def fixsyspath(self):
  sys.path=list(dict.fromkeys(sys.path))

"""
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
  str_=re.sub(r'^(?:\s*\n)?(.*?)(?:\n\s*)?$',r'\1',str_,flags=re.DOTALL)
  str_=re.sub(r'^'+re.sub(r'^(\s*).*',r'\1',str_,flags=re.DOTALL),'',str_,flags=re.M)
#  print(f'><_helpc.str2hash {str_=}')
  hashl=[dict()]
  tabspace=''
  for i in [i for i in re.split(r'\n',str_) if not re.search(r'^\s*$',i)]:
   key=re.sub(r'^\s*','',i)
   initialspace=re.sub(r'^(\s*).*$',r'\1',i)
   print(f'<=> {key=} {i=} {initialspace=} {tabspace=} {hashl=}')
   if re.search(r'^\s*--',i):
    if len(initialspace)<len(tabspace):
#     [hashl.pop() for l in range((len(tabspace)-len(initialspace))//len(_helpc.tabspace)+1)]
     [hashl.pop() for l in range((len(tabspace)-len(initialspace))//len(_helpc.tabspace))]
    print(f'<=> {hashl=}')
    hashl[-1][key]=dict()
    hashl.append(hashl[-1][key])
   elif re.search(r'^\s*-[^-]',i):
#    hashl[-1][key]=None
    hashl[-1][re.sub(r'(.*?)\s+.*',r'\1',key)]=re.sub(r'.*?\s+(.*)$',r'\1',key)
   tabspace=initialspace
  return hashl[0]

 def removetype(self,hashd_):
  if not type(hashd_)==dict:
   return hashd_
  return {re.sub(r'^(.*)\(\s+\)?$',r'\1',key):self.removetype(hashd_[key]) for key in hashd_}

 def cmd2hash(self,refhash_,argv_):
  '''refhash_(dict) reference command line help'''
  print(f'>< {refhash_=} {argv_=}')
  tabsize='    '
  tabspace=tabsize
  jsonstr='{'
  if not type(refhash_)==dict:
   refhash_=self.removetype(self.str2hash(refhash_))
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
     tabspace=re.sub(r'^'+tabsize,'',tabspace)
     jsonstr+='\n'+tabspace+'}'
    while key not in hashtmpl[-1][0]:
     hashtmpl.pop()
     tabspace=re.sub(r'^'+tabsize,'',tabspace)
     jsonstr+='\n'+tabspace+'}'
    jsonstr+=(',' if hashtmpl[-1][1]>=1 else '')+'\n'+tabspace+f'"{key}"'+' : {'
    hashtmpl[-1][1]+=1
    tabspace+=tabsize
    hashtmpl.append([hashtmpl[-1][0][key],0])
   elif re.search(r'^\s*-',key):
#    value="'"+re.sub(r'^\s*(\S+).*$',r'\1',argv_)+"'"
#    value="'"+re.sub(r'^\s*(.*?(?=\s+-|\s*$)).*$',r'\1',argv_)+"'"
    value=re.sub(r'^\s*(.*?(?=\s+-|\s*$)).*$',r'\1',argv_)
    argv_=re.sub(r'^\s*'+value+'(.*)',r'\1',argv_)
    if hashtmpl[-1][1]>=1:
     jsonstr=re.sub('$',',',jsonstr,flags=re.DOTALL)
    print(f'<=> cmd2str {key=} {value=} {jsonstr=}')
    jsonstr+='\n'+tabspace+f'"{key}"'+' : '+f'"{value}"'
    hashtmpl[-1][1]+=1
  while hashtmpl:
   tabspace=re.sub(r'^'+tabsize,'',tabspace)
   jsonstr+='\n'+tabspace+'}'
   hashtmpl.pop()
  print(f'<> _configc.cmd2hash jsonstr=\n')
  print(jsonstr)
  print(f'<=> {json.loads(jsonstr,object_pairs_hook=lambda o:o)=}')
  return json.loads(jsonstr,object_pairs_hook=lambda o:o)

 def sortlist(self,listl_,sortcriteriahash_):
  i=0
  for k in sortcriteriahash_:
   print(f'D {i=} {k=}')
   listl_=listl_[0:i]+sorted(listl_[i:],key=lambda m:not m[0]==k)
   print(f'D {listl_}=')
   i=([count for count in range(len(listl_)) if listl_[count][0]==k] or [0])[0]+1
  return listl_
"""

class _registryc:
 def register(self,classname_):
  '''\
  register classinstance so to help making singleton class intantiation to the caler
  classname_([so]) if string then classname_ for which classname_ object to be fetched
                   else classname_ is object which needs to be stored in list\
  _registryi.register(_sendmailc())
  '''
  if not hasattr(self,'registryl'):
   self.registryl=[]
  print(f'>< _config.register {classname_=} {self.registryl=}')
  if type(classname_) != str:
   if [x for x in self.registryl if x.__class__.__name__==classname_.__class__.__name__]:
    raise Exception(f'{classname_.__class_.__name__} already registered')
   else:
    self.registryl.append(classname_)
    return classname_
  else:
   classname_=[x for x in self.registryl if x.__class__.__name__==classname_]
   return classname_[0] if classname_ else None
_configc.createmoduleclassinstance(None,__name__,_configc)
#_configc.createmoduleclassinstance(None,__name__,_helpc)
_configc.createmoduleclassinstance(None,__name__,_registryc)
from MISC.extra.util import _jsonc
_configc.createmoduleclassinstance(None,__name__,_jsonc)
from MISC.extra.util import _helpc
#print(f'{_helpc=}')
_configc.createmoduleclassinstance(None,__name__,_helpc)
_configi.shortname(instance_=_configi,keyvaluepair_={'cmc':'createmoduleclassinstance','dmt':'disablemultitouch','cac':'checkattributecollision','cmh':'checkmandatoryhashkeyword'})
'''\
Other module to insert following line(s) at the end of module file
from MISC.extra.config import _configi;_configi.cmc(__name__,<classname>,<non-keyword arguments>,<keyword arguments>)
from MISC.extra.config import _configi;_configi.cmc(__name__,<classname>,1,2,3,'one'=1,'two'=2)
from MISC.extra.config import _configi;_configi.cmc(__name__,<classname>,*[1,2,3,4],*{'one':1,'two':2})
'''
