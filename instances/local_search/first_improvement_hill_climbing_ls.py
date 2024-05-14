#! /usr/bin/env python
# -*- coding: utf-8 -*-
import random

from search import LocalSearchAlgorithm
from functools import cmp_to_key
from .hill_climbing_ls import HillClimbingLS

class FirstImprovementHillClimbingLS(HillClimbingLS):
    """
    Algorithme de recherche locale Hill Climbing avec choix du premier voisin améliorant
    """

    def __init__(self, prob, options):
        """ Constructeur de la super classe 
        """
        super().__init__(prob, options)
   
    @property
    def name(self):
        return "FIHillClimbing"

    def select_next_solution(self, candidates):
        """ Si il y des solutions (après filtrage), retourne la première solution améliorante
        """
        if len(candidates) >0 :
            for candidate in candidates:
                if self.better(self._problem.evaluate(candidate), self._solution.value):
                    return candidate
        return None

    def accept(self, new_solution) :
        """ FirstImprovementHillClimbingLS accepte les solutions améliorantes, retourner True
        """

        # Dans un autre algorithme il  faut faire un choix, les
        # valeurs des solutions son obtenues comme suit :
        #
        cur_solution_val = self._solution.value
        new_solution_val = self._problem.evaluate(new_solution)
                
        return self.better(new_solution_val, cur_solution_val)
    
  

