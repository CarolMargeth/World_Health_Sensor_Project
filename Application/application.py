# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.


# Import packages
import dash
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px


# Load the datasets into DataFrames
final_prevalence = pd.read_csv('final_prevalence.csv')
final_premature_deaths = pd.read_csv('final_premature_deaths.csv')
final_O_P = pd.read_csv('final_O_P.csv')
scatter_data = pd.read_csv('scatter_data.csv')

# Create the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define the layout of the app
app.layout = dbc.Container([
    html.H1("Global Tobacco Insights: Visualizing Smoking Trends, Control Policies, and Health Related Problems"),  # Dashboard Title
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='big-graph'),
        ], width=12)  # Occupying the entire width
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='small-graph-1'),
        ], width=4),  # Occupying 4 out of 12 columns
        dbc.Col([
            dcc.Graph(id='small-graph-2'),
        ], width=4),
        dbc.Col([
            dcc.Graph(id='small-graph-3'),
        ], width=4),
    ]),
])

# Define callback to update the table and graphs based on user input



    # Filter data for the selected country

    # Create the data table
    
    # Create customizable graphs using Plotly Express
   
   
# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
