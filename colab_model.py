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
        doc Collaboration
    '''

    def __init__(self, scientist_num, time_step, chance_of_org_change, health_factor, financial_need_weight):
        
        self.schedule = RandomActivation(self)
        self.running = True
        
        self.scientist_num = scientist_num
        self.time_step = time_step
        self.chance_of_org_change = chance_of_org_change
        self.health_factor = health_factor
        self.financial_need_weight = financial_need_weight
        self.scientists = []

        # Inicializa lista de organizações
        with open('organizacoes.csv', mode='r', encoding='utf-8') as csvfile:
            self.organizations = [row for row in csv.DictReader(csvfile, delimiter=';')]

        with open('interesses-academicos.csv', mode='r', encoding='utf-8') as csvfile:
            self.interests = [row for row in csv.DictReader(csvfile, delimiter=';')]

        # create grid
        # prob = self.organizations.line_num / self.scientist_num
        self.G = nx.erdos_renyi_graph(n=self.scientist_num, p=0.05)
        self.grid = NetworkGrid(self.G)

        # Create agents
        for i, node in enumerate(self.G.nodes()):
            # a = TerritoryAgent(i, self, 2, 20000, self.pib_instituition_weight, self.pop_instituition_weight)
            self.createScientist(i, node)

        # create data collector
        def colab_count(model):
            cc = sum([ scientist.color == '#00FF00' for scientist in model.scientists])
            return cc

        self.datacollector = DataCollector(
            {
                "Colaboration": colab_count
                # model_reporters={"Gini": compute_gini},
                # agent_reporters={"Wealth": "wealth"}
            }
        )

    def createScientist(self, id, node):
        age = randint(20, 50)
        health = randint(75, 100) if random() > self.health_factor else randint(15, 75)
        financial = random()
        org = choice(self.organizations)
        interest = choice(self.interests)
        
        scientist = ScientistAgent(id, self, age=age, health=health, financial_need=financial, organization=org, area_of_interest=interest)
        self.schedule.add(scientist)
        self.grid.place_agent(scientist, node)
        self.scientists.append(scientist)
        return scientist

    def export(self, filename):
        with open(filename, 'w', newline='') as file:
            wr = csv.writer(file, quoting=csv.QUOTE_ALL)
            wr.writerow(["id","color"])
            for sc in self.scientists:
                wr.writerow([sc.id, sc.color])

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()
        self.export("./results.csv")