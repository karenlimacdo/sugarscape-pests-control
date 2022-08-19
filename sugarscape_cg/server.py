import mesa
from .agents import SsAgent, Sugar, Bt
from .model import SugarscapeCg
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.modules import ChartModule
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter

color_dic = {4: "#005C00", 3: "#008300", 2: "#00AA00", 1: "#00F800"}


def SsAgent_portrayal(agent):
    if agent is None:
        return

    portrayal = {}

    if type(agent) is SsAgent:
        portrayal["Shape"] = "sugarscape_cg/resources/Lagarta.png"
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 1

    elif type(agent) is Sugar:
        if agent.amount != 0:
            portrayal["Color"] = color_dic[agent.amount]
        else:
            portrayal["Color"] = "#D6F5D6"
        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 0
        portrayal["w"] = 1
        portrayal["h"] = 1

    elif type(agent) is Bt:
        portrayal["Shape"] = "sugarscape_cg/resources/Bt.png"
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 1

    return portrayal

model_params = {
    "width": 50,
    "height": 50,
    "initial_population": UserSettableParameter("slider", "Initial Population", 100, 0, 200, 10),
    "initial_population_bt": UserSettableParameter("slider", "Bacteria Population", 50, 0, 200, 10),
    "vento": UserSettableParameter("slider", "Vento", 0, 0, 5, 1),
}

canvas_element = CanvasGrid(SsAgent_portrayal, 50, 50, 500, 500)
chart_element = ChartModule(
    [{"Label": "Lagarta Saudavel", "Color": "red"},
    {"Label": "Bacteria", "Color": "green"},
    {"Label": "Lagarta Infectada", "Color": "yellow"}]
)

server = ModularServer(
    SugarscapeCg, [canvas_element, chart_element], "Sugarscape 2 Constant Growback", model_params
)
# server.launch()