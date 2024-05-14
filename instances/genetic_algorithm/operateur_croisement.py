from search.solutions import BinarySolution
import random

class OperateurCroisement:
    """ 
    Classe abstraite pour les opérateurs de croisement 
    """
    def __init__(self):
        self._type_xover = 0

    def xover(self, parent1: BinarySolution, parent2: BinarySolution) -> list[BinarySolution]:
        """ 
        Croisement de deux parents.
        
        Entrée : deux instances de la classe BinarySolution.
        Sortie : une liste de solutions issue du croisement
        """
        raise NotImplementedError
    
    def __str__(self):
        return f"type_xover:{self._type_xover}"
    
class CroisementOnePoint(OperateurCroisement):
    """
    Opérateur de croisement en un point.
    """
    def __init__(self):
        super().__init__()
        self._type_xover = 1

    def xover(self, parent1: BinarySolution, parent2: BinarySolution) -> list[BinarySolution]:
        point = random.randint(0, len(parent1.solution)-1)

        for i in range(point, len(parent1.solution)):
            tmp = parent1.solution[i]
            parent1.solution[i] = parent2.solution[i]
            parent2.solution[i] = tmp
        return [parent1, parent2]
    
    
class CroisementUniforme(OperateurCroisement):
    """
    Opérateur de croisement uniforme.
    """
    def __init__(self):
        super().__init__()
        self._type_xover = 2

    def xover(self, parent1: BinarySolution, parent2: BinarySolution) -> list[BinarySolution]:
        n = len(parent1.solution)
        for i in range(n):
            if random.random() < 0.5:
                parent1.solution[i] = parent2.solution[i]

        return [parent1]