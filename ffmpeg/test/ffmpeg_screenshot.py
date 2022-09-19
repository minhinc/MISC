import sys;sys.path.append('/home/minhinc/tmp')
import re,os
if len(sys.argv)==1:
 print(f'usage - python3 ffmpeg_screenshot <videoname> [><referencetime] [<timestamp><timestamp>...]')
 print(f'python3 ffmepg_screenshot.py abc.mp4')
 print(f'python3 ffmpeg_screenshot.py abc.mp4 00:02:00.1 200.2 00:08:00 00:10:00 ...')
 print(f'python3 ffmpeg_screenshot.py abc.mp4 ><00:01:00')
 print(f'python3 ffmpeg_screenshot.py abc.mp4 ><00:01:00 <>00:01:10 #-ss ><* -to <>* pushed in logdir/refsnapshot directory')
 print(f'python3 ffmpeg_screenshot.py silenceaudiostring marianatrench_recorded_audocity.mp3 syncimagename logdir/mariana_trench.mp4 20 22 marianatrench_recorded.mp4 58 62')
 sys.exit(-1)
from MISC.ffmpeg.utilm import utilc
u=utilc()
os.system('rm '+u.libi.adddestdir(r'screenshot*.png'))
if len(sys.argv)==4 and re.search(r'^><',sys.argv[2]) and re.search(r'^<>',sys.argv[3]):
 if not os.path.exists(u.libi.adddestdir('refsnapshot')):
  os.mkdir(u.libi.adddestdir('refsnapshot'))
 os.system('rm '+u.libi.adddestdir('refsnapshot')+r'/*')
 u.libi.system("ffmpeg -ss "+re.sub(r'^><(.*)',r'\1',sys.argv[2])+" -to "+str(re.sub(r'^<>(.*)',r'\1',sys.argv[3]))+" -i "+sys.argv[1]+' -y '+u.libi.adddestdir(r'refsnapshot')+r'/screenshot%03d.png')
 print(f"************ printed at ",u.libi.adddestdir('refsnapshot')+r'/screenshot%03d.png'," **********")
elif len(sys.argv)==10 and re.search(r'^silenceaudiostring',sys.argv[1],flags=re.I):
 print(u.silencenaudiolist(sys.argv[2],(sys.argv[3],(sys.argv[4],sys.argv[5],sys.argv[6]),(sys.argv[7],sys.argv[8],sys.argv[9]))))
else:
 for i in (range(20) if len(sys.argv)==2 or (len(sys.argv)==3 and re.search(r'^><',sys.argv[2])) else sys.argv[2:]):
  i=i*4+float(u.libi.getsecond(re.sub(r'^><','',sys.argv[2]))) if len(sys.argv)==3 and re.search(r'^><',sys.argv[2]) else i
  u.screenshot(sys.argv[1],i if len(sys.argv)==2 or (len(sys.argv)==3 and re.search(r'^><',sys.argv[2])) else i)
 print(rf'************************\n***** {u.libi.adddestdir("screenshot*.png")=} *****\n**************************')
