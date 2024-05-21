from instances import *
from search import *
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed
import multiprocessing
import os

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

def multiple_runs(problem, algo_class,  max_iter, nb_runs, alg_options,
                  extra_stats=[], screen_output=True):
    """
    Lance plusieurs fois un algorithme de recherche pour un problème donné et retourne les statistiques
    de chaque exécution.
    
    "stats": [
        dataframe avec les statistiques de chaque exécution
    ]
    """
    stats =  pd.DataFrame()

    for i in range(nb_runs):
        # initialiser le problème 
        problem.reset()

        # instancier un algorithme avec le problem
        algorithm = algo_class( problem, alg_options )
        if i == 0:
            print ("Running {} on {} for {} runs [max eval {} or max iter {}]".\
                   format(algorithm.name, problem.name, nb_runs,
                          problem.max_eval, max_iter))

        nb_iterations , stats_run = run_algorithm(algorithm, max_iter, extra_stats, screen_output)
        stats_run = pd.DataFrame(stats_run)
        stats_run['run'] = i
        stats = pd.concat([stats, stats_run], axis=0)
        # Si le probleme s'y prete, on dessine la solution 
        try : 
            s = algorithm.best_solution
            
            problem.draw_solution(s, f"data/{algorithm.name}-{problem.name}-solution.png")
        except NotImplementedError :
            pass # la solution ne se dessine pas, alors on ne fait pas 

    return stats

def execute_multiple_algo_on_problem_sequentialy(problem_name, algo_list, max_iter_list, nb_runs_list, algo_options_list, extra_stats_list, verbose_list, all_problems):
    """
    Exécute plusieurs algorithmes sur un problème donné et génère des statistiques pour chaque algorithme de façon séquentielle.
    resultat: un dictionnaire avec les statistiques pour chaque algorithme
    """
    problem = all_problems[problem_name]  # Charger l'instance de problème
    stats = {}  # Pour stocker les statistiques pour chaque algorithme
    
    for i, algo_class in enumerate(algo_list):
        algo_stats = multiple_runs(problem,
                                    algo_class,
                                    max_iter_list[i],
                                    nb_runs_list[i],
                                    algo_options_list[i],
                                    extra_stats=extra_stats_list[i],
                                    screen_output=verbose_list[i])
        stats.update({algo_class.__name__: algo_stats})

    return stats

def execute_multiple_algo_on_problem_concurrently(problem_name, algo_list, max_iter_list, nb_runs_list, algo_options_list, extra_stats_list, verbose_list, all_problems):
    """
    Exécute plusieurs algorithmes sur un problème donné en utilisant des threads concurrents et génère des statistiques pour chaque algorithme.
    resultat: un dictionnaire avec les statistiques pour chaque algorithme
    """
    problem = all_problems[problem_name]  # Charger l'instance de problème
    
    stats = {}  # Pour stocker les statistiques pour chaque algorithme
    print(f"{multiprocessing.current_process().name} is working on {problem_name}")
    # Créer un pool de threads pour exécuter les algorithmes en parallèle
    with ThreadPoolExecutor() as executor:
        futures = {}
        for i, algo_class in enumerate(algo_list):
            # Lancer l'exécution de l'algorithme dans un thread séparé
            future = executor.submit(multiple_runs, problem, algo_class, max_iter_list[i], nb_runs_list[i], algo_options_list[i], extra_stats_list[i], verbose_list[i])
            futures[future] = algo_class.__name__  # Stocker le future avec le nom de l'algo comme clé
        
        for future in as_completed(futures):
            algo_name = futures[future]  # Récupérer le nom de l'algorithme à partir du future
            # try:
            stats[algo_name] = future.result()
            stats[algo_name]['algo'] = algo_name
            stats[algo_name]['problem'] = problem_name
            # except Exception as e:
            #     print(f"{multiprocessing.current_process().name}: Error while executing {algo_name} on {problem_name}: {e}")

    return stats

def execute_algos_on_problems_concurrently(problem_name_list, algo_list, max_iter_list, nb_runs_list, algo_options_list, extra_stats_list, verbose_list, all_problems):
    """
    Exécute plusieurs algorithmes sur une liste de problèmes en utilisant des processus concurrents pour chaque problème et dans chaque processus, exécute les algorithmes en utilisant des threads concurrents.
    Le résultat est un dictionnaire avec les statistiques pour chaque algorithme et chaque problème.
    """
      
    stats = {}
    # Exécute les algorithmes sur la liste des problèmes en utilisant des processus concurrents.
    nb_process_max = os.cpu_count()
    with ProcessPoolExecutor(max_workers=nb_process_max) as executor:
        futures = {}
        for problem_name in problem_name_list:
            # Lancer l'exécution des algorithmes dans un processus séparé
            future = executor.submit(
                execute_multiple_algo_on_problem_concurrently,
                problem_name,
                algo_list,
                max_iter_list,
                nb_runs_list,
                algo_options_list,
                extra_stats_list,
                verbose_list,
                all_problems
            )
            futures[future] = problem_name
        
        for future in as_completed(futures):
            problem_name = futures[future]
            stats[problem_name] = future.result()
    return stats

def go_variation(problem_name, algo_class, param_var, max_iter, nb_runs, algo_opt_base, extra_stats, verbose, probleme_size, all_problems):
    """
    Exécute un algorithme avec différentes valeurs d'un paramètre spécifique et utilise plot_by_final_solution pour générer un plot des performances.

    :param problem_name: Nom du problème à résoudre.
    :param algo_class: Classe de l'algorithme à exécuter.
    :param param_name: Nom du paramètre à varier.
    :param param_values: Liste des valeurs à tester pour le paramètre.
    :param max_iter: Nombre maximum d'itérations par exécution de l'algorithme.
    :param nb_runs: Nombre d'exécutions pour chaque valeur du paramètre.
    :param algo_opt_base: Options de base pour l'algorithme (dictionnaire).
    :param extra_stats: Statistiques supplémentaires à collecter.
    :param verbose: Affichage détaillé des exécutions.
    :param probleme_size: Taille du problème ('small', 'medium', 'large', 'random').
    """
    (param_name, param_values) = param_var
    problem = all_problems[problem_name]  # Charger l'instance de problème
    algo_stats = []  # pour stocker les stats de toutes les variations
    algo_names = []  # pour les noms des configurations dans les courbes
    print(f"{multiprocessing.current_process().name} is working on {problem_name} with {param_name}")
    # Exécuter l'algorithme pour chaque valeur du paramètre
    for value in param_values:
        algo_opt = algo_opt_base.copy()
        algo_opt[param_name] = value  # Modifier la valeur du paramètre
        stats_list = []  # Pour stocker les stats pour chaque run
        name_suffix = f"{param_name}={value}"  # Nom unique pour chaque configuration
        
        # Exécuter l'algorithme nb_runs fois pour la valeur actuelle du paramètre
        for _ in range(nb_runs):
            stats, _ = multiple_runs(problem, algo_class, max_iter, 1, algo_opt, extra_stats=extra_stats, screen_output=verbose)
            stats_list.append(stats)
        
        algo_stats.append(stats_list)
        algo_names.append(name_suffix)

    # Utiliser plot_by_final_solution pour générer les boxplots des performances
    plot_by_final_solution(algo_stats, algo_names, f"boxplot-{problem_name}-{probleme_size}-{algo_class.__name__}-{param_name}-variations.png")

# Exemple d'utilisation :
# go_variation('knapsac', RandomLS, 'mu', [50, 100, 150], 5000, 30, {'lambda': 20, 'pc': 0.5, 'pm': 0.5, 'type_cdf': 'fitness', 's': 2}, [], False, 'small')

def execute_and_save_stats(
        problem_size='small',
        nb_exec = 1,
        max_evaluations=5000,
        max_iterations=1000,
        nb_runs=30,
        algo_options_lambda={},
        extra_stats=[],
        verbose=False,
        algo_list=[RandomLS],
        problems_name=['binval'], save=True):
    """
    Exécute les algorithmes sur les problèmes et sauvegarde les statistiques dans des fichiers CSV.
    """
    stats = []
    dfs = {}
    for i in range(nb_exec):
        all_problems = setup_problems(problem_size, max_evaluations)
        algo_options = {}
        for key, value in algo_options_lambda.items():
            algo_options[key] = value()
        stats.append(
            execute_algos_on_problems_concurrently(problems_name, algo_list, [max_iterations]*len(algo_list), [nb_runs]*len(algo_list), [algo_options]*len(algo_list), [extra_stats]*len(algo_list), [verbose]*len(algo_list), all_problems)
        )

        # Sauvegarde des statistiques
        if save:
            for problem_name, problem_stats in stats[i].items():
                for algo_name, algo_stats in problem_stats.items():
                    # ajoute un header si le fichier n'existe pas
                    nom_fichier = f"data/{algo_name}-{problem_name}-{problem_size}.csv"
                    exist = not os.path.exists(nom_fichier)
                    if not exist:
                        previous_stats = pd.read_csv(nom_fichier)
                        run = previous_stats['run'].max() + 1
                        algo_stats['run'] += run
                        algo_stats = pd.concat([previous_stats, algo_stats],ignore_index=True, sort=False)
                    algo_stats.to_csv(nom_fichier, mode='w', header=True, index=False)
        # Aggrégation des statistiques
        for problem_name, stat in stats[i].items():
            for algo_name, algo_stat in stat.items():
                dfs[algo_name] = pd.concat([dfs.get(algo_name, pd.DataFrame()), algo_stat])
                dfs[algo_name]['problem_size'] = problem_size
    return dfs

def get_stats_from_csv(algo_name:str, problems_name:list[str], problems_size:list[str]=['small', 'medium', 'large']):
    """
    Charge les statistiques à partir des fichiers CSV et les stocke dans un Pandas DataFrame.
    """
    data = pd.DataFrame()
    
    for problem_name in problems_name:
        for problem_size in problems_size:
            nom_fichier = f"data/{algo_name}-{problem_name}-{problem_size}.csv"
            if  os.path.exists(nom_fichier):
                new_data = pd.read_csv(nom_fichier,)
                new_data['problem_size'] = problem_size
                data = pd.concat([data, new_data], ignore_index=True, sort=False)
    return data