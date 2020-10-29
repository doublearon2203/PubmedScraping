#%% JSON to dataframe
import pandas as pd
import json

with open('database.json') as f:
    data = json.load(f)

df = pd.DataFrame(columns=['article', 'source', 'link'])

pos = 0

for i, ID in enumerate(data):

    entry = len(data[ID]['Citedby'])

    for j in range(entry):
        link = 'https://pubmed.ncbi.nlm.nih.gov' + ID
        df.loc[pos] = [ID, data[ID]['Citedby'][j], link]

        pos +=1
##%% Imports

import networkx as nx
# from plotly.offline import download_plotlyjs, init_notebook_mode, iplot
import plotly.graph_objs as go
# import plotly

network_df = df

# init_notebook_mode(connected=True)

A = list(network_df["source"].unique())
B = list(network_df["article"].unique())
node_list = set(A+B)

# #%% Creating nodes and edges and add to graph

G = nx.Graph()
for i in node_list:
    G.add_node(i)

for i,j in network_df.iterrows():
    G.add_edges_from([(j["source"],j["article"])])

pos = nx.spring_layout(G, k=0.5, iterations=50)

#Adding Positions of nodes
for n, p in pos.items():
    G.nodes[n]['pos'] = p
## %% Adding to plotly api

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

#%%
plotAnnotes = []
countAnnotes = []
i = 0
for node in G.nodes():
    x, y = G.nodes[node]['pos']
    node_trace['x'] += tuple([x])
    node_trace['y'] += tuple([y])

    link = df['link'][i]
    print(link)
    print(node)
    plotAnnotes.append(dict(x=x,
                        y=y,
                        text=f"""<a href="{link}">Link</a>""".format("Text"),
                        showarrow=False
                        ))

    # countAnnotes.append(dict(x=x,
    #                     y=y,
    #                     text='# of connections: '+str(len(adjacencies[1])),
    #                     showarrow=False
    #                     ))                   
    i += 1

#%% Color node points
node_adjacencies = []
node_text = []
for node, adjacencies in enumerate(G.adjacency()):
    node_adjacencies.append(len(adjacencies[1]))
    node_text.append('# of connections: '+str(len(adjacencies[1])) + '\n' + df['link'][node][-10:])
    # node_text.append(f"""<a href='{df['link'][node]}'> {df['link'][node]}</a>""".format("Text"))
    # node_text.append(dict(x=G.nodes[node]['pos'][0],
    #                     y=G.nodes[node]['pos'][1],
    #                     text="""<a href="https://plot.ly/">{}</a>""".format("Text"),
    #                     showarrow=False
    #                     ))
    # countAnnotes.append(dict(x=x,
    #                     y=y,
    #                     text='# of connections: '+str(len(adjacencies[1])),
    #                     showarrow=False
    #                     ))   


node_trace.marker.color = node_adjacencies
node_trace.text = node_text

#%% Create Network Graph
fig = go.Figure(data=[edge_trace, node_trace],
             layout=go.Layout(
                title='<br>Article network graph',
                titlefont_size=16,
                showlegend=False,
                hovermode='closest',
                margin=dict(b=20,l=5,r=5,t=40),
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                )

fig.update_layout(
    updatemenus=[
        dict(
            type="buttons",
            direction="right",
            active=0,
            x=0.4,
            y=1.2,
            buttons=list([
                dict(label="Apperance Count",
                    method="update",
                    args=[{"visible": [True, True]},
                        {"annotations": countAnnotes,
                        'data': [edge_trace, node_trace]}]),
                dict(label="Link",
                    method="update",
                    args=[{"visible": [False, True]},
                        {"annotations": plotAnnotes,
                        'data': [edge_trace, node_trace]}])
            ]),
        )
    ])

fig.show()
# %%
