import pygame as pg
import pygame_gui as pgui
import numpy as np
import pandas as pd
import networkx as nx
from random import random
from src.view.node_button import NodeButton
from src.view.canvas_element_manager import CanvasElementManager
from src.backend.node import Node
import pprint
import cProfile
import pstats


class Layout:
    def __init__(self, digraph: nx.DiGraph, cem: CanvasElementManager):
        self.WIDTH = 3000
        self.HEIGHT = 3000
        if len(digraph) == 0:
            return
        self.nodes: list[Node] = [n for n in digraph.nodes]
        self.edge_list = [(lhs, rhs) for (lhs, rhs) in digraph.edges]

        self.node_map = {node.id: i for i, node in enumerate(self.nodes)}
        self.adjacency_list = [[] for _ in range(len(self.nodes))]
        self.complement_adjacency_list = [[] for _ in range(len(self.nodes))]
        for lhs, rhs in self.edge_list:
            self.adjacency_list[self.node_map[lhs.id]].append(self.node_map[rhs.id])
            self.complement_adjacency_list[self.node_map[rhs.id]].append(self.node_map[lhs.id])
        self.cem = cem
        if cem.created:
            NotImplemented
        else:
            self.create_elems()

    def create_elems(self):
        if self.cem.focused:
            NotImplemented
        else:
            height = 600 + 3 * len(self.nodes) + len(self.edge_list)
            width = height
            pos = self.init_positions(height, width)
            profiler = cProfile.Profile()
            profiler.enable()
            self.fruchterman_reingold(self.nodes, self.edge_list, pos)
            profiler.disable()
            stats = pstats.Stats(profiler).sort_stats('cumulative')
            stats.print_stats()
            self.cem.create_edges(color=(150, 0, 0))
            for node, node_button in self.cem.node_buttons:
                print(f'{node_button.text}: {node_button.x}, {node_button.y}')



    def init_positions(self, height, width):
        pos = {node.id: (0, 0) for node in self.nodes}
        rest_height = height / 2

        # DAG -> BFS TODO
        for node in self.nodes:
            if (
                    not self.adjacency_list[self.node_map[node.id]]
                    and not self.complement_adjacency_list[self.node_map[node.id]]
            ):
                x = random() * width
                y = random() * rest_height
                pos[node.id] = (x, y)
                self.cem.create_node_button(x, y, node)
                print(f"isolated: {node.id} at {x}, {y}")
                continue

            x = random() * width
            y = random() * rest_height + rest_height
            pos[node.id] = (x, y)
            self.cem.create_node_button(x, y, node)
            print(f"normal: {node.id} at {x}, {y}")
        return pos

    def fruchterman_reingold(self, nodes, edge_list, pos, k=None, t=1000):
        if k is None:
            k = (self.WIDTH * self.HEIGHT / len(self.nodes)) ** 0.5
        k_sq = k ** 2
        print(f"nodes: {len(nodes)}, edges: {len(edge_list)}")

        pos_values = np.array(list(pos.values()))

        while t > 0.1:
            print(f"at step: {t}")

            disps = np.zeros((len(nodes), 2))

            # Repell
            for i in range(len(nodes)):
                n, nb = self.cem.node_buttons[i]
                x, y = nb.x, nb.y

                delta = np.subtract(pos_values, [x, y])
                distance = np.linalg.norm(delta, axis=1)
                mask = (distance > 0.05)
                delta_norm = np.where(mask[:, np.newaxis], delta / distance[:, np.newaxis], np.zeros_like(delta))
                disps += np.where(mask[:, np.newaxis], delta_norm * k_sq / distance[:, np.newaxis], np.zeros_like(delta))

            # Attract
            for i, neighbours in enumerate(self.adjacency_list):
                for j in neighbours:
                    v = self.cem.node_buttons[i][1]
                    u = self.cem.node_buttons[j][1]

                    delta = np.subtract([v.x, v.y], [u.x, u.y])
                    (delta_x, delta_y) = delta
                    delta_norm = (delta_x ** 2 + delta_y ** 2) ** 0.5

                    if delta_norm < 0.05:
                        continue

                    delta = np.divide(delta, delta_norm)

                    disps[i] = np.subtract(disps[i], np.multiply(delta, k_sq / delta_norm))
                    disps[j] = np.subtract(disps[i], np.multiply(delta, k_sq / delta_norm))

            # Cool
            for i in range(len(nodes)):
                n, nb = self.cem.node_buttons[i]

                x, y = nb.x, nb.y
                disp = disps[i]
                (disp_x, disp_y) = disp
                disp_norm = (disp_x ** 2 + disp_y ** 2) ** 0.5

                if disp_norm < 0.05:
                    continue

                if min(disp_norm, t) == 0:
                    continue

                pos = np.multiply(np.divide(disp, disp_norm), min(disp_norm, t))

                pos = (min(max(nb.x + pos[0], 0), self.WIDTH), min(max(nb.y + pos[1], 0), self.HEIGHT))

                nb.x = pos[0] + 300
                nb.y = pos[1]
            t *= 0.9
        print(f"done")

    def draw(self):
        self.cem.draw_arrows()
        self.cem.draw_node_buttons()
