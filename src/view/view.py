import pygame as pg
import pygame_gui as pgui
import networkx as nx
import sys
from src.view.node_button import NodeButton
from src.view.ui_panel import UIPanel
from src.view.ui_header import UIHeader
from src.view.ui_graph import UIGraph
from src.viewmodel.view_model import ViewModel
import time
import os
import json


class View:
    # Constructor for the View class
    def __init__(self, digraph: nx.DiGraph, focused_graph: nx.DiGraph = None, focused=False):
        pg.init()

        self.digraph = digraph
        self.focused_graph = focused_graph
        self.focused = focused
        self.view_model = ViewModel()
        self.WIDTH = 1280
        self.HEIGHT = 720
        self.HEADER_WIDTH = self.WIDTH
        self.HEADER_HEIGHT = 35
        self.PANEL_WIDTH = 380
        self.PANEL_HEIGHT = self.HEIGHT - self.HEADER_HEIGHT + 5
        self.GRAPH_WIDTH = self.WIDTH - self.PANEL_WIDTH + 5  # Width available for the graph
        self.GRAPH_HEIGHT = self.HEIGHT - self.HEADER_HEIGHT + 5
        self.NODE_RADIUS = 15
        self.window = pg.display.set_mode((self.WIDTH, self.HEIGHT), pg.RESIZABLE)

        relative_path = "view/assets/theme.json"
        relative_path_for_close_image = "view/assets/close.jpeg"
        relative_path_for_open_image = "view/assets/open.jpeg"
        absolute_path = os.path.abspath(relative_path)
        absolute_path_for_close_image = os.path.abspath(relative_path_for_close_image)
        absolute_path_for_open_image = os.path.abspath(relative_path_for_open_image)
        print(absolute_path)
        self.theme_path = absolute_path

        with open(self.theme_path, 'r') as file:
            data = json.load(file)
        data["#panel_close_button"]["images"]["normal_image"]["path"] = absolute_path_for_close_image
        data["#panel_open_button"]["images"]["normal_image"]["path"] = absolute_path_for_open_image
        with open(self.theme_path, "w") as file:
            json.dump(data, file, indent=4)

        self.manager = pgui.UIManager((self.WIDTH, self.HEIGHT), theme_path=self.theme_path)
        self.ui_panel = UIPanel(
            self.window,
            self.manager,
            self.PANEL_WIDTH,
            self.PANEL_HEIGHT,
            self.digraph,
            2,
            3, 3,
            self.HEADER_HEIGHT
        )
        self.colors = self.ui_panel.handle_light_mode_pressed()
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
            self.colors
        )
        pg.display.set_caption("Interactive Subgraph Visualiser")
        self.dragging = False
        self.dragged_button = None
        self.dragged_button_x = 0
        self.dragged_button_y = 0
        self.res = None
        self.offset_x = 0
        self.offset_y = 0
        self.zoom_lvl = 0
        self.zoom_scale = 1.1 ** self.zoom_lvl

    # Method to run the main loop of the application
    def run(self):
        clock = pg.time.Clock()
        running = True

        while running:
            time_delta = clock.tick(60) / 1000.0
            running = self.handle_events()

            self.window.fill(self.colors['background'])
            self.ui_header.update(time_delta)
            self.ui_header.draw_ui()
            self.ui_panel.update(time_delta)
            self.ui_panel.draw_ui()
            self.ui_graph.update(time_delta)
            self.ui_graph.draw_ui()
            pg.display.update()
        pg.quit()
        sys.exit()

    # Method to handle all the events in the application
    def handle_events(self):
        running = True
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            self.ui_panel.process_events(event)
            self.ui_header.process_events(event)
            e = pg.VIDEORESIZE
            if event.type == pg.VIDEORESIZE:
                self.WIDTH = event.w
                self.HEIGHT = event.h
                self.HEADER_WIDTH = self.WIDTH
                self.HEADER_HEIGHT = 35
                self.PANEL_WIDTH = 380
                self.PANEL_HEIGHT = self.HEIGHT - self.HEADER_HEIGHT + 5
                self.GRAPH_WIDTH = self.WIDTH - self.PANEL_WIDTH + 5
                self.GRAPH_HEIGHT = self.HEIGHT - self.HEADER_HEIGHT + 5
                self.window = pg.display.set_mode((self.WIDTH, self.HEIGHT), pg.RESIZABLE)
                self.manager = pgui.UIManager((self.WIDTH, self.HEIGHT), theme_path=self.theme_path)
                self.ui_graph.resize(self.GRAPH_WIDTH, self.GRAPH_HEIGHT, self.window, self.manager)
                self.ui_panel.resize(self.PANEL_WIDTH, self.PANEL_HEIGHT, self.window, self.manager)
                self.ui_header.resize(self.HEADER_WIDTH, self.HEADER_HEIGHT, self.window, self.manager)
            if event.type == pg.MOUSEBUTTONDOWN:
                was_button = False
                was_edge = False
                for node, button in self.ui_graph.get_node_buttons():
                    res = button.handle_click(event, time.time())
                    if res > 0 and self.ui_panel.popup is None and self.ui_header.popup is None and event.button == 1:
                        was_button = True
                        self.dragged_button = button
                        self.dragged_button_x = button.x
                        self.dragged_button_y = button.y
                        self.res = res
                        break
                if not was_button:
                    for arrow in self.ui_graph.get_arrows():
                        res = arrow[2].handle_click(event)
                        if res == 1 and self.ui_panel.popup is None and self.ui_header.popup is None and event.button == 1:
                            self.edge_clicked(arrow)
                            was_edge = True
                            break
                if not was_button and not was_edge:
                    if event.button == 1:
                        mouse_x, mouse_y = event.pos
                        if self.ui_panel.popup is None and self.ui_header.popup is None and mouse_x > self.PANEL_WIDTH and mouse_y > self.HEADER_HEIGHT:
                            self.dragging = True
                            self.offset_x = mouse_x
                            self.offset_y = mouse_y
                    if event.button == 4:
                        if self.zoom_scale < 3:
                            mouse_x, mouse_y = event.pos
                            if self.ui_panel.popup is None and self.ui_header.popup is None and mouse_x > self.PANEL_WIDTH and mouse_y > self.HEADER_HEIGHT:
                                self.zoom_lvl += 1
                                self.zoom_scale = 1.1 ** self.zoom_lvl
                                self.ui_graph.zoom_all(self.zoom_lvl, 1.1, event.pos)
                    if event.button == 5:
                        if self.zoom_scale > 1 / 3:
                            mouse_x, mouse_y = event.pos
                            if self.ui_panel.popup is None and self.ui_header.popup is None and mouse_x > self.PANEL_WIDTH and mouse_y > self.HEADER_HEIGHT:
                                self.zoom_lvl -= 1
                                self.zoom_scale = 1.1 ** self.zoom_lvl
                                self.ui_graph.zoom_all(self.zoom_lvl, 100 / 110, event.pos)
            elif event.type == pg.MOUSEBUTTONUP:
                if event.button == 1:
                    self.dragging = False
                    button = self.dragged_button
                    self.dragged_button = None
                    if self.res == 1 and button.x == self.dragged_button_x and button.y == self.dragged_button_y:
                        self.node_button_clicked(button)
                    if self.res == 2:
                        print(f'Double clicked button {button.text}')
                        focused_depth = self.ui_panel.get_focused_depth()
                        vertical_scatter = self.ui_panel.get_vertical_scatter()
                        horizontal_scatter = self.ui_panel.get_horizontal_scatter()
                        focused_digraph = self.view_model.handle_node_focused(button.node,
                                                                              focused_depth)
                        self.focus_changed(focused_digraph)
                        self.ui_graph.handle_node_focused(focused_digraph, button.node, focused_depth, vertical_scatter,
                                                          horizontal_scatter)
                    self.res = None
            elif event.type == pg.MOUSEMOTION:
                if self.dragged_button is not None:
                    mouse_x, mouse_y = event.pos
                    self.dragged_button.set_position(mouse_x, mouse_y)
                if self.dragging:
                    mouse_x, mouse_y = event.pos
                    dx = mouse_x - self.offset_x
                    dy = mouse_y - self.offset_y
                    self.offset_x = mouse_x
                    self.offset_y = mouse_y
                    self.ui_graph.move_all(dx, dy)

            elif event.type == pgui.UI_BUTTON_PRESSED:
                if event.ui_element == self.ui_panel.search_box['search_by_id_button']:
                    self.ui_panel.handle_search_by_id_button_pressed()
                elif event.ui_element == self.ui_panel.search_box['search_by_name_button']:
                    self.ui_panel.handle_search_by_name_button_pressed()
                elif event.ui_element == self.ui_panel.close_button:
                    self.ui_panel.handle_close_button_pressed()
                elif event.ui_element == self.ui_panel.edit_box['dark_mode']:
                    self.dark_mode_pressed()
                elif event.ui_element == self.ui_panel.edit_box['light_mode']:
                    self.light_mode_pressed()
                elif event.ui_element == self.ui_panel.edit_box['personal_mode']:
                    self.personal_mode_pressed()
                elif event.ui_element == self.ui_panel.switch_panel['search']:
                    self.ui_panel.handle_switch_search_pressed()
                elif event.ui_element == self.ui_panel.switch_panel['edit']:
                    self.ui_panel.handle_switch_edit_pressed()
                elif event.ui_element == self.ui_panel.search_box['return_button']:
                    self.ui_graph.handle_return_button_pressed()
                    self.focus_changed(self.digraph)
                elif event.ui_element == self.ui_panel.infos['show_popup_button']:
                    self.ui_panel.handle_popup_button_pressed()
                elif event.ui_element == self.ui_panel.search_box['focus_button']:
                    self.ui_panel.handle_focus_button_pressed()
                    focused_node = self.ui_panel.get_focused_node()
                    if focused_node is None:
                        continue
                    focused_depth = self.ui_panel.get_focused_depth()
                    vertical_scatter = self.ui_panel.get_vertical_scatter()
                    horizontal_scatter = self.ui_panel.get_horizontal_scatter()
                    focused_digraph = self.view_model.handle_node_focused(focused_node,
                                                                          focused_depth)
                    self.focus_changed(focused_digraph)
                    self.ui_graph.handle_node_focused(focused_digraph, focused_node, focused_depth, vertical_scatter,
                                                      horizontal_scatter)
                elif event.ui_element == self.ui_header.load_button:
                    column_names = self.view_model.handle_load_button_pressed()
                    if column_names is None:
                        continue
                    self.ui_header.handle_load_button_pressed(column_names)
                elif event.ui_element == self.ui_header.save_button:
                    export_digraph = self.ui_graph.get_focused_digraph()
                    if export_digraph is None:
                        continue
                    self.view_model.handle_save_button_pressed(export_digraph)
                elif event.ui_element == self.ui_header.help_button:
                    self.ui_header.handle_help_button_pressed()
                elif self.ui_header.menu_buttons is not None and event.ui_element in self.ui_header.menu_buttons.values():
                    self.ui_header.handle_menu_button_pressed(event.ui_element)
                elif self.ui_header.load_popup_items is not None and event.ui_element == \
                        self.ui_header.load_popup_items['okay_button']:
                    (must_have_pairings, optional_pairings) = self.ui_header.handle_load_popup_okay_button_pressed()
                    self.digraph = self.view_model.create_digraph(must_have_pairings, optional_pairings)
                    self.digraph_loaded(optional_pairings)
                elif self.ui_header.load_popup_items is not None and event.ui_element == \
                        self.ui_header.load_popup_items[
                            'cancel_button']:
                    self.ui_header.handle_load_popup_cancel_button_pressed()

            elif event.type == pgui.UI_TEXT_ENTRY_CHANGED:
                if event.ui_element == self.ui_panel.search_box['search_text']:
                    filtered_info, mode = self.ui_panel.handle_search_bar_changed()
                    self.ui_graph.handle_searched_nodes_changed(filtered_info, mode)
            elif event.type == pgui.UI_WINDOW_CLOSE:
                if event.ui_element == self.ui_panel.popup:
                    self.ui_panel.popup = None
                if event.ui_element == self.ui_header.popup:
                    self.ui_header.popup = None
            elif event.type == pgui.UI_DROP_DOWN_MENU_CHANGED:
                if self.ui_header.load_popup_items is not None:
                    if event.ui_element in self.ui_header.load_popup_items['must_have'] + \
                            self.ui_header.load_popup_items['optional']:
                        self.ui_header.handle_must_have_dropdown_changed()

        return running

    # Method to handle the event of light mode being pressed
    def light_mode_pressed(self):
        colors = self.ui_panel.handle_light_mode_pressed()
        self.colors = colors
        self.ui_graph.change_colors(colors)

    # Method to handle the event of dark mode being pressed
    def dark_mode_pressed(self):
        colors = self.ui_panel.handle_dark_mode_pressed()
        self.colors = colors
        self.ui_graph.change_colors(colors)

    # Method to handle the event of personal mode being pressed
    def personal_mode_pressed(self):
        colors = self.ui_panel.handle_personal_mode_pressed()
        self.colors = colors
        self.ui_graph.change_colors(colors)

    # Method to handle the event of a node button being clicked
    def node_button_clicked(self, button: NodeButton):
        self.ui_panel.update_information_box(button.node)
        self.ui_graph.handle_node_selected(button)

    # Method to handle the event of an edge being clicked
    def edge_clicked(self, arrow):
        self.ui_panel.update_information_box(arrow, edge=True)
        self.ui_graph.handle_edge_selected(arrow)

    # Method to handle the event of the focus being changed
    def focus_changed(self, focused_digraph):
        self.zoom_lvl = 0
        focused_depth = self.ui_panel.get_focused_depth()
        horizontal_scatter = self.ui_panel.get_horizontal_scatter()
        vertical_scatter = self.ui_panel.get_vertical_scatter()
        ui_panel_closed = self.ui_panel.closed
        optional_pairings = self.ui_panel.optional_pairings
        self.ui_panel.killall()
        self.ui_panel = UIPanel(
            self.window,
            self.manager,
            self.PANEL_WIDTH,
            self.PANEL_HEIGHT,
            focused_digraph,
            focused_depth,
            vertical_scatter,
            horizontal_scatter,
            self.HEADER_HEIGHT,
            colors=self.colors,
            optional_pairings=optional_pairings
        )
        if ui_panel_closed:
            self.ui_panel.handle_close_button_pressed()
        self.ui_panel.update(0)
        self.ui_panel.draw_ui()

    # Method to handle the event of a digraph being loaded
    def digraph_loaded(self, optional_pairings):
        self.zoom_lvl = 0
        self.ui_panel.killall()
        self.ui_header.killall()

        self.ui_panel = UIPanel(
            self.window,
            self.manager,
            self.PANEL_WIDTH,
            self.PANEL_HEIGHT,
            self.digraph,
            2,
            3,
            3,
            self.HEADER_HEIGHT,
            colors=self.colors,
            optional_pairings=optional_pairings
        )
        self.ui_graph.digraph_loaded(self.digraph)
        self.ui_header = UIHeader(self.window, self.manager, self.HEADER_WIDTH, self.HEADER_HEIGHT, self.digraph)

        self.ui_panel.update(0)
        self.ui_panel.draw_ui()
        self.ui_graph.update(0)
        self.ui_graph.draw_ui()
        self.ui_header.update(0)
        self.ui_header.draw_ui()
        pg.display.update()
        self.run()
