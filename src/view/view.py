import pygame as pg
import random
import math
import sys
from src.view.node_button import NodeButton

class View:
    def __init__(self, digraph):
        pg.init()
        self.digraph = digraph
        self.WIDTH = 1280
        self.HEIGHT = 720
        self.PANEL_WIDTH = 300
        self.GRAPH_WIDTH = self.WIDTH - self.PANEL_WIDTH  # Width available for the graph
        self.NODE_RADIUS = 20
        self.ATTRACTIVE_FORCE = 0.005
        self.REPULSIVE_FORCE = 10000
        self.DAMPING = 0.85
        self.window = pg.display.set_mode((self.WIDTH, self.HEIGHT))
        self.node_buttons = []
        self.positions = self.generate_random_positions()
        self.velocities = {node: (0, 0) for node in self.digraph.nodes}
        self.setup_positions()

    def setup_positions(self):
        max_iterations = 1000
        for _ in range(max_iterations):
            force_map = {node: (0, 0) for node in self.digraph.nodes}
            # Repulsive forces between every pair
            for node in self.digraph.nodes:
                for other_node in self.digraph.nodes:
                    if node != other_node:
                        dist = self.distance(self.positions[node], self.positions[other_node])
                        force = self.repulsive_force(dist)
                        direction_x = (self.positions[node][0] - self.positions[other_node][0]) / dist
                        direction_y = (self.positions[node][1] - self.positions[other_node][1]) / dist
                        force_map[node] = (
                            force_map[node][0] + direction_x * force,
                            force_map[node][1] + direction_y * force
                        )
            # Attractive forces between connected nodes
            for node in self.digraph.nodes:
                for neighbor in self.digraph.neighbors(node):  # Assuming edges is a dictionary where key is node id
                    force = self.attractive_force(self.positions[node], self.positions[neighbor])
                    force_map[node] = (
                        force_map[node][0] - ((self.positions[node][0] - self.positions[neighbor][0]) * force),
                        force_map[node][1] - ((self.positions[node][1] - self.positions[neighbor][1]) * force)
                    )
            # Update positions based on forces
            for node in self.digraph.nodes:
                dx, dy = force_map[node]
                vx, vy = self.velocities[node]
                vx = (vx + dx) * self.DAMPING
                vy = (vy + dy) * self.DAMPING
                self.velocities[node] = (vx, vy)
                new_x = max(self.NODE_RADIUS, min(self.GRAPH_WIDTH - self.NODE_RADIUS, self.positions[node][0] + vx))
                new_y = max(self.NODE_RADIUS, min(self.HEIGHT - self.NODE_RADIUS, self.positions[node][1] + vy))
                self.positions[node] = (new_x, new_y)

    def run(self):
        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                elif event.type == pg.MOUSEBUTTONDOWN:
                    for button in self.node_buttons:
                        if button.handle_click(event):
                            print("Node clicked:", button.text)
            self.window.fill((255, 255, 255))
            self.draw_nodes()
            self.draw_ui_panel()
            pg.display.update()
        pg.quit()
        sys.exit()

    def distance(self, pos1, pos2):
        dist = math.sqrt((pos2[0] - pos1[0]) ** 2 + (pos2[1] - pos1[1]) ** 2)
        return dist if dist != 0 else 0.0001

    def attractive_force(self, pos1, pos2):
        dist = self.distance(pos1, pos2)
        return (dist - 100) * self.ATTRACTIVE_FORCE

    def repulsive_force(self, distance):
        return self.REPULSIVE_FORCE / (distance ** 2)

    def generate_random_positions(self):
        return {node: (random.randint(0, self.GRAPH_WIDTH), random.randint(0, self.HEIGHT)) for node in self.digraph.nodes}

    def draw_nodes(self):
        self.node_buttons = [NodeButton(self.window, pos[0], pos[1], self.NODE_RADIUS, node) for node, pos in self.positions.items()]

    def draw_ui_panel(self):
        panel_color = (200, 200, 200)  # Light grey
        panel_rect = pg.Rect(self.GRAPH_WIDTH, 0, self.PANEL_WIDTH, self.HEIGHT)
        pg.draw.rect(self.window, panel_color, panel_rect)
        font = pg.font.Font(None, 36)
        text = font.render('UI Panel', True, (0, 0, 0))
        self.window.blit(text, (self.GRAPH_WIDTH + 10, 10))  # Adjust position accordingly
