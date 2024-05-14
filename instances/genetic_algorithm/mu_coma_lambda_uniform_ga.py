#! /usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np

import random
from .mu_coma_lambda_ga import MuComaLambdaGA
from search import PopulationSearchAlgorithm, BinarySolution, sort_pop

class MuComaLambdaUniformGA(MuComaLambdaGA):

    def __init__ (self, prob, options) :
        """
        Entrées : 

        * Un problème donnée instance de la classe Problem.
        Seules les problèmes dont les solution sont des tableaus booléens sont 
        acceptée. 
        
        * Un dictionnaire des paramètres des algorithmes 

        """
        MuComaLambdaGA.__init__(self, prob, options)
    @property
    def name(self):
        return "µ,λ (uniform) µ{}_λ{}_pc{}_pm{}".format(self._mu, self._lambda, self._pc, self._pm).replace('.',',')

    def _mutation_uniform(self, x):
        """
        Mutation uniforme d'une solution x. Chaque bit a une probabilité 
        1/len(x.solution) d'être modifié.
        """
        if not isinstance(x, BinarySolution) :
            raise TypeError("Algorithm only works on binary solution problems")
        
        proba = 1.0/len(x.solution)
        for i in range(len(x.solution)):
            if random.random() < proba :
                x.solution[i] = not x.solution[i]

        return x

    def _xover_uniform(self, x1, x2):
        """
        Croisement uniforme de deux solutions x1 et x2. Chaque bit a une 
        probabilité 0.5 de venir de x1 ou x2.
        """
        if not (isinstance(x1, BinarySolution) and
                isinstance(x2, BinarySolution) ) :
            raise TypeError("Algorithm only works on binary solution problems!")
        
        for i in range(len(x1.solution)):
            if random.random() < 0.5 :
                x1.solution[i] = x2.solution[i]
        
        return x1


    def evolve_pop(self):
        """
        Créer des nouvelles solution par evolution des parents. Les opérateurs 
        génétique son appliqué ici. 

        Entrée : une liste de parents (cf. make_parent_pop)
        Sortie : une liste de solutions enfants de taille self._lambda

        """
        offspring = []
        done = False
        while not done : 

            # on prend une solution 
            p1 = self._select_one_random ( self._pop )
            p2 = self._select_one_random ( self._pop )
            
            # croisement
            if random.random() < self._pc :
                p1 = self._xover_uniform(p1, p2)
            
            
            # mutation
            if random.random() < self._pm :
                p1 = self._mutation_uniform( p1 )
         
            # on rajoute a la liste
            offspring.append(p1)

            # si la population des enfants est remplie, on la retourne
            done = len(offspring) == self._lambda
            
        return offspring
