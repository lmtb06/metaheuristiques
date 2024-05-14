from search import BinarySolution, sort_pop, eval_solutions, is_finite, Problem
import random, math

class CDF:
    """
    Classe pour créer une fonction de distribution cumulée.
    """
    def __init__(self, problem: Problem):
        self._problem = problem
        self._type_cdf = 0
    
    def get_proba(self, population: list[BinarySolution]) -> list[float]:
        """ 
        Crée une liste de probabilité associée à la population.
        
        Entrée : une liste d'instances de la classe BinarySolution.
        Sortie : une liste de probabilité associée à la population.
        """
        raise NotImplementedError
    
    def type_cdf(self):
        return self._type_cdf

    def create_cdf(self, population: list[BinarySolution]) -> list[float]:
        """
        Crée une fonction de distribution cumulée associée à la population.
        """
        proba = self.get_proba(population)
        cdf = [proba[0]]
        for i in range(1, len(proba)):
            cdf.append(cdf[i-1] + proba[i])
        return cdf
    
class CDFFitness(CDF):
    """
    Crée une fonction de distribution cumulée basée sur les fitness.
    """
    def __init__(self, problem: Problem):
        super().__init__(problem)
        self._type_cdf = 1

    def get_proba(self, population: list[BinarySolution]) -> list[float]:
        # La manière dont on calcul la probabilité dépend de si on cherche à maximiser ou minimiser
        if self._problem.maximize:
            somme = sum([x.value for x in population if is_finite(x.value)]) # on ne prend pas en compte les valeurs infinies
            probabilites = [x.value/somme if is_finite(x.value) else 0 for x in population] # on ne prend pas en compte les valeurs infinies les probabilités sont nulles
        else:
            somme = sum([1/x.value for x in population if is_finite(x.value)]) # on ne prend pas en compte les valeurs infinies
            probabilites = [((1 / x.value)/somme) if is_finite(x.value) else 0 for x in population]

        return probabilites
    
class CDFRang(CDF):
    """
    Crée une fonction de distribution cumulée basée sur les rangs.
    """
    def __init__(self, problem: Problem, s: float):
        super().__init__(problem)
        self._s = s
        self._type_cdf = 2

    def get_proba(self, population: list[BinarySolution]) -> list[float]:
        # A chaque individu on associe un rang
        rangs = sort_pop(population.copy(), self._problem)
        taille = len(population)
        # On calcule les probabilités en fonction des rangs ici le meilleur individu a un rang de 0 donc on inverse les rangs dans la formule
        probabilites = [
            ((2 - self._s) / taille) + 2 * ((taille - i - 1) - 1) * (self._s - 1) / (taille * (taille - 1)) for i in rangs]
        return probabilites

class OperateurSelection:
    """ 
    Classe abstraite pour les opérateurs de selection de parents
    """
    def __init__(self, problem: Problem):
        self._problem = problem
        self._type_selection = 0
        self._type_cdf = 0

    def select(self, population: list[BinarySolution], n: int) -> list[BinarySolution]:
        """ 
        Selection d'un individu pour être parent parmi la population.
        
        Entrée : une liste d'instances de la classe BinarySolution.
        Sortie : une liste de taille n d'instances de la classe BinarySolution sélectionnées.
        """
        raise NotImplementedError
    
    def __str__(self):
        return f"type_selection:{self._type_selection} type_cdf:{self._type_cdf}"
    
class SelectionAleatoire(OperateurSelection):
    """
    Opérateur de selection aléatoire.
    """
    def __init__(self, problem: Problem):
        super().__init__(problem)
        self._type_selection = 1

    def select(self, population: list[BinarySolution], n: int) -> list[BinarySolution]:
        """
        Selectionne n individus de la population de manière aléatoire. Avec remise.
        """
        return random.choices(population, k=n)
    
class SelectionDeterministe(OperateurSelection):
    """
    Opérateur de selection déterministe.
    Selectionne les n meilleurs individus de la population.
    """
    def __init__(self, problem: Problem, n: int):
        super().__init__(problem)
        self._type_selection = 2
        self._n = n

    def select(self, population: list[BinarySolution], n: int) -> list[BinarySolution]:
        sort_pop(population, self._problem)
        return [x.clone() for x in population[:n]]
    
class SelectionRoulette(OperateurSelection):
    """
    Opérateur de selection par méthode de la roulette.
    """
    def __init__(self, problem: Problem, CDF: CDF):
        super().__init__(problem)
        self._type_selection = 3
        self._CDF = CDF
        self._type_cdf = CDF.type_cdf()


    def select(self, population: list[BinarySolution], n: int) -> list[BinarySolution]:
        cdf = self._CDF.create_cdf(population)
        return random.choices(population, cum_weights=cdf, k=n)

class SelectionTournoi(OperateurSelection):
    """
    Opérateur de selection par méthode du tournoi.
    #TODO
    """
    def __init__(self, problem: Problem, k: int):
        super().__init__(problem)
        self._k = k
        self._type_selection = 4

    def select(self, population: list[BinarySolution], n: int) -> list[BinarySolution]:
        return [self._tournoi(population) for _ in range(n)]

    def _tournoi(self, population: list[BinarySolution]) -> BinarySolution:
        participants = random.sample(population, self._k)
        for participant in participants:
            # On évalue les participants si ce n'est pas déjà fait
            if not participant.value:
                participant.value = self._problem.evaluate(participant)
        return sort_pop(participants, self._problem)[0].clone()