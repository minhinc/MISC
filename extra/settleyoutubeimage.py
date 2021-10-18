import json,sys,os,re
sys.path.append('..')
from utillib import requestm
from gtc import databasem
db=databasem.databasec(False)
for i in sys.argv[1:]:
 imagefile=[j[1] for j in json.loads(re.sub(r'\\\n',r'\\n',db.get('tech','content','name',i)[0][0]))["youtube"]]
 print('tech,imagefile',i,imagefile)
# os.system('~/tmp/ftp.sh mdelete image '+' '.join([j+'.jpg' for j in imagefile]))
# [requestm.youtubeimage(j) for j in imagefile]
 os.system('~/tmp/ftp.sh mput image '+r' '.join([r'./'+j+'.jpg' for j in imagefile]))
# os.system('~/tmp/ftp.sh mput image '+r'./'.join([j+'.jpg' for j in imagefile]))
