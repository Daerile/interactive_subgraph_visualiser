import pygame as pg
import pygame_gui as pgui
import numpy as np
import pandas as pd
import networkx as nx
from random import random
from src.view.node_button import NodeButton
from src.view.canvas_element_manager import CanvasElementManager
from src.backend.node import Node
from src.backend.graph_system import GraphSystem
from src.viewmodel.loader import Loader


class ViewModel:
    def __init__(self):
        self.column_names = None
        self.data = None
        self.graph_system = None

    def create_digraph(self, must_have_pairings, optional_pairings):
        self.graph_system = GraphSystem(self.data, self.column_names, must_have_pairings, optional_pairings)
        return self.graph_system.digraph

    def handle_load_button_pressed(self):
        data = Loader.load_file()
        if data is None:
            return None
        else:
            print(f'Data loaded')
            self.data = data
            self.column_names = data.columns
            return self.column_names

    def handle_node_focused(self, focused_node, focused_depth):
        if focused_node is None:
            return None
        focused_subgraph = self.graph_system.get_subgraph(focused_node.id, focused_depth)
        print(focused_subgraph.nodes)
        return focused_subgraph

    def handle_save_button_pressed(self, export_digraph: nx.DiGraph):
        to_save = "csúcsid;alcsúcsid;kapcsolat\n"
        for node in export_digraph.nodes:
            to_save += node.focused_connections_to_csv()
        Loader.save_file(to_save)
