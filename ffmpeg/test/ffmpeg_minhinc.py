import os,datetime,random,re,sys
sys.path.append(os.path.expanduser('~')+r'/tmp')
from MISC.ffmpeg.gifm import gifc
if len(sys.argv)<=1:
 print('usage ---\npython3 ffmpeg test.py "<title>" "=<videoneedsscaling.mp4>" "<duration>" "<without_=_firstreferencevideo.mp4>" "<duration>" .... "<[gif|.mp4|.mov|.png|text]:<audio>:<volume> <filter:position> <duration>" ....')
 print('python3 ffmpeg_techawal.py "Syntax Highlighting Pyside6 QML Chain-Of-Responsibility" "=VID_20210910_180110.mp4" "00:00:51-00:07:37" syntax.mp4 "00:00:00-00:27:05,00:28:05-00:57:30,00:57:43-01:00:34" syntax2.mp4 "00:00:00-00:21:18,00:21:40-00:22:08,00:22:38-00:24:27" "xyz.gif 5 00:20:00 00:30:00" "logo.png:ting.mp3:0.1 01:5 00:04:00-00:04:30" "Have a cup of Coffee... 23:52 00:31:47-00:34:20" "Have a cup of Coffee...:cork.mp3:10 23:52 00:31:47-00:34:20"')
 sys.exit(-1)
title=sys.argv[1]
g=gifc()
stroketuple=g.libi.setduration(sys.argv[2:])
print(f'title={title} duration={g.libi.duration} stroketuple={stroketuple}')


tempduration=None
stroketuple.append(('videologo_s.png','W-w,h','2-'+str(g.libi.duration-2)))
stroketuple.append((g.utili.logotext(size=0.3),5,0))

tempduration=g.libi.getslotstamp(min(int(g.libi.duration/1800),2),begintime=0)
stroketuple.append((g.utili.omnitext(re.sub(r'\s',r'\\n',title),size=max(0.6,1.0-len(re.split(r'\s',title))*0.1),duration=6),566,','.join(str(x) for x in [6]+tempduration if x)))
stroketuple.append(('cork.mp3',None,','.join(str(x+1.0) for x in [6]+tempduration if x)))
tempduration=g.libi.getslotstamp(min(int(g.libi.duration/400),3),begintime=0)
stroketuple.append((g.utili.image2gif('contact.gif',filtermode=re.sub(r'T/\d+',r'T/24',g.libi.filter['09']),duration=10),'(W-w)/2,(H-h)/2',','.join(str(x)+'-'+str(x+12) for x in tempduration)))
stroketuple.append((('cracker.gif','cracker.mp3',0.1),'(W-w-w/10)/2,(H-h)/2',','.join(str(x) for x in tempduration if x)))
 
stroketuple.append((title,('22',822),','.join((str(x)+'-'+str(x+10) for x in g.libi.getslotstamp(int(g.libi.duration/180),begintime=0) if x))))
#arguments
stroketuple.append(tuple([tuple([re.sub(r'\\:',':',z) for z in re.split(r'(?<!\\):',y)]) if re.search(r'(?<!\\):',y) and count!=2 else re.sub(r'\\:',':',y) for x in sys.argv[2:] if len(re.findall(r'\s+',x))>=2 for count,y in enumerate(re.findall(r'(.*)\s+(\S+)\s+(\S+)$',x)[0])])) if [x for x in sys.argv[2:] if len(re.findall(r'\s+',x))>=2] else None

print(f'######stroke tuple##### stroketuple={stroketuple}')
outputfile=re.sub(r'\s+','_',re.sub(r'[.]mp4','{0:%Y-%m-%d}'.format(datetime.datetime.now())+'.mp4',title+'_'+re.sub(r'(.*)[.]py$',r'\1',sys.argv[0])+'.mp4',re.I))
g.stroke2(*[x for x in stroketuple if x[-1] or x[-1]==0],outputfile=outputfile)# final mp4 creation
print(f'###################\n##############\n######  outputfile={outputfile}  ########\n################\n##############')
