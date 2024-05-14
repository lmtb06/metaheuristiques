#! /usr/bin/env python
# -*- coding: utf-8 -*-

from collections import deque
from .random_ls import RandomLS

class TabuLS(RandomLS):
    """
    Algorithme de Recherche Tabou
    """

    def __init__(self, prob, options):
        """ Constructeur de la super classe 
        """
        super().__init__(prob, options)
        # Taille de la liste tabou
        self.t = options.get('t', 10)
        # liste tabou (utilisation d'une deque pour une gestion automatique de la taille et pour plus d'efficacité)
        self._tabu_list = deque(maxlen=self.t)

    @property
    def name(self):
        return "Tabu"
    
    def select_next_solution(self, candidates):
        """ Si il y des solutions (après filtrage), retourne la meilleure solution non dans la liste tabou
        """
        if len(candidates) > 0:
            meilleur = None # pour stocker la meilleure solution

            for candidate in candidates:
                # Si la solution n'est pas dans la liste tabou on la compare avec la meilleure solution et on la remplace si elle est meilleure
                if candidate not in self._tabu_list:

                    if not candidate.value: # Si la solution n'a pas été évaluée, on l'évalue
                        self._problem.evaluate(candidate)

                    if not meilleur: # Si c'est la première solution on la stocke
                        meilleur = candidate
                    elif self.better(candidate, meilleur): # Si la solution est meilleure que la meilleure solution on la stocke
                        meilleur = candidate
            return meilleur
        return None

    def accept(self, new_solution) :
        """
        Met à jour la liste taboue (toutes les solution sont acceptées)
        """
        # Si la taille de la file est atteinte, retire le dernier élément
        if len(self._tabu_list) == self._tabu_list.maxlen:
            self._tabu_list.popleft()

        # append la nouvelle solution à la liste taboue
        self._tabu_list.append(new_solution)
        
        return True
    
    def print_step(self):
        """ Retourne des infos sur l'itération
        """
        return f"{super().print_step()} t:{self.t}"

