import geopandas as gpd
import pandas as pd
import shapely.geometry
from shapely.geometry import Polygon
import json

import plotly.graph_objects as go

p1 = Polygon([(0, 0), (1, 0), (1, 1)])
p2 = Polygon([(0, 0), (1, 0), (1, 1), (0, 1)])
p3 = Polygon([(2, 0), (3, 0), (3, 1), (2, 1)])

g = gpd.GeoSeries([p1, p2, p3])

poly_json = g.to_json()

data = [[0,10],[1,4],[2,15]]
df = pd.DataFrame(data, columns = ['id','color'])

fig = go.Figure(data = go.Choropleth(
    geojson=poly_json,
    locations=df['id'].astype(str),
    z = df['color'].astype(float)
))
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.layout.template= None
fig.show()
