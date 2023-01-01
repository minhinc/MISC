import os,re,sys
if len(sys.argv)<=1:
 print(f'{"------usage------":^30}')
 print(f'python3 spellcheck <word>|<filename> ["<line1,line2>"]')
 print(f'python3 spellcheck a.txt')
 print(f'python3 spellcheck a.txt "20,30"')
 print(f'python3 spellcheck donkey')
 sys.exit(-1)
wordlist=[];checklinelist=[];result=dict()
line1=line2=None
with open(r'/usr/share/dict/british-english') as file:
 wordlist=[x.rstrip().lower() for x in file]
if os.path.exists(sys.argv[1]):
 line1,line2=(1,len(open(sys.argv[1]).readlines())) if not len(sys.argv)==3 else [int(x) for x in re.split(',',sys.argv[2])]
 with open(sys.argv[1]) as file:
  checklinelist=[tuple([re.sub(r'^\W*(.*?)\W*$',r'\1',i) for i in re.split(r'[\s\W]+',x.rstrip()) if i and not re.search(r'^[\W\d]+$',i)]) for count,x in enumerate(file) if (count+1)>=line1 and (count+1)<=line2]
else:
 checklinelist=[(sys.argv[1],)]
for count,i in enumerate(checklinelist):
 for countj,j in enumerate(i):
  if j.lower() not in wordlist:
   if j in result:
    result[j].append((count+1,countj+1))
   else:
    result[j]=[(count+1,countj+1)]
for x in result.keys():
 print(f'{x:<20}{result[x]}')
