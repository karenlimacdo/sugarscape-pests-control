"""
Sugarscape Constant Growback Model
================================
Replication of the model found in Netlogo:
Li, J. and Wilensky, U. (2009). NetLogo Sugarscape 2 Constant Growback model.
http://ccl.northwestern.edu/netlogo/models/Sugarscape2ConstantGrowback.
Center for Connected Learning and Computer-Based Modeling,
Northwestern University, Evanston, IL.
"""

import mesa

from sugarscape_cg.scheduler import RandomActivationByTypeFiltered
from .agents import SsAgent, Sugar, Bt
from mesa.time import RandomActivationByType
from mesa.space import MultiGrid
from mesa import datacollection

class SugarscapeCg(mesa.Model):
    """
    Sugarscape 2 Constant Growback
    """

    verbose = True  # Print-monitoring

    def __init__(self, width=50, height=50, initial_population=100, inicial_population_bt=150, vento=0, current_id=0):
        """
        Create a new Constant Growback model with the given parameters.
        Args:
            initial_population: Number of population to start with
        """

        # Set parameters
        self.width = width
        self.height = height
        self.initial_population = initial_population
        self.initial_population_bt = inicial_population_bt
        self.vento = vento
        self.current_id = current_id

        #self.schedule = RandomActivationByType(self)
        self.schedule = RandomActivationByTypeFiltered(self)
        self.grid = MultiGrid(self.width, self.height, torus=False)
        self.datacollector = datacollection.DataCollector(
            {
                "Lagarta Infectada": lambda m: m.schedule.get_type_count(
                    SsAgent, lambda x: x.infectada == True),
                "Lagarta Saudável": lambda m: m.schedule.get_type_count(
                    SsAgent),
                "Bacteria": lambda m: m.schedule.get_type_count(Bt)
            }
        )

        # Create sugar
        import numpy as np

        sugar_distribution = np.genfromtxt("sugarscape_cg/sugar-map.txt")
        agent_id = 0
        self.current_id = agent_id
        for _, x, y in self.grid.coord_iter():
            max_sugar = sugar_distribution[x, y]
            sugar = Sugar(agent_id, (x, y), self, max_sugar)
            agent_id += 1
            self.current_id = agent_id
            self.grid.place_agent(sugar, (x, y))
            self.schedule.add(sugar)

        # Create agent:
        for i in range(self.initial_population):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            sugar = self.random.randrange(6, 25)
            metabolism = self.random.randrange(2, 4)
            vision = self.random.randrange(1, 6)
            ssa = SsAgent(agent_id, (x, y), self, False, sugar, metabolism, vision)
            agent_id += 1
            self.current_id = agent_id
            self.grid.place_agent(ssa, (x, y))
            self.schedule.add(ssa)

        for i in range(self.initial_population_bt):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            sugar = self.random.randrange(10, 35)
            metabolism = self.random.randrange(4, 12)
            ssa = Bt(agent_id, (x, y), self, False, sugar, metabolism)
            agent_id += 1
            self.current_id = agent_id
            self.grid.place_agent(ssa, (x, y))
            self.schedule.add(ssa)

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        self.schedule.step()
        # collect data
        self.datacollector.collect(self)
        if self.verbose:
            print([self.schedule.time, self.schedule.get_type_count(SsAgent, lambda x: x.infectada == True), self.schedule.get_type_count(SsAgent), self.schedule.get_type_count(Bt)])

    def run_model(self, step_count=200):

        if self.verbose:
            print(
                "Initial number Sugarscape Agent: ",
                self.schedule.get_type_count(SsAgent, lambda x: x.infectada == True),
                self.schedule.get_type_count(SsAgent),
                self.schedule.get_type_count(Bt)
            )

        for i in range(step_count):
            self.step()

        if self.verbose:
            print("")
            print(
                "Final number Sugarscape Agent: ",
                self.schedule.get_type_count(SsAgent, lambda x: x.infectada == True),
                self.schedule.get_type_count(SsAgent),
                self.schedule.get_type_count(Bt)
            )
