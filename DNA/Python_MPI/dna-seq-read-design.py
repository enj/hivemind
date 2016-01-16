from collections import OrderedDict
PL='ILLUMINA'
dessep=','

design=OrderedDict()
for line in open('des.csv','r'):
    line=line.strip().split(dessep)
    rg=r'"@RG\tID:"+line[0]+"."+line[1]+":\tSM:"+line[0]+"\tPL:"+PL'
    design[line[1],line[2]]=[line[3],line[4]]

newdes=OrderedDict()

for i in list(set([i[0] for i in design.keys()])):
    newdes[i]={}

for i in  design.keys():
    newdes[i[0]]=["PROC2/"+i[0]+"/"+i[0],{}]

for i in  design.keys():
    rg='"'+'@RG\tID:'+i[0]+'.'+i[1]+'\tSM:'+i[0]+'\tPL:ILLUMINA'+'"'
    newdes[i[0]][1][i[1]]=[design[i][0],design[i][1],rg]
