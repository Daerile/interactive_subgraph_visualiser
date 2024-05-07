import pygame as pg
import pygame_gui as pgui
import math
from src.view.node_button import NodeButton
from src.view.arrow import Arrow
from src.backend.node import Node
from src.view.layout import Layout


class CanvasElementManager:
    def __init__(self, digraph, window, manager, colors, node_radius=15, focused=False, focused_depth=None, focused_node=None):
        self.digraph = digraph
        self.window = window
        self.manager = manager
        self.NODE_RADIUS = node_radius
        self.colors = colors
        self.focused = focused
        self.focused_node = focused_node
        self.focused_depth = focused_depth
        self.selected_button = None

        self.node_buttons: [(Node, NodeButton)] = []
        self.arrows: [(Node, Node, Arrow)] = []
        self.layout = Layout(self.digraph, self)

    def move_all(self, dx, dy):
        for node, button in self.node_buttons:
            button.move(dx, dy)

    def zoom_all(self, zoom_lvl, scale_factor, cursor_pos):

        for node, button in self.node_buttons:
            button.zoom(zoom_lvl, scale_factor, cursor_pos)
        for arrow in self.arrows:
            arrow[2].zoom(scale_factor)

    def change_colors(self, colors):
        self.colors = colors
        for node, button in self.node_buttons:
            button.change_colors(colors)
        for arrow in self.arrows:
            arrow[2].change_color(colors['edge'])

    def selected_node_changed(self, selected_button):
        if selected_button == self.selected_button:
            return
        for node, button in self.node_buttons:
            if button == selected_button:
                button.change_colors(self.colors, selected=True)
            if self.selected_button is not None and button == self.selected_button:
                button.change_colors(self.colors)
        self.selected_button = selected_button

    def searched_nodes_changed(self, filtered_ids):
        if filtered_ids is None:
            for node, button in self.node_buttons:
                if button != self.selected_button:
                    button.change_colors(self.colors)
                else:
                    button.change_colors(self.colors, selected=True)
        else:
            for node, button in self.node_buttons:
                if button == self.selected_button:
                    button.change_colors(self.colors, selected=True)
                    continue
                if node.id in filtered_ids:
                    button.change_colors(self.colors, searched=True)
                else:
                    button.change_colors(self.colors)

    def center_around(self, x, y):
        diff_x = ((1280 + 300) / 2) - x
        diff_y = (720 / 2) - y
        for node, button in self.node_buttons:
            button.move(diff_x, diff_y)

    def draw_node_buttons(self):
        for node, button in self.node_buttons:
            button.draw()

    def draw_arrows(self):
        for arrow in self.arrows:
            arrow[2].draw()

    def create_node_button(self, x, y, node, child_num=0):
        button = NodeButton(self.window, x, y, self.NODE_RADIUS, node, self.colors['node'], self.colors['text'])
        self.node_buttons.append((node, button))

    def create_edges(self):
        for edge in self.digraph.edges():
            start_button, end_button = None, None
            for node, button in self.node_buttons:
                if node == edge[0]:
                    start_button = button
                if node == edge[1]:
                    end_button = button
            if start_button is not None and end_button is not None:
                self.create_arrow(self.colors['edge'], start_button, end_button, edge[0], edge[1])

    def create_arrow(self, color, start_button, end_button, node_start, node_end, arrow_size=2, arrowhead_size=3):
        arrow = Arrow(self.window, start_button, end_button, color, arrow_size, arrowhead_size)
        self.arrows.append((node_start, node_end, arrow))


