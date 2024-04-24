import pygame as pg
import pygame_gui as pgui
import math
from src.view.node_button import NodeButton
from src.view.arrow import Arrow
from src.backend.node import Node


class CanvasElementManager:
    def __init__(self, digraph, window, manager, node_radius=15):
        self.digraph = digraph
        self.window = window
        self.manager = manager
        self.NODE_RADIUS = node_radius
        self.offset_x = 0
        self.offset_y = 0

        self.node_buttons: [(Node, NodeButton)] = []
        self.arrows: [(Node, Node, Arrow)] = []

    def move_all(self, dx, dy):
        for node, button in self.node_buttons:
            button.move(dx, dy)
        for arrow in self.arrows:
            arrow[2].move(dx, dy)

    def zoom_all(self, zoom_scale, scale_factor, cursor_pos):
        cursor_x, cursor_y = cursor_pos
        self.offset_x = cursor_x - (cursor_x - self.offset_x) * scale_factor
        self.offset_y = cursor_y - (cursor_y - self.offset_y) * scale_factor

        for node, button in self.node_buttons:
            button.zoom(zoom_scale)
        for arrow in self.arrows:
            arrow[2].zoom(zoom_scale)

        self.move_all(self.offset_x, self.offset_y)

    def create_node_button(self, x, y, node, color=(0, 0, 0)):
        button = NodeButton(self.window, x, y, self.NODE_RADIUS, node, color)
        self.node_buttons.append((node, button))

    def draw_node_buttons(self):
        for node, button in self.node_buttons:
            button.draw()

    def draw_arrows(self):
        for arrow in self.arrows:
            arrow[2].draw()

    def create_edges(self):
        for edge in self.digraph.edges():
            start_pos, end_pos = 0, 0
            for node, button in self.node_buttons:
                if node == edge[0]:
                    start_pos = button.x, button.y
                if node == edge[1]:
                    end_pos = button.x, button.y
            self.create_arrow((0, 0, 0), start_pos, end_pos, edge[0], edge[1])

    def create_arrow(self, color, start, end, node_start, node_end, arrow_size=2, arrowhead_size=3):
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        distance = math.sqrt(dx ** 2 + dy ** 2)
        if distance == 0:
            return

        dx /= distance
        dy /= distance

        end_adj = (end[0] - self.NODE_RADIUS * dx, end[1] - self.NODE_RADIUS * dy)

        main_line = (start, end_adj)

        angle = math.atan2(dy, dx)

        x1 = end_adj[0] - arrowhead_size * math.cos(angle - math.pi / 6)
        y1 = end_adj[1] - arrowhead_size * math.sin(angle - math.pi / 6)
        x2 = end_adj[0] - arrowhead_size * math.cos(angle + math.pi / 6)
        y2 = end_adj[1] - arrowhead_size * math.sin(angle + math.pi / 6)

        arrow_1 = ((x1, y1), end_adj)
        arrow_2 = ((x2, y2), end_adj)

        arrow = Arrow(self.window, [main_line, arrow_1, arrow_2], node_start, node_end, color, arrow_size, arrowhead_size)
        self.arrows.append((node_start, node_end, arrow))


