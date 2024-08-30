import builtins
import sys
import os,re
import configparser
#write to config file 'minh.ini' as
#debug level 'F' 'I' 'C' -> "FUNCTION ENTRY MIDDLE OUT" "INFO" "CRITICAL"
#TODELETE 'D' will be displace below 'C' level, no need to set it as level explicitely
'''
######## minh.ini ########
[debug]
 level=0
#######
'''
config=configparser.ConfigParser()
if not os.path.exists(os.path.expanduser('~')+r'/minh.ini'):
 config.add_section('debug');config['debug']['level']='F'
 with open(os.path.expanduser('~')+r'/minh.ini','w') as configfile:
  config.write(configfile)
 builtins.print(r'''####################### ~/minh.ini missing ##################\n...created\n#################''')
config.read(os.path.expanduser('~')+r'/minh.ini')
def print(*arg,**kwarg):
 printlevel=re.sub(r'^\s*(.)\s+.*',r'\1',arg[0],flags=re.DOTALL)
 if not len(printlevel)==1 or not printlevel.isupper() or printlevel not in 'EMOIDC':
  builtins.print(f'PRINT LEVEL MUST BE [[EMO]|I|D|C]\n{arg=} {kwarg=} {printlevel=} ,exiting..')
  sys.exit(-1)
# (int(config['debug']['level'])==0 and not re.search(r'^\s*(><|<=>|<>)',str(arg[0])) or int(config['debug']['level'])==1) and builtins.print(*arg,**kwarg)
 if config['debug']['level']=='F' or config['debug']['level']=='I' and not re.search('^[EMO]$',printlevel) or config['debug']['level']=='C' and not re.search('^[DEMOI]$',printlevel):
  builtins.print(*(re.sub(r'^\s*I\s+','',arg[0]),*arg[1:]),**kwarg)
