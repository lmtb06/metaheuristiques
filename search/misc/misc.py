#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import numpy as np

import random

from .plots import *


def eval_solutions(pop, problem):
    """
    Evaluation d'une list de solutions sur un probleme 
        
    Entrée : une liste d'instances de la classe Solution
    Sortie : la liste des valeurs des solution 
     
    Note : les valeurs de fitness sont aussi stockés dans les solutions.

    Note : les solutions infeasable ont une fitness infini 
    """
        
    vals = [ problem.evaluate(x) for x in pop]
    feasable = [ problem.feasable(x) for x in pop ]

    for i in range(len(feasable)) :
        if not feasable[i] :
            vals[i] = float("inf")
            if problem.maximize :
                vals[i] = float("-inf")
        pop[i]._value = vals[i]
                    
    # retourne le tableau des valeur (suit le même ordre que pop)
    return vals
        
def sort_pop(pop, problem) : 
        """Trie la population par ordre de fitness pop[0] est la meilleure 
        solution 
        
        Entrée : une liste de solution evaluée.

        Note : le tri est fait en place 
        
        Sortie : pop est triée (modifiée) et idx contient les indices par 
        rapport a la population intiale (avant le tri)

        """
        
        if problem.maximize :
            idx = [i[0] for i in sorted(enumerate(pop),\
                                        key=lambda x:x[1].value, reverse=True)]
        else:
            idx = [i[0] for i in sorted(enumerate(pop),\
                                        key=lambda x:x[1].value)]
         
        srt_pop = [pop[i] for i in idx]
        pop[:] = srt_pop

        return idx

def is_finite(numbers):
    """
    Prend un liste de nombres, pour verifier s'ils ne sont pas infinit

    """
    for n in numbers :
        if n == float('inf') or n == float('-inf'):
            return False
    return True

def plot_by_evaluation(data, x, y, fname):
    """
    Dessine des courbes de valeurs de la solution courante vs. 
    nombre évaluations. Il y a une courbe par exécution.

    Abcisse :le nombre d'évaluations 
    Ordonnée : la valeur de la solution courante 
    """

    ax = start_figure()
    for d in data:
        ax.plot(d[x], d[y], lw=0.3, color="0.5")
    finish_figure(ax, fname, x, y)
    print("Generated run curves {}".format(fname))
    
def plot_by_final_solution(data, names, fname):
    """
    Dessine les distributions des valeurs des solutions finales de chaque 
    exécution. Autant de boites à moustaches que d'algorithmes testés.

    Ordonnée : la valeur de la solution finale 
    """

    ax = start_figure()
    plot_boxplot(ax, data, names)
    finish_figure(ax, fname, '', 'Value')
    print("Generated {} with boxplots for: {}".format(fname, ", ".join(names)))
    

def split_stat_line(line, extra_values=list()):
    """
    Découpe une ligne de statistique et retourne les valeur 
    itération, évaluations, valeur, sous forme de dictionnaire,

    note les valeur intéressantes sont dans : watched_values

    Ex. si la ligne contient :  "... iter:3 eval:420 val:79.0 ... "
    le valeur retournées sont : {'iter':3, 'eval':420, 'val':79.0 }

    Prend un string
    Retourne un dict 
    
    """

    watched_values = ['eval', 'val', 'iter']
    watched_values.extend(extra_values)
    
    data = dict()
    for d in line.split() :
        for k in  watched_values:
            if d.startswith(k) :
                data[k] = float(d.split(':')[1])
    return data



def run_algorithm(algo, max_iter, extra_stats=list(), screen_output=True) :
    """
    Lance une instance d'un algorithme de recherche et retourne 
    ses resultas.
   
    prend :
       algo : une instance de la classe Algorithme 
       max_iter : entier le nombre d'itération maximum
       screen : booléen pour afficher ou non une ligne de stat par itération 

    retourne :
       un entier : le nombre d'itérations consomé
       un tableau : chaque case contient un tuple 
          (itération, évaluation, valeur) cf. split_stat_line plus haut. Il y 
          a autant de case que d'itération 
    """
   
    stats = list()
    done = False
    it = 0

    # sauter une ligne 
    if screen_output :
        print()
        
    # tan que pas fini 
    while not done:
        it += 1
        
        # exécuter une itération de l'algorithme 
        finished = algo.step()

        # récupérer les statistiques sur la solution courante
        stat_line = "iter:{} {}".format(it, algo.print_step())
        stats.append( split_stat_line(stat_line, extra_values=extra_stats) )
        if screen_output :
            print ("\r\t"+stat_line+"\r", end="")
          
        # a-t-on fini ? Finished est modifiée par l'algorythme 
        done = it > max_iter or finished

    # sauter une ligne 
    if screen_output :
        print()
        print() 
        
    # retournons le nombre d'iteration consomés et les stats complètes
    stats_l = [ tuple(l.values()) for l in stats]
    dtype = dict(names=list(stats[0].keys()), formats=['f8'] * len(stats[0].keys()))

    return it, np.array(stats_l, dtype=dtype)


def multiple_runs(problem, algo_class_name,  max_iter, nb_runs, alg_options,
                  extra_stats=[], screen_output=True):
    """
    Exécute plusieurs fois un algorithme de recherche local sur un problème 
    donné. 

    Note : Un fichier de courbe avec les valeur des solutions courante est 
           créer a la fin de l'éxécution . Il a le nom de la classe de 
           l'algorithme et l'extension .png

    prend :
       problem : une instance de la classe problem 
       algo_class_name : le NOM DE LA CLASSE d'un algorithme 
       max_iter : entier le nombre d'itération maximum
       nb_runs : entier le nombre nombre d'exécutions
       extra_stats : une liste de noms de statistiques a sauvegarder pour 
                     les courbes par défaut c'est : 'val' 'iter', 'eval'
                     (c'est les noms affiché par Algorithm.print_step())

    retourne : 
       Un tuple 
            un tableau : avec toute les valeur des solution finale, autant que 
                         nb_runs
            le nom de l'algorithme : string, pour affichage
    """
  
    # Pour stocker les stat de sortie  
    iter_data = []   # les stats par iteration     
    final_data = []  # les stats finales, la meilleurs solution 
      
    for r in range(nb_runs) :

        # initialiser le problème 
        problem.reset()
        
        # instancier un algorithme avec le problem
        algorithm = algo_class_name( problem, alg_options )
        if r == 0:
            print ("Running {} on {} for {} runs [max eval {} or max iter {}]".\
                   format(algorithm.name, problem.name, nb_runs,
                          problem.max_eval, max_iter))
            
        # exécuter l'algorithme jusqua la fin et récupérer ses stats
        it, iter_stats = run_algorithm(algorithm, max_iter, \
                                       extra_stats=extra_stats,
                                       screen_output=screen_output)
           

        iter_data.append( iter_stats )

        # recuperons et affichons les stats de fin 
        final_stat = algorithm.print_final()
        final_data.append (split_stat_line(final_stat)['val']) # juste la valeur
        print ("Run {}, iter:{} {}".format(r, it, final_stat))

        # Si le probleme s'y prete, on dessine la solution 
        try : 
            s = algorithm.best_solution
            problem.draw_solution(s, "{}-{}-{}.png".format(problem.name,
                                                           algorithm.name,r))
        except NotImplementedError :
            pass # la solution ne se dessine pas, alors on ne fait pas 
            

    # Afficher une ligne pour séparer les affichages
    print ("-"*80)

    # Réaliser les courbes pour chaque exécution
    plot_by_evaluation(iter_data, 'eval', 'val',\
                       "{}-{}.png".format(algorithm.name, 'val'))
    for s_name in extra_stats :
        try : 
            plot_by_evaluation(iter_data, 'eval', s_name,\
                               "{}-{}.png".format(algorithm.name, s_name))
        except ValueError :
            pass
    
    # retourner les valeur des solution final et le nom de l'algorithme 
    return np.array(final_data), algorithm.name

