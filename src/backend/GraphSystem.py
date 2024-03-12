import pandas as pd
import networkx as nx

class GraphSystem:
    def __init__(self, dataframe):
        self.dataframe = dataframe
        self.graphs = []