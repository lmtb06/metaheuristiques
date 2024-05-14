#! /usr/bin/env python
# -*- coding: utf-8 -*-
import random

from functools import cmp_to_key
from .hill_climbing_ls import HillClimbingLS

class RandomizedHillClimbingLS(HillClimbingLS):
    """
    Algorithme de recherche locale Hill Climbing avec un choix aléatoire.
    alpha est la probabilité d'explorer un voisin aléatoire
    """

    def __init__(self, prob, options):
        """ Constructeur de la super classe 
        """
        super().__init__(prob, options)
        self._alpha = options.get('alpha', 0.45)

    @property
    def name(self):
        return "RHillClimbing"
    
    def select_next_solution(self, candidates):
        """ Si il y des solutions (après filtrage), retourne une solution aléatoire avec une probabilité _alpha ou la meilleure solution sinon (1 - _alpha)
        """
        if len(candidates) >0 :
            if self._alpha < random.uniform(0, 1):
                # on choisit un voisin aléatoire
                candidate = random.choice(candidates)
                # si le candidat est déjà évalué on ne le réévalue pas
                if not candidate.value:
                    self._problem.evaluate(candidate)
                return candidate
            else:
                # on choisit le meilleur voisin
                for candidate in candidates:
                    if not candidate.value:
                        self._problem.evaluate(candidate)
                candidates.sort(key=cmp_to_key(self.compare), reverse=True)
                return candidates[0]
        return None

    def accept(self, new_solution) :
        """ Accepte la solution courante
        (Le choix de la solution est fait dans select_next_solution)
        """
        if not new_solution.value:
            self._problem.evaluate(new_solution)
                
        return True
    
    def print_step(self):
        """ Retourne des infos sur l'itération
        """
        return f"{super().print_step()} alpha:{self._alpha}" 


