import builtins,sys,os,re,configparser,inspect,pathlib
import sys;sys.path.append(os.path.expanduser('~')+'/tmp') if not os.path.expanduser('~')+'/tmp' in sys.path else None
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
  arg[0]=re.sub(r'^\s*('+printlevels+')\s*',r'\1'+(f' {inspect.stack()[1][0].f_locals["self"].__class__.__name__}' if "self" in inspect.stack()[1][0].f_locals else " ")+f'.{inspect.stack()[1][0].f_code.co_name} ',arg[0])
#  builtins.print(f'_configc.__call_ {arg[0]=}')
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
  print(f'><_configc.createmoduleclassinstance {modulename=} {classobj=} {arg=} {kwarg=}')
  classinstancename=re.sub('c$','',classobj.__name__)+'i'
  print(f'I _configc.createmoduleclassinstance {modulename=} available {dir(sys.modules[modulename])=}') if modulename in sys.modules else print(f'I _configc.createmoduleclassinstance {modulename=} not avilable')
  alreadyloadedmodule=[sys.modules[xx] for xx in sys.modules if hasattr(sys.modules[xx],'__file__') and hasattr(sys.modules[xx],'__name__')  and not sys.modules[xx].__name__ == sys.modules[modulename].__name__ and str(pathlib.Path(str(sys.modules[xx].__file__)).resolve())==str(pathlib.Path(str(sys.modules[modulename].__file__)).resolve())]
  print(f'D config.createmoduleclassinstance {alreadyloadedmodule=}')
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
_configc.createmoduleclassinstance(None,__name__,_configc)
_configi.shortname(instance_=_configi,keyvaluepair_={'cmc':'createmoduleclassinstance','dmt':'disablemultitouch','cac':'checkattributecollision','cmh':'checkmandatoryhashkeyword'})
'''\
Other module to insert following line(s) at the end of module file
from MISC.extra.config import _configi;_configi.cmc(__name__,<classname>,<non-keyword arguments>,<keyword arguments>)
'''
