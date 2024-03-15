import pandas as pd
from src.backend.graph_system import GraphSystem

def main():
    data = read_data()
    graph = GraphSystem(data)

def read_data():
    data = pd.read_csv('../data/allc_model_tulertkek_grafmegjeleníteshez.csv', sep=';')
    return data


if __name__ == '__main__':
    main()