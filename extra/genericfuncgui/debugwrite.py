import builtins
import os,re
import configparser
#write to config file 'minh.ini' as
#import configparser;config=configparser.ConfigParser()
#config.add_section('debug');cfg['debug']['level']='1'
#with open(os.path.expanduser('~')+r'/minh.ini') as configfile:
# config.write(configfile)
def print(*arg,**kwarg):
 if not hasattr('print','config'):
  print.config=configparser.ConfigParser()
  print.config.read(os.path.expanduser('~')+r'/minh.ini')
 if int(print.config['debug']['level'])==1 and not re.search(r'^\s*(><|<=>|<>)',str(arg[0])):
  builtins.print(*arg,**kwarg)
 elif int(print.config['debug']['level'])==0:
  builtins.print(*arg,**kwarg)
