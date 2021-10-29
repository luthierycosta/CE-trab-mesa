'''
import mesa Agent.
'''
from mesa import Agent

class ScientistAgent(Agent):
    '''
    doc Scientist Agent.
    '''
    def __init__(self, unique_id, model, **args):
        super().__init__(unique_id, model)
        vars(self).update(args)

    def step(self):
        '''
        doc step.
        '''
        self.get_neighbors()

    def get_neighbors(self):
        '''
        doc get_neighbors.
        '''
        neighbors_nodes = self.model.grid.get_neighbors(self.pos, include_center=False)
        print(f'im agent {self.unique_id} and my neighbors are {neighbors_nodes}')
