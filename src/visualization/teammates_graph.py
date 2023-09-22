import os

import numpy as np
import networkx as nx
import pandas as pd
import plotly.graph_objects as go

from src.cache_manager import CacheManager
from src.constants import CACHE_PATH


class GraphDrawer:
    def __init__(self, nodes, edges):
        self.__graph = nx.Graph()
        self.__graph.add_nodes_from(nodes)
        self.__graph.add_edges_from(edges)
        for node in self.__graph.nodes():
            self.__graph.nodes[node]['pos'] = np.random.rand(2)

    def draw(self):
        # Create a graph
        edge_trace, node_trace = self.__create_edges()
        self.__color_node_points(node_trace)
        self.__create_graph(edge_trace, node_trace)

    def __create_edges(self):
        edge_x = []
        edge_y = []
        for edge in self.__graph.edges():
            x0, y0 = self.__graph.nodes[edge[0]]['pos']
            x1, y1 = self.__graph.nodes[edge[1]]['pos']
            edge_x.append(x0)
            edge_x.append(x1)
            edge_x.append(None)
            edge_y.append(y0)
            edge_y.append(y1)
            edge_y.append(None)

        edge_trace = go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=0.5, color='#888'),
            hoverinfo='none',
            mode='lines')

        node_x = []
        node_y = []
        labels = []
        for node in self.__graph.nodes():
            x, y = self.__graph.nodes[node]['pos']
            node_x.append(x)
            node_y.append(y)
            labels.append(node)

        node_trace = go.Scatter(
            x=node_x, y=node_y,
            text=labels,
            mode='markers',
            hoverinfo='text',
            marker=dict(
                showscale=True,
                colorscale='YlGnBu',
                reversescale=True,
                color=[],
                size=10,
                colorbar=dict(
                    thickness=15,
                    title='Node Connections',
                    xanchor='left',
                    titleside='right'
                ),
                line_width=2))

        return edge_trace, node_trace

    def __color_node_points(self, node_trace):
        node_adjacencies = []
        node_text = []
        for node, adjacencies in enumerate(self.__graph.adjacency()):
            node_adjacencies.append(len(adjacencies[1]))
            node_text.append('connections: ' + str(len(adjacencies[1])))
        node_trace.marker.color = node_adjacencies
        node_trace.text = [f"{node_trace.text[i]} <br> {node_text[i]}" for i in range(len(node_trace.text))]

    def __create_graph(self, edge_trace, node_trace):
        fig = go.Figure(data=[edge_trace, node_trace],
                        layout=go.Layout(
                            title='Network graph for NBA teammates',
                            showlegend=True,
                            hovermode='closest',
                            margin=dict(b=20, l=5, r=5, t=40),
                            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                        )
        fig.show()

def get_data_from_cache():
    path = os.path.join(CACHE_PATH, CacheManager.TEAMMATES_CACHE_SUBDIR)
    player_nodes: set = set()
    teammate_edges: set = set()
    for file in os.listdir(path):
        try:
            # TODO temporary solution
            df = pd.read_csv(os.path.join(path, file))
        except pd.errors.EmptyDataError:
            continue
        player: str = file.split('.')[-2]
        player_nodes.add(player)

        # TODO temporary solution
        teammates: [str] = [teammate for teammate in df["id"].tolist() if type(teammate) == str]
        player_nodes.update(teammates)
        teammate_edges.update((tuple(sorted((player, teammate))) for teammate in teammates))

    return player_nodes, teammate_edges


if __name__ == "__main__":
    # Create a graph
    player_nodes, teammate_edges = get_data_from_cache()
    GraphDrawer(player_nodes, teammate_edges).draw()