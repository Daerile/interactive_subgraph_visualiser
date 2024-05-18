import math

import networkx as nx
import pandas as pd

class Node:
    def __init__(self, node: pd.Series, column_names, must_have_pairings, optional_pairings):
        self.column_names = column_names
        self.id = str(node[must_have_pairings['node_id']])
        self.sub_ids = [str(node[must_have_pairings['sub_id']])]
        self.sub_id = str(node[must_have_pairings['sub_id']])
        if optional_pairings['node_name'] != 'None':
            self.name = node[optional_pairings['node_name']]
            self.names = [node[optional_pairings['node_name']]]
        else:
            self.name = None
            self.names = []
        self.must_have_pairings = must_have_pairings
        self.optional_pairings = optional_pairings
        self.connections = self.init_connections(node)

        self.attributes = self.init_attributes(node)

        self.focused_connections = None

    def init_attributes(self, node):
        starter_dict = {
            'connections': self.connections
        }

        for column_name in self.column_names:
            if column_name not in self.must_have_pairings.values() and column_name not in self.optional_pairings.values():
                starter_dict.update({column_name: node[column_name]})

        return starter_dict

    def init_connections(self, node):
        try:
            if math.isnan(node[self.must_have_pairings['connections']]):
                return None
        except TypeError:
            ret_dict = {
                node[self.must_have_pairings['sub_id']]: node[self.must_have_pairings['connections']].split(',')
            }
            return ret_dict

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

    def add_connections(self, node):
        try:
            if math.isnan(node[self.must_have_pairings['connections']]):
                return self.connections
        except TypeError:
            new_dict = {
                node[self.must_have_pairings['sub_id']]: node[self.must_have_pairings['connections']].split(',')
            }
            if self.connections is not None:
                return self.connections.update(new_dict)
            else:
                return new_dict

    def append_diff_sub_id(self, node: pd.Series):
        self.sub_ids.append(node[self.must_have_pairings['sub_id']])
        if self.names:
            self.names.append(node[self.optional_pairings['node_name']])
        self.connections = self.add_connections(node)

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