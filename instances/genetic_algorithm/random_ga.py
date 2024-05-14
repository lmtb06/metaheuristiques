#! /usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np

import random 

from search import PopulationSearchAlgorithm, BinarySolution, sort_pop

class RandomGA(PopulationSearchAlgorithm):

    def __init__ (self, prob, options) :
        """
        Entrées : 

        * Un problème donnée instance de la classe Problem.
        Seules les problèmes dont les solution sont des tableaus booléens sont 
        acceptée. 
        
        * Un dictionnaire des paramètres des algorithmes 

        """
        super().__init__(prob, options)

    @property
    def name(self):
        return "RandomGA µ{}_λ{}".format(self._mu, self._lambda).replace('.',',')

    def _select_one_random(self, pool):
        """
        On selectionnne une solution aleatoire de la population donnée

        Entrée : une liste de solutions
        Sortie : un element aléatoire (une copie de l'élément)
        
        """
        return random.choice( pool ).clone()

    def _select_n_best(self, pool, n):
        """
        Retourne les n meilleures solution dans la liste donnée, 
        on trie pool et retourne les n premiers.
        
        Entrée : une liste de solutions (précédemment évaluées)
        Sortie : une liste des n meilleures 
        """
        
        sort_pop(pool, self._problem)
        return [x.clone() for x in pool[:n]]

    def _xover_one_point(self, x1, x2):
        """
        Croisement en un point de deux individus.

        Entrée : deux instances de la classe Solution
        Sortie : les deux solution croisée 

        """
        if not (isinstance(x1, BinarySolution) and
                isinstance(x2, BinarySolution) ) :
            raise TypeError("Algorithm only works on binary solution problems")
        
     
        # le point de croisement
        point = random.randint(0, len(x1.solution)-1)

        for i in range(point, len(x1.solution)):
            tmp = x1.solution[i]
            x1.solution[i] = x2.solution[i]
            x2.solution[i] = tmp
        
        return x1, x2
    
    def _mutation_bitflip(self, x) :
        """ 
        Mutation d'un individu. On modifie un bit aléatoire de la solution.
        
        Entrée : une instance de la classe Solution.
        Sortie : la solution modifiée
        """
        if not isinstance(x, BinarySolution) :
            raise TypeError("Algorithm only works on binary solution problems")
      
        i = random.randint(0, len(x.solution)-1 )
        x.solution[i] = not x.solution[i]
            
        return x
             
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
            p1, p2 = self._xover_one_point(p1, p2)
            
            # mutation 
            p1 = self._mutation_bitflip( p1 )
            p2 = self._mutation_bitflip( p2 )
         
            # on rajoute a la liste
            offspring.append(p1)
            offspring.append(p2)

            # si la population des enfants est remplie, on la retourne
            done = len(offspring) == self._lambda
            
        return offspring

    def update_pop(self, offspring):
        """
        Constituer la nouvelle population selon une stratégie de selection 
        donnée depuis les enfants et self._pop.  

        Entrée : une liste de solutions enfants 
        Sortie : une liste de solutions de taille self._mu

        """
        new_pop = self._select_n_best(offspring, self._mu)
        
        return new_pop
