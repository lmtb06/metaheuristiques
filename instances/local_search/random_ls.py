#! /usr/bin/env python
# -*- coding: utf-8 -*-
import random

from search import LocalSearchAlgorithm

class RandomLS(LocalSearchAlgorithm):

    def __init__(self, prob, options):
        """ Constructeur de la super classe 
        """
        LocalSearchAlgorithm.__init__(self, prob, options)
   
    def get_neighbors(self):
        """ retourner les voisins de la solution courante 
        """ 
        return self._solution.neighbors()

    def filter_neighbors(self, neighbors):
        """ filtrer toutes les solutions violant les contraintes 
        """
        return [ n for n in neighbors if self._problem.feasable(n) ]
    
    def select_next_solution(self, candidates):
        """ Si il y des solutions (après filtrage), retourner une au hasard
        """
        if len(candidates) >0 :
            return random.choice(candidates)
        return None

    def accept(self, new_solution) :
        """ RandomLS accepte toutes les solutions, retourner True
        """

        # Dans un autre algorithme il  faut faire un choix, les
        # valeurs des solutions son obtenues comme suit :
        #
        cur_solution_val = self._solution.value
        new_solution_val = self._problem.evaluate(new_solution)
                
        return True
    
  

