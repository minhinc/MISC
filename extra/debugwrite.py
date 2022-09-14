import builtins
import os,re
import configparser
#write to config file 'minh.ini' as
#import configparser;config=configparser.ConfigParser()
#config.add_section('debug');cfg['debug']['level']='1'
#with open(os.path.expanduser('~')+r'/minh.ini') as configfile:
# config.write(configfile)
config=configparser.ConfigParser()
config.read(os.path.expanduser('~')+r'/minh.ini')
def print(*arg,**kwarg):
 (int(config['debug']['level'])==1 and not re.search(r'^\s*(><|<=>|<>)',str(arg[0])) or int(config['debug']['level'])==0) and builtins.print(*arg,**kwarg)
