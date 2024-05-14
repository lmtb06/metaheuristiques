#! /usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np

import random
from .random_ga import RandomGA
from .operateur_croisement import  *
from .operateur_mutation import *
from .operateur_selection import *

class MuComaLambdaGA(RandomGA):

    def __init__ (self, prob, options) :
        """
        Entrées : 

        * Un problème donnée instance de la classe Problem.
        Seules les problèmes dont les solution sont des tableaus booléens sont 
        acceptée. 
        
        * Un dictionnaire des paramètres des algorithmes 

        """
        super().__init__(prob, options)
        self._pc = options.get('pc', 0.5)
        self._pm = options.get('pm', 0.5)
        self.setup_operateurs(options)

    def print_step(self):
        """ Retourne des infos sur l'itération
        """
        return f"{super().print_step()} pc:{self._pc} pm:{self._pm} {self._mutation_class} {self._xover_class} {self._population_selection_class.__str__().replace('type_selection:', 'type_selection_population:')}"

    def _setup_operateur_croisement(self, options):
        """
        Initialiser l'opérateur de croisement en fonction des options.
        type de croisement :
        - 'onepoint'
        - 'uniform'
        """
        type_xover = options.get('xover', 'onepoint')
        if type_xover == 'onepoint':
            self._xover_class = CroisementOnePoint()
        elif type_xover == 'uniform':
            self._xover_class = CroisementUniforme()
        else:
            raise ValueError("Unknown type of crossover")
    
    def _setup_operateur_mutation(self, options):
        """
        Initialiser l'opérateur de mutation en fonction des options.
        type de mutation :
        - bitflip
        - uniform
        """
        type_mutation = options.get('mutation', 'bitflip')
        if type_mutation == 'bitflip':
            self._mutation_class = MutationBitflip()
        elif type_mutation == 'uniform':
            self._mutation_class = MutationUniform()
        else:
            raise ValueError("Unknown type of mutation")
    def _get_cdf_class(self, options):
        """
        Retourne la class de fonction de distribution cumulative en fonction des options.
        cdf :
        - fitness
        - rank
        """
        type_cdf = options.get('cdf', 'fitness')
        if type_cdf == 'fitness':
            return CDFFitness(self._problem)
        elif type_cdf == 'rank':
            return CDFRang(self._problem, options.get('S', 2))
        else:
            raise ValueError("Unknown type of cdf function")

    def _setup_operateur_selection_population(self, options):
        """
        Initialiser l'opérateur de selection en fonction des options.
        type de selection :
        - aleatoire
        - deterministe
        - roulette
        - tournoi
        """
        type_selection = options.get('selection_population', 'aleatoire')
        if type_selection == 'aleatoire':
            self._population_selection_class = SelectionAleatoire(self._problem)
        elif type_selection == 'deterministe':
            n = options.get('n', self._mu)
            self._population_selection_class = SelectionDeterministe(self._problem, n)
        elif type_selection == 'roulette':
            cdf = self._get_cdf_class(options)
            self._population_selection_class = SelectionRoulette(self._problem, cdf)
        elif type_selection == 'tournoi':
            k = options.get('k', self._mu)
            self._population_selection_class = SelectionTournoi(self._problem, k)
        else:
            raise ValueError("Unknown type of selection method for parents")     
    
    def setup_operateurs(self, options):
        """
        Initialiser les opérateurs en fonction des options.
        """
        self._setup_operateur_croisement(options)
        self._setup_operateur_mutation(options)
        self._setup_operateur_selection_population(options)

    @property
    def name(self):
        return "µ,λ µ{}_λ{}_pc{}_pm{}".format(self._mu, self._lambda, self._pc, self._pm).replace('.',',')

    def evolve_pop(self):
        """
        Créer des nouvelles solution par evolution des parents. Les opérateurs 
        génétique son appliqué ici. 

        Entrée : une liste de parents (cf. make_parent_pop)
        Sortie : une liste de solutions enfants de taille self._lambda

        """
        offspring = []
        done = False
        while not done : 

            # on prend une solution 
            p1 = self._select_one_random ( self._pop )
            p2 = self._select_one_random ( self._pop )
            enfants = []
            # croisement avec probabilité pc
            if random.random() < self._pc :
                enfants = self._xover_class.xover(p1, p2)
            
            # mutation avec probabilité pm
            if random.random() < self._pm :
                for e in enfants:
                    self._mutation_class.mutate(e)
         
            # on rajoute a la liste les enfants
            offspring.extend(enfants)

            # si la population des enfants est remplie, on la retourne
            done = len(offspring) == self._lambda
            
        return offspring
    
    def print_final(self):
        return super().print_final() + " pc:{} pm:{}".format(self._pc, self._pm)

    def update_pop(self, offspring):
        """
        Constituer la nouvelle population selon une stratégie de selection 
        donnée depuis les enfants et self._pop.  

        Entrée : une liste de solutions enfants 
        Sortie : une liste de solutions de taille self._mu

        """
        new_pop = self._population_selection_class.select(offspring, self._mu)
        
        return new_pop