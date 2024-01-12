#! /usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from random import shuffle

from .solution import Solution

class BinarySolution(Solution):

    """
    Classe abstraite pour representer une solution  binnaire
    
    """
    
    def __init__(self, dim=None, x=None):
        Solution.__init__(self, dim, x)
        if x is None :
            self._sol = np.zeros(dim, dtype=np.bool_)

    def random(self):
        """ Retourne une solution aléatoire """
        rnd = np.random.random(self.dim) < 0.5
        return BinarySolution(x=rnd)
    
    def neighbors(self):
        """ Retourne toutes les solutions voisines i.e. differentes de 1 """
        N = []
        for i in range(len(self._sol)):
            n = np.copy( self._sol )
            n[i] = not n[i]
            N.append(BinarySolution(x=n))

        # mélanger pour rendre le parcours non déterministe 
        shuffle(N)
        return N
    
    def clone(self):
        """ Pour cloner la solution """
        clone_sol = BinarySolution( x=self._sol )   
        clone_sol._value = self.value
        return clone_sol
    
    def __str__(self):
        """ une méthode to string pour afficher la solution """
        return "".join([ '1' if i else '0' for i in  self._sol ])
    
