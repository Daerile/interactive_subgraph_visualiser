import networkx as nx
from src.backend.graph_system import GraphSystem
from src.viewmodel.loader import Loader


class ViewModel:
    def __init__(self):
        # Initialize ViewModel with empty column names, data, and graph system
        self.column_names = None
        self.data = None
        self.graph_system = None

    def create_digraph(self, must_have_pairings, optional_pairings):
        # Create a directed graph (digraph) using the GraphSystem class
        # must_have_pairings and optional_pairings are used to define the graph structure
        self.graph_system = GraphSystem(self.data, self.column_names, must_have_pairings, optional_pairings)
        return self.graph_system.digraph

    def handle_load_button_pressed(self):
        # Load data from a file when the load button is pressed
        # If data is loaded successfully, update self.data and self.column_names
        data = Loader.load_file()
        if data is None:
            return None
        else:
            print(f'Data loaded')
            self.data = data
            self.column_names = data.columns
            return self.column_names

    def handle_node_focused(self, focused_node, focused_depth):
        # Handle the event when a node is focused
        # Get the subgraph of the focused node with the specified depth
        if focused_node is None:
            return None
        focused_subgraph = self.graph_system.get_subgraph(focused_node.id, focused_depth)
        print(focused_subgraph.nodes)
        return focused_subgraph

    def handle_save_button_pressed(self, export_digraph: nx.DiGraph):
        # Handle the event when the save button is pressed
        # Save the current state of the graph to a file
        to_save = ""
        for must_have_column in self.graph_system.must_have_columns:
            to_save += f"{must_have_column};"
        for optional_column in self.graph_system.optional_columns:
            to_save += f"{optional_column};"
        for column_name in self.column_names:
            invalid_column_names = []
            for must_have_column_name in self.graph_system.must_have_pairings.values():
                invalid_column_names.append(must_have_column_name)
            for optional_column_name in self.graph_system.optional_pairings.values():
                invalid_column_names.append(optional_column_name)
            if column_name not in invalid_column_names:
                to_save += f"{column_name};"
        to_save = to_save[:-1]
        to_save += "\n"
        for node in export_digraph.nodes:
            to_save += node.focused_connections_to_csv()
        Loader.save_file(to_save)