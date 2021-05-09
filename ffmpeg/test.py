import datetime
import random
import re
from gifm import gifc;from utilm import utilc;from libm import libc
g=gifc();u=utilc();l=libc()
uploaddata={ \
"file":"", \
"title":"Magnify Desktop Linux", \
"description":"How to magnify or zoom desktop in certain area. Maginfication happens when mouse rolls", \
"keywords":"linux mint,linux,magnify desktop,zoom desktop,magnify desktop mouse roller,zoom desktop mouse roller", \
"privacyStatus":"private", \
"category":"28", \
"jsonfile":"client_secrets_techawal.json" \
}
uploaddata['file']=re.sub(r'\s+','_',re.sub(r'[.]mp4','{0:%Y-%m-%d}'.format(datetime.datetime.now())+'.mp4',uploaddata['title']+'.mp4',re.I))
duration=float(l.exiftool('input.mp4','Duration'))

def video(endmargin=10):
 endscaledvideo=u.cropscalepad(begintime=duration-endmargin,dimension='0.6,0.6',duration=endmargin)
 g.overlay(endscaledvideo,begintime=duration-endmargin)
 presentationimg=u.text2image(r'ThankYou::w:shade6\n::::40\nvisit:0.2:\nwww.minhinc.com:0.7:gi',margin=20,backcolor=(0,0,0,28))
 g.overlay(presentationimg,begintime=duration-endmargin,position=l.filter['overlay']['up'],duration=endmargin)
# g.overlay(u.cropscalepad('input.mp4','crop','0.7,1.0','iw*0.3,0','0,0',20,20,'0xffff00ff'),begintime=20)

def image():
# subscribegif=u.image2gif('new.gif','blend','fadein',duration=endmargin)
# for i in ['(W-w)/2,0','(W-w)/2,(H-h)','0,(H-h)/2','(W-w),(H-h)/2']:
#  g.overlay(subscribegif,begintime=duration-endmargin,position=i)
 g.overlay(u.image2gif(u.addalpha(u.cropscalepad('mousezoom.mp4',dimension='0.4,0.4',padcolor=None),196),'blend','fadein'),position='W-w,H-h',begintime=72)
 g.overlay(u.image2gif(u.addalpha(u.cropscalepad('mouseunzoom.mp4',dimension='0.4,0.4',padcolor=None),196),'blend','fadein'),position='W-w,H-h',begintime=107)

def test():
 pass

def text():
 global g,u,l,uploaddata,duration
 g.overlay(('videologo.png'),position='W-w,h',begintime=2.0,duration=duration-2.0)
 g.overlay(u.omnitext(re.sub(r'\s+',r'\\n',uploaddata['title']),size=0.8,duration=6),begintime=5.0)
 g.overlay(('cork.mp3',3.0),begintime=5.0+1.0)
 time=[]
 if duration>=600:
  time=range(120,int(duration),120)
 elif duration>=180:
  time=[duration/2]
 if len(time):
  dialogtextimg=u.text2image(uploaddata['title'],backcolor=(0,0,0,20),size=0.4)
  dialogtextleftgif=u.image2gif(dialogtextimg,'overlay','left',duration=6)
  dialogtextrightgif=u.image2gif(dialogtextimg,'blend','right',duration=6)
 for count,i in enumerate(time):
  g.overlay([dialogtextleftgif,dialogtextrightgif][random.randrange(0,max(len(list(time)),2))%2],begintime=i,position='(W-w)-(W*0.1),(H-h)-(H*0.1)')

video(6)
image()
text()
test()
g.stroke(uploaddata['file'])
#input("Video Created, press any key to continue")
#u.screenshot(imagename=uploaddata['file'],begintime='00:02:45',outimagename='screenshot.png')
#g.push2socialmedia('youtube',uploaddata)
