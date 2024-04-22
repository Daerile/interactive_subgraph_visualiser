import pygame as pg
import pygame_gui as pgui
import random
import math
import sys
from src.view.node_button import NodeButton
from src.view.ui_panel import UIPanel
import src.utils.layout as layout


class View:
    def __init__(self, digraph):
        pg.init()
        self.digraph = digraph
        self.WIDTH = 1280
        self.HEIGHT = 720
        self.PANEL_WIDTH = 300
        self.GRAPH_WIDTH = self.WIDTH - self.PANEL_WIDTH  # Width available for the graph
        self.GRAPH_HEIGHT = self.HEIGHT
        self.NODE_RADIUS = 3
        self.window = pg.display.set_mode((self.WIDTH, self.HEIGHT))
        self.manager = pgui.UIManager((self.WIDTH, self.HEIGHT))
        self.node_buttons = []
        self.ui_panel = UIPanel(self.window,self.manager, self.PANEL_WIDTH, self.HEIGHT)
        pg.display.set_caption('Interactive Subgraph Visualiser')
        self.positions = self.get_pos()

        self.initialize_node_buttons()

    def run(self):
        clock = pg.time.Clock()
        running = True
        while running:
            time_delta = clock.tick(60) / 1000.0
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                elif event.type == pg.MOUSEBUTTONDOWN:
                    for button in self.node_buttons:
                        if button.handle_click(event):
                            self.node_button_clicked(button)
                elif event.type == pgui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.ui_panel.infos[2]:
                        self.ui_panel.handle_popup_button_pressed()
                self.ui_panel.process_events(event)

            self.window.fill((255, 255, 255))
            self.draw_nodes()
            self.ui_panel.update(time_delta)
            self.ui_panel.draw_ui()
            pg.display.update()
        pg.quit()
        sys.exit()

    def node_button_clicked(self, button: NodeButton):
        self.ui_panel.update_information_box(button.node)

    def draw_nodes(self):
        for button in self.node_buttons:
            button.draw(self.window)

    def initialize_node_buttons(self):
        for (node, pos) in self.positions.items():
            x, y = pos
            button = NodeButton(surface=self.window, x=int((self.PANEL_WIDTH + x)), y=int(y), radius=self.NODE_RADIUS, node=node)
            self.node_buttons.append(button)

    def get_pos(self):
        pos = layout.rescale_layout(layout.fruchterman_reingold(self.digraph), self.GRAPH_WIDTH, self.GRAPH_HEIGHT)
        return pos

