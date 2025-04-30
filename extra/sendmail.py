import os,sys,re
import builtins
import json
sys.path.append(os.path.expanduser('~')+r'/tmp')
from MISC.extra.config import _configi as print
from MISC.extra.config import _helpi,_registryi,_configi,_jsoni
from MISC.utillib.emailclient import _brevoemailclienti,_gmailemailclienti
from MISC.utillib.webdownload.webdownload import _webdownloadi
helpstr=_helpi.hash2str({'--sendmail':{'-collectivesend(b)':'Send everyone in one mail(False)','-id(l)':'list of email ids or txt file name','-subject':'subject of the mail','-message':'email message text file'},'--webmail':{'-pagecount(n)':'Search pages count(1)','-searchtext':'Text to search','-searchengine(l)':'engines name,i.e.Google Naukri Linkedin(google)'}})
if len(sys.argv)<=1:
 print(f'{helpstr}')
 sys.exit(-1)

def makecall(listnames_):
 return('''\
class texec:
 for i in '''+listnames_+''':
  callablename=re.sub('^-+(.*?)(?:\(\S+\))?$',r'\\1',i[0])
  print(f'>< {callablename=}')
  if hasattr(self,callablename):
   exec(f'{callablename}=self.{callablename}=i[1]') if not hasattr(eval('self.'+callablename),'__call__') else exec(f'{callablename}=self.{callablename}(i[1])') if not (type(eval('self.'+callablename))==type or issubclass(type(eval('self.'+callablename)),type)) else exec(f'{callablename}=(_registryi.register(callablename) or _registryi.register(eval("self.__class__."+callablename+"()")))(self,i[1])')
  elif (lambda callablename=callablename: [x for x in globals() if re.search(r'_'+callablename+'c?$',x)])():
   callableclassname=f'_{callablename}'+("" if (lambda callablename=callablename: [x for x in globals() if re.search(r"_"+callablename+"$",x)])() else "c")
   exec(f'{callablename}=(_registryi.register(callableclassname) or _registryi.register(eval(callableclassname+"()")))(self,i[1])')''')

class _searchengine:
 def google(self,text_):
  print(f'>< {text_=}')
  return [[x[1],x[0],_webdownloadi.getemail(_webdownloadi.getdata(url_=x[1],mode='-dump'))] for x in re.findall(r'url\?q=(https:.*?)\&.*?<span.*?>(.*?)<\/span>',_webdownloadi.getdata(url_=_webdownloadi.googlelink(text_),mode='-source'),flags=re.I|re.DOTALL)]
 
 def linkedin(self,text_):
  print(f'>< {text_=}')

 def naukri(self,text_):
  print(f'>< {text_=}')

 def __call__(self,parenti_,optionl_):
  print(f'>< {eval("self.google(parenti_.searchtext)")=} {parenti_=} {parenti_.__dict__=} {optionl_=}')
  return '\n'.join([eval('self.'+x.lower()+'(parenti_.searchtext)',{'self':self,'parenti_':parenti_}) for x in re.split(r'\s+',optionl_)])
#  return '\n'.join([x for x in re.split(r'\s+',optionl_)])

class _webmail:
 def __init__(self,*arg,**kwarg):
  super().__init__(*arg,**kwarg)
  self.pagecount=1
  self.searchtext=''


 def __call__(self,parenti_,optionl_):
  print(f'{parenti_=} {optionl_=}')
  optionl_=_helpi.sortlist(optionl_,_helpi.str2hash(helpstr)['--webmail'])
  print(f'<=> {optionl_=}')
  exec(makecall('optionl_'),dict(globals(),**locals()),locals())
  return locals()['texec'].searchengine

class _sendmail:
 clientl=[_gmailemailclienti,_brevoemailclienti]

 def __init__(self,*args,**kwargs):
  self.collectivesend=False
  self.subject=''

 def id(self,file_):
  if type(file_)==str and not re.search(r'@',file_):
   return [x for x in re.split(r'\s+',open(file_).read()) if not re.search(r'^s*$',x)]
  else:
   return file_ if _configi.type(file_)=='sequence' else re.split(r'\s+',file_)

 def message(self,file_):
  print(f'>< {file_=}')
  if not re.search(r'\s+',file_) and os.path.isfile(file_):
   if self.subject=='':
    self.subject=_jsoni.loads(open(file_).read())['subject']
#    self.message='\n'.join(_jsoni.loads(open(file_).read())['message'])
    self.message=_jsoni.loads(open(file_).read())['message']
    print(f'------------- {self.message=}')
    return open(file_).read()
   else:
    self.message=open(file_).read()
  else:
   self.message=file_

 def subject(self,subjects_):
  self.subject=subjects_

 def __call__(self,parenti_,optionl_):
  print(f'>< {optionl_=}')
  count=0
  optionl_=_helpi.sortlist(optionl_, _helpi.removetype(_helpi.str2hash(helpstr)['--sendmail']))
  print(f'<=> {optionl_=}')
  exec(makecall('optionl_'),dict(globals(),**locals()),locals())
  print(f'>< {locals()["texec"].__dict__=}')
  while count<len(_sendmail.clientl):
   try:
    _sendmail.clientl[count].sendmail(tol_=locals()['texec'].id,htmlmessage_=self.message,subject_=self.subject)
   except Exception as e:
    print(f'<=> Caught exception {e=} on email client class {_sendmail.clientl[count].__class__=}')
    locals()['texec'].id=locals()['texec'].id[_sendmail.clientl[count].sentcount:]
    count+=1
   else:
    print(f'<=> Successfully Sent Messages')
    break
  else:
   print(f'<=> All {len(_sendmail.clientl)} clients done, exiting...')
  return 'CHECK'

class _main:
 def __call__(self,*arg,**kwarg):
  print('-----')
  print(makecall('''_helpi.cmd2list(os.popen('python3 /home/pi/tmp/sendmail/sendmail.py').read(),sys.argv[1:])'''))
  print('------')
  exec(makecall('''_helpi.cmd2list(os.popen('python3 /home/pi/tmp/sendmail/sendmail.py').read(),sys.argv[1:])'''),dict(globals(),**locals()),locals())
  print(f'<=> {dir(locals()["texec"])=}')
  print(locals()['texec'].webmail)
_main()(sys.argv[1:])
