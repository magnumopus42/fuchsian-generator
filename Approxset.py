import numpy as np
import json
import os

class ApproxSet():
    """An Approxset class which could be used in a more refined version of this project"""

    def __init__(self, epsilon=None):
        """Set attributes of s and epsilon"""
        self.s=[]
        if epsilon==None: 
            self.epsilon=10**-10
        else:
            self.epsilon=epsilon

    def __contains__(self,element):
        """If an element's components are not greater than epsilon, it doesn't belong"""
        element=np.array(element)
        for x in self:
            if np.linalg.norm(x-element) < self.epsilon:  #return the bool value here
                return True
            if np.linalg.norm(x+element) < self.epsilon:
                return True
        return False

    def add(self, element):
        """"""
        if element not in self:  #if true, we concatenate the arrays
            self.s.append(element)

    def union(self,other):
        """"""
        eps=max(self.epsilon, other.epsilon)
        T=ApproxSet(eps)
        for x in self:
            T.add(x)
        for x in other:
            T.add(x)
        return T

    def __iter__(self):
        """"""
        return iter(self.s)

    def symdiff(self, other):
        """Return an approxset C that contains unique elements from self and other"""
        C=ApproxSet()
        for x in self:
            if x in other:
                continue
            else:
                C.add(x)   
        for y in other:
            if y in self:
                continue
            else:
                C.add(y)
        
    def __len__(self):
        """"""
        return len(self.s)

    def __mul__(self, other):
        """Return the Approxset of every element in self multiplied with every thing in other"""
        P=ApproxSet(self.epsilon)
        for x in self:
            for y in other:  
                P.add(x.dot(y))

        return P

    def __str__(self):
        return str(self.s)
              

