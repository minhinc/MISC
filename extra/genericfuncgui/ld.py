import sys
def ld_fixed(source,target,discost=(1,1,1)):
 LDM=[[0]*(len(target)+1) for x in range(len(source)+1)]
 for i in range(1,len(source)+1):
  LDM[i][0]=LDM[i-1][0]+discost[0]
 for i in range(1,len(target)+1):
  LDM[0][i]=LDM[0][i-1]+discost[1]
 for col in range(1,len(target)+1):
  for row in range(1,len(source)+1):
   LDM[row][col]=min(LDM[row-1][col]+discost[0],
                     LDM[row][col-1]+discost[1],
                     LDM[row-1][col-1]+(discost[2] if not source[row-1]==target[col-1] else 0))

 for i in range(len(source)+1):
  print(LDM[i])
 return LDM[len(source)][len(target)]

def ld_character(source,target,**kwarg):
 costmap=dict()
 for i in range(ord('a'),ord('z')+1):
  costmap[chr(i)]=costmap[chr(i).upper()]=(1,1,1)
 costmap.update(kwarg)
 print(f'{costmap=}')
 LDM=[[0]*(len(target)+1) for x in range(len(source)+1)]
 for i in range(1,len(source)+1):
  LDM[i][0]=LDM[i-1][0]+costmap[source[i-1]][0]
 for i in range(1,len(target)+1):
  LDM[0][i]=LDM[0][i-1]+costmap[target[i-1]][1]
 for col in range(1,len(target)+1):
  for row in range(1,len(source)+1):
   LDM[row][col]=min(LDM[row-1][col]+costmap[source[row-1]][0],
                     LDM[row][col-1]+costmap[target[col-1]][1],
                     LDM[row-1][col-1]+(min(costmap[source[row-1]][0],costmap[target[col-1]][1]) if not source[row-1]==target[col-1] else 0))

 for i in range(len(source)+1):
  print(LDM[i])
 return LDM[len(source)][len(target)]

#print(ld_fixed(sys.argv[1],sys.argv[2]))
#print(ld_character('TAL','AL',a=(2,2,1)))
