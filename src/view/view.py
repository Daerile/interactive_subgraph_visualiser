import pygame as pg
import pygame_gui as pgui
import networkx as nx
import random
import math
import sys
from src.view.node_button import NodeButton
from src.view.ui_panel import UIPanel
from src.view.canvas_element_manager import CanvasElementManager
import src.utils.layout as layout


class View:
    def __init__(self, digraph: nx.DiGraph):
        pg.init()
        self.digraph = digraph
        self.WIDTH = 1280
        self.HEIGHT = 720
        self.PANEL_WIDTH = 300
        self.GRAPH_WIDTH = self.WIDTH - self.PANEL_WIDTH  # Width available for the graph
        self.GRAPH_HEIGHT = self.HEIGHT
        self.NODE_RADIUS = 15
        self.window = pg.display.set_mode((self.WIDTH, self.HEIGHT))
        self.manager = pgui.UIManager((self.WIDTH, self.HEIGHT))
        self.CanvasElementManager = CanvasElementManager(self.digraph, self.window, self.manager, self.NODE_RADIUS)
        self.ui_panel = UIPanel(self.window,self.manager, self.PANEL_WIDTH, self.HEIGHT, self.digraph)
        pg.display.set_caption('Interactive Subgraph Visualiser')
        self.positions = self.get_pos()
        self.dragging = False
        self.offset_x = 0
        self.offset_y = 0
        self.zoom_scale = 1.0

        self.initialize_elements()

    def run(self):
        clock = pg.time.Clock()
        running = True
        while running:
            time_delta = clock.tick(60) / 1000.0
            running = self.handle_events()

            self.window.fill((255, 255, 255))
            self.draw_elements()
            self.ui_panel.update(time_delta)
            self.ui_panel.draw_ui()
            pg.display.update()
        pg.quit()
        sys.exit()

    def handle_events(self):
        running = True
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

            self.ui_panel.process_events(event)

            if event.type == pg.MOUSEBUTTONDOWN:
                was_button = False
                for node, button in self.CanvasElementManager.node_buttons:
                    if button.handle_click(event):
                        was_button = True
                        self.node_button_clicked(button)
                if not was_button:
                    if event.button == 1:
                        self.dragging = True
                        mouse_x, mouse_y = event.pos
                        self.offset_x = mouse_x
                        self.offset_y = mouse_y
                    if event.button == 4:
                        if self.zoom_scale < 3:
                            self.zoom_scale *= 1.1
                            self.CanvasElementManager.zoom_all(self.zoom_scale, 1.1, event.pos)
                    if event.button == 5:
                        if self.zoom_scale > 1/3:
                            self.zoom_scale *= 0.9
                            self.CanvasElementManager.zoom_all(self.zoom_scale, 0.9, event.pos)
            elif event.type == pg.MOUSEBUTTONUP:
                if event.button == 1:
                    self.dragging = False
            elif event.type == pg.MOUSEMOTION:
                if self.dragging:
                    mouse_x, mouse_y = event.pos
                    dx = mouse_x - self.offset_x
                    dy = mouse_y - self.offset_y
                    self.offset_x = mouse_x
                    self.offset_y = mouse_y
                    self.CanvasElementManager.move_all(dx, dy)

            elif event.type == pgui.UI_BUTTON_PRESSED:
                if event.ui_element == self.ui_panel.infos[2]:
                    self.ui_panel.handle_popup_button_pressed()
            elif event.type == pgui.UI_TEXT_ENTRY_CHANGED:
                if event.ui_element == self.ui_panel.search_box[2]:
                    self.ui_panel.handle_search_bar_changed()
        return running

    def node_button_clicked(self, button: NodeButton):
        self.ui_panel.update_information_box(button.node)

    def draw_elements(self):
        self.CanvasElementManager.draw_node_buttons()
        self.CanvasElementManager.draw_arrows()

    def initialize_elements(self):
        for (node, pos) in self.positions.items():
            x, y = pos
            self.CanvasElementManager.create_node_button(x + self.PANEL_WIDTH, y, node)
        self.CanvasElementManager.create_edges()

    def get_pos(self):
        pos = layout.rescale_layout(layout.fruchterman_reingold(self.digraph), self.GRAPH_WIDTH, self.GRAPH_HEIGHT)
        return pos

