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
    pos = nx.kamada_kawai_layout(G)
    print("Drawing graph...")
    nx.draw(G, with_labels=True, node_color="skyblue", edge_cmap=plt.colormaps["Blues"])
    print("Displaying graph...")
    plt.show()
    print("Graph displayed.")


def draw_pyvis_graph(G: nx.Graph):
    net = Network(width="100vw", height="100vh", bgcolor="#222222", font_color="white")

    node_degree = dict(G.degree)  # Ignore error
    node_degree = normalize_values(node_degree, new_min=1, new_max=100)

    nx.set_node_attributes(G, node_degree, "size")

    net.from_nx(G)
    net.show("../index.html")


def normalize_values(d, new_min=1, new_max=100):
    values = d.values()
    min_val = min(values)
    max_val = max(values)

    def normalize(value):
        return ((value - min_val) / (max_val - min_val)) * (new_max - new_min) + new_min

    return {k: normalize(v) for k, v in d.items()}


if __name__ == "__main__":
    relationship_df = load_data_into_df()
    relationship_df = aggregate_relationships(relationship_df)
    print(relationship_df)
    G = construct_graph(relationship_df)
    draw_pyvis_graph(G)
