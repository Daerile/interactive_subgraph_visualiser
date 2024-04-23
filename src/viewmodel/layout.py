import pygame as pg
import pygame_gui as pgui
import numpy as np
import pandas as pd
import networkx as nx
from random import random
from src.view.node_button import NodeButton
from src.view.canvas_element_manager import CanvasElementManager
from src.backend.node import Node
from src.view.view import View

class Vector:

    @classmethod
    def add(cls, vec0: tuple[float, float], vec1: tuple[float, float]):
        return (vec0[0] + vec1[0], vec0[1] + vec1[1])

    @classmethod
    def sub(cls, vec0: tuple[float, float], vec1: tuple[float, float]):
        return (vec0[0] - vec1[0], vec0[1] - vec1[1])

    @classmethod
    def norm(cls, vec: tuple[float, float]):
        return (vec[0] ** 2 + vec[1] ** 2) ** 0.5

    @classmethod
    def mul(cls, vec: tuple[float, float], scalar: float):
        return (vec[0] * scalar, vec[1] * scalar)

    @classmethod
    def div(cls, vec: tuple[float, float], scalar: float):
        return (vec[0] / scalar, vec[1] / scalar)


class Layout:
    def __init__(self, digraph: nx.DiGraph, cem: CanvasElementManager):

        self.WIDTH = 3000
        self.HEIGHT = 3000

        self.nodes: list[Node] = [n for n in digraph.nodes]
        edge_list = [(lhs, rhs) for (lhs, rhs) in digraph.edges]

        self.node_map = {node.id: i for i, node in enumerate(self.nodes)}
        self.adjacency_list = [[] for _ in range(len(self.nodes))]
        self.complement_adjacency_list = [[] for _ in range(len(self.nodes))]

        for lhs, rhs in edge_list:
            self.adjacency_list[self.node_map[lhs.id]].append(self.node_map[rhs.id])
            self.complement_adjacency_list[self.node_map[rhs.id]].append(self.node_map[lhs.id])

        self.cem = cem

        self.positions = [(random() * 1280, random() * 720) for _ in range(len(self.nodes))]

        self.REST_H = self.HEIGHT / 2

        # DAG -> BFS
        visited = [False for _ in range(len(self.nodes))]
        level = [0] * len(self.nodes)
        queue = [self.node_map[n.id] for n in self.nodes if not self.complement_adjacency_list[self.node_map[n.id]]]

        for q in queue:
            visited[q] = True
            level[q] = 0

        while queue:
            current = queue.pop(0)
            for neighbour in self.adjacency_list[current]:
                if not visited[neighbour]:
                    visited[neighbour] = True
                    level[neighbour] = level[current] + 1
                    queue.append(neighbour)

        level_with: set[map[int, int]] = {}
        for i, l in enumerate(level):
            if l not in level_with:
                level_with[l] = {}
            level_with[l][i] = len(level_with[l])

        max_level = max(level_with.keys())

        for node in self.nodes:
            if (
                not self.adjacency_list[self.node_map[node.id]]
                and not self.complement_adjacency_list[self.node_map[node.id]]
            ):
                x = random() * self.WIDTH
                y = random() * self.REST_H

                self.cem.create_node_button(x, y, node)
                print(f"isolated: {node.id} at {x}, {y}")
                continue

            l = level[self.node_map[node.id]]

            order = level_with[l][self.node_map[node.id]]
            w = len(level_with[l])

            y = ((l + 1) / (max_level + 1)) * (self.HEIGHT - self.REST_H) + self.REST_H
            x = (order / w) * self.WIDTH

            self.cem.create_node_button(x, y, node)
            print(f"normal: {node.id} at {x}, {y}")

        self.cem.create_edges()

        self.k = (self.WIDTH * self.HEIGHT / len(self.nodes)) ** 0.5
        self.k_sq = self.k**2
        self.t = 100

        print(f"nodes: {len(self.nodes)}, edges: {len(edge_list)}")

    def draw(self, dt: float, window: pg.Surface):

        if self.t < 0.1:
            self.cem.draw_node_buttons()
            for i, neighbours in enumerate(self.adjacency_list):
                for j, node in enumerate(neighbours):
                    v = self.cem.node_buttons[i][1]
                    u = self.cem.node_buttons[j][1]

                    pg.draw.line(window, (255, 0, 0), (int(v.x), int(v.y)), (int(u.x), int(u.y)), 1)

            return

        print(f"at step: {self.t}")
        disps = [(0, 0) for _ in range(len(self.nodes))]

        # Repell
        for i in range(len(self.nodes)):
            n, nb = self.cem.node_buttons[i]
            x, y = nb.x, nb.y

            for j in range(len(self.nodes)):
                if i == j:
                    continue

                rhs_n, rhs_nb = self.cem.node_buttons[j]

                delta = Vector.sub((x, y), (rhs_nb.x, rhs_nb.y))
                delta_norm = Vector.norm(delta)

                if delta_norm < 0.05:
                    continue

                delta = Vector.div(delta, delta_norm)
                disps[i] = Vector.add(disps[i], Vector.mul(delta, self.k_sq / delta_norm))

        # Attract
        for i, neighbours in enumerate(self.adjacency_list):
            for j in neighbours:
                v = self.cem.node_buttons[i][1]
                u = self.cem.node_buttons[j][1]

                delta = Vector.sub((v.x, v.y), (u.x, u.y))
                delta_norm = Vector.norm(delta)

                if delta_norm < 0.05:
                    continue

                delta = Vector.div(delta, delta_norm)

                disps[i] = Vector.sub(disps[i], Vector.mul(delta, self.k_sq / delta_norm))
                disps[j] = Vector.add(disps[j], Vector.mul(delta, self.k_sq / delta_norm))

        # Cool
        for i in range(len(self.nodes)):
            n, nb = self.cem.node_buttons[i]

            x, y = nb.x, nb.y
            disp = disps[i]
            disp_norm = Vector.norm(disp)

            if delta_norm < 0.05:
                nb.draw()
                continue

            if min(disp_norm, self.t) == 0:
                nb.draw()
                continue

            pos = Vector.mul(Vector.div(disp, disp_norm), min(disp_norm, self.t))

            pos = (min(max(nb.x + pos[0], 0), self.WIDTH), min(max(nb.y + pos[1], 0), self.HEIGHT))

            nb.x = pos[0] + 300
            nb.y = pos[1]
        self.t /= 1.8

        for i in range(len(self.nodes)):
            n, nb = self.cem.node_buttons[i]
            nb.draw()

        self.cem.draw_node_buttons()

        for i, neighbours in enumerate(self.adjacency_list):
            for j, node in enumerate(neighbours):
                v = self.cem.node_buttons[i][1]
                u = self.cem.node_buttons[j][1]

                pg.draw.line(window, (255, 0, 0), (int(v.x), int(v.y)), (int(u.x), int(u.y)), 5)