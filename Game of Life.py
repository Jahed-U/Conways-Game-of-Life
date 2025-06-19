#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 31 10:11:06 2024

@author: jahed
"""

from mesa import Agent, Model
from mesa.space import MultiGrid
from mesa.time import SimultaneousActivation
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer


class Cell(Agent):
    def __init__(self, unique_id, model, x, y, initial_state):
        super().__init__(unique_id, model)
        self.x = x
        self.y = y
        self.state = initial_state
        self.next_state = None

    def step(self):
        self.state = self.next_state


class GameOfLife(Model):
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.grid = MultiGrid(width, height, True)
        self.schedule = SimultaneousActivation(self)

        # Create cells and place them on the grid
        for x in range(self.width):
            for y in range(self.height):
                cell = Cell((x, y), self, x, y, self.random.choice([0, 1]))
                self.grid.place_agent(cell, (x, y))
                self.schedule.add(cell)

    def step(self):
        for cell in self.schedule.agents:
            neighbors = self.grid.get_neighbors((cell.x, cell.y), moore=True)
            live_neighbors = sum(1 for neighbor in neighbors if
                                 neighbor.state == 1)
            # Implement the rules of Conway's Game of Life
            if cell.state == 0 and live_neighbors == 3:
                cell.next_state = 1
            elif cell.state == 1 and (live_neighbors < 2 or
                                      live_neighbors > 3):
                cell.next_state = 0
            else:
                cell.next_state = cell.state

        # Update cell states simultaneously
        for cell in self.schedule.agents:
            cell.step()


def agent_portrayal(agent):
    portrayal = {"Shape": "rect", "w": 1, "h": 1, "Filled": "true",
                 "Layer": 0}
    portrayal["x"] = agent.x
    portrayal["y"] = agent.y
    if agent.state == 1:
        portrayal["Color"] = "black"
    else:
        portrayal["Color"] = "white"
    return portrayal


grid = CanvasGrid(agent_portrayal, 10, 10, 500, 500)
server = ModularServer(GameOfLife, [grid], "Game of Life", {"height": 10,
                                                            "width": 10})
server.port = 8522  # The default
server.launch()
