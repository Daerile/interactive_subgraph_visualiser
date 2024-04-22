import pygame as pg
import pygame_gui as pgui
import networkx as nx
import random
import math
import sys
from src.view.node_button import NodeButton
from src.view.ui_panel import UIPanel
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
        self.node_buttons = []
        self.arrows = []
        self.ui_panel = UIPanel(self.window,self.manager, self.PANEL_WIDTH, self.HEIGHT, self.digraph)
        pg.display.set_caption('Interactive Subgraph Visualiser')
        self.positions = self.get_pos()
        self.dragging = False
        self.offset_x = 0
        self.offset_y = 0

        self.initialize_node_buttons()
        self.initialize_arrows()

    def run(self):
        clock = pg.time.Clock()
        running = True
        while running:
            time_delta = clock.tick(60) / 1000.0
            running = self.handle_events()

            self.window.fill((255, 255, 255))
            self.draw_nodes()
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
                for button in self.node_buttons:
                    if button.handle_click(event):
                        was_button = True
                        self.node_button_clicked(button)
                if not was_button:
                    if event.button == 1:
                        self.dragging = True
                        mouse_x, mouse_y = event.pos
                        self.offset_x = mouse_x
                        self.offset_y = mouse_y
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
                    for button in self.node_buttons:
                        button.move(dx, dy)

            elif event.type == pgui.UI_BUTTON_PRESSED:
                if event.ui_element == self.ui_panel.infos[2]:
                    self.ui_panel.handle_popup_button_pressed()
            elif event.type == pgui.UI_TEXT_ENTRY_CHANGED:
                if event.ui_element == self.ui_panel.search_box[2]:
                    self.ui_panel.handle_search_bar_changed()
        return running

    def node_button_clicked(self, button: NodeButton):
        self.ui_panel.update_information_box(button.node)

    def draw_nodes(self):
        for button in self.node_buttons:
            button.draw(self.window)
        self.draw_edges()

    def draw_edges(self):
        for edge in self.digraph.edges():
            for button in self.node_buttons:
                if button.node == edge[0]:
                    start_pos = button.x, button.y
                if button.node == edge[1]:
                    end_pos = button.x, button.y
            self.draw_arrow(self.window, (0, 0, 0), start_pos, end_pos, edge[0], edge[1])

    def draw_arrow(self, window, color, start, end, node_start, node_end, arrow_size=10):
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        distance = math.sqrt(dx ** 2 + dy ** 2)
        if distance == 0:
            return

        dx /= distance
        dy /= distance

        end_adj = (end[0] - self.NODE_RADIUS * dx, end[1] - self.NODE_RADIUS * dy)

        main_line = pg.draw.line(window, color, start, end_adj, 2)

        angle = math.atan2(dy, dx)

        x1 = end_adj[0] - arrow_size * math.cos(angle - math.pi / 6)
        y1 = end_adj[1] - arrow_size * math.sin(angle - math.pi / 6)
        x2 = end_adj[0] - arrow_size * math.cos(angle + math.pi / 6)
        y2 = end_adj[1] - arrow_size * math.sin(angle + math.pi / 6)

        arrow_1 = pg.draw.line(window, color, (x1, y1), end_adj, 2)
        arrow_2 = pg.draw.line(window, color, (x2, y2), end_adj, 2)

        self.arrows.append((main_line, arrow_1, arrow_2, start, end, node_start, node_end))

    def initialize_node_buttons(self):
        for (node, pos) in self.positions.items():
            x, y = pos
            button = NodeButton(surface=self.window, x=int((self.PANEL_WIDTH + x)), y=int(y), radius=self.NODE_RADIUS, node=node)
            self.node_buttons.append(button)

    def initialize_arrows(self):
        self.draw_edges()

    def get_pos(self):
        pos = layout.rescale_layout(layout.fruchterman_reingold(self.digraph), self.GRAPH_WIDTH, self.GRAPH_HEIGHT)
        return pos

