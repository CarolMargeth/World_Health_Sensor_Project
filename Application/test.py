# Import packages
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import dash
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64

finaL_MPOWER = pd.read_csv('finaL_MPOWER.csv')

app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    html.H1("Country Scores Dashboard"),
    
    dcc.Dropdown(
        id='country-dropdown',
        options=[{'label': country, 'value': country} for country in finaL_MPOWER['Country'].unique()],
        value=finaL_MPOWER['Country'].iloc[0]
    ),
    
    dash_table.DataTable(
        id='score-table',
        columns=[
            {'name': 'Year', 'id': 'Year'},
            {'name': 'M_score', 'id': 'M_score'},
            {'name': 'P_score', 'id': 'P_score'},
            {'name': 'O_score', 'id': 'O_score'},
            {'name': 'W_score', 'id': 'W_score'},
            {'name': 'E_score', 'id': 'E_score'},
            {'name': 'R_score', 'id': 'R_score'},
        ],
    )
])

# Define a callback to update the table based on the selected country
@app.callback(
    Output('score-table', 'data'),
    Input('country-dropdown', 'value')
)
def update_table(selected_country):
    filtered_df = finaL_MPOWER[finaL_MPOWER['Country'] == selected_country]
    return filtered_df.to_dict('records')

if __name__ == '__main__':
    app.run_server(debug=True)