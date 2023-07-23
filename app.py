from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
from data import read_clean
df = read_clean('eksport-1')
df_summed = df.groupby('date').sum()
fig = px.line(df_summed, x=df_summed.index, y="balance", markers=True, hover_data=["amount", "source"])

app = Dash(__name__)

app.layout = html.Div([
    dcc.Graph(figure=fig)
])

# @callback(
#     Output('graph-content', 'figure'),
#     Input('dropdown-selection', 'value')
# )
# def update_graph(value):
#     dff = df[df.country==value]
#     return px.line(dff, x='date', y='balance')

if __name__ == '__main__':
    app.run(debug=True)