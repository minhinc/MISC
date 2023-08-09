def getcoord(*,begintime,attribtuple):
 file=open('t2.txt','w')
 attribtuple=(attribtuple,) if not type(attribtuple)==tuple and not type(attribtuple)==list else attribtuple
 precision=0.1
 lastkey=None
 duration=max(x['duration'] for x in attribtuple)
 for i in range(int(duration/precision)):
  for j in attribtuple:
   file.write(f"\n{round(begintime+i*precision,5)} {j['id']} {j['key'][0]}") if lastkey!=j['key'][0] else None
   lastkey=j['key'][0]
   if 'angle' in j:
    file.write(f"\n{round(begintime+i*precision,5)} {j['id']} {list(((j['angle']*precision)/j['duration'],*j['key'][1]))}")
   else:
    file.write(f"\n{round(begintime+i*precision,5)} {j['id']} {[(j['key'][2][count]-j['key'][1][count])/(j['duration']/precision) for count in range(3)]}")

#getcoord(begintime=1691413759.059825,attribtuple=({'id':14,'duration':10,'angle':360,'key':['G',(0,1,0)]},{'id':15,'duration':20,'angle':360,'key':['g',(0,1,0)]},{'id':16,'duration':30,'angle':360,'key':['g',(0,1,0)]},{'id':17,'duration':10,'key':['g',(10,1,8),(1,3,0)]}))
#getcoord(begintime=1691506432.835419,attribtuple=({'id':15,'duration':24,'angle':360,'key':['g',(0,1,0)]},{'id':17,'duration':30*4,'angle':360,'key':['g',(0,1,0)]},{'id':14,'duration':26*4,'angle':360,'key':['G',(0,1,0)]},{'id':14,'duration':20,'key':['g',(1,1,1),(6,6,6)]}))
getcoord(begintime=1691506453.7188904,attribtuple=({'id':15,'duration':24,'angle':360,'key':['g',(0,1,0)]},{'id':17,'duration':30*4,'angle':360,'key':['g',(0,1,0)]},{'id':14,'duration':26*4,'angle':360,'key':['G',(0,1,0)]}))
