#! /usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np

from search.solutions import BinarySolution
from search.problems import Problem

"""
La sous-classe de Problem pour les problemes de fonctions binnaires

OneMax, BinVal, LeadingOnes

Porblèmes de maximization, sans contraintes.

"""
class BinaryFunctionProblem(Problem) : 

    def __init__(self, size,  max_eval=1000):
        Problem.__init__(self, max_eval)
        self._size = size
        self._minimize = False
        
    def feasable(self, sol) :
        """ pas de contraintes """
        return True
          
    def print_solution(self, sol):
        """ Retourne la solution sous forme de string """
        
        if not isinstance(sol, BinarySolution):
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

        initial_solution = BinarySolution(dim=self._size)
        if sol_type == 'random':
            initial_solution = initial_solution.random()
        return initial_solution


"""
La sous-classe de Problem pour le OneMax

"""
class OneMax(BinaryFunctionProblem) : 

    def __init__(self, size,  max_eval=1000):
        BinaryFunctionProblem.__init__(self, size, max_eval)
        
    def evaluate(self, sol):
        """ 
        Retourne la valeur de la solution 
        
        Le nombre de un (vrai) dans la solution 
        """
        if not isinstance(sol, BinarySolution):
            raise TypeError("x must be a instance of BinarySolution")
    
        self.nb_evaluations += 1
        x = sol.solution
        val = len(np.where(x)[0])
        sol._value = val*1.0
        return sol._value


"""
La sous-classe de Problem pour le LeadingOnes

"""
class LeadingOnes(BinaryFunctionProblem) : 

    def __init__(self, size,  max_eval=1000):
        BinaryFunctionProblem.__init__(self, size, max_eval)
        
    def evaluate(self, sol):
        """
        Retourne la valeur de la solution 

        la longeur de la suite de 1 depuis le début de la solution   
        """
        if not isinstance(sol, BinarySolution):
            raise TypeError("x must be a instance of BinarySolution")
        
        self.nb_evaluations += 1
        x = sol.solution
        
        val = 0
        for i in range(len(x)):
            prod = int(x[i])
            for j in range(1, i):
                prod *= int(x[j])
            val += prod

        sol._value  = val*1.0
        return sol._value 
           
"""
La sous-classe de Problem pour le BinVal

"""
    
class BinVal(BinaryFunctionProblem) : 

    def __init__(self, size,  max_eval=1000):
        BinaryFunctionProblem.__init__(self, size, max_eval)
        
    def evaluate(self, sol):
        """ 
        Retourne la valeur de la solution  

        La valeur en décimal
        """
        if not isinstance(sol, BinarySolution):
            raise TypeError("x must be a instance of BinarySolution")
        
        self.nb_evaluations += 1
        x = np.array(sol.solution, dtype=np.int)
        
        val = 0
        for i in range(len(x)):
            val +=  x[i] << i
        sol._value = val*1.0
        return sol._value



"""
Factory pour generer des instances de OneMax

"""
        
def generate_binary_test_function_instance(function, prob_type, max_eval):
    """
    prend : prob_type : type 'small', 'medium', 'large'
    retourne : une instance de la classe OneMax

    """
    if function not in [OneMax, LeadingOnes, BinVal]:
        raise ValueError("Unknown binary function instance")
    
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
  
