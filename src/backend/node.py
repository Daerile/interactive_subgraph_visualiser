import math

import networkx as nx
import pandas as pd


def init_connections(node):
    try:
        if math.isnan(node['kapcsolat']):
            return None
    except TypeError:
        ret_dict = {
            node['alcsúcsid']: node['kapcsolat'].split(',')
        }
        return ret_dict


def add_connections(node, connections):
    try:
        if math.isnan(node['kapcsolat']):
            return connections
    except TypeError:
        new_dict = {
            node['alcsúcsid']: node['kapcsolat'].split(',')
        }
        if connections is not None:
            return connections.update(new_dict)
        else:
            return new_dict


class Node:
    def __init__(self, node: pd.Series):
        self.id = node['csúcsid']
        self.sub_ids = [node['alcsúcsid']]
        self.sub_id = node['alcsúcsid']
        self.connections = init_connections(node)
        self.attributes = {
            'connections': self.connections
        }

        self.focused_connections = None

    def create_focused_connections(self, edges):
        self.focused_connections = {}
        for sub_id in self.sub_ids:
            connections = []
            for edge in edges:
                if self.connections is None or sub_id not in self.connections.keys():
                    continue
                if edge[0].id == self.id and edge[1].id in self.connections[sub_id]:
                    connections.append(edge[1].id)
            self.focused_connections.update({sub_id: connections})

    def append_diff_subid(self, node: pd.Series):
        self.sub_ids.append(node['alcsúcsid'])
        self.connections = add_connections(node, self.connections)

    def focused_connections_to_csv(self):
        if self.focused_connections is None:
            return None
        else:
            res = ""
            for key in self.focused_connections.keys():
                res += f"{self.id};{key};{','.join(self.focused_connections[key])}\n"
            return res

    def get_connected_nodes(self):
        return_set = set()
        if self.connections is None:
            return return_set
        else:
            for key in self.connections.keys():
                for value in self.connections[key]:
                    if value == '' or value == key:
                        continue
                    return_set.add(value)
            return return_set

    def get_id(self):
        return self.id

    def get_sub_id(self):
        return self.sub_id

    def get_attributes(self):
        if self.focused_connections is not None:
            return {'connections': self.focused_connections}
        return self.attributes

    def get_other_attributes(self):
        return self.attributes