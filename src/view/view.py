from time import sleep
import pygame as pg
import pygame_gui as pgui
import networkx as nx
import sys
from src.view.node_button import NodeButton
from src.view.ui_panel import UIPanel
from src.view.ui_header import UIHeader
from src.view.ui_graph import UIGraph
from src.view.canvas_element_manager import CanvasElementManager
from src.viewmodel.view_model import ViewModel
import time


class View:
    def __init__(self, digraph: nx.DiGraph):
        pg.init()

        self.digraph = digraph
        self.view_model = ViewModel()
        self.WIDTH = 1280
        self.HEIGHT = 720
        self.HEADER_WIDTH = self.WIDTH
        self.HEADER_HEIGHT = 35
        self.PANEL_WIDTH = 300
        self.PANEL_HEIGHT = self.HEIGHT - self.HEADER_HEIGHT + 5
        self.GRAPH_WIDTH = self.WIDTH - self.PANEL_WIDTH + 5  # Width available for the graph
        self.GRAPH_HEIGHT = self.HEIGHT - self.HEADER_HEIGHT + 5
        self.NODE_RADIUS = 15
        self.window = pg.display.set_mode((self.WIDTH, self.HEIGHT))
        self.manager = pgui.UIManager((self.WIDTH, self.HEIGHT))
        self.canvas_element_manager = CanvasElementManager(self.digraph, self.window, self.manager, self.NODE_RADIUS)
        self.ui_panel = UIPanel(self.window, self.manager, self.PANEL_WIDTH, self.PANEL_HEIGHT, self.digraph, self.HEADER_HEIGHT)
        self.ui_header = UIHeader(self.window, self.manager, self.HEADER_WIDTH, self.HEADER_HEIGHT, self.digraph)
        self.ui_graph = UIGraph(
            self.window,
            self.manager,
            self.GRAPH_WIDTH,
            self.GRAPH_HEIGHT,
            self.NODE_RADIUS,
            self.digraph,
            self.PANEL_WIDTH,
            self.HEADER_HEIGHT,
            self.canvas_element_manager,
        )
        pg.display.set_caption("Interactive Subgraph Visualiser")
        self.dragging = False
        self.offset_x = 0
        self.offset_y = 0
        self.zoom_scale = 1.0

        #self.graph = Graph(self.digraph, self.canvas_element_manager)

    def run(self):
        clock = pg.time.Clock()
        running = True

        while running:

            time_delta = clock.tick(60) / 1000.0
            running = self.handle_events()

            self.window.fill((255, 255, 255))
            self.ui_graph.draw_ui()
            self.ui_header.update(time_delta)
            self.ui_header.draw_ui()
            self.ui_panel.update(time_delta)
            self.ui_panel.draw_ui()
            self.ui_graph.update(time_delta)
            self.ui_graph.draw_ui()
            pg.display.update()
        pg.quit()
        sys.exit()

    def handle_events(self):
        running = True
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

            self.ui_panel.process_events(event)
            self.ui_header.process_events(event)

            if event.type == pg.MOUSEBUTTONDOWN:
                was_button = False
                for node, button in self.canvas_element_manager.node_buttons:
                    res = button.handle_click(event, time.time())
                    if res > 0 and self.ui_panel.popup is None and event.button == 1:
                        was_button = True
                        if res == 1:
                            self.node_button_clicked(button)
                        if res == 2:
                            print(f'Double clicked button {button.text}')
                if not was_button:
                    if event.button == 1:
                        mouse_x, mouse_y = event.pos
                        if self.ui_panel.popup is None and mouse_x > self.PANEL_WIDTH and mouse_y > self.HEADER_HEIGHT:
                            self.dragging = True
                            self.offset_x = mouse_x
                            self.offset_y = mouse_y
                    if event.button == 4:
                        if self.zoom_scale < 3:
                            mouse_x, mouse_y = event.pos
                            if self.ui_panel.popup is None and mouse_x > self.PANEL_WIDTH and mouse_y > self.HEADER_HEIGHT:
                                self.zoom_scale *= 1.1
                                self.canvas_element_manager.zoom_all(self.zoom_scale, 1.1, event.pos)
                    if event.button == 5:
                        if self.zoom_scale > 1 / 3:
                            mouse_x, mouse_y = event.pos
                            if self.ui_panel.popup is None and mouse_x > self.PANEL_WIDTH and mouse_y > self.HEADER_HEIGHT:
                                self.zoom_scale *= 0.9
                                self.canvas_element_manager.zoom_all(self.zoom_scale, 0.9, event.pos)
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
                    self.canvas_element_manager.move_all(dx, dy)

            elif event.type == pgui.UI_BUTTON_PRESSED:
                if event.ui_element == self.ui_panel.infos[2]:
                    self.ui_panel.handle_popup_button_pressed()
                if event.ui_element == self.ui_panel.search_box[4]:
                    self.ui_panel.handle_focus_button_pressed()
                if event.ui_element == self.ui_header.load_button:
                    new_digraph = self.view_model.handle_load_button_pressed()
                    if new_digraph is None:
                        continue
                    self.digraph = new_digraph
                    self.digraph_changed()
            elif event.type == pgui.UI_TEXT_ENTRY_CHANGED:
                if event.ui_element == self.ui_panel.search_box[2]:
                    self.ui_panel.handle_search_bar_changed()
            elif event.type == pgui.UI_WINDOW_CLOSE:
                if event.ui_element == self.ui_panel.popup:
                    self.ui_panel.popup = None
        return running

    def node_button_clicked(self, button: NodeButton):
        self.ui_panel.update_information_box(button.node)

    def digraph_changed(self):
        self.ui_panel.killall()
        self.ui_header.killall()
        self.canvas_element_manager = CanvasElementManager(self.digraph, self.window, self.manager, self.NODE_RADIUS)
        self.ui_panel = UIPanel(self.window, self.manager, self.PANEL_WIDTH, self.PANEL_HEIGHT, self.digraph, self.HEADER_HEIGHT)
        self.ui_graph.digraph_changed(self.digraph, self.canvas_element_manager)
        self.ui_header = UIHeader(self.window, self.manager, self.HEADER_WIDTH, self.HEADER_HEIGHT, self.digraph)

        self.ui_panel.update(0)
        self.ui_panel.draw_ui()
        self.ui_graph.update(0)
        self.ui_graph.draw_ui()
        self.ui_header.update(0)
        self.ui_header.draw_ui()
        pg.display.update()
        sleep(0.1)
        self.run()