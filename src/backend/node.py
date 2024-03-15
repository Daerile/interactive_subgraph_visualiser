import math

import networkx as nx
import pandas as pd


class Node:
    def __init__(self, node: pd.Series):
        self.id = node['csúcsid']
        self.sub_id = node['alcsúcsid']
        self.connections = self.get_connections(node)
        self.attributes = {
            'id': self.id,
            'sub_id': self.sub_id,
            'connections': self.connections
        }

    def get_connections(self, node):
        try:
            if math.isnan(node['kapcsolat']):
                return None
        except TypeError:
            return node['kapcsolat'].split(',')
