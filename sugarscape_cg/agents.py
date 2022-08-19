import math

import mesa


def get_distance(pos_1, pos_2):
    """Get the distance between two point
    Args:
        pos_1, pos_2: Coordinate tuples for both points.
    """
    x1, y1 = pos_1
    x2, y2 = pos_2
    dx = x1 - x2
    dy = y1 - y2
    return math.sqrt(dx**2 + dy**2)

#Lagarta
class SsAgent(mesa.Agent):
    def __init__(
        self, unique_id, pos, model, moore=False, sugar=0, metabolism=0, vision=0, infectada=False
    ):
        super().__init__(unique_id, model)
        self.pos = pos
        self.moore = moore
        self.sugar = sugar
        self.metabolism = metabolism
        self.vision = vision
        self.infectada = infectada

    def get_sugar(self, pos):
        this_cell = self.model.grid.get_cell_list_contents([pos])
        for agent in this_cell:
            if type(agent) is Sugar:
                return agent


    def is_occupied(self, pos):
        this_cell = self.model.grid.get_cell_list_contents([pos])
        return any(isinstance(agent, SsAgent) for agent in this_cell)

    def move(self):
        # Get neighborhood within vision
        neighbors = [
            i
            for i in self.model.grid.get_neighborhood(
                self.pos, self.moore, False, radius=self.vision
            )
            if not self.is_occupied(i)
        ]
        neighbors.append(self.pos)
        # Look for location with the most sugar
        max_sugar = max(self.get_sugar(pos).amount for pos in neighbors)
        candidates = [
            pos for pos in neighbors if self.get_sugar(pos).amount == max_sugar
        ]
        # Narrow down to the nearest ones
        min_dist = min(get_distance(self.pos, pos) for pos in candidates)
        final_candidates = [
            pos for pos in candidates if get_distance(self.pos, pos) == min_dist
        ]
        self.random.shuffle(final_candidates)
        self.model.grid.move_agent(self, final_candidates[0])

    def eat(self):
        sugar_patch = self.get_sugar(self.pos)
        self.sugar = self.sugar - self.metabolism + sugar_patch.amount
        sugar_patch.amount = 0

    def step(self):
        if self.infectada == False:
            self.move()
            self.eat()
            neighbors = [
                i
                for i in self.model.grid.get_neighborhood(
                    self.pos, self.moore, False, radius=10
                )
            ]
            for pos in neighbors:
                this_cell = self.model.grid.get_cell_list_contents([pos])
                bacteria = [agent for agent in this_cell if isinstance(agent, Bt)]
                if len(bacteria) > 0:
                    bt_inside = self.random.choice(bacteria)
                    self.metabolism += 4
                    self.infectada = True
                    self.model.grid.remove_agent(bt_inside)
                    self.model.schedule.remove(bt_inside)
        else:
            self.sugar = self.sugar - self.metabolism
        
        if self.sugar <= 0:
            if self.infectada:
                for i in range(4):
                    x, y = self.pos
                    if(x + i < 50):
                        x += i
                    elif(x - 1 > 0):
                        x -= i
                    if(y + i < 50): 
                        y += i
                    elif(y - 1 > 0):
                        y -= i
                    else:
                        x = self.random.randrange(50)
                        y = self.random.randrange(50)
                    sugar = self.random.randrange(6, 10)
                    metabolism = self.random.randrange(1, 2)
                    bacteria = Bt(
                        self.model.next_id(), (x, y), self.model, False, sugar, metabolism, False
                    )
                    self.model.grid.place_agent(bacteria, (x, y))
                    self.model.schedule.add(bacteria)
            else:
                x, y = self.pos
                sugar = self.random.randrange(6, 25)
                metabolism = self.random.randrange(2, 4)
                vision = self.random.randrange(1, 6)
                lagarta = SsAgent(
                    self.model.next_id(), (x, y), self.model, False, sugar, metabolism, vision, False
                )
                self.model.grid.place_agent(lagarta, self.pos)
                self.model.schedule.add(lagarta)
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)


class Sugar(mesa.Agent):
    def __init__(self, unique_id, pos, model, max_sugar):
        super().__init__(unique_id, model)
        self.amount = max_sugar
        self.max_sugar = max_sugar

    def step(self):
        self.amount = min([self.max_sugar, self.amount + 1])


class Bt(mesa.Agent):
    def __init__(
        self, unique_id, pos, model, moore=False, sugar=0, metabolism=0, vento=0
    ):
        super().__init__(unique_id, model)
        self.pos = pos
        self.moore = moore
        self.sugar = sugar
        self.metabolism = metabolism
        self.vento = vento

    def is_occupied(self, pos):
        this_cell = self.model.grid.get_cell_list_contents([pos])
        return any(isinstance(agent, SsAgent) for agent in this_cell) or any(isinstance(agent, Bt) for agent in this_cell)

    def move(self):
        # Get neighborhood within vision
        neighbors = [
            i
            for i in self.model.grid.get_neighborhood(
                self.pos, self.moore, False, radius=self.vento
            )
            if not self.is_occupied(i)
        ]
        if(len(neighbors) > 0):
            self.random.shuffle(neighbors)
            self.model.grid.move_agent(self, neighbors[0])

    def step(self):
        if self.vento:
            self.move()

        self.sugar = self.sugar - self.metabolism

        if self.sugar <= 0:
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)
