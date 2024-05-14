from search.solutions import BinarySolution
import random

class OperateurMutation:
    """ 
    Classe abstraite pour les opérateurs de mutation 
    """
    def __init__(self):
        self._type_mutation = 0

    def mutate(self, individu: BinarySolution) -> BinarySolution:
        """ 
        Mutation d'un individu.
        
        Entrée : une instance de la classe BinarySolution.
        Sortie : la solution modifiée
        """
        raise NotImplementedError
    
    def __str__(self):
        return f"type_mutation:{self._type_mutation}"
    

class MutationBitflip(OperateurMutation):
    """
    Opérateur de mutation bitflip.
    """
    def __init__(self):
        super().__init__()
        self._type_mutation = 1

    def mutate(self, individu: BinarySolution) -> BinarySolution:
        i = random.randint(0, len(individu.solution)-1 )
        individu.solution[i] = not individu.solution[i]
            
        return individu
    
class MutationUniform(OperateurMutation):
    """
    Opérateur de mutation uniforme.
    """
    def __init__(self):
        super().__init__()
        self._type_mutation = 2

    def mutate(self, individu: BinarySolution) -> BinarySolution:
        n = len(individu.solution)
        probabilite_mutation = 1/n
        for i in range(n):
            if random.random() < probabilite_mutation:
                individu.solution[i] = not individu.solution[i]

            
        return individu