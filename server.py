from colab_model import CollaborationModel as model
from visualization import visualization, ModularServer, UserSettableParameter

model_params = {
    "scientist_num": UserSettableParameter(
        "slider",
        "Número de cientistas",
        50,
        2,
        200,
        2,
        description="Número de cientistas",
    ),
    "time_step": UserSettableParameter(
        "slider",
        "Passagem do tempo em meses",
        6,
        1,
        36,
        1,
        description="Passagem do tempo em meses",
    ),
    "chance_of_org_change": UserSettableParameter(
        "slider",
        "Chance de mudar de organização",
        0,
        0,
        1,
        0.05,
        description="Chance de mudar de organização",
    ),
    "health_factor": UserSettableParameter(
        "slider",
        "Chance de cientistas com má saude",
        0,
        0,
        1,
        0.05,
        description="Controla quantos cientistas serão criados com má condição de saúde",
    ),
    "financial_need_weight": UserSettableParameter(
        "slider",
        "Peso da condição financeira",
        0,
        0,
        1,
        0.05,
        description="Controla o quanto a necessidade financeira pode interferir na propensão do cientista para colaborar",
    ),
    # instituition creation variance
}

model_name = "CollaborationModel"

server = ModularServer(model, visualization, model_name, model_params)
server.port = 8521
