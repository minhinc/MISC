import sys;sys.path.append('/home/minhinc/tmp')
import re,os
if len(sys.argv)==1:
 print(f'usage - python3 ffmpeg_screenshot <videoname> [><referencetime] [<timestamp><timestamp>...]')
 print(f'python3 ffmepg_screenshot.py abc.mp4')
 print(f'python3 ffmpeg_screenshot.py abc.mp4 00:10:00.1 200.2')
 print(f'python3 ffmpeg_screenshot.py abc.mp4 ><00:01:00')
 sys.exit(-1)
from MISC.ffmpeg.utilm import utilc
u=utilc()
os.system('rm '+u.libi.adddestdir(r'screenshot*.png'))
for i in (range(20) if len(sys.argv)==2 or (len(sys.argv)==3 and re.search(r'^><',sys.argv[2])) else sys.argv[2:]):
 i=i*4+float(u.libi.getsecond(re.sub(r'^><','',sys.argv[2]))) if len(sys.argv)==3 and re.search(r'^><',sys.argv[2]) else i
 u.screenshot(sys.argv[1],i if len(sys.argv)==2 or (len(sys.argv)==3 and re.search(r'^><',sys.argv[2])) else i)
print(rf'************************\n***** {u.libi.adddestdir("screenshot*.png")=} *****\n**************************')
