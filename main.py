#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function

from instances import *
from search import *

def setup_problems(probleme_size, max_evaluations):
    
    return {

        # Espaces discrets
        
        'knapsac' : generate_knapsac_instance(
            probleme_size, max_evaluations), 
        'set_covering' : generate_set_covering_instance(
            probleme_size, max_evaluations),
        'tsp' : generate_tsp_instance(
            probleme_size, max_evaluations),

        # Fonction test discretes
        
        'onemax': generate_binary_test_function_instance(
            OneMax, probleme_size, max_evaluations),
        'leadingones' : generate_binary_test_function_instance(
            LeadingOnes, probleme_size, max_evaluations),
        'binval' : generate_binary_test_function_instance(
            BinVal, probleme_size, max_evaluations),

        # Expace continus (fonctions test)
    
        'sphere' : generate_continuous_test_function_instance(
            Sphere, probleme_size, max_evaluations),
        'rosenbrock' : generate_continuous_test_function_instance(
            Rosenbrock, probleme_size, max_evaluations),
        'sharpridge' : generate_continuous_test_function_instance(
            SharpRidge, probleme_size, max_evaluations),
        'tablet' : generate_continuous_test_function_instance(
            Tablet, probleme_size, max_evaluations),    
    }
   
    
def go(problem, algo_list, max_iter, nb_runs, algo_opt, extra_stats, verbose):

    """  
    Exécution de tous les algorithmes avec les reglages choisis 
    
    """
    algo_stats = [] # pour stocker les stats
    algo_names = [] # pour les courbes

    # chaque algorithme de la liste est exécuté nb_runs fois 
    
    for algo_class in algo_list :
        stats, name = multiple_runs(problem,
                                    algo_class,
                                    max_iter,
                                    nb_runs,
                                    algo_opt,
                                    extra_stats=extra_stats,
                                    screen_output=verbose)
        algo_stats.append( stats )
        algo_names.append( name )
   
    # Génération des courbes finales 
   
    plot_by_final_solution(algo_stats, algo_names, 'boxplots.png' )
    
      

if __name__ == '__main__':

    #
    # Choix des aramètre globaux, a modifier selon la taille des problèmes  
    ############################################################# 
    
    probleme_size   = 'medium' # 'small', 'medium', 'large' or 'random'
     
    max_evaluations = 5000  # Les critères d'arrêt 
    max_iterations  = 5000
   
    nb_runs         = 30    # le nombre d'exécution de chaque algorithme

    verbose         = False # True = affichage par iteration (plus lent)


    #
    # choix des algorithme et des paramètre 
    ############################################################################
    
    algo_list = [    # Liste des algorithmes lancés (le nom des classes)
        RandomLS,
    ]

    algo_options = { # Paramètres spécifiques aux algorithmes. Ce dictionnaire 
        'mu' : 5,    # est passé aux constructeurs de l'algorithme 
        'lambda' : 10,
    }
    
    extra_stats = [  # Liste des chose à afficher à l'écran
        'sig',       # a remplir en fonction de l'affichage de l'algorithme  
    ]                # (il faut surcharger la print_step dans l'agorithme)    
                     # cf. split_stat_line dans seach/misc/misc.py
                         

                     
    #
    # Choix du problem à resoudre (voir la liste en haut de ce fichier)
    ############################################################################
    all_problems = setup_problems(probleme_size, max_evaluations) # la liste complète 
    
    problem = all_problems ['knapsac']
    
     
    #
    # Lancer 
    ############################################################################
    
    go(problem, algo_list, max_iterations, nb_runs, algo_options,
       extra_stats, verbose)
