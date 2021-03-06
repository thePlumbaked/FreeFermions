#!/usr/bin/env python
# coding: utf-8

# In[2]:


# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 15:25:02 2020

@author: cinzi
"""

import sys
import numpy as np
from z3 import *
import itertools
set_param(proof=True)
ctx = Context()
s = Solver(ctx=ctx)
c = [Int('c%s' % (i), ctx=ctx) for i in range(36)]

#c[0]= 1 S, c[1 ]= 1 T1, c[2 ]= 1 T2, c[3 ]= 1 T3, c[4 ]= 1 b1, c[5 ]= 1 b2, c[6 ]= 1 b3, c[7 ]= 1 z1
#           c[8 ]= S T1, c[9 ]= S T2, c[10]= S T3, c[11]= S b1, c[12]= S b2, c[13]= S b3, c[14]= S z1
#                        c[15]=T1 T2, c[16]=T1 T3, c[17]=T1 b1, c[18]=T1 b2, c[19]=T1 b3, c[20]=T1 z1
#                                     c[21]=T2 T3, c[22]=T2 b1, c[23]=T2 b2, c[24]=T2 b3, c[25]=T2 z1
#                                                  c[26]=T3 b1, c[27]=T3 b2, c[28]=T3 b3, c[29]=T3 z1
#                                                               c[30]=b1 b2, c[31]=b1 b3, c[32]=b1 z1 
#                                                                            c[33]=b2 b3, c[34]=b2 z1
#                                                                                         c[35]=b3 z1

#s = Solver() # create a solver s
# add the clauses
for item in c:
    s.add(Or([item == 0, item == 1]))
    
#9 arbitrary phases: not in any projection equations
s.add(And(c[0]==1,c[4]==1,c[5]==1,c[6]==1,c[7]==1,c[11]==1,c[12]==1,c[13]==1,c[14]==1))

#Tachyon free conditions
#T3{R}
T3cond1=c[10]+(1+c[3]+c[16]+c[21]+c[26]+c[27]+c[28])%2+c[16]+c[21]+c[29]!=1
T3cond2=c[10]+(1+c[3]+c[16]+c[21]+c[26]+c[27]+c[28])%2+c[16]+c[21]+c[29]!=0
T3cond3=Not(And(c[10]+(1+c[3]+c[16]+c[21]+c[26]+c[27]+c[28])%2+c[16]+c[21]+c[29]==2,c[10]+c[29]==2))

#T2{R}
T2cond1=c[9]+(1+c[2]+c[15]+c[21]+c[22]+c[23]+c[24])%2+c[15]+c[21]+c[25]!=1
T2cond2=c[9]+(1+c[2]+c[15]+c[21]+c[22]+c[23]+c[24])%2+c[15]+c[21]+c[25]!=0
T2cond3=Not(And(c[9]+(1+c[2]+c[15]+c[21]+c[22]+c[23]+c[24])%2+c[15]+c[21]+c[25]==2,c[9]+c[25]==2))

#T1{R}
T1cond1=c[8]+(1+c[1]+c[15]+c[16]+c[17]+c[18]+c[19])%2+c[15]+c[16]+c[20]!=1
T1cond2=c[8]+(1+c[1]+c[15]+c[16]+c[17]+c[18]+c[19])%2+c[15]+c[16]+c[20]!=0
T1cond3=Not(And(c[8]+(1+c[1]+c[15]+c[16]+c[17]+c[18]+c[19])%2+c[15]+c[16]+c[20]==2,c[8]+c[20]==2))

s.add(And(T1cond1,T1cond2,T1cond3,T2cond1,T2cond2,T2cond3,T3cond1,T3cond2,T3cond3))

z2tach=(c[30]+c[31]+c[32])%2+(c[30]+c[33]+c[34])%2+(c[31]+c[33]+c[35])%2+(c[32]+c[34]+c[35])%2 +       (c[1]+c[17]+c[18]+c[19]+c[20])%2+(c[2]+c[22]+c[23]+c[24]+c[25])%2!=0

z2T1=(1+c[30]+c[31]+c[32]+c[17])%2+(c[2]+c[22]+c[23]+c[24]+c[25]+c[15])%2+     (c[3]+c[26]+c[27]+c[28]+c[29]+c[16])%2+(c[32]+c[34]+c[35]+c[20])%2!=0

z2T2=(1+c[30]+c[33]+c[35]+c[28])%2+(c[1]+c[17]+c[18]+c[19]+c[20]+c[16])%2+     (c[3]+c[26]+c[27]+c[28]+c[29]+c[21])%2+(c[32]+c[34]+c[35]+c[25])%2!=0

z2T3=(1+c[31]+c[33]+c[35]+c[28])%2+(c[1]+c[17]+c[18]+c[19]+c[20]+c[15])%2+     (c[2]+c[22]+c[23]+c[24]+c[25]+c[21])%2+(c[32]+c[34]+c[35]+c[29])%2!=0

s.add(And(z2tach,z2T1,z2T2,z2T3))     
     
z1tach=c[20]+c[25]+c[29]+c[32]+c[34]+c[35]!=0

z1T1tach=(1+c[32]+c[17])%2+(c[25]+c[15])%2+(c[29]+c[16])%2+(c[1]+c[17]+c[18]+c[19]+c[20]+c[32]+c[34]+c[35])%2!=0

z1T2tach=(1+c[34]+c[23])%2+(c[20]+c[15])%2+(c[29]+c[21])%2+(c[2]+c[22]+c[23]+c[24]+c[25]+c[32]+c[34]+c[35])%2!=0

z1T3tach=(1+c[35]+c[28])%2+(c[20]+c[16])%2+(c[25]+c[21])%2+(c[3]+c[26]+c[27]+c[28]+c[29]+c[32]+c[34]+c[35])%2!=0

s.add(And(z1tach,z1T1tach,z1T2tach,z1T3tach))

#Condition on having a 16/16bar
#BF1=b1+pT2+qT3
BF1Proj=[(c[17]+p*c[15]+q*c[16])%2+(c[32]+p*c[25]+q*c[29])%2+(c[30]+c[31]+c[32]+p*(c[2]+c[22]+c[23]+c[24]+c[25])+          q*(c[3]+c[26]+c[27]+c[28]+c[29]))%2 for p in range(0,2) for q in range(0,2)]

BF1ProjBools=[x==3 for x in BF1Proj]
s.add(Sum([If(BF1ProjBools[i],1,0) for i in range(len(BF1ProjBools))]) >= 1)


# conditions on projection of twisted bosons: vectorials
#V6= T1+T2
V6cond1=Not(And((c[20]+c[25])%2+(c[16]+c[21])%2+(c[1]+c[2]+c[17]+c[22]+c[18]+c[23]+c[19]+c[24]+c[20]+c[25])%2+        +(1+c[8]+c[9])%2==1,(1+c[8]+c[9])%2==0))
V6cond2=Not(And((c[20]+c[25])%2+(c[16]+c[21])%2+(c[1]+c[2]+c[17]+c[22]+c[18]+c[23]+c[19]+c[24]+c[20]+c[25])%2+        +(1+c[8]+c[9])%2!=2,(1+c[8]+c[9])%2+(c[20]+c[25])%2==2))
V6cond3=Not(And((c[20]+c[25])%2+(c[16]+c[21])%2+(c[1]+c[2]+c[17]+c[22]+c[18]+c[23]+c[19]+c[24]+c[20]+c[25])%2+        +(1+c[8]+c[9])%2!=2,(1+c[8]+c[9])%2+(c[1]+c[2]+c[17]+c[22]+c[18]+c[23]+c[19]+c[24]+c[20]+c[25])%2==2))

#V5= T1+T3
V5cond1=Not(And((c[20]+c[29])%2+(c[15]+c[21])%2+(c[1]+c[3]+c[17]+c[26]+c[18]+c[27]+c[19]+c[28]+c[20]+c[29])%2+        +(1+c[8]+c[10])%2==1, (1+c[8]+c[10])%2==0))
V5cond2=Not(And((c[20]+c[29])%2+(c[15]+c[21])%2+(c[1]+c[3]+c[17]+c[26]+c[18]+c[27]+c[19]+c[28]+c[20]+c[29])%2+        +(1+c[8]+c[10])%2!=2, (1+c[8]+c[10])%2+(c[20]+c[29])%2==2))
V5cond3=Not(And((c[20]+c[29])%2+(c[15]+c[21])%2+(c[1]+c[3]+c[17]+c[26]+c[18]+c[27]+c[19]+c[28]+c[20]+c[29])%2+        +(1+c[8]+c[10])%2!=2, (1+c[8]+c[10])%2+(c[1]+c[3]+c[17]+c[26]+c[18]+c[27]+c[19]+c[28]+c[20]+c[29])%2==2))

#V4= T2+T3
V4cond1=Not(And((c[25]+c[29])%2+(c[15]+c[16])%2+(c[2]+c[3]+c[22]+c[26]+c[23]+c[27]+c[24]+c[28]+c[25]+c[29])%2        +(1+c[9]+c[10])%2==1,(1+c[9]+c[10])%2==0))
V4cond2=Not(And((c[25]+c[29])%2+(c[15]+c[16])%2+(c[2]+c[3]+c[22]+c[26]+c[23]+c[27]+c[24]+c[28]+c[25]+c[29])%2+        +(1+c[9]+c[10])%2==2, (1+c[9]+c[10])%2+(c[25]+c[29])%2==2))
V4cond3=Not(And((c[25]+c[29])%2+(c[15]+c[16])%2+(c[2]+c[3]+c[22]+c[26]+c[23]+c[27]+c[24]+c[28]+c[25]+c[29])%2+        +(1+c[9]+c[10])%2==2, (1+c[9]+c[10])%2+(c[2]+c[3]+c[22]+c[26]+c[23]+c[27]+c[24]+c[28]+c[25]+c[29])%2==2))
    
s.add(And(V4cond1,V4cond2,V4cond3,V5cond1,V5cond2,V5cond3,V6cond1,V6cond2,V6cond3))

#V3= b_1+b_2+T3 +pT1+qT2= chi^... [y/w] eta^12 {lambda_R^a}
V3proj=[(c[32]+c[34]+c[29]+p*c[20]+q*c[25])%2+(c[26]+c[27]+1+c[3]+p*c[16]+q*c[21])%2 +        (c[3]+c[26]+c[27]+c[28]+c[29]+c[31]+c[33]+c[32]+c[34]+p*(c[1]+c[17]+c[18]+c[19]+c[20])+          q*(c[2]+c[22]+c[23]+c[24]+c[25]))%2 +         (p+q+c[31]+c[33]+c[28]+p*c[19]+q*c[24]+p*(c[17]+c[18]+c[16]+1+c[1]+q*c[15])+          q*(c[22]+c[23]+c[21]+p*c[15]+1+c[2]))%2!=1 for p in range(0,2) for q in range(0,2)]
    

#V2= b_1+b_3+T2 +pT1+qT3= chi^... [y/w] eta^13 {lambda_R^a}
V2proj=[(c[32]+c[35]+c[25]+p*c[20]+q*c[29])%2+(c[22]+c[24]+1+c[2]+p*c[15]+q*c[21])%2 +        (c[2]+c[22]+c[23]+c[24]+c[25]+c[30]+c[33]+c[32]+c[35]+p*(c[1]+c[17]+c[18]+c[19]+c[20])+          q*(c[3]+c[26]+c[27]+c[28]+c[29]))%2 +         (p+q+c[30]+c[33]+c[23]+p*c[18]+q*c[27]+p*(c[17]+c[19]+c[15]+1+c[1]+q*c[16])+          q*(c[26]+c[28]+c[21]+p*c[16]+1+c[3]))%2!=1 for p in range(0,2) for q in range(0,2)]



#V1= b_2+b_3+T1 +pT2+qT3= chi^... [y/w] eta^23 {lambda_R^a}
V1proj=[(c[34]+c[35]+c[20]+p*c[25]+q*c[29])%2+(c[18]+c[19]+1+c[1]+p*c[15]+q*c[16])%2 +        (c[1]+c[17]+c[18]+c[19]+c[20]+c[30]+c[31]+c[34]+c[35]+p*(c[2]+c[22]+c[23]+c[24]+c[25])+          q*(c[3]+c[26]+c[27]+c[28]+c[29]))%2 +         (p+q+c[30]+c[31]+c[17]+p*c[22]+q*c[26]+p*(c[23]+c[24]+c[15]+1+c[2]+q*c[21])+          q*(c[27]+c[28]+c[16]+p*c[21]+1+c[3]))%2!=1 for p in range(0,2) for q in range(0,2)]
    
s.add(V2proj+V3proj) #V1proj


# conditions on projection of twisted bosons: spinorials
#B12=1+b1+b2+b3+z1+T1+T2=z2+T1+T2
B12proj=(c[32]+c[34]+c[35]+c[20]+c[25])%2+(c[3]+c[16]+c[21]+c[26]+c[27]+c[28]+c[29])%2!=0

#B11=1+b1+b2+b3+z1+T1+T3=z2+T1+T3
B11proj=(c[32]+c[34]+c[35]+c[20]+c[29])%2+(c[2]+c[15]+c[21]+c[22]+c[23]+c[24]+c[25])%2!=0


#B10=1+b1+b2+b3+z1+T2+T3=z2+T2+T3
B10proj=(c[32]+c[34]+c[35]+c[25]+c[29])%2+(c[1]+c[15]+c[16]+c[17]+c[18]+c[19]+c[20])%2!=0

s.add(And(B10proj,B11proj,B12proj))


#B9=1+b3+T3+z1+pT1+qT2 
B9proj_pq=[(c[28]+1+c[29]+p*c[16]+q*c[21])%2+(c[35]+c[29]+p*c[20]+q*c[25])%2 +         (1+p+q+c[28]+c[35]+p*c[19]+q*c[24]+p*(c[1]+c[19]+c[16]+c[20]+(1+c[1])+q*c[15])+q*(c[2]+c[24]+c[21]+c[25]+p*c[15]+(1+c[2])))%2!=0          for p in range(0,2) for q in range(0,2)]

#B8=1+b2+T2+z1+pT1+qT3 
B8proj_pq=[(c[23]+1+c[25]+p*c[15]+q*c[21])%2+(c[34]+c[25]+p*c[20]+q*c[29])%2 +         (1+p+q+c[23]+c[34]+p*c[18]+q*c[27]+p*(c[1]+c[18]+c[15]+c[20]+(1+c[1])+q*c[16])+q*(c[3]+c[27]+c[21]+c[29]+p*c[16]+(1+c[3])))%2!=0          for p in range(0,2) for q in range(0,2)]

#B7=1+b1+T1+z1+pT2+qT3 
B7proj_pq=[(c[17]+1+c[20]+p*c[15]+q*c[16])%2+(c[32]+c[20]+p*c[25]+q*c[29])%2 +         (1+p+q+c[17]+c[32]+p*c[22]+q*c[26]+p*(c[2]+c[22]+c[15]+c[25]+(1+c[2])+q*c[21])+q*(c[3]+c[26]+c[16]+c[29]+p*c[21]+(1+c[3])))%2!=0          for p in range(0,2) for q in range(0,2)]
    
s.add(B7proj_pq+B8proj_pq+B9proj_pq)
    
#B6=z1+T1+T2
B6proj=(c[1]+c[2]+c[32]+c[17]+c[22]+c[34]+c[18]+c[23]+c[35]+c[19]+c[24]+c[20]+c[25])%2 +         (c[32]+c[17]+c[22]+c[34]+c[18]+c[23]+c[35]+c[19]+c[24]+c[20]+c[1]+c[25]+c[2])%2 +         (c[29]+c[16]+c[21])%2!=0

#B5=z1+T1+T3
B5proj=(c[1]+c[3]+c[32]+c[17]+c[26]+c[34]+c[18]+c[27]+c[35]+c[19]+c[28]+c[20]+c[29])%2 +         (c[32]+c[17]+c[26]+c[34]+c[18]+c[27]+c[35]+c[19]+c[28]+c[20]+c[1]+c[29]+c[3])%2 +         (c[25]+c[15]+c[21])%2!=0

#B4=z1+T2+T3
B4proj=(c[2]+c[3]+c[32]+c[22]+c[26]+c[34]+c[23]+c[27]+c[35]+c[24]+c[28]+c[25]+c[29])%2 +         (c[32]+c[22]+c[26]+c[34]+c[23]+c[27]+c[35]+c[24]+c[28]+c[25]+c[2]+c[29]+c[3])%2 +         (c[20]+c[15]+c[16])%2!=0

s.add(And(B4proj,B5proj,B6proj))

#B3 b1+b2+z1+T3+pT1+qT2
B3proj_pq=[(c[26]+c[27]+c[29]+1+c[3]+p*c[16]+q*c[21])%2+       (c[3]+c[26]+c[27]+c[28]+c[29]+c[31]+c[33]+c[35]+p*(c[1]+c[17]+c[18]+c[19]+c[20])+q*(c[2]+c[22]+c[23]+c[24]+c[25]))%2 +       (1+p+q+c[31]+c[33]+c[35]+c[28]+p*c[19]+q*c[24]+p*(c[17]+c[18]+c[20]+c[16]+1+c[1]+q*c[15])+q*(c[22]+c[23]+c[25]+c[21]+p*c[15]+1+c[2]))%2!=0           for p in range(0,2) for q in range(0,2) ]

#B2 b1+b3+z1+T2+pT1+qT3
B2proj_pq=[(c[22]+c[24]+c[25]+1+c[2]+p*c[15]+q*c[21])%2+       (c[2]+c[22]+c[23]+c[24]+c[25]+c[30]+c[33]+c[34]+p*(c[1]+c[17]+c[18]+c[19]+c[20])+q*(c[3]+c[26]+c[27]+c[28]+c[29]))%2 +       (1+p+q+c[30]+c[33]+c[34]+c[23]+p*c[18]+q*c[27]+p*(c[17]+c[19]+c[20]+c[15]+1+c[1]+q*c[16])+q*(c[26]+c[28]+c[29]+c[21]+p*c[16]+1+c[3]))%2!=0           for p in range(0,2) for q in range(0,2) ]

# B1=b2+b3+z1+T1+pT2+qT3

B1proj_pq=[(c[18]+c[19]+c[20]+1+c[1]+p*c[15]+q*c[16])%2+       (c[1]+c[17]+c[18]+c[19]+c[20]+c[30]+c[31]+c[32]+p*(c[2]+c[22]+c[23]+c[24]+c[25])+q*(c[3]+c[26]+c[27]+c[28]+c[29]))%2 +       (1+p+q+c[30]+c[31]+c[32]+c[17]+p*c[22]+q*c[26]+p*(c[23]+c[24]+c[25]+c[15]+1+c[2]+q*c[21])+q*(c[27]+c[28]+c[29]+c[16]+p*c[21]+1+c[3]))%2!=0           for p in range(0,2) for q in range(0,2) ]
#B1projBools=[x==0 for x in B1proj_pq]

s.add(B1proj_pq+B2proj_pq+B3proj_pq)

import timeit
import json 
start1 = timeit.default_timer()
print(s.check()) 
stop1 = timeit.default_timer()
print("Time:", stop1 - start1)
start2 = timeit.default_timer()

"""
if s.check() == unsat:
    s.set("smt.core.minimize","true")
    print(s.unsat_core())
    #NumbFile1 = open('ProofNo16s.txt','a')
    #old_stdout = sys.stdout  #  store the default system handler to be able to restore it
    #sys.stdout = NumbFile1
    #print(s.proof())
    #NumbFile1.close()
    #sys.stdout=old_stdout
    
else: """
while s.check() == sat:
    m = s.model ()
    if not m:
        break
    NumbFile = open('IntTest356.txt','a')
    old_stdout = sys.stdout  #  store the default system handler to be able to restore it
    sys.stdout = NumbFile
    #t2=time()
    #elapsed=t2-t1
    #print(elapsed)
    print([m[c[i]] for i in range(36)])
    #print(sorted ([(d, m[d]) for d in m], key = lambda x: str(x[0])))
    #print(sorted ([(m[d]) for d in m], key = lambda x: str(x[0])))
    NumbFile.close()
    sys.stdout=old_stdout

    s.add(Not(And([v() == m[v] for v in m])))

stop2 = timeit.default_timer()
print("Time:", stop2 - start2)
"""
def n_solutions(n):
    s = Solver()
    # add constraints s.add()
    count = 0
    while s.check() == sat and count < n:
        m = s.model()
        print(count)
        print([m[c[i]] for i in range(36)])
        print("\n")
        s.add(Not(And([v() == m[v] for v in m])))
        count += 1
        
n_solutions(10)
""" 


# In[ ]:




