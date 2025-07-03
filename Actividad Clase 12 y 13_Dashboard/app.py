# app.py
import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
# Dataset de ejemplo
df = px.data.iris()
# Figura Plotly
fig = px.scatter(df, x="sepal_width", y="sepal_length", color="species")
# Crear app Dash
app = dash.Dash(__name__)
server = app.server # IMPORTANTE para PythonAnywhere
# Layout
app.layout = html.Div(children=[
html.H1(children='Dashboard interactivo en PythonAnywhere'),
dcc.Graph(id='grafico-ejemplo',figure=fig)])