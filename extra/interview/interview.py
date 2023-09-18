import re,sys
import math
def usage():
 print(f'{"Usage":-^40}')
 print(f'python3 fgl.py <featurelist> <classlist>')
 print(f'python3 fgl.py \'domain=["machine learning","algorithms"] text="what is bayes theorem?"\' \'experience=1 lanugage=[python,c]\'')
 print(f'python3 fgl.py \'domain="machine learning" and algorithms" text="what is bayes theorm?"\' \'experience=1 lanugage=python and c\'')
 print(f'{"":-^40}')
data=[]
'''
def getdatafield(line):
# print(f'TEST getdatafield {line=}')
# return dict([(x[0],(re.sub(r'^["\'](.*?)["\']$',r'\1',x[1]).lower(),) if re.search(r'^["\'](((?!["\']).)|\\["\'])*["\']$',x[1]) else [str(x) for x in range(*[int(y) if not count else int(y)+1 for count,y in enumerate(re.findall(r'\d+',x[1]))])] if re.search(r'^\d+-\d+$',x[1]) else [re.sub(r'^["\']*(.*?)["\']*$',r'\1',y).lower() for y in re.split(',',x[1])])  for x in re.findall(r'(\w+)=\s*(.*?)\s*(?=\w+=|$)',line)])
# return dict([(x[0],(re.sub(r'^["\'](.*?)(?<!\\)["\']$',r'\1',x[1]).lower(),) if re.search(r'(^["\']((?!["\']).)*["\']$|^["\'].*\\["\'].*["\']$)',x[1]) else [str(x) for x in range(*[int(y) if not count else int(y)+1 for count,y in enumerate(re.findall(r'\d+',x[1]))])] if re.search(r'^\d+-\d+$',x[1]) else [re.sub(r'^["\']*(.*?)["\']*$',r'\1',y).lower() for y in re.split(',',x[1])])  for x in re.findall(r'(\w+)=\s*(.*?)\s*(?=\w+=|$)',line)])
 return dict([(x[0], [str(x) for x in range(*[int(y) if not count else int(y)+1 for count,y in enumerate(re.findall(r'\d+',x[1]))])] if re.search(r'^\d+-\d+$',x[1]) else [re.sub(r'^["\']*(.*?)["\']*$',r'\1',y).lower() for y in re.split(',',x[1])] if re.search(r'^.*(?<!\\),',x[1]) else re.sub(r'^["\'](.*)["\']$',r'\1',x[1])) for x in re.findall(r'(\w+)=\s*(.*?)\s*(?=\w+\s*(?<!\\)=|$)',line)])
'''

def getdatafield(i):
 tmp={}
 while not re.search(r'^\s*$',i):
  key,i=re.split('=',i,maxsplit=1)
#  print(f'TEST {(key,i)=}')
  if re.search(r'^\s*\d+\s*-\s*\d+',i):
   value,i=re.sub(r'(?P<id>\s*\d+\s*-\s*\d+).*',lambda m:m.group('id'),i),re.sub(r'^\s*\d+\s*-\s*\d+(?P<id>.*)',lambda m:m.group('id'),i)
   value=[str(x) for x in range(*[int(y) if not count else int(y)+1 for count,y in enumerate(re.findall(r'\d+',value))])]
#   print(f'TEST 1 {(value,i)=}')
  elif re.search(r'^\s*("((?!\\").)*?"|\'((?!\\\').)*?\'|\S+)\s*,',i):
   value,i=re.sub(r'^(.*?)(?:\w+\s*=.*|\s*$)',r'\1',i),re.sub(r'^.*?(\w+\s*=.*$|$)',r'\1',i)
#   print(f'TEST 2 {(value,i)=}')
   value= [re.sub(r'^["\'](.*?)["\']$',r'\1',re.sub(r'^\s*(.*?)\s*$',r'\1',y)).lower() for y in re.split(',',value)]
  else:
   value,i=re.sub(r'\s*(?P<id>"((?!\\").)*?"|\'((?!\\\').)*?\'|\S+)(?P<id2>.*)$',lambda m:m.group('id'),i),re.sub(r'\s*(?P<id>"((?!\\").)*?"|\'((?!\\\').)*?\'|\S+)(?P<id2>.*)$',lambda m:m.group('id2'),i)
#   print(f'TEST 3 {(value,i)=}')
   value= (re.sub(r'^["\'](.*?)["\']$',r'\1',re.sub(r'^\s*(.*?)\s*$',r'\1',value)).lower(),)
  tmp[re.sub(r'^\s*(.*?)\s*$',r'\1',key)]=value
 return tmp

def getlen(llist):
 '''llist list or tuple of dict'''
# print(f'TEST getlen {len(llist)=} {llist=}')
# print(f'<> getlen {len(llist)=} {llist=} {sum(math.prod(len(i[x]) for x in i) for i in llist)=}')
 return sum(math.prod(len(i[x]) for x in i) for i in llist)

datadefault={}
data=[]
tmp=None
def readdata(filename):
 global data,datadefault,tmp
 for count,i in enumerate(re.split('\n',open(filename).read())):
  if re.search(r'^\w+[.]txt$',i):
   readdata(i)
  elif re.search(r'^\s*#\s*default\s+',i):
   datadefault=dict(datadefault,**getdatafield(re.sub(r'^\s*#\s*default\s+(.*)$',r'\1',i)))
  elif not re.search(r'^\s*(#|$)',i):
   i=getdatafield(i)
   for x in [x for x in i if x not in datadefault or [y for y in i[x] if len(datadefault[x])>1 and not y in datadefault[x]]]:
    tmp='Error'
    print(f'---> {datadefault=} {i} - {filename} - {x} linenumber={count+1}')
   data.append(dict(datadefault,**i))

def getp(*,in2,out):
# outdata=[dict(x,**{y:list(set(x[y]) & set(out[y])) for y in out}) for x in data if len([y for y in out if len(set(out[y]) & set(x[y]))==len(out[y])])==len(out)]
 outdata=[dict(x,**{y:list(set(x[y]) & set(out[y])) for y in out}) for x in data if len([y for y in out if set(out[y]) & set(x[y])])==len(out)]
# print(f'<=> getp {outdata=}') if in2['text'][0]=='what is bayes theorem' else None
 outdata_len,data_len=getlen(outdata),getlen(data)
 count_m=getlen([dict(x,**{y:list(set(x[y]) & set(in2[y])) for y in in2}) for x in outdata if len([y for y in in2 if set(in2[y]) & set(x[y])])==len(in2)])
 count_s=[getlen([dict(x,**{y:list(set(in2[y]) & set(x[y]))}) for x in outdata if set(in2[y]) & set(x[y])]) for y in in2]
# print(f'<=>getp {in2=} {(outdata_len,data_len)=} {out=} {(count_m,count_s)=} {(count_m/data_len,(math.prod(count_s)/math.pow(outdata_len,len(in2)))*(outdata_len/data_len))}') if count_m or sum(count_s) else None
 return max((count_m/outdata_len)*(outdata_len/data_len),(math.prod(count_s)/math.pow(outdata_len,len(in2)))*(outdata_len/data_len))

def get(*,in2,out):
 probn=getp(in2=in2,out=out)
# probd=0
 probd=[]
# print(f'\nget Numera {in2=} {out=} {probn=} {probd=}')
 for x in set(y for x in data for y in x[list(out.keys())[0]]):
#  probd+=getp(in2=in2,out=dict(out,**{list(out.keys())[0]:(x,)}))
  probd.append(getp(in2=in2,out=dict(out,**{list(out.keys())[0]:(x,)})))
# print(f'get {in2=} {out=} {probn=} {probd=} {probn/sum(probd)=}\n') if sum(probd) else None
# return probn/probd if probd else 0
 return probn/sum(probd) if sum(probd) else 0

if __name__=='__main__':
 if len(sys.argv)<=1:
  usage()
  sys.exit(-1)
 readdata('fgc.txt')
 if tmp:
  sys.exit(-1)
# print(f'{tmp=}\n{datadefault=}\n{data=}\n{len(data)=}')
 questionprob=[]
 for count,i in enumerate(set(y for i in data for y in i['text'])):
  questionprob.append((i,get(in2=dict(getdatafield(sys.argv[1]),text=(i,)),out=getdatafield(sys.argv[2]))))
 print(f'\n\n\n')
 [print(x[0].capitalize(),x[1]) for count,x in enumerate(sorted(questionprob,key=lambda m:m[1],reverse=True)) if count<(len(sys.argv)>3 and int(sys.argv[3]) or len(questionprob))]
