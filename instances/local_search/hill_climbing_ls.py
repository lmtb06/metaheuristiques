#! /usr/bin/env python
# -*- coding: utf-8 -*-

from search import LocalSearchAlgorithm

class HillClimbingLS(LocalSearchAlgorithm):

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
        """ Si il y des solutions (après filtrage), retourner la meilleure
        """
        if len(candidates) >0 :
            return max(candidates, key = lambda x : self._problem.evaluate(x))
        return None

    def accept(self, new_solution) :
        """ HillClimbing accepte la solution si elle est supérieure ou égale à la solution courante
        """
        cur_solution_val = self._solution.value
        new_solution_val = self._problem.evaluate(new_solution)
        if new_solution_val >= cur_solution_val :
            return True
                
        return False
    
  

