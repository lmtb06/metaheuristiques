#! /usr/bin/env python
# -*- coding: utf-8 -*-
import random
import math

from search import LocalSearchAlgorithm
from .random_ls import RandomLS

class SimulatedAnnealingLS(RandomLS):
    """
    Algorithme de Recuit Simulé
    """

    def __init__(self, prob, options):
        """ Constructeur de la super classe
        T0 : Température initiale
        gamma : Coefficient de refroidissement
        """
        super().__init__(prob, options)
        self._T0 = options.get('T0', 100)  # Température initiale
        self._T = self._T0
        self._gamma = options.get('gamma', 0.99)  # Coefficient de refroidissement

    @property
    def name(self):
        return "RecuitSimulé"
    
    def select_next_solution(self, candidates):
        """ Si il y des solutions (après filtrage), retourne la première solution améliorante
        """
        if len(candidates) >0 :
            return random.choice(candidates)
        return None

    def probability_accept(self, solution) :
        """ La probabilité d'accepter une solution
        """
        return math.exp(-abs(solution.value - self._solution.value) / self._T)

    def accept(self, new_solution) :
        """
        Accepte ou non une solution
        """
        # Si la solution n'a pas été évaluée, on l'évalue
        if new_solution.value is None:
            self._problem.evaluate(new_solution)
        # Si la solution est meilleure ou si la probabilité est acceptée
        accepter = self.better(new_solution, self._solution) or self.probability_accept(new_solution) > random.uniform(0, 1)
        # Mis à jour de T
        self._T = self._T * self._gamma

        return accepter
    
    def print_step(self):
        """ Retourne des infos sur l'itération
        """
        return f"{super().print_step()} gamma:{self._gamma} T:{self._T} T0:{self._T0}"

