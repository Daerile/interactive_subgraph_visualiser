import pandas as pd
from backend.graph_system import GraphSystem

def main():
    data = read_data()
    graph = GraphSystem(data)

def read_data():
    data = pd.read_csv('../data/allc_model_tulertkek_grafmegjeleníteshez.csv', sep=';')
    data = data.dropna(how='all', subset=['kapcsolat'])
    return data


if __name__ == '__main__':
    main()