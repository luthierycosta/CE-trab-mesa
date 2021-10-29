from mesa.visualization.modules import ChartModule
from mesa.visualization.modules import NetworkModule
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter

def network_portrayal(graph):
    '''
      The model ensures there is always 1 agent per node
    '''

    def node_color(agent):
        return "#FF0000"

    def edge_color(agent1, agent2):
        return "#000000"

    def edge_width(agent1, agent2):
        # if State.RESISTANT in (agent1.state, agent2.state):
        #   return 3
        return 2

    def get_agents(source, target):
        return graph.nodes[source]["agent"][0], graph.nodes[target]["agent"][0]

    portrayal = dict()
    portrayal["nodes"] = [
      {
        "size": 6,
        "color": node_color(agents[0]),
        "tooltip": "id: {}<br>ppc: {}<br> pop den: {} hab/km²".format(
          agents[0].unique_id, agents[0].pib_per_capita, agents[0].pop_density
        ),
      }
      for (_, agents) in graph.nodes.data("agent")
    ]

    portrayal["edges"] = [
      {
        "source": source,
        "target": target,
        "color": edge_color(*get_agents(source, target)),
        "width": edge_width(*get_agents(source, target)),
      }
      for (source, target) in graph.edges
    ]

    return portrayal

# Network
network = NetworkModule(network_portrayal, 500, 500, library="d3")

# text element
# class MyTextElement(TextElement):
#   def render(self, model):
#     ratio = 0.23456
#     ratio_text = "&infin;" if ratio is math.inf else "{0:.2f}".format(ratio)
#     infected_text = str(1337)
#     return "Resistant/Susceptible Ratio: {}<br>Infected Remaining: {}".format(
#       ratio_text, infected_text
#     )

# Chart
chart = ChartModule(
  [
    {"Label": "Infected", "Color": "#FF0000"},
    {"Label": "Susceptible", "Color": "#008000"},
    {"Label": "Resistant", "Color": "#808080"},
  ]
)

visualization = [network, chart]
