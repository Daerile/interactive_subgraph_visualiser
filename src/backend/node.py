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
            self.names = {self.sub_id: self.name}
        else:
            self.name = None
            self.names = {}
        if optional_pairings['sub_id_value_name'] != 'None':
            self.sub_id_value_name = node[optional_pairings['sub_id_value_name']]
            self.sub_id_value_names = {self.sub_id: self.sub_id_value_name}
        else:
            self.sub_id_value_name = None
            self.sub_id_value_names = {}
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
            key = node[self.must_have_pairings['sub_id']]
            value = node[self.must_have_pairings['connections']].split(',')
            for i in range(len(value)):
                if value[i] == '':
                    value.pop(i)
            ret_dict = {
                key: value
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
            key = node[self.must_have_pairings['sub_id']]
            value = node[self.must_have_pairings['connections']].split(',')
            for i in range(len(value)):
                if value[i] == '':
                    value.pop(i)
            new_dict = {
                key: value
            }
            if self.connections is not None:
                self.connections.update(new_dict)
            else:
                self.connections = new_dict

    def append_diff_sub_id(self, node: pd.Series):
        self.sub_ids.append(node[self.must_have_pairings['sub_id']])
        if self.sub_id_value_names:
            self.sub_id_value_names[str(node[self.must_have_pairings['sub_id']])] = node[self.optional_pairings['sub_id_value_name']]
        if self.names:
            self.names[str(node[self.must_have_pairings['sub_id']])] = node[self.optional_pairings['node_name']]
        self.add_connections(node)
        self.attributes['connections'] = self.connections

    def focused_connections_to_csv(self):
        if self.focused_connections is None:
            return None
        else:
            res = ""
            for key in self.focused_connections.keys():
                res += f"{self.id};{key};{','.join(self.focused_connections[key])}"
                if self.names:
                    res += f";{str(self.names[str(key)]).replace(';',',')}"
                if self.sub_id_value_names:
                    res += f";{str(self.sub_id_value_names[str(key)]).replace(';',',')}"
                for (key_2, value) in self.attributes.items():
                    if key_2 == 'connections':
                        continue
                    res += f";{str(value).replace(';',',')}"
                res += "\n"
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
