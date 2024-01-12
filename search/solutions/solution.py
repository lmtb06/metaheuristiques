#! /usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from random import shuffle


class Solution(object):
    
    """
    Classe abstraite a concrétiser, voire plus bas.
    
    """
    
    def __init__(self, dim=None, x=None):
        """ constructeur presque vide  voire les classe concrèrte plus bas """

        if dim is None and x is None :
            raise ValueError("Il faut spécifier la dimension ou une solution")
              
        if x is not None :
            self._sol = np.copy(x)
            
        self._value = None

    @property
    def dim(self):
        return len(self._sol)
        
    @property
    def solution(self):
        return self._sol

    @property
    def value(self):
        return self._value
    
    def random(self):
        """ 
        crée une solution aléatoire
        retourne un instance de Solution 
        """
        raise NotImplementedError
    
    def neighbors(self):
        """
        permet de construire l'ensemble des solutions voisines de la solution
	    courante retourne ensemble solutions voisines de self
        """
        raise NotImplementedError
        
    def clone(self):
        """ clone la solution dans une nouvelle instance """
        raise NotImplementedError

    def __str__(self):
        """ une méthode to string """
        raise NotImplementedError
        
    def __eq__(self, other):
        """ 
        une méthode pour vérifier l'égalité de deux solutions 
        Il faut la même dimention et que les tableaus soient identiques
       
        """
        if  self.dim != other.dim : 
            return False
        if self._sol.shape != other._sol.shape :
            return False
        return (self._sol == other._sol).all()




    
