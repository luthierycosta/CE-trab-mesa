'''
import mesa Agent.
'''
from functools import reduce
from mesa import Agent, Model
from random import random

class ScientistAgent(Agent):
    '''
    doc Scientist Agent.
    '''
    def __init__(self, unique_id: int, model: Model, **args):
        super().__init__(unique_id, model)
        self.color = None
        vars(self).update(args)
        self.neighbors = []
    
    def __should_colaborate__(self, neighbor):
        """
        colorir ao colaborar
        """
        def normalize(value,old_min,old_max,new_min,new_max):
            return (new_max-new_min)/(old_max-old_min)*(value-old_max)+new_max

        normalize_age = lambda age: normalize(age,20,50,0,1)

        p = float(neighbor.organization["sigla"] == self.organization["sigla"]) +\
            float(neighbor.organization["cidade"] == self.organization["cidade"]) +\
            float(neighbor.area_of_interest == self.area_of_interest) +\
            float(normalize_age(abs(neighbor.age - self.age))) +\
            float(self.health / 100 if self.health > 20 else -3) -\
            float(self.financial_need)

        # print(f"""
        #     sigla={neighbor.organization["sigla"] == self.organization["sigla"]}
        #     cidade={neighbor.organization["cidade"] == self.organization["cidade"]}
        #     interesse={neighbor.area_of_interest == self.area_of_interest}
        #     idade={normalize_age(abs(neighbor.age - self.age))}
        #     saude={self.health / 100 if self.health > 20 else -3}
        #     financas={self.financial_need}
        #     p={p}
        # """
        # )
        return p * random() > 0.3

    def step(self):
        '''
        doc step.
        '''
        for sc in self.get_neighbors():
            if self.__should_colaborate__(sc):
                self.color = sc.color = '#00FF00'

    def get_neighbors(self):
        '''
        doc get_neighbors.
        '''
        if self.neighbors:
            return self.neighbors

        neighbors_nodes = self.model.grid.get_neighbors(self.pos, include_center=False)
        self.neighbors = filter(lambda s: s.unique_id in neighbors_nodes, self.model.scientists)

        return self.neighbors
