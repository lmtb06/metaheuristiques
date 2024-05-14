#! /usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from random import shuffle

from .solution import Solution

class PermutationSolution(Solution):
    """
    Classe abstraite pour representer une solution comme une permutation

    """
    
    def __init__(self, dim=None, x=None):
        Solution.__init__(self, dim, x)
        if x is None :
            self._sol = np.zeros(dim, dtype=np.int32)

    def random(self):
        """ Retourne une solution aléatoire """
        rnd = np.arange(self.dim, dtype=np.int32)
        np.random.shuffle(rnd)
        return PermutationSolution(x=rnd)
        
    def neighbors(self):
        """ 
        Retourne toutes les solutions voisines i.e. differentes de 1 
        échanger 2 elements du tableau 
        
        """
        N = []
        for i in range(len(self._sol)):
            for j in range(i+1,len(self._sol)):
                if i != j :
                    n = np.copy( self._sol )
                    tmp = n[i] 
                    n[i] = n[j]
                    n[j] = tmp
                    N.append( PermutationSolution (x=n) )

        # mélanger pour rendre le parcour non déterministe 
        shuffle(N)
        return N
    
    def clone(self):
        """ Pour cloner la solution """
        clone_sol = PermutationSolution( x=self._sol )
        clone_sol._value = self.value
        return clone_sol
    
    def __str__(self):
        """ une méthode to string pour afficher la solution """
        return ",".join([ str(i) for i in  self._sol ])
    

