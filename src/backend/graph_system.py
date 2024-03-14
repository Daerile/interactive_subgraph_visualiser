import pandas as pd
import networkx as nx

class GraphSystem:
    def __init__(self, dataframe: pd.DataFrame):
        self.dataframe = dataframe
        self.graphs = []
        self.create_graphs()


    def create_graphs(self):
        unprocessed_nodes = self.dataframe['csúcsid'].unique()
        process_queue = []
        digraph = None
        for node in unprocessed_nodes:
            if process_queue is None:
                process_queue = [node]
                digraph = nx.DiGraph()
            else:
