#! /usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np

import random
from .random_ga import RandomGA
from search import PopulationSearchAlgorithm, BinarySolution, sort_pop, eval_solutions

class MuComaLambdaGA(RandomGA):

    def __init__ (self, prob, options) :
        """
        Entrées : 

        * Un problème donnée instance de la classe Problem.
        Seules les problèmes dont les solution sont des tableaus booléens sont 
        acceptée. 
        
        * Un dictionnaire des paramètres des algorithmes 

        """
        self.__init__(prob, options)
        self._pc = options.get('pc', 0.5)
        self._pm = options.get('pm', 0.5)
        self.setup_operateurs(options)

    def print_step(self):
        """
        Retourne une chaîne de caractères décrivant l'état courant de l'algorithme.
        lambda : taille de la population d'enfants (entier)
        mu : taille de la population de parents (entier)
        pc : probabilité de croisement (réel entre 0 et 1)
        pm : probabilité de mutation (réel entre 0 et 1)
        type_cdf : type de fonction de distribution cumulative (0 : fitness, 1 : rang)
        mutation : type de mutation (0 : bitflip, 1 : uniforme)
        xover : type de croisement (0 : un point, 1 : uniforme)
        selection : type de sélection (0 : déterministe, 1 : proportionnelle, 2 : roulette, 3 : tournoi)
        S : paramètre de la sélection par rang (entier)
        """
        # Commencez par appeler la méthode de la classe parente et initialisez la chaîne de caractères
        output = super().print_step()

        # Ajoutez chaque attribut à la chaîne de sortie s'il est défini (c'est-à-dire non None)
        if hasattr(self, '_pc') and self._pc is not None:
            output += f" pc:{self._pc}"
        if hasattr(self, '_pm') and self._pm is not None:
            output += f" pm:{self._pm}"
        if hasattr(self, '_type_cdf') and self._type_cdf is not None:
            output += f" type_cdf:{self._type_cdf}"
        if hasattr(self, '_mutation') and self._mutation is not None:
            output += f" mutation:{self._mutation}"
        if hasattr(self, '_xover') and self._xover is not None:
            output += f" xover:{self._xover}"
        if hasattr(self, '_selection') and self._selection is not None:
            output += f" selection:{self._selection}"
        if hasattr(self, '_S') and self._S is not None:
            output += f" S:{self._S}"

        return output

    def _setup_operateur_croisement(self, options):
        """
        Initialiser l'opérateur de croisement en fonction des options.
        type de croisement :
        - 0 : un point
        - 1 : uniforme
        """
        self._xover = options.get('xover', 0)
        if self._xover == 0:
            self._fonction_xover = self._xover_one_point
        elif self._xover == 1:
            self._fonction_xover = self._xover_uniform
        else:
            raise ValueError("Unknown type of crossover function")
    
    def _setup_operateur_mutation(self, options):
        """
        Initialiser l'opérateur de mutation en fonction des options.
        type de mutation :
        - 0 : bitflip
        - 1 : uniforme
        """
        self._mutation = options.get('mutation', 0)
        if self._mutation == 0:
            self._fonction_mutation = self._mutation_bitflip
        elif self._mutation == 1:
            self._fonction_mutation = self._mutation_uniform
    
    def _setup_operateur_selection(self, options):
        """
        Initialiser l'opérateur de selection en fonction des options.
        type de selection : 
        - 0 : deterministe
        - 1 : proportionnelle
        - 2 : roulette
        - 3 : tournoi
        """
        self._selection = options.get('selection', 0)
        if self._selection == 0:
            self._fonction_selection = self._select_n_best
        elif self._selection == 1:
            self._setup_selection_proportionnelle(options)
        elif self._selection == 2:
            self._fonction_selection = self._select_roulette
        elif self._selection == 3:
            self._fonction_selection = self._select_tournoi
        else:
            raise ValueError("Unknown type of selection function")   
        
    
    def _setup_selection_proportionnelle(self, options):
        """
        Initialiser la selection proportionnelle en fonction des options.
        """
        self._fonction_cdf = self._generate_cdf_function(options)
        self._fonction_selection = self._select_roulette
    
    def _setup_selection_deterministe(self, options):
        """
        Initialiser la selection deterministe en fonction des options.
        """
        def select_n_best(pool):
            """
            Retourne la fonction de sélection des n meilleurs solutions dans la population.
            """
            return self._select_n_best(pool, self._mu)
        
        return select_n_best

    def _setup_selection_tournoi(self, options):
        """
        Initialiser la selection par tournoi en fonction des options.
        """
        def select_tournoi(pool):
            """
            Sélectionne n individu dans la population en utilisant la méthode du tournoi
            """
            pool = pool.copy()
            selection = []
            if len(pool) < k:
                raise ValueError("La taille de la population est inférieure à la taille du tournoi")
            
            while len(selection) < self._mu:
                preselection = random.sample(pool, k)
                eval_solutions(preselection, self._problem)
                selection.append(preselection[0])
                pool.remove(preselection[0])
            return selection

        k = options.get('k', self._mu)
        return select_tournoi

    def setup_operateurs(self, options):
        """
        Initialiser les opérateurs en fonction des options.
        """
        self._setup_operateur_croisement(options)
        self._setup_operateur_mutation(options)
        self._setup_operateur_selection(options)

    @property
    def name(self):
        return "µ,λ µ{}_λ{}_pc{}_pm{}".format(self._mu, self._lambda, self._pc, self._pm).replace('.',',')

    def make_parent_pop(self):
        """
        Créer la population de parents. 
        """
        
        return self._select_n_best(self._pop, self._mu)

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
            
            # croisement avec probabilité pc
            if random.random() < self._pc :
                p1, p2 = self._xover_one_point(p1, p2)
            
            # mutation avec probabilité pm
            if random.random() < self._pm :
                p1 = self._mutation_bitflip( p1 )
                p2 = self._mutation_bitflip( p2 )
         
            # on rajoute a la liste
            offspring.append(p1)
            offspring.append(p2)

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
        new_pop = self._select_n_best(offspring, self._mu)
        
        return new_pop

    def _mutation_uniform(self, x):
        """
        Mutation uniforme d'une solution x. Chaque gene a une probabilité 
        1/len(x.solution) d'être modifié.
        """
        if not isinstance(x, BinarySolution) :
            raise TypeError("Algorithm only works on binary solution problems")
        
        n = len(x.solution)
        probabilite_mutation = 1.0/n
        for i in range(n):
            if random.random() < probabilite_mutation :
                x.solution[i] = not x.solution[i]

        return x

    def _xover_uniform(self, x1, x2):
        """
        Croisement uniforme de deux solutions x1 et x2. Chaque bit a une 
        probabilité 0.5 de venir de x1 ou x2.
        """
        if not (isinstance(x1, BinarySolution) and
                isinstance(x2, BinarySolution) ) :
            raise TypeError("Algorithm only works on binary solution problems!")
        
        x1 = x1.clone()
        
        for i in range(len(x1.solution)):
            if random.random() < 0.5 :
                x1.solution[i] = x2.solution[i]
        
        return x1

    def _generate_cdf_function(self, options):
        """
        Génère la fonction qui calcule la cumulative distribution function en fonction des options. (higher order function)
        type_cdf :
        - 0 : fitness
        - 1 : rank
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
                proba = (2 - self._S) / taille + 2 * rank * (self._S - 1) / (taille * (taille - 1))
                cdf.append(proba)
            # On calcule la somme cumulée des probabilités
            for i in range(1, len(cdf)):
                cdf[i] += cdf[i-1]
            return cdf

        self._type_cdf = options.get('type_cdf', 0)
        if self._type_cdf == 0:
            return cdf_using_fitness
        elif self._type_cdf == 1:
            self._S = options.get('S', 2)
            return cdf_using_rank
        else:
            raise ValueError("Unknown type of cdf function")

    def _select_roulette(self, pool):
        """
        Sélectionne n individu dans la population en utilisant la méthode de la roulette.
        Avec cdf la cumulative distribution function.
        """
        selection = []
        cdf = self._fonction_cdf(pool)
        s = 0
        while s < self._mu:
            r = random.random()
            i = 0
            while cdf[i] < r:
                i += 1
            selection.append(pool[i].clone())
            s += 1
        return selection
    
    def _select_tournoi(self, pool):
        """
        Sélectionne n individu dans la population en utilisant la méthode du tournoi.
        """
        selection = []
        taille = len(pool)
        for i in range(self._mu):
            idx = random.sample(range(taille), 2)
            if pool[idx[0]].value < pool[idx[1]].value:
                selection.append(pool[idx[0]].clone())
            else:
                selection.append(pool[idx[1]].clone())
        return selection
        