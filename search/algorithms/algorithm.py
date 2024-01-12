#! /usr/bin/env python
# -*- coding: utf-8 -*-

import math

import numpy as np

from search.problems import Problem
from search.solutions import Solution

from search.misc import is_finite, eval_solutions, sort_pop


class Algorithm(object):
    
    """ Classe Abstraite représentant un algorithme de recherche """

    def __init__(self, prob, options):

        if not isinstance(prob, Problem):
            raise TypeError("prob must be a instance of Problem")

        self._problem = prob

        # un critère d'arrête dépendant de l'algorithme et du problème 
        self._stop = False

        # place pour la meilleure solution 
        self._best_solution = None
                
    @property
    def best_solution(self):
        """ retourne la meilleure solution """
        return self._best_solution
    
    @property
    def name(self):
        """ Retourne le nom de l'algorithme """
        return self.__class__.__name__.rsplit(".")[0]
        
    def stop(self) :
        """ 
        Un critère d'arrêt atteint  max eval ou plus a définir 
        retourne un boolean vrai si on s'arrête 
        """
        return self._problem.no_more_evals() or self._stop

    def better(self, v1, v2) :
        """
        En fonction du context minimisation ou maximisation 
        retourn si la valeur de v1 est meilleur que la valeur v2

        Prend : deux valeurs de solution ou deux solution  
        Retourne :  un booléen
        """

        if isinstance(v1, Solution) and isinstance(v2, Solution) :
            if self._problem.maximize and v1.value >= v2.value:
                return True
            if self._problem.minimize and v1.value <= v2.value:
                return True
            return False
        
        elif isinstance(v1, float) and isinstance(v2, float) :
            if self._problem.maximize and v1 >= v2:
                return True
            if self._problem.minimize and v1 <= v2:
                return True
            return False

        else :
            raise TypeError("v1 et v2 doivent être des Solutions ou float.")


    def compare (self, x1, x2) :
        """
        Comparaison pour le fonctions de tri en fonction du context 
        minimisation ou maximisation 

        Prend : deux Solution 
        Retourne : un entier 

        """
        if isinstance(v1, Solution) and isinstance(v2, Solution) :
            if self._problem.maximize and v1.value >= v2.value:
                return 1
            if self._problem.minimize and v1.value <= v2.value:
                return 1
            return -1
        
        else :
            raise TypeError("v1 et v2 doivent être des Solutions.")


    def print_final(self):
        """ retourne des infos finale  """
        sol_str = self._problem.print_solution(self._best_solution)
        return "Final solution: eval:{} {}".format(
            self._problem.nb_evaluations, sol_str )
        
class OneSolutionAlgorithm(Algorithm) :

    """ Classe Abstraite représentant un algorithme a une solution """

    def __init__(self, prob, options):
    
        Algorithm.__init__(self, prob, options)

        # génération de la solution initiale 
        self._solution = self._problem.generate_initial_solution(\
                                                        sol_type='random')
        self._problem.evaluate(self._solution)

        # on enregistre la meilleure solution trouvée
        # utile pour les algorithmes qui autorise la dègradation
        
        self._best_solution = self._solution.clone()

        self.update_stats()

    @property
    def curent_solution(self):
        """ retourne la solution courante """
        return self._solution

    def value(self):
        """ Retourne la valeur de la solution courante  """
        return  self._solution.value

    def update_stats(self):
        """ Mettre a jour la meilleure solution rencontrée """
        
        old_val = self._best_solution.value
        new_val = self._solution.value

        if self._problem.maximize and new_val >= old_val:
            self._best_solution = self._solution.clone()
        
        if self._problem.minimize and new_val <= old_val:
            self._best_solution = self._solution.clone()
    
    def print_step(self):
        """ retourne des infos sur l'itération  """
        sol_str = self._problem.print_solution(self._solution)
        return "eval:{} {}".format(self._problem.nb_evaluations, sol_str )

 
class ManySolutionAlgorithm(Algorithm) :

    """ Classe Abstraite représentant un algorithme a une population """
    
    def __init__(self, prob, options):
    
        Algorithm.__init__(self, prob, options)
    
        # lecture des paramètres éventuels 
        self._mu = options.get('mu', 5 )
        self._lambda = options.get('lambda', 10 )

        # Création et évaluation de la population initiale
        self._pop = [ self._problem.generate_initial_solution(sol_type='random')
                      for i in range(self._mu) ]
              
        eval_solutions(self._pop, self._problem)

        # utiles pour la méthode print_dist
        self._max_ever = self.max_value = float("-inf")
        self._min_ever = self.min_value = float("inf")
        
        self.update_stats( self._pop )
        
    def update_stats(self, pop):
        """
        Mise à jours des statistique de la population. La meilleure solution 
        est mise à jour ainsi que les valeurs de fitness maximun, minimum, 
        et moyenne.

        Entrée : une population de solution 

        Note : cette population a déjà été évaluée 
        """
        vals = [ x.value for x in pop ]
        
        self.min_value = min(vals)
        self.max_value = max(vals)
        self.ave_value = np.average(vals)

        if self.max_value > self._max_ever:
            self._max_ever = self.max_value
        if self.min_value < self._min_ever:
            self._min_ever = self.min_value
        
        
        # on enregistre la meilleure solution trouvée
        if self._problem.maximize :
            self._best_solution = pop[np.argmax(vals)].clone()
        else:
            self._best_solution = pop[np.argmin(vals)].clone()

    def print_step(self):
        """ retourne des infos sur l'itération  """
        return "eval:{} val:{} max:{} min:{} [{}]".format(
            self._problem.nb_evaluations,
            self.ave_value, self.max_value, self.min_value,
            self._print_dist())
    
    def _print_dist(self):
        """ Pour afficher graphiqument les stats """
        
        l = 20
        dist=list('.'*(l+2))
        if is_finite( [  self._max_ever, 
                         self._min_ever, 
                         self.max_value, 
                         self.min_value, 
                         self.ave_value ] ): 
            
            a = 0
            b = 0
            if self._max_ever-self._min_ever != 0:
                a = l/(self._max_ever-self._min_ever) 
                b = - (l*self._min_ever)/(self._max_ever-self._min_ever) 
                
            idx_max = int(a*self.max_value + b)
            idx_ave = int(a*self.ave_value + b)
            idx_min = int(a*self.min_value + b)
            dist[idx_max] ='|'
            dist[idx_min] ='|'
            dist[idx_ave] ='|'
        
        return "".join(dist)        
