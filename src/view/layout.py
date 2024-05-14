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
        self.WIDTH = len(self.cem.digraph.nodes) * (self.cem.horizontal_scatter * 50)
        self.HEIGHT = len(self.cem.digraph.nodes) * (self.cem.vertical_scatter * 50)
        center_pos = (int(self.WIDTH / 2), int(self.HEIGHT / 2))
        start_node = self.node_map[self.cem.focused_node.id]
        nodes = {self.node_map[node.id]: node for node in self.cem.digraph.nodes}
        pos_map = {self.node_map[node.id]: (0, 0) for node in self.cem.digraph.nodes}
        pos_map[self.node_map[self.cem.focused_node.id]] = center_pos

        # Create layers based on path length

        x_breakpoints_forwards = []
        x_breakpoints_backwards = []
        for i in range(1, self.cem.focused_depth + 1):
            if i == 1:
                x_breakpoints_forwards.append(center_pos[0] + 2*i * (center_pos[0] / self.cem.focused_depth + 1))
                x_breakpoints_backwards.append(center_pos[0] - 2*i * (center_pos[0] / self.cem.focused_depth + 1))
            else:
                x_breakpoints_forwards.append(x_breakpoints_forwards[-1] + i * (center_pos[0] / self.cem.focused_depth + 3))
                x_breakpoints_backwards.append(x_breakpoints_backwards[-1] - i * (center_pos[0] / self.cem.focused_depth + 3))

        self.create_from_layer(start_node, center_pos, x_breakpoints_forwards, x_breakpoints_backwards, forward=True)
        self.create_from_layer(start_node, center_pos, x_breakpoints_forwards, x_breakpoints_backwards, forward=False)

        self.cem.create_node_button(center_pos[0], center_pos[1], self.cem.focused_node)
        self.cem.create_edges()
        self.cem.center_around(center_pos[0], center_pos[1])

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
                child_num = len(self.adjacency_list[node_idx]) + len(self.complement_adjacency_list[node_idx])
                self.cem.create_node_button(x, y, self.nodes[node_idx])
                print(f"node: {self.nodes[node_idx].id}, pos: {x}, {y}")
        print(f'breakpoints: {y_breakpoints}')
        return y_breakpoints

    def create_full_elems(self):
        height = 600 + 3 * len(self.nodes) + len(self.edge_list)
        width = 600 + 3 * len(self.nodes) + len(self.edge_list)
        pos = self.init_positions(height, width)
        self.fruchterman_reingold(width, height, self.edge_list, pos)
        self.cem.create_edges()

    def init_positions(self, height, width):
        pos = {}
        rest_height = height / 2

        # DAG -> BFS TODO
        for node in self.nodes:
            if (
                    not self.adjacency_list[self.node_map[node.id]]
                    and not self.complement_adjacency_list[self.node_map[node.id]]
            ):
                x = random() * width
                y = random() * rest_height
                child_num = len(self.adjacency_list[self.node_map[node.id]]) + len(self.complement_adjacency_list[self.node_map[node.id]])
                self.cem.create_node_button(x, y, node)
                continue

            x = random() * width
            y = random() * rest_height + rest_height
            pos[node] = (x, y)
            child_num = len(self.adjacency_list[self.node_map[node.id]]) + len(
                self.complement_adjacency_list[self.node_map[node.id]])
            self.cem.create_node_button(x, y, node)
        return pos

    def fruchterman_reingold(self, width, height, edge_list, pos, k=None, t=1000, shift=0, focused=False):
        if k is None:
            k = (width * height / len(pos.keys())) ** 0.5
        k_sq = k ** 2

        pos_array = np.array(list(pos.values()))
        node_indices = {node.id: idx for idx, node in enumerate(pos.keys())}

        while t > 0.1:
            print(f"at step: {t}")

            disps = np.zeros_like(pos_array)

            # Repell
            # Calculate repulsive forces
            delta = pos_array[:, np.newaxis, :] - pos_array[np.newaxis, :, :]
            distance = np.linalg.norm(delta, axis=2)
            safe_distance = np.where(distance > 0, distance, 1)  # Avoid division by zero
            repulsive_force = k_sq / safe_distance ** 3
            displacement = np.sum(delta * (repulsive_force[:, :, np.newaxis]), axis=1)

            # Attract
            for i, j in edge_list:
                if i not in pos.keys() or j not in pos.keys():
                    continue
                idx_i = node_indices[i.id]
                idx_j = node_indices[j.id]
                delta = pos_array[idx_i] - pos_array[idx_j]
                dist = np.linalg.norm(delta)
                if dist > 0:
                    attractive_force = (dist ** 2 / k) * (delta / dist)
                    displacement[idx_i] -= attractive_force
                    displacement[idx_j] += attractive_force

            # Cool
            # Limit displacement
            disp_norm = np.linalg.norm(displacement, axis=1)
            limited_disp = (np.minimum(disp_norm, t) / disp_norm)[:, np.newaxis] * displacement
            pos_array += limited_disp
            pos_array = np.clip(pos_array, [0, 0], [width, height])

            t *= 0.9

        pos_key_list = [node for node in pos.keys()]
        for i, pos_end in enumerate(pos_array):
            for n, nb in self.cem.node_buttons:
                if n == pos_key_list[i]:
                    nb.set_position(pos_end[0], pos_end[1])
                    break
        print(f"done")
