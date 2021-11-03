from mesa.visualization.modules import ChartModule
from mesa.visualization.modules import NetworkModule
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter

def network_portrayal(graph):
    '''
      The model ensures there is always 1 agent per node
    '''

    def node_color(agent):
        # if (agent.color == None):
        #     return "#FF0000"
        # else:
        #     return agent.color
        return agent.color or "#FF0000"


    def edge_color(agent1, agent2):
        if (agent1.color and agent2.color):
                return agent1.color
        return "#000000"

        # return agent1.color and agent2.color

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
            "tooltip": f'id: {agents[0].unique_id}<br>age: {agents[0].age}<br> organization: {agents[0].organization["sigla"]} ({agents[0].organization["cidade"]})<br> health: {agents[0].health}',
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
# chart_no_colab = ChartModule(
#     [
#         {"Label": "Sem colaboração", "Color": "#FF0000"}
#     ]
# )

chart_colab = ChartModule(
    [
        {"Label": "Colaboration", "Color": "#00FF00"}
    ]
)


visualization = [network, chart_colab]
