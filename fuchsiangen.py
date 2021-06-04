import numpy as np  
import math
import json
import csv
import Approxset as ap
import datetime
import time
import sage.all

M_default=10

def fuchsiangen(a,b,M=M_default):
    """Consider a cube centered at the origin and evaluate all lattice points in it that have a determinant of 1"""
    p=0
    q=0
    r=0
    s=0  #for loops
    T = ap.ApproxSet()
    #iterate through all possible tuples {p,q,r,s} in range M
    for p in range(-M, M+1):
        for q in range(-M, M+1):
            for r in range(-M, M+1):
                for s in range(-M, M+1):
                    det=p**2-a*q**2-b*r**2+a*b*s**2
                    if det==1:  #make our set p,q,r,s into a matrix if det=1
                        m = np.array([[1,0],[0,1]])*p + np.array([[math.sqrt(a),0],[0,-math.sqrt(a)]])*q+np.array([[0,math.sqrt(b)],[math.sqrt(b),0]])*r+np.array([[0,math.sqrt(a*b)],[-math.sqrt(a*b),0]])*s 
                        T.add(list(m.ravel()))
    return T

def fuchsiangenrectangle(a,b):
    """Consider a rectangular prism and evaluate all lattice points in it that have a determinant of 1"""
    p=0
    q=0
    r=0
    s=0  
    #Consider a rectangle of integer side lengths and iterate through every lattice point in it
    p_range=int(10*math.sqrt(a*b))
    q_range=int(10*math.sqrt(b))
    r_range=int(10*math.sqrt(a))
    s_range=5
    T=ap.ApproxSet()
    #iterate through all possible tuples {p,q,r,s} in a rectangular prism
    for p in range(-p_range, p_range):
        for q in range(-q_range, q_range+1):
            for r in range(-r_range, r_range+1):
                for s in range(-s_range, s_range+1):
                    det=p**2-a*q**2-b*r**2+a*b*s**2
                    if det==1:  #make our set p,q,r,s into a matrix if det=1
                        m = np.array([[1,0],[0,1]])*p + np.array([[math.sqrt(a),0],[0,-math.sqrt(a)]])*q+np.array([[0,math.sqrt(b)],[math.sqrt(b),0]])*r+np.array([[0,math.sqrt(a*b)],[-math.sqrt(a*b),0]])*s 
                        T.add(m)
    return T

def write_elements_json(a,b,M=M_default):
    D=sage.all.QuaternionAlgebra(a,b) 
    val=D.discriminant()
    matrices=fuchsiangen(a,b,M)
    date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    outfn="disc{}-hilb{}-{}-maxcoef{}.json".format(val,a,b,M)
    d=dict()
    d["format"] = "slview_v1"
    d["mode"] = "sl2"
    d["layout"]=["a","b","c","d"]
    d["vectors"]=[]
    d["title"]="D={}:({},{}|Q)".format(val,a,b)
    for m in matrices:
        d["vectors"].append(m)   

    d["shortdesc"]="Arith Fuchs/Q, D={} (maxcoef {})".format(val,M) 
    d["longdesc"]="""The Arithmetic Fuchsian group associated to the order Z+Zi+Zj+Zij in the quaternion algebra ({},{}|Q), which has discriminant {}. 
    Dataset of elements with coefficients at most {} relative to basis 1,i,j,ij.
    Created with fuchsiangen on {}.""".format(a,b,D,M,date)

    with open(outfn, "w") as outfile:
        json.dump(d, outfile)

def write_elements_json_discoutcsv(M):
    """Carry out the calcuation with a cube's lattice points for some size M and make json files for everything in discout.csv"""
    with open('discout.csv', 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            a,b=int(row["a"]), int(row["b"])
            vectors=write_elements_json(a,b,M)
            filename= open("threedaygeneration/disc({}a{}b).json".format(a,b), 'w', newline="")
            d=dict()
            d["format"] = "slview_v1"
            d["mode"] = "sl2"
            d["layout"]=["a","b","c","d"]
            d["vectors"]=[]
            T=ap.ApproxSet()
            for vector in vectors[0]:
                T.add(vector) 
            d["vectors"].append(T)
            json.dump(d, filename)
            filename.close()



