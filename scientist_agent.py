'''
import mesa Agent.
'''
from mesa import Agent, Model
from random import random, randrange

class ScientistAgent(Agent):
    '''
    doc Scientist Agent.
    '''
    def __init__(self, unique_id: int, model: Model, **args):
        super().__init__(unique_id, model)
        self.color = None
        vars(self).update(args)
        self.neighbors = []
        self.collaborators = set()
        self.aging_months = 0

    def __update_age__(self):
        self.aging_months += self.model.time_step
        if self.aging_months >= 12:
            self.age += 1
            self.aging_months -= 12

    def __update_health__(self):
        self.health += randrange(-self.model.time_step, self.model.time_step+1)
        self.health = min(self.health, 100)
        self.health = max(self.health, 1)

    def __should_colaborate__(self, neighbor):
        """
        colorir ao colaborar
        """
        def normalize(value,old_min,old_max,new_min,new_max):
            return (new_max-new_min)/(old_max-old_min)*(value-old_max)+new_max

        normalize_age = lambda age: normalize(age,20,50,0,1)

        p = 1 * float(neighbor.organization["sigla"] == self.organization["sigla"]) +\
            1 * float(neighbor.organization["cidade"] == self.organization["cidade"]) +\
            2 * float(neighbor.area_of_interest["area"] == self.area_of_interest["area"]) +\
            2 * float(neighbor.area_of_interest["interesse"] == self.area_of_interest["interesse"]) +\
            1 * float(normalize_age(abs(neighbor.age - self.age))) +\
            self.model.financial_need_weight * float(self.financial_need)

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
        return p >= 2.0

    def step(self):
        '''
        doc step.
        '''
        self.__update_age__()
        self.__update_health__()
       
        for sc in self.get_neighbors():
            if self.health > 50 and self.__should_colaborate__(sc):
                self.collaborators.add(sc)
                #sc.collaborators.add(self)
            else:
                self.collaborators.discard(sc)
                #sc.collaborators.discard(self)

    def get_neighbors(self):
        '''
        doc get_neighbors.
        '''
        if self.neighbors:
            return self.neighbors

        neighbors_nodes = self.model.grid.get_neighbors(self.pos, include_center=False)
        self.neighbors = filter(lambda s: s.unique_id in neighbors_nodes, self.model.scientists)

        return self.neighbors
