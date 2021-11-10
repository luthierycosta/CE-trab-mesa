from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid, NetworkGrid
from mesa.datacollection import DataCollector

import networkx as nx
from random import random, randint, choice

import csv

from scientist_agent import ScientistAgent

class CollaborationModel(Model):
    '''
        Classe do modelo de colaboração.
    '''

    def __init__(self, scientist_num, time_step, chance_of_org_change, initial_health_factor, financial_need_weight, health_delta_factor):
        '''
        Construtor do modelo de colaboração.
        '''
        self.schedule = RandomActivation(self)
        self.running = True
        
        self.scientist_num = scientist_num
        self.time_step = time_step
        self.chance_of_org_change = chance_of_org_change
        self.initial_health_factor = initial_health_factor
        self.financial_need_weight = financial_need_weight
        self.health_delta_factor = health_delta_factor
        self.scientists = []

        # Inicializa lista de organizações
        with open('organizacoes.csv', mode='r', encoding='utf-8') as csvfile:
            self.organizations = [row for row in csv.DictReader(csvfile, delimiter=';')]

        with open('interesses-academicos.csv', mode='r', encoding='utf-8') as csvfile:
            self.interests = [row for row in csv.DictReader(csvfile, delimiter=';')]

        # create grid
        # prob = self.organizations.line_num / self.scientist_num
        self.G = nx.erdos_renyi_graph(n=self.scientist_num, p=0.2)
        self.grid = NetworkGrid(self.G)

        # Create agents
        for i, node in enumerate(self.G.nodes()):
            # a = TerritoryAgent(i, self, 2, 20000, self.pib_instituition_weight, self.pop_instituition_weight)
            self.createScientist(i, node)

        # Create data collector
        def colab_count(model):
            '''
            Soma de todas as colaborações no grafo.
            '''
            cc = sum([scientist.get_color() in ['#00FF00','#8F34EB'] for scientist in model.scientists])
            return cc

        self.datacollector = DataCollector(
            {
                "Colaboration": colab_count
                # model_reporters={"Gini": compute_gini},
                # agent_reporters={"Wealth": "wealth"}
            }
        )

    def createScientist(self, id, node):
        '''
        Cria um cientista no grafo.
        '''
        age = randint(20, 50)
        health = randint(75, 100) if random() > self.initial_health_factor else randint(15, 75)
        financial = random()
        org = choice(self.organizations)
        interest = choice(self.interests)
        
        scientist = ScientistAgent(id, self, age=age, health=health, financial_need=financial, organization=org, area_of_interest=interest)
        self.schedule.add(scientist)
        self.grid.place_agent(scientist, node)
        self.scientists.append(scientist)
        return scientist

    def getScientist(self, id):
        '''
        É retornado um cientista de acordo com o id passado.
        '''
        return list(filter(lambda x: x.unique_id == id, self.scientists))[0]

    def export(self, filename):
        '''
        Exporta as colaborações ocorridas no grafo para um arquivo txt.
        '''
        with open(filename, 'w') as f:
            f.write("# FromNodeId\tToNodeId\n")
            for sci in self.scientists:
                for colab in sci.collaborators:
                    f.write(f"{sci.unique_id}\t{colab}\n")

    def step(self):
        '''
        Em cada passo de nossa simulação exportamos as colaborações do grafo. O arquivo é sobreescrevido em cada passo.
        '''
        self.datacollector.collect(self)
        self.schedule.step()
        self.export("./results.txt")