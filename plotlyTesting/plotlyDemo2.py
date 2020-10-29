# Following the example on: https://www.kaggle.com/anand0427/network-graph-with-at-t-data-using-plotly

#%% Imports

import pandas as pd
import numpy as np
import networkx as nx
from plotly.offline import download_plotlyjs, init_notebook_mode, iplot
import plotly.graph_objs as go
import plotly
import json

network_df = pd.read_csv("data.csv") 

init_notebook_mode(connected=True)

A = list(network_df["source_ip"].unique())
B = list(network_df["destination_ip"].unique())
node_list = set(A+B)

# %% Creating nodes and edges and add to graph

G = nx.Graph()
for i in node_list:
    G.add_node(i)

for i,j in network_df.iterrows():
    G.add_edges_from([(j["source_ip"],j["destination_ip"])])

pos = nx.spring_layout(G, k=0.5, iterations=50)

#Adding Positions of nodes
for n, p in pos.items():
    G.nodes[n]['pos'] = p
# %% Adding to plotly api

edge_trace = go.Scatter(
    x=[],
    y=[],
    line=dict(width=0.5,color='#888'),
    hoverinfo='none',
    mode='lines')

for edge in G.edges():
    x0, y0 = G.nodes[edge[0]]['pos']
    x1, y1 = G.nodes[edge[1]]['pos']
    edge_trace['x'] += tuple([x0, x1, None])
    edge_trace['y'] += tuple([y0, y1, None])

node_trace = go.Scatter(
    x=[],
    y=[],
    text=[],
    mode='markers',
    hoverinfo='text',
    marker=dict(
        showscale=True,
        colorscale='RdBu',
        reversescale=True,
        color=[],
        size=15,
        colorbar=dict(
            thickness=10,
            title='Node Connections',
            xanchor='left',
            titleside='right'
        ),
        line=dict(width=0)))

for node in G.nodes():
    x, y = G.nodes[node]['pos']
    node_trace['x'] += tuple([x])
    node_trace['y'] += tuple([y])

#%% coloring
for node, adjacencies in enumerate(G.adjacency()):
    node_trace['marker']['color']+=tuple([len(adjacencies[1])])
    node_info = adjacencies[0] +' # of connections: '+str(len(adjacencies[1]))
    node_trace['text']+=tuple([node_info])

#%% Plotting
fig = go.Figure(data=[edge_trace, node_trace],
             layout=go.Layout(
                title='<br>AT&T network connections',
                titlefont=dict(size=16),
                showlegend=False,
                hovermode='closest',
                margin=dict(b=20,l=5,r=5,t=40),
                annotations=[ dict(
                    text="No. of connections",
                    showarrow=False,
                    xref="paper", yref="paper") ],
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))

iplot(fig)
plotly.plot(fig)
# %%
