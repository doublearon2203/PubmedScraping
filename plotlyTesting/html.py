#%% asdfs
from plotly.offline import plot
import pandas as pd
import plotly.graph_objs as go
import re

mapbox_access_token = 'pk.eyJ1IjoiZG91YmxlYXJvbiIsImEiOiJja2d1d25hangxYjh6MnltZmFhdzRoMDc1In0.HXB0QC6MKhxv0RosSTdu4Q'

# Build scattermapbox trace and store URL's in the customdata
# property. The values of this list will be easy to get to in the
# JavaScript callback below
data = [
    go.Scattermapbox(
        lat=['45.5017', '45.7', '45.3'],
        lon=['-73.5673', '-73.7', '-73.3'],
        mode='markers',
        marker=dict(
            size=14
        ),
        name='mapbox 1',
        text=['Montreal'],
        customdata=['https://google.com', 'https://bing.com', 'https://duckduckgo.com']
    )
]

# Build layout
layout = go.Layout(
    hovermode='closest',
    mapbox=dict(
    accesstoken=mapbox_access_token,
    bearing=0,
    center=dict(
        lat=45,
        lon=-73
    ),
    pitch=0,
    zoom=6,
    )
)

# Build Figure
fig = go.Figure(
    data=data,
    layout=layout,
)

# Get HTML representation of plotly.js and this figure
plot_div = plot(fig, output_type='div', include_plotlyjs=True)

# Get id of html div element that looks like
# <div id="301d22ab-bfba-4621-8f5d-dc4fd855bb33" ... >
res = re.search('<div id="([^"]*)"', plot_div)
div_id = res.groups()[0]

# Build JavaScript callback for handling clicks
# and opening the URL in the trace's customdata 
js_callback = """
<script>
var plot_element = document.getElementById("{div_id}");
plot_element.on('plotly_click', function(data){{
    console.log(data);
    var point = data.points[0];
    if (point) {{
        console.log(point.customdata);
        window.open(point.customdata);
    }}
}})
</script>
""".format(div_id=div_id)

# Build HTML string
html_str = """
<html>
<body>
{plot_div}
{js_callback}
</body>
</html>
""".format(plot_div=plot_div, js_callback=js_callback)

# Write out HTML file
with open('hyperlink_fig.html', 'w') as f:
    f.write(html_str)