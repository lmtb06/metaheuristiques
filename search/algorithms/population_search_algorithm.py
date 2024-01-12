#! /usr/bin/env python
# -*- coding: utf-8 -*-

from .algorithm import Algorithm, ManySolutionAlgorithm
from search.misc import eval_solutions

"""
Classe Abstraite représentant un algorithme de recherche a population

A chaque itération la population interne (self._pop) de taille self._mu  
est modifée et remplacée. 

La meilleure solution trouvée est mise à jour et accessible avec l'attribut 
best_solution.

Les classes concrètes doivent implanter les méthodes suivantes :

evolve_pop
make_new_pop

"""

class PopulationSearchAlgorithm(ManySolutionAlgorithm):

    def __init__ (self, prob, options) :
        """
        Crée la population initiale et l'évalue 
        
        Entrées : 

        * Un problème donnée instance de la classe Problem.
        * Un dictionnaire des paramètres des algorithmes 

        """

        # Initialisation de la partie héritée
        ManySolutionAlgorithm.__init__(self, prob, options)


    def evolve_pop(self):
        """
        Créer des nouvelles solution par evolution des parents (self._pop). 
   
        Sortie : une liste de solution enfants de taille self._lambda

        """
        raise NotImplementedError

    def update_pop(self, offspring):
        """
        Constituer la nouvelle population selon une stratégie de selection 
        donnée depuis les enfants et self._pop.  

        Entrée : une liste de solutions enfants 
        Sortie : une lisre de solutions de taille self._mu

        """
        raise NotImplementedError
     
    def step(self):

        # évolution et création des enfants 
        O = self.evolve_pop()
               
        # évaluation des enfants
        eval_solutions( O, self._problem)
               
        # remplacement des parents 
        self._pop = self.update_pop ( O )

        # mise a jour des statistiques
        self.update_stats( self._pop )
        
        return self.stop() 
        
    
   

    
 

