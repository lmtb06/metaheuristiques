#! /usr/bin/env python
# -*- coding: utf-8 -*-
from .random_ls import RandomLS
from functools import cmp_to_key

class HillClimbingLS(RandomLS):

    def __init__(self, prob, options):
        """ Constructeur de la super classe 
        """
        super().__init__(prob, options)
   
    @property
    def name(self):
        return "HillClimbing"
    
    def select_next_solution(self, candidates):
        """ Si il y des solutions (après filtrage), retourner la meilleure
        """
        if candidates:  # Vérifie si la liste n'est pas vide
            for c in candidates:
                # Si le candidat n'est pas évalué, on l'évalue
                if not c.value:
                    self._problem.evaluate(c)
                    
            # Trie les candidats en utilisant le comparateur et retourne le meilleur
            candidates.sort(key=cmp_to_key(self.compare), reverse=True)
            return candidates[0]
        return None

    def accept(self, new_solution) :
        """ HillClimbing accepte la solution si elle est supérieure ou égale à la solution courante
        """
        return self.better(new_solution, self._solution)
    
  

