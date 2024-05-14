#! /usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np

from search.solutions import RealSolution
from search.problems import Problem


"""
La sous-classe de Problem pour les problemes de fonctions continues

Sphere, Tablet, Sharp Ridge, Rosenbrock

Porblèmes de minimisation, sans contraintes.

"""
class ContinuousFunctionProblem(Problem) : 

    def __init__(self, size,  max_eval=1000):
        Problem.__init__(self, max_eval)
        self._size = size
        self._name = "Generic continuous function "
        self._minimize = True
        
    def feasable(self, sol) :
        """ pas de contraintes """
        return True
    
    def print_solution(self, sol):
        """ Retourne la solution sous forme de string """
        
        if not isinstance(sol, RealSolution):
            raise TypeError("x must be a instance of Solution")
        
        self.nb_evaluations -= 1 # on ne compte cette evaluation
        self.evaluate(sol)
        return "val:{} sol:{}".format(sol.value, str(sol))

    def generate_initial_solution(self, sol_type='empty'):
        """ 
        Genérer une solution initial vide ou aléatoire 
        Retourne une instance de BinarySolution
        
        """
        if sol_type not in [ 'empty', 'random' ] :
            raise ValueError("Unknown inital solution type")

        initial_solution = RealSolution(dim=self._size)
        if sol_type == 'random':
            initial_solution = initial_solution.random()
        return initial_solution

"""
La sous-classe de Problem pour le OneMax

"""
    
class Rosenbrock(ContinuousFunctionProblem) : 

    def __init__(self, size,  max_eval=1000):
        ContinuousFunctionProblem.__init__(self, size, max_eval)
        self._name = "Rosenbrock"

    def evaluate(self, sol):

        if not isinstance(sol, RealSolution):
            raise TypeError("x must be a instance of RealSolution")
    
        self.nb_evaluations += 1
        x = sol.solution
        val=[100.*(x[i]**2-x[i+1])**2 +(1.-x[i])**2 for i in range(len(x)-1)]
        sol._value = sum(val)
        return sol._value


"""
La sous-classe de Problem pour le OneMax

"""
    
class Sphere(ContinuousFunctionProblem) : 

    def __init__(self, size,  max_eval=1000):
        ContinuousFunctionProblem.__init__(self, size, max_eval)
        self._name = "Sphere"

    def evaluate(self, sol):

        if not isinstance(sol, RealSolution):
            raise TypeError("x must be a instance of RealSolution")
    
        self.nb_evaluations += 1
        x = sol.solution
        val = sum((x + 0)**2)
        sol._value = val
        return sol._value

"""
La sous-classe de Problem pour SharpRidge

"""
   
class SharpRidge(ContinuousFunctionProblem) : 

    def __init__(self, size,  max_eval=1000):
        ContinuousFunctionProblem.__init__(self, size, max_eval)
        self._name = "SharpRidge"

    def evaluate(self, sol):

        if not isinstance(sol, RealSolution):
            raise TypeError("x must be a instance of RealSolution")
    
        self.nb_evaluations += 1
        x = sol.solution
        val = -x[0]
        val += 100. * np.sqrt(sum([ x[i]**2 for i in range(1,len(x))]))
        sol._value = val
        return sol._value

"""
La sous-classe de Problem pour Tablet

"""
    
class Tablet(ContinuousFunctionProblem) : 

    def __init__(self, size,  max_eval=1000):
        ContinuousFunctionProblem.__init__(self, size, max_eval)
        self._name = "Tablet"

    def evaluate(self, sol):

        if not isinstance(sol, RealSolution):
            raise TypeError("x must be a instance of RealSolution")
    
        self.nb_evaluations += 1
        x = sol.solution
        val = 1e6*x[0]**2
        val += sum([ x[i]**2 for i in range(1,len(x))])
        sol._value = val
        return sol._value



"""
Factory pour generer des instances de OneMax

"""
        
def generate_continuous_test_function_instance(function, prob_type, max_eval):
    """
    function : le nom de la classe de la fonction 
    prend : prob_type : type 'small', 'medium', 'large'
    max_eval : nombre d'evaluation maximum 

    retourne : une instance de la classe OneMax

    """
    if function not in [Rosenbrock, Sphere, SharpRidge, Tablet]:
        raise ValueError("Unknown continuous function instance")
    
    if prob_type not in ['small', 'medium', 'large'] :
        raise ValueError("Unknown prob_type instance")
    
    size = 0
    if prob_type == 'small' :
        size = 10
    elif prob_type == 'medium' :
        size = 30
    elif prob_type == 'large' :
        size = 100

    return function(size=size, max_eval=max_eval)
        
