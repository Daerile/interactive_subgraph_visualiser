import pygame as pg
import pygame_gui as pgui

from src.view.canvas_element_manager import CanvasElementManager

class UIGraph:
    def __init__(self, window, manager, width, height, node_radius, digraph, panel_width, header_height):
        self.window = window
        self.width = width
        self.height = height
        self.node_radius = node_radius
        self.manager = manager
        self.digraph = digraph
        self.panel_width = panel_width
        self.header_height = header_height
        self.focused_cem = None
        self.full_cem = CanvasElementManager(self.digraph, self.window, self.manager, self.node_radius)

    def digraph_loaded(self, digraph, ):
        self.digraph = digraph
        self.full_cem = CanvasElementManager(self.digraph, self.window, self.manager, self.node_radius)
        self.focused_cem = None

    def move_all(self, dx, dy):
        self.get_current_cem().move_all(dx, dy)

    def zoom_all(self, zoom_scale, scale_factor, cursor_pos):
        self.get_current_cem().zoom_all(zoom_scale, scale_factor, cursor_pos)

    def process_events(self, event):
        self.manager.process_events(event)

    def draw_ui(self):
        if len(self.digraph) != 0:
            self.get_current_cem().draw_arrows()
            self.get_current_cem().draw_node_buttons()
        self.manager.draw_ui(self.window)

    def handle_node_focused(self, focused_digraph, focused_node):
        self.focused_cem = CanvasElementManager(
            focused_digraph,
            self.window,
            self.manager,
            self.node_radius,
            focused=True,
            focused_depth=3,
            focused_node=focused_node
        )

    def get_node_buttons(self):
        return self.get_current_cem().node_buttons

    def get_arrows(self):
        return self.get_current_cem().arrows

    def get_manager(self):
        return self.manager

    def get_current_cem(self):
        if self.focused_cem is not None:
            return self.focused_cem
        else:
            return self.full_cem

    def update(self, time_delta):
        self.manager.update(time_delta)
