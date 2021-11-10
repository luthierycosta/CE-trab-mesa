'''
import mesa Agent.
'''
from mesa import Agent, Model
from random import randrange, random
from enum import Enum

class ScientistState(Enum):
    '''
    Estados do cientista.
    '''
    WILLING = 1
    COLLABORATING = 2
    COORDINATING = 3
    UNAVAILABLE = 4


class ScientistAgent(Agent):
    '''
    Classe do agente cientista.
    '''
    def __init__(self, unique_id: int, model: Model, **args):
        '''
        Construtor do agente cientista.
        '''
        super().__init__(unique_id, model)
        self.color = None
        vars(self).update(args)
        # Cientistas vizinhos
        self.neighbors = []
        # Cientistas colaboradores
        self.collaborators = set()
        # Constante de variação de idade
        self.aging_months = 0
        # Estado inicial do cientista
        self.state = ScientistState.WILLING

    def __update_age__(self):
        '''
        Metódo de atualização da idade do cientista.
        '''
        self.aging_months += self.model.time_step
        if self.aging_months >= 12:
            self.age += 1
            self.aging_months -= 12

    def __update_health__(self):
        '''
        Método de atualização da saúde do cientista.
        '''
        self.health += randrange(-self.model.health_delta_factor, self.model.health_delta_factor+1)
        self.health = min(self.health, 100)
        self.health = max(self.health, 1)
        if self.health < 50:
            self.state = ScientistState.UNAVAILABLE
        else:
            self.state = ScientistState.WILLING

    def __update_financial_need(self):
        '''
        A cada passo, o cientista tem uma chance de 20% de mudar de necessidade financeira
        para um valor aleatório.
        '''
        if random() <= 0.2:
            self.financial_need = random()

    def __should_colaborate__(self, neighbor):
        '''
        Verifica os atributos do cientista atual e do cientista vizinho e informa se os cientistas devem colaborar.
        '''
        
        # Verificamos a Universidade, Cidade, Área de conhecimento, Área de Interesse, Idade, Necessidade financeira e Estado do agente
        # para indicar se o cientista deve ou não colaborar com outro.
        p = 1 * float(neighbor.organization["sigla"] == self.organization["sigla"]) +\
            1 * float(neighbor.organization["cidade"] == self.organization["cidade"]) +\
            2 * float(neighbor.area_of_interest["area"] == self.area_of_interest["area"]) +\
            2 * float(neighbor.area_of_interest["interesse"] == self.area_of_interest["interesse"]) +\
            2 * float(neighbor.state != self.state) +\
            2 * float(self.financial_need)

        return p >= 5.0

    def step(self):
        '''
        Passo do agente cientista.
        '''
        # No início do passo atualizamos a idade e saúde do cientista.
        self.__update_age__()
        self.__update_health__()
        self.__update_financial_need()
       
       # Para cada vizinho do cientista verificamos se o cientista deve colaborar com o seu vizinho.
        for id in self.get_neighbors():
            scientist = self.model.getScientist(id)
            # Se o cientista estiver indisponível não ele não colabora com seus vizinhos.
            # Se o vizinho estiver indisponível o cientista não colabora com ele.
            # Verificamos se o cientista deve colaborar utilizando nosso método. 
            # Caso seja positivo adicionamos ao conjunto de colaboradores do cientista o vizinho.
            if self.state is not ScientistState.UNAVAILABLE and\
                scientist.state is not ScientistState.UNAVAILABLE and\
                self.__should_colaborate__(scientist):
                self.collaborators.add(id)
            else:
                # Caso negativo removemos o vizinho de seu conjunto de colaboradores.
                self.collaborators.discard(id)

        self.state = self.__update_state__()

    def __update_state__(self):
        '''
        Método para a atualização do estado do cientista.
        '''
        if self.state == ScientistState.UNAVAILABLE:
            return ScientistState.UNAVAILABLE
        # Um cientista é um coordenador se possui pelo menos 3 ou mais colaboradores.
        if len(self.collaborators) >= 3:
            return ScientistState.COORDINATING
        elif self.collaborators:
            return ScientistState.COLLABORATING
        else:
            return ScientistState.WILLING


    def get_color(self):
        '''
        Método que retorna a cor de acordo com o estado do cientista.
        '''
        return {
            ScientistState.WILLING: '#FF0000',
            ScientistState.COLLABORATING: '#00FF00',
            ScientistState.COORDINATING: '#8F34EB',
            ScientistState.UNAVAILABLE: '#737373'
        }[self.state]

    def get_neighbors(self):
        '''
        Método que retorna os vizinhos do cientista.
        '''
        if self.neighbors:
            return self.neighbors

        neighbors_nodes = self.model.grid.get_neighbors(self.pos, include_center=False)
        self.neighbors = [s.unique_id for s in self.model.scientists if s.unique_id in neighbors_nodes]

        return self.neighbors
