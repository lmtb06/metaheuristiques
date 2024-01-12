#! /usr/bin/env python
# -*- coding: utf-8 -*-
from .algorithm import OneSolutionAlgorithm

"""
Classe Abstraite représentant un algorithme de recherche local générique 


Les classes concrètes doivent implanter les méthodes suivantes :

get_neighbors
filter_neighbors
select_next_solution
accept

"""

class LocalSearchAlgorithm(OneSolutionAlgorithm):

    def __init__(self, prob, options):
        """ 
        Initialise une solution aléatoire

        Entrées : 

        * Un problème donnée instance de la classe Problem.
        * Un dictionnaire des paramètres des algorithmes 

        """

        # Initialisation de la partie héritée
        OneSolutionAlgorithm.__init__(self, prob, options)

        # lecture des paramètres éventuels 
        # RAS ici
        
    def get_neighbors(self):
        """
        Retourne la liste des solutions voisines de la solution courante
        retourne une liste de d'instances de Solution
        """
        raise NotImplementedError

        
    def filter_neighbors(self, neighbors):
        """
        Elemine les solutions voisines non valides.
        Dépend du probleme et de l'algo 
        
        prend une liste d'instances de Solution 
        retourne une liste de d'instances de Solution
        """
        raise NotImplementedError
     
    def select_next_solution(self, candidates):
        """
        Retourne une solutions, peut-être pas.
        Dépend du probleme et de l'algo 
        
        prend une liste d'instances de Solution 
        retourne une instances de Solution ou None si pas de solution
        """
        raise NotImplementedError
    
    def accept(self, new_solution) :
        """
        Accepte ou pas la nouvele solution.
        Dépend du probleme et de l'algo 
        
        prend une instance de Solution 
        retourne un booléen, acepter / refusé 
        """
        raise NotImplementedError
        
    def step(self) :
        """ 
        Réalise une iteration 
        retourne booleen vrai si fin, faut sinon 
        """
        # se préparer a arrêter
        self._stop = True

        # générer les voisin de la solution courante 
        N = self.get_neighbors()

        # éliminer touts les voisins non feasable (dépend du problème)
        S = self.filter_neighbors(N)

        # choir une solution parmis les voisins
        s = self.select_next_solution(S)

        # accepter ou non la solution 
        if s is not None and self.accept(s) :
            self._solution = s
            self._stop = False

        # mise a jour des statistiques
        self.update_stats()
        
        return self.stop() 
    
   
        
   
   
