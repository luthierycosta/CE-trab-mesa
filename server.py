from colab_model import CollaborationModel as model
from visualization import visualization, ModularServer, UserSettableParameter

MODEL_PARAMS = {
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

MODEL_NAME = "CollaborationModel"

server = ModularServer(model, visualization, MODEL_NAME, MODEL_PARAMS)
server.port = 8521
