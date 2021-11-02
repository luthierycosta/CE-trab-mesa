from colab_model import CollaborationModel as model
from visualization import visualization, ModularServer, UserSettableParameter

model_params = {
    "avgNeighbors": UserSettableParameter(
        "slider",
        "Average Neighbors",
        3,
        0,
        10,
        1,
        description="Number of territories",
    ),
    "territory_num": UserSettableParameter(
        "slider",
        "Number of Territories",
        35,
        1,
        100,
        1,
        description="Number of territories",
    ),
    "pib_instituition_weight": UserSettableParameter(
        "slider",
        "PIB per capita weight",
        0,
        0.4,
        1,
        0.05,
        description="how much the pib per capita factors into the probability of a new instituition opening up in a territory",
    ),
    "pop_instituition_weight": UserSettableParameter(
        "slider",
        "population density weight",
        0,
        0.4,
        1,
        0.05,
        description="how much the population density factors into the probability of a new instituition opening up in a territory",
    ),
    # instituition creation variance
}

model_name = "CollaborationModel"

server = ModularServer(model, visualization, model_name, model_params)
server.port = 8521
