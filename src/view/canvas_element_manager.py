import pygame as pg
import pygame_gui as pgui
import math
from src.view.node_button import NodeButton
from src.view.arrow import Arrow
from src.backend.node import Node
from src.view.layout import Layout


class CanvasElementManager:
    def __init__(self, digraph, window, manager, node_radius=15, focused=False, focused_depth=None, focused_node=None):
        self.digraph = digraph
        self.window = window
        self.manager = manager
        self.NODE_RADIUS = node_radius
        self.focused = focused
        self.focused_node = focused_node
        self.focused_depth = focused_depth
        self.offset_x = 0
        self.offset_y = 0

        self.node_buttons: [(Node, NodeButton)] = []
        self.arrows: [(Node, Node, Arrow)] = []
        self.layout = Layout(self.digraph, self)

    def move_all(self, dx, dy):
        for node, button in self.node_buttons:
            button.move(dx, dy)

    def zoom_all(self, zoom_scale, scale_factor, cursor_pos):
        cursor_x, cursor_y = cursor_pos
        self.offset_x = cursor_x - (cursor_x - self.offset_x) * scale_factor
        self.offset_y = cursor_y - (cursor_y - self.offset_y) * scale_factor

        for node, button in self.node_buttons:
            button.zoom(zoom_scale)
        for arrow in self.arrows:
            arrow[2].zoom(zoom_scale)

        self.move_all(self.offset_x, self.offset_y)

    def draw_node_buttons(self):
        for node, button in self.node_buttons:
            button.draw()

    def draw_arrows(self):
        for arrow in self.arrows:
            arrow[2].draw()

    def create_node_button(self, x, y, node, color=(0, 0, 0)):
        button = NodeButton(self.window, x, y, self.NODE_RADIUS, node, color)
        self.node_buttons.append((node, button))

    def create_edges(self, color=(0, 0, 0)):
        for edge in self.digraph.edges():
            start_button, end_button = None, None
            for node, button in self.node_buttons:
                if node == edge[0]:
                    start_button = button
                if node == edge[1]:
                    end_button = button
            if start_button is not None and end_button is not None:
                self.create_arrow(color, start_button, end_button, edge[0], edge[1])

    def create_arrow(self, color, start_button, end_button, node_start, node_end, arrow_size=2, arrowhead_size=3):
        arrow = Arrow(self.window, start_button, end_button, color, arrow_size, arrowhead_size)
        self.arrows.append((node_start, node_end, arrow))


