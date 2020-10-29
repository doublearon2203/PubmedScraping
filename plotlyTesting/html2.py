import webbrowser
import pandas as pd
import plotly.graph_objs as go
df = pd.DataFrame({'x': [1, 2, 3],
                   'y': [1, 3, 2],
                   'link': ['https://google.com', 'https://bing.com', 'https://duckduckgo.com']})

fig = go.FigureWidget(layout={'hovermode': 'closest'})
scatter = fig.add_scatter(x=df.x, y=df.y, mode='markers', marker={'size': 20})

def do_click(trace, points, state):
    if points.point_inds:
        ind = points.point_inds[0]
        url = df.link.iloc[ind]
        webbrowser.open_new_tab(url)
        
scatter.on_click(do_click)
fig