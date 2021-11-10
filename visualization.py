from mesa.visualization.modules import ChartModule
from mesa.visualization.modules import NetworkModule
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter

def network_portrayal(graph):
    '''
      The model ensures there is always 1 agent per node
    '''

    def node_color(agent):
        return agent.get_color()


    def edge_color(agent1, agent2):
        if (agent1.unique_id in agent2.collaborators and agent2.unique_id in agent1.collaborators):
                return '#00FF00'
        return "#000000"

    def edge_width(agent1, agent2):
        return 2

    def get_agents(source, target):
        return graph.nodes[source]["agent"][0], graph.nodes[target]["agent"][0]

    portrayal = dict()
    portrayal["nodes"] = [
        {
            "size": 6,
            "color": node_color(agents[0]),
            "tooltip": f'id: {agents[0].unique_id}<br>\
                        age: {agents[0].age}<br>\
                        health: {agents[0].health}<br>\
                        organization: {agents[0].organization["sigla"]} ({agents[0].organization["cidade"]})<br>\
                        interest: {agents[0].area_of_interest["area"]} - {agents[0].area_of_interest["interesse"]}',
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

chart_colab = ChartModule(
    [
        {"Label": "Colaboration", "Color": "#00FF00"}
    ]
)


visualization = [network, chart_colab]
