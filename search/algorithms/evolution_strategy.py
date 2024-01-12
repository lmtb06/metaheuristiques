#! /usr/bin/env python
# -*- coding: utf-8 -*-

from .algorithm import OneSolutionAlgorithm

"""
Classe Abstraite représentant une stratégie d'evolution générique 

Les classes concrètes doivent implanter les méthodes suivantes :

sample_solutions
update_sigma
update_m

"""

class EvolutionStrategy(OneSolutionAlgorithm):

    def __init__(self, prob, options):
        """
        Initialise une solution aléatoire 
        
        Entrées : 

        * Un problème donnée instance de la classe Problem.
        * Un dictionnaire des paramètres des algorithmes 

        """

        # Initialisation de la partie héritée
        
        OneSolutionAlgorithm.__init__(self, prob, options)

        # lecture des paramètres éventuels (valeurs par défaut si absentes)
       
        self._mu     = options.get('mu', 5 )
        self._lambda = options.get('lambda', 10 )
        self._sigma  = options.get('sigma', 1.0 )
     
    def sample_solutions(self):
        """ 
        Échantillonage depuis une distribution normale autour de la solution 
        courante (moyennne) et self._sigma comme variance. 
        
        Retourne une liste de Lambda solutions évaluée et triée
        """
        raise NotImplementedError

    def update_sigma(self, sample):
        """ 
        Mise à jour du pas de mutation sigma (variance) selon une règle donnée.

        Entrées :

        * l'échantillon de lambda solutions 

        """
        raise NotImplementedError

    def update_m(self, sample):   
        """
        Mise à jour de la moyenne (solution courrante) de la distribution

        Entrées :

        * l'échantillon de lambda solutions 

        """
        raise NotImplementedError

    def print_step(self):
        """ retourne des infos sur l'itération  """        
        step_data = OneSolutionAlgorithm.print_step(self)
        
        # on ajoute la valeur de sigma a la ligne pour en faire un courbe
        
        return "{} sig:{}".format(step_data, self._sigma)
    
    def step(self):
        """ 
        Une itération de l'algorithme 

        """ 

        # Echantillonage de solutions 
        S = self.sample_solutions()
              
        # Mis a jour des parammetre de la distribution
        self.update_sigma( S )
        
        self.update_m( S )
                
        # mise a jour des statistiques
        self.update_stats()
        
        return self.stop() 
        
    
    
