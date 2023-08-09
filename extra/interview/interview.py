import re,sys
def usage():
 print(f'{"Usage":-^40}')
 print(f'python3 fgl.py <featurelist> <classlist>')
 print(f'python3 fgl.py \'domain=["machine learning","algorithms"] text="what is bayes theorem?"\' \'experience=1 lanugage=[python,c]\'')
 print(f'python3 fgl.py \'domain="machine learning" and algorithms" text="what is bayes theorm?"\' \'experience=1 lanugage=python and c\'')
 print(f'{"":-^40}')
data=[]
def getdatafield(line):
# print(f'TEST getdatafield {line=}')
# return dict([(x[0], (x[1],) if not re.search(r'^[\["\']',x[1]) else (re.sub(r'^["\'](.*)["\']$',r'\1',x[1]),) if re.search(r'^["\']',x[1]) else [str(x) for x in range(*[int(y) if not count else int(y)+1 for count,y in enumerate(re.findall(r'\d+',x[1]))])] if re.search(r'^\[\d+-\d+\]$',x[1]) else [re.sub(r'^[\["\']*(.*?)[\]"\']*$',r'\1',y) for y in re.split(',',x[1])]) for x in re.findall(r'(\w+)=((?:\[.*?\]|["\'].*?["\'])|\S+)',line)])
# return dict([(x[0].lower(), (x[1].lower(),) if not re.search(r'^[\["\']',x[1]) else (re.sub(r'^["\'](.*)["\']$',r'\1',x[1]).lower(),) if re.search(r'^["\']',x[1]) else [str(x) for x in range(*[int(y) if not count else int(y)+1 for count,y in enumerate(re.findall(r'\d+',x[1]))])] if re.search(r'^\[\d+-\d+\]$',x[1]) else [re.sub(r'^[\["\']*(.*?)[\]"\']*$',r'\1',y).lower() for y in re.split(',',x[1])]) for x in re.findall(r'(\w+)=((?:\[.*?\]|["\'].*?["\'])|\S+)',line)])
# return dict([(x[0],(re.sub(r'^["\'](.*?)["\']$',r'\1',x[1]).lower(),) if re.search(r'^["\'](((?!").)|\\")*["\']$',x[1]) else [str(x) for x in range(*[int(y) if not count else int(y)+1 for count,y in enumerate(re.findall(r'\d+',x[1]))])] if re.search(r'^\d+-\d+$',x[1]) else [re.sub(r'^["\']*(.*?)["\']*$',r'\1',y).lower() for y in re.split(',',x[1])])  for x in re.findall(r'(\w+)=\s*(.*?)\s*(?=\w+=|$)',line)])
 return dict([(x[0],(re.sub(r'^["\'](.*?)["\']$',r'\1',x[1]).lower(),) if re.search(r'^["\'](((?!["\']).)|\\["\'])*["\']$',x[1]) else [str(x) for x in range(*[int(y) if not count else int(y)+1 for count,y in enumerate(re.findall(r'\d+',x[1]))])] if re.search(r'^\d+-\d+$',x[1]) else [re.sub(r'^["\']*(.*?)["\']*$',r'\1',y).lower() for y in re.split(',',x[1])])  for x in re.findall(r'(\w+)=\s*(.*?)\s*(?=\w+=|$)',line)])

def getlen(llist,out=None):
# print(f'TEST getlen {out=}')
 count_m=0
 for i in llist:
  count=1
  for x in [x for x in i if x not in (out if out else dict())]:
   count*=len(i[x])
  count_m+=count
# print(f'<> getlen {llist=} {count_m=}')
 return count_m

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
   print(f'<=>readdata {filename=} {datadefault=}')
  elif not re.search(r'^\s*(#|$)',i):
   i=getdatafield(i)
   for x in [x for x in i if x not in datadefault or [y for y in i[x] if len(datadefault[x])>1 and not y in datadefault[x]]]:
    tmp='Error'
    print(f'---> {i} - {filename} - {x} linenumber={count+1}')
   data.append(dict(datadefault,**i))
def getp(*,in2,out):
 outdata=[]
 for x in data:
  for y in out:
   if not len([z for z in out[y] if z in x[y]])==len(out[y]):
    break
  else:
   outdata.append(x)
# print(f'<=> getp {outdata=} {in2=} {out=}')
 if not outdata:
  return 0
 count_m=0
 for x in outdata:
  for y in in2:
#   print(f'TEST getp coexistance {x=} {y=} {in2=} {out=}')
   if not len([z for z in in2[y] if z in x[y]])==len(in2[y]):
    break
  else:
   count_m+=1
 prob=getlen(outdata,out)/getlen(data)
 count_m=(count_m/getlen(outdata,out))*prob
 for y in in2:
  for z in in2[y]:
   prob*=len([x for x in outdata if z in x[y]])/getlen(outdata,out)
# print(f'<=>getp count_m < prob {count_m=} {prob=} {in2=} {out=}') if count_m<prob else 0
 return max(count_m,prob)

def get(*,in2,out):
 probn=getp(in2=in2,out=out)
 probd=0
 for x in set(y for x in data for y in x[list(out.keys())[0]]):
  probd+=getp(in2=in2,out=dict(out,**{list(out.keys())[0]:(x,)}))
# print(f'get {in2=} {out=} {probn=} {probd=}')
 return probn/probd if probd else 0

if len(sys.argv)<=1:
 usage()
 sys.exit(-1)
readdata('fgc.txt')
if tmp:
 sys.exit(-1)
print(f'{tmp=} {datadefault=}\n{data=}')
questionprob=[]
for i in set(y for i in data for y in i['text']):
 questionprob.append((i,get(in2=dict(getdatafield(sys.argv[1]),text=(i,)),out=getdatafield(sys.argv[2]))))
[print(x[0],x[1]) for count,x in enumerate(sorted(questionprob,key=lambda m:m[1],reverse=True)) if count<(len(sys.argv)>3 and int(sys.argv[3]) or len(questionprob))]
