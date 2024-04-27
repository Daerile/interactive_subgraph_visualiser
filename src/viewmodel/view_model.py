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


def read_data():
    data = pd.read_csv('../data/allc_model_tulertkek_grafmegjeleníteshez.csv', sep=';')
    return data


class ViewModel:
    def __init__(self):
        data = read_data()
        self.graph_system = GraphSystem(data)

    def handle_load_button_pressed(self):
        data = Loader.load_file()
        if data is None:
            return None
        else:
            self.graph_system = GraphSystem(data)
            digraph = self.graph_system.digraph
            return digraph

    def handle_node_focused(self, focused_node):
        focused_subgraph = self.graph_system.get_subgraph(focused_node.id, 3)
        print(focused_subgraph.nodes)
        return focused_subgraph

