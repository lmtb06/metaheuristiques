#! /usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np

from .solution import Solution

class RealSolution(Solution):

    """
    Classe abstraite pour representer une solution comme un vecteur de réels

    """
    def __init__(self, dim=None, x=None):
        Solution.__init__(self, dim, x)
        if x is None :
            self._sol = np.zeros(dim, dtype=np.double)

    def random(self):
        """ Retourne une solution aléatoire dans [-5, 5]^dim """
        rnd = np.random.random(self.dim)
        rnd *= 10
        rnd -= 5
        return RealSolution(x=rnd)
    
    def neighbors(self):
        raise NotImplementedError("Une solution réelle n'a pas de voisinage")
    
    def clone(self):
        """ Pour cloner la solution """
        clone_sol =  RealSolution( x=self._sol )   
        clone_sol._value = self.value
        return clone_sol
    
    def __str__(self):
        """ une méthode to string pour afficher la solution """
        return "Not printed"
        return ",".join([ str(i) for i in  self._sol ])
    
