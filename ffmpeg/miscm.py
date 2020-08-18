import re
class miscc:
 '''##misc##'''
 def __init__(self,libip):
  self.libi=libip

 def scenetransition(self,args_p,filter_p,beginstring_p,returnstring_p,count_p):
  '''<index[50]>'''
  self.libi.ffmpeg('ffmpeg -i input.mp4 -filter_complex "'+filter_p)
  print([(self.libi.getsecond(x[1]),'img0'+str(x[0]+1)+'.png') for x in enumerate(re.findall('pts_time:([\d.]+)',open('time.txt').read()))])
  return (beginstring_p,returnstring_p,count_p)
