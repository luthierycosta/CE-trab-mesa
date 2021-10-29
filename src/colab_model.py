from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid, NetworkGrid
from mesa.datacollection import DataCollector

import networkx as nx
from random import random, randint

from scientist_agent import ScientistAgent

class CollaborationModel(Model):
    '''
        doc Collaboration
    '''

    def __init__(self, territory_num, avgNeighbors, pib_instituition_weight, pop_instituition_weight):
        self.num_agents = territory_num
        self.schedule = RandomActivation(self)
        self.running = True

        self.pib_instituition_weight = pib_instituition_weight
        self.pop_instituition_weight = pop_instituition_weight

        # create grid
        prob = avgNeighbors / territory_num
        self.G = nx.erdos_renyi_graph(n=self.num_agents, p=prob)
        self.grid = NetworkGrid(self.G)

        # Create agents
        for i, node in enumerate(self.G.nodes()):
            # a = TerritoryAgent(i, self, 2, 20000, self.pib_instituition_weight, self.pop_instituition_weight)
            scientist = self.createScientist(i)
            self.schedule.add(scientist)
            self.grid.place_agent(scientist, node)

        # create data collector
        self.datacollector = DataCollector(
            # model_reporters={"Gini": compute_gini},
            # agent_reporters={"Wealth": "wealth"}
        )

    def createScientist(self, id):
        # codigo
        return ScientistAgent(id, self)
    
    
    # def createTerritory(self, id):
    #     pib_per_capita = randint(500, 35000) if random() < 0.95 else randint(3500, 65000)
    #     pop_density = randint(10, 24) if random() < 0.70 else randint(24, 7300)
    #     return ScientistAgent(id, self, pop_density, pib_per_capita, self.pib_instituition_weight, self.pop_instituition_weight)

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()
