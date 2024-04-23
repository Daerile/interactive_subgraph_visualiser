import pygame as pg
import pygame_gui as pgui
import numpy as np
import pandas as pd
import networkx as nx
from random import random
from src.view.node_button import NodeButton
from src.view.canvas_element_manager import CanvasElementManager
from src.backend.node import Node
from src.view.view import View


def read_data():
    data = pd.read_csv('../data/allc_model_tulertkek_grafmegjeleníteshez.csv', sep=';')
    return data


class ViewModel:
    def __init__(self):
        self.digraph = None
        self.view = None
        self.startup()

    def startup(self):
        self.digraph = nx.DiGraph()
        self.view = View(self.digraph)
        self.view.run()
