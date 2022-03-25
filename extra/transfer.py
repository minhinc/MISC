import sys,os,shutil
import re
if len(sys.argv)<=2:
 print('''usage
python3 transfer.py <destinationdir> [<files>|<<filename>>]
python3 transfer.py ~/tmp/MISC_new/extra/imageviewer CustomMenu.qml CustomMenuItem.qml
python3 transfer.py ~/tmp/MISC_new/extra/imageviewer <~/tmp/t.txt>''')
 sys.exit(-1)
file=re.split('\n',open(os.path.expanduser(re.sub(r'^<(.*)>$',r'\1',sys.argv[2]))).read()) if re.search(r'^<.*>$',sys.argv[2]) else sys.argv[2:]
for i in [i for i in file if i]:
# print(rf"copy file ./{i} -> ",sys.argv[1]+(r'/'+re.sub(r'^(.*)/.*',r'\1',i) if re.search(r'/',i) else ''))
 print(shutil.copy2(i,sys.argv[1]+(r'/'+re.sub(r'^(.*)/.*',r'\1',i) if re.search(r'/',i) else '')))
