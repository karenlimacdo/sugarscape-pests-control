import mesa
from .agents import SsAgent, Sugar, Bt
from .model import SugarscapeCg
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.modules import ChartModule
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import Checkbox, Slider, StaticText

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


canvas_element = CanvasGrid(SsAgent_portrayal, 50, 50, 500, 500)
chart_element = ChartModule(
    [{"Label": "Lagarta Saudavel", "Color": "#AA0000"},
    {"Label": "Bacteria", "Color": "green"},
    {"Label": "Lagarta Infectada", "Color": "yellow"}]
)

model_params = {
    # The following line is an example to showcase StaticText.
    "title": StaticText("Parameters:"),
    "vento": Checkbox("Vento", False),
    "initial_sheep": Slider(
        "Initial Sheep Population", 100, 10, 300
    ),
    "initial_wolves": Slider("Initial Wolf Population", 50, 10, 300),
}

server = ModularServer(
    SugarscapeCg, [canvas_element, chart_element], "Sugarscape 2 Constant Growback"#, model_params
)
server.port = 8521
# server.launch()