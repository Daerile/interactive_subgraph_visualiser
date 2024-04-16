import pygame as pg
import random
import math
import sys
from src.view.node_button import NodeButton
from src.view.ui_panel import UIPanel

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
        self.ui_panel = UIPanel(self.window, self.PANEL_WIDTH, self.HEIGHT)

    def setup_positions(self):
        max_iterations = 1000
        for _ in range(max_iterations):
            force_map = {node: (0, 0) for node in self.digraph.nodes}
            # Repulsive forces between every pair
            for node in self.digraph.nodes:
                x1, y1 = self.positions[node]
                for other_node in self.digraph.nodes:
                    if node != other_node:
                        x2, y2 = self.positions[other_node]
                        dist = self.distance((x1, y1), (x2, y2))
                        if dist == 0:
                            dist = 0.0001  # Avoid division by zero
                        force = self.repulsive_force(dist)
                        direction_x = (x1 - x2) / dist
                        direction_y = (y1 - y2) / dist
                        force_map[node] = (
                            force_map[node][0] + direction_x * force,
                            force_map[node][1] + direction_y * force
                        )
            # Attractive forces between connected nodes
            for node in self.digraph.nodes:
                for neighbor in self.digraph.neighbors(node):
                    x1, y1 = self.positions[node]
                    x2, y2 = self.positions[neighbor]
                    dist = self.distance((x1, y1), (x2, y2))
                    force = self.attractive_force((x1, y1), (x2, y2))
                    direction_x = (x1 - x2) / dist
                    direction_y = (y1 - y2) / dist
                    force_map[node] = (
                        force_map[node][0] - direction_x * force,
                        force_map[node][1] - direction_y * force
                    )
                    force_map[neighbor] = (
                        force_map[neighbor][0] + direction_x * force,
                        force_map[neighbor][1] + direction_y * force
                    )

            # Update positions based on forces, ensuring nodes stay to the right of the panel
            for node in self.digraph.nodes:
                dx, dy = force_map[node]
                vx, vy = self.velocities[node]
                vx = (vx + dx) * self.DAMPING
                vy = (vy + dy) * self.DAMPING
                new_x = max(self.PANEL_WIDTH + self.NODE_RADIUS,
                            min(self.WIDTH - self.NODE_RADIUS, self.positions[node][0] + vx))
                new_y = max(self.NODE_RADIUS, min(self.HEIGHT - self.NODE_RADIUS, self.positions[node][1] + vy))
                self.positions[node] = (new_x, new_y)

    def run(self):
        clock = pg.time.Clock()
        running = True
        while running:
            time_delta = clock.tick(60) / 1000.0
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                elif event.type == pg.MOUSEBUTTONDOWN:
                    for button in self.node_buttons:
                        if button.handle_click(event):
                            print("Node clicked:", button.text)
                self.ui_panel.process_events(event)

            self.window.fill((255, 255, 255))
            self.ui_panel.update(time_delta)
            self.draw_nodes()
            self.ui_panel.draw_ui()
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
        return {node: (random.randint(self.PANEL_WIDTH, self.WIDTH), random.randint(0, self.HEIGHT)) for node in self.digraph.nodes}

    def draw_nodes(self):
        self.node_buttons = [NodeButton(self.window, pos[0], pos[1], self.NODE_RADIUS, node) for node, pos in self.positions.items()]