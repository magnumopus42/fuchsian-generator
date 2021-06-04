import sys
import sage.all
import csv

"""Compute a large number of non isomorphic quaternion algebras"""

M=100

if len(sys.argv)==1:
    M=100
else:  
    M=sys.argv[1]

disc={}   #our different lists which are used in the dictionary


for b in range(2, int(M)+1):
    for a in range(2, b): 
        D=sage.all.QuaternionAlgebra(a,b)  #compute our quaternion algebra discriminant
        val=D.discriminant()
        if val not in disc:                #append new discriminants and the key a,b to our dict
            disc[val]=(a,b)

filename = open('discout.csv','w', newline="")   #begin writting to csv
fieldnames = ["D","a","b"]                       
writer = csv.DictWriter(filename, fieldnames)
writer.writeheader()
for D in sorted(disc):
    if D==1:
        continue
    a,b=disc[D]
    writer.writerow({"D":D , "a": a , "b": b})  #write the row as discriminant, a, b
filename.close()








