import pygame as pg
import pygame_gui as pgui

from src.view.layout import Layout


class UIGraph:
    def __init__(self, window, manager, width, height, node_radius, digraph, panel_width, header_height, cem):
        self.window = window
        self.width = width
        self.height = height
        self.node_radius = node_radius
        self.manager = manager
        self.digraph = digraph
        self.panel_width = panel_width
        self.header_height = header_height
        self.canvas_element_manager = cem
        self.layout = Layout(self.digraph, self.canvas_element_manager)

    def digraph_changed(self, digraph, cem):
        self.digraph = digraph
        self.canvas_element_manager = cem
        self.layout = Layout(self.digraph, self.canvas_element_manager)

    def process_events(self, event):
        self.manager.process_events(event)

    def draw_ui(self):
        if len(self.digraph) != 0:
            self.layout.draw()
        self.manager.draw_ui(self.window)

    def get_manager(self):
        return self.manager

    def update(self, time_delta):
        self.manager.update(time_delta)
