import builtins
import os,re
import configparser
#write to config file 'minh.ini' as
'''
######## minh.ini ########
[debug]
 level=0
#######
'''
config=configparser.ConfigParser()
if not os.path.exists(os.path.expanduser('~')+r'/minh.ini'):
 config.add_section('debug');config['debug']['level']='1'
 with open(os.path.expanduser('~')+r'/minh.ini','w') as configfile:
  config.write(configfile)
 builtins.print(r'''####################### ~/minh.ini missing ##################
  ...created
#################''')
config.read(os.path.expanduser('~')+r'/minh.ini')
def print(*arg,**kwarg):
 (int(config['debug']['level'])==0 and not re.search(r'^\s*(><|<=>|<>)',str(arg[0])) or int(config['debug']['level'])==1) and builtins.print(*arg,**kwarg)
