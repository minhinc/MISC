#!/usr/bin/python3
import time
import sys,os,re
sys.path.append(f'/home/minhinc/tmp')
from MISC.ffmpeg.libm import libcm
_prints_=''
def exec(str_):
 global _prints_
 os.system(str_)
 _prints_+=('\n' if _prints_ else '')+str_
if not [x for x in sys.argv if re.search(r'[.]mp4$',x,flags=re.I)]:
 print(f'---usage---\n./a.py [*.mp4] [cutpoints]\n./a.py abc.mp4\n./a.py abc.mp4 1.2:23 34.4:$\n./a.py 0:23 34.5:$')
 sys.argv[1:1]=[re.findall(f'^(.*[.](?:(?!(?:py|mp3)).)*)$',os.popen(f'ls -t').read(),flags=re.M)[0]]
print(f'File to change {sys.argv[1:]=}\nsleep for 15 seconds press ctrl+c to cancel')
time.sleep(15)
_cutpointl_=[[y if re.search(r'\$',y) else str(int(re.sub(r'^(.*)[.].*$',r'\1',y))*60)+(re.sub(r'^.*([.].*)$',r'\1',y) if re.search(r'[.]',y) else '') for y in re.split(r':',x)] for x in sys.argv if re.search(r'^[0-9.:$]+$',x)]
_singleoutputfile_=re.sub(r'^(.*)[.](.*)$',r'\1'+'_a.'+r'\2',sys.argv[1])
_audiofile_=re.sub(r'^(.*)[.].*$',r'\1'+'.mp3',sys.argv[1])
exec(f"ffmpeg -i {sys.argv[1]} -y {_audiofile_}")
volume=[x[0] for x in re.findall(r'histogram_([0-9.]+)\s*db:\s+([0-9.]+)',os.popen(f'ffmpeg -i {_audiofile_} -af volumedetect -vn -f null - 2>&1').read(),flags=re.I|re.M) if float(x[1])<1000][-1]
volume=max(float(re.sub(r'.*?max_volume:\s+-([0-9.]+)\s+dB.*$',r'\1',os.popen(f'ffmpeg -i {_audiofile_} -af volumedetect -vn -f null - 2>&1').read(),flags=re.DOTALL|re.I)),float(volume))
if volume!=0.0:
 exec(f'ffmpeg -i {_audiofile_} -af volume=+{volume}dB -y inter.mp3')
 exec(f'ffmpeg -i {sys.argv[1]} -i inter.mp3 -map 0:v -map 1:a -c copy -y inter.mp4')
 exec(f'mv inter.mp4 {_singleoutputfile_};rm inter.mp* {_audiofile_}')
else:
 print(f'volume found zero not proceeding')
 sys.exit(-1)
if _cutpointl_:
 for count,x in enumerate(_cutpointl_):
  exec(f'ffmpeg'+(f' -ss {libcm.getsecond(x[0],True)}' if float(x[0])!=0.0 else '')+(f' -to {libcm.getsecond(x[1],True)}' if x[1]!='$' else '')+f' -i {_singleoutputfile_} -c copy -y '+re.sub(r'^(.*)[.](.*)$',r'\1'+f'_{count}.'+r'\2',_singleoutputfile_))

print(f'*********command executed**********\n{_prints_}\n{volume=}\n{_audiofile_=}\n**********')
