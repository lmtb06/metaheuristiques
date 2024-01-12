#! /usr/bin/env python
# -*- coding: utf-8 -*-

import math
import random
import numpy as np

from search import EvolutionStrategy, RealSolution, eval_solutions, sort_pop

class RandomES(EvolutionStrategy):

    def __init__ (self, prob, options) :

        EvolutionStrategy.__init__(self, prob, options)

        # On fixe les paramètres de l'algorithme en dur
        #
        # *NOTE* : il est mieux de les passer en argument au constructeur de
        #          EvolutionStrategy depuis le script main.py
        #          (cf. le constructeur de evolution_strategy.py )
        # 
        # Exemple : algo_options = { 'mu' : 10, 'lambda' : 20, 'sigma' : 1.3 }
        #           dans main.py
        #
        
        self._mu = 5
        self._lambda = 10
        self._sigma = 1.0
        
        # ATTENTION : Quelque étapes dans ce code ne sont pas nécessaires, 
        #             elles sont là pour illustrer comment le faire pour
        #             les autres instance des algorithme.
        #             Ne pas hésitez à corriger cela. 
        #
        #
        # 1) comme on choisi un point aléatoire de l'échantillon 
        #    il n'est pas nécessaire d'en générer lambda.
        #
        # 2) De même pour l'évaluation et le tri
        #
        
    def sample_solutions(self):
        """ 
        Échantillonage depuis une distribution normale autour de la solution 
        courante (moyennne) et self._sigma comme variance. 
        
        Retourne une liste de Lambda solutions évaluée et triée

        """
        sample = [] 
        for i in range(self._lambda) :
            
            # un vecteur normal de dimension n, de moyenne 0 et variance 1
            
            z = np.random.normal(size=self._solution.dim)

            # on le met à l'échelle et le translate 
            
            x = RealSolution(x=(z * self._sigma + self._solution.solution))
            sample.append(x)

        # évaluer les solutions de l'échantillon
        eval_solutions(sample, self._problem)
         
        # le trie n'a aucune utilité pour cet algorithme-ci 
        self._idx = sort_pop(sample, self._problem)
            
        return sample

    def update_m(self, sample):
        """ 
        Mise à jour de la moyenne (solution courrante) de la distribution
        Entrées :

        * l'échantillon de lambda solutions 
        
        Ici : Choisir une solution aléatoire et la garder si elle améliore.
       
        """
        new_solution = random.choice(sample)
        if self.better(new_solution, self._solution) :
            self._solution = new_solution
        
    def update_sigma(self, sample):
        """ 
        Mise à jour du pas de mutation sigma (variance) selon une règle donnée.

        Entrées :

        * l'échantillon de lambda solutions 

        Ici : cet algorithme on ne change pas la valeur de sigma 
        """
        pass

        
  
