from collections import deque

import pygame as pg
import pygame_gui as pgui
import numpy as np
import pandas as pd
import networkx as nx
from random import random
from src.view.node_button import NodeButton
from src.backend.node import Node
import pprint
import cProfile
import pstats


class Layout:
    def __init__(self, digraph: nx.DiGraph, cem):
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
        self.create_view(digraph)

    def create_view(self, digraph: nx.DiGraph):
        if not self.cem.focused:
            self.create_full_elems()
        else:
            self.create_focused_elems(digraph)

    def create_focused_elems(self, digraph: nx.DiGraph):
        self.WIDTH = len(self.cem.digraph.nodes) * 150
        self.HEIGHT = len(self.cem.digraph.nodes) * 150
        center_pos = (int(self.WIDTH / 2), int(self.HEIGHT / 2))
        start_node = self.node_map[self.cem.focused_node.id]
        nodes = {self.node_map[node.id]: node for node in self.cem.digraph.nodes}
        pos_map = {self.node_map[node.id]: (0, 0) for node in self.cem.digraph.nodes}
        pos_map[self.node_map[self.cem.focused_node.id]] = center_pos



        # Create layers based on path length
        x_breakpoints_forwards = []
        x_breakpoints_backwards = []
        for i in range(1, self.cem.focused_depth + 1):
            x_breakpoints_forwards.append(center_pos[0] + i * (center_pos[0] / self.cem.focused_depth))
            x_breakpoints_backwards.append(center_pos[0] - i * (center_pos[0] / self.cem.focused_depth))

        self.create_from_layer(start_node, center_pos, x_breakpoints_forwards, x_breakpoints_backwards, forward=True)
        self.create_from_layer(start_node, center_pos, x_breakpoints_forwards, x_breakpoints_backwards, forward=False)

        # Debugging outputs
        pprint.pprint(self.node_map)
        pprint.pprint(self.adjacency_list)
        pprint.pprint(self.complement_adjacency_list)

        self.cem.create_node_button(center_pos[0], center_pos[1], self.cem.focused_node)
        self.cem.create_edges(color=(150, 0, 0))

    def create_from_layer(self, start_node, center_pos, x_breakpoints_forwards, x_breakpoints_backwards, forward=True):
        layer_before = []
        y_breakpoints = []
        y_breakpoints_before = []
        for i in range(self.cem.focused_depth):
            if i == 0:
                next_layer = self.adjacency_list[start_node] if forward else self.complement_adjacency_list[start_node]
                layer_before = next_layer
                if forward:
                    y_breakpoints_before = self.create_buttons(center_pos[0], x_breakpoints_forwards[i], 0, self.HEIGHT,
                                                           next_layer)
                else:
                    y_breakpoints_before = self.create_buttons(center_pos[0], x_breakpoints_backwards[i], 0, self.HEIGHT,
                                                           next_layer)
            else:
                next_layer = []
                for j, node in enumerate(layer_before):
                    a_n = self.adjacency_list[node] if forward else self.complement_adjacency_list[node]
                    next_layer.extend(a_n)
                    if forward:
                        y_breakpoints.append(self.create_buttons(x_breakpoints_forwards[i - 1], x_breakpoints_forwards[i],
                                                             y_breakpoints_before[j], y_breakpoints_before[j + 1], a_n))
                    else:
                        y_breakpoints.append(self.create_buttons(x_breakpoints_backwards[i - 1], x_breakpoints_backwards[i],
                                                             y_breakpoints_before[j], y_breakpoints_before[j + 1], a_n))
                layer_before = next_layer
                y_breakpoints_before = []
                for ls in y_breakpoints:
                    y_breakpoints_before.extend(ls)

    def create_buttons(self, box_left, box_right, box_top, box_bottom, nodes):
        y_breakpoints = []
        n = len(nodes)
        if n > 0:
            y_breakpoints.append(box_top)
            for i, node_idx in enumerate(nodes):
                y_br = ((box_bottom - box_top) * (i + 1) / n) + box_top
                x = (box_left + box_right) / 2
                y = y_br - 0.5 * (box_bottom - box_top) / n
                y_breakpoints.append(y_br)
                self.cem.create_node_button(x, y, self.nodes[node_idx])
                print(f"node: {self.nodes[node_idx].id}, pos: {x}, {y}")
        print(f'breakpoints: {y_breakpoints}')
        return y_breakpoints

    def create_full_elems(self):
        height = 600 + 3 * len(self.nodes) + len(self.edge_list)
        width = height
        pos = self.init_positions(height, width)
        self.fruchterman_reingold(width, height, self.nodes, self.edge_list, pos)
        self.cem.create_edges(color=(150, 0, 0))

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

    def fruchterman_reingold(self, width, height, nodes, edge_list, pos, k=None, t=1000, shift=0, focused=False):
        if k is None:
            k = (width * height / len(self.nodes)) ** 0.5
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

                pos = (min(max(nb.x + pos[0], 0), width), min(max(nb.y + pos[1], 0), height))

                nb.x = pos[0] + 300 + shift
                nb.y = pos[1]
            t *= 0.9
        print(f"done")
