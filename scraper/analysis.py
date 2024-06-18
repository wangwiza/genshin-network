from definitions import DATA_DIR
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network

# Load into DataFrame
def load_data_into_df() -> pd.DataFrame:
    with open(f"{DATA_DIR}/exchanges.csv", mode="r", encoding="utf-8") as f:
        return pd.read_csv(f, sep="|")

def aggregate_relationships(relationship_df: pd.DataFrame) -> pd.DataFrame:
    relationship_df["value"] = 1
    return relationship_df.groupby(
        ["source", "target"], sort=False, as_index=False
    ).sum()

# Graph analysis and visualization

def construct_graph(relationship_df: pd.DataFrame) -> nx.Graph:
    print("Constructing graph...")
    G = nx.from_pandas_edgelist(
        relationship_df,
        source="source",
        target="target",
        edge_attr="value",
        create_using=nx.Graph(),
    )
    print("Graph constructed.")
    return G

def draw_graph(G: nx.Graph):
    print("Getting pos...")
    # pos = nx.kamada_kawai_layout(G)
    print("Drawing graph...")
    nx.draw(G, with_labels=True, node_color="skyblue", edge_cmap=plt.colormaps['Blues'])
    print("Displaying graph...")
    plt.show()
    print("Graph displayed.")

def draw_pyvis_graph(G: nx.Graph):
    net = Network(width="100vw", height="100vh", bgcolor="#222222")

    node_degree = dict(G.degree) # Ignore error

    nx.set_node_attributes(G, node_degree, "size")

    net.from_nx(G)
    net.show("genshin_dialogue_graph.html")


if __name__ == "__main__":
    relationship_df = load_data_into_df()
    relationship_df = aggregate_relationships(relationship_df)
    print(relationship_df)
    G = construct_graph(relationship_df)
    draw_pyvis_graph(G)
