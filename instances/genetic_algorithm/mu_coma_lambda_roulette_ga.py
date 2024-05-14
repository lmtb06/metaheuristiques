#! /usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np

import random
from .mu_coma_lambda_ga import MuComaLambdaGA
from search import PopulationSearchAlgorithm, BinarySolution, sort_pop, eval_solutions

class MuComaLambdaRouletteGA(MuComaLambdaGA):

    def __init__ (self, prob, options) :
        """
        Entrées : 

        * Un problème donnée instance de la classe Problem.
        Seules les problèmes dont les solution sont des tableaus booléens sont 
        acceptée. 
        
        * Un dictionnaire des paramètres des algorithmes 

        """
        MuComaLambdaGA.__init__(self, prob, options)
        self._cdf_function = self._generate_cdf_function(options)
    
    @property
    def name(self):
        return "µ,λ(roulette) µ{}_λ{}_pc{}_pm{}_type{}".format(self._mu, self._lambda, self._pc, self._pm, self._type_cdf).replace('.',',')

    def _generate_cdf_function(self, options):
        """
        Génère la fonction qui calcule la cumulative distribution function en fonction des options. (higher order function)
        la fonction retournée prend en entrée une liste de solutions et retourne une liste de probabilités cumulées.
        """
        def cdf_using_fitness(pool):
            """
            Retourne la cumulative distribution function pour la sélection des parents
            basée sur la fitness des solutions dans la population.
            """
            cdf = []
            # On calcule la somme des fitness sans considérer les valeurs infinies
            fitnessTotal = 0
            for s in pool:
                if s.value != float('inf') and s.value != float('-inf'):
                    fitnessTotal += s.value
            # Pour chaque solution on calcule la probabilité de sélection
            # en fonction de sa fitness
            for s in pool:
                if s.value != float('inf') and s.value != float('-inf'):
                    cdf.append(s.value / fitnessTotal)
                else:
                    cdf.append(0)

            # On calcule la somme cumulée des probabilités
            for i in range(1, len(cdf)):
                cdf[i] += cdf[i-1]
            # print(cdf)
            return cdf
            

        def cdf_using_rank(pool):
            """
            Retourne la cumulative distribution function pour la sélection des parents
            basée sur le rang des solutions dans la population.
            """
            cdf = []
            # on calcule le rang de chaque solution par ordre croissant de fitness (dictionnaire)
            copy_pool = pool.copy()
            idx = sort_pop(copy_pool, self._problem)
            # on calcule la probabilité de sélection en fonction du rang
            taille = len(pool)
            for i in range(taille):
                rank = idx[i]
                proba = (2 - S) / taille + 2 * rank * (S - 1) / (taille * (taille - 1))
                cdf.append(proba)
            # On calcule la somme cumulée des probabilités
            for i in range(1, len(cdf)):
                cdf[i] += cdf[i-1]
            return cdf

        self._type_cdf = options.get('type_cdf', 'fitness')
        if self._type_cdf == 'fitness':
            return cdf_using_fitness
        elif self._type_cdf == 'rank':
            S = options.get('S', 2)
            return cdf_using_rank
        else:
            raise ValueError("Unknown type of cdf function")

    def update_pop(self, offspring):
        """
        Constituer la nouvelle population selon une stratégie de selection 
        donnée depuis les enfants et self._pop.  

        Entrée : une liste de solutions enfants 
        Sortie : une liste de solutions de taille self._mu

        """
        eval_solutions(offspring, self._problem)
        population = self._pop + offspring
        new_pop = self._select_roulette(population)
        
        return new_pop

    
    def _select_roulette(self, pool):
        """
        Sélectionne n individu dans la population en utilisant la méthode de la roulette.
        Avec cdf la cumulative distribution function.
        """
        selection = []
        cdf = self._cdf_function(pool)
        s = 0
        while s < self._mu:
            r = random.random()
            i = 0
            while cdf[i] < r:
                i += 1
            selection.append(pool[i].clone())
            s += 1
        return selection

