import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# Load your data into a Pandas DataFrame
final_prevalence = pd.read_csv('/Data clean/final_prevalence.csv')
print(final_prevalence)


# Create the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    html.H1("Smoking Prevalence Dashboard"),

    # Interactive country input
    dcc.Input(id='country-input', value='Enter Country', type='text'),

    # Table to display data for the entered country
    html.Table(id='data-table'),

    # Dropdowns for graph customization
    dcc.Dropdown(id='indicator-dropdown', options=[...], value='Smoking Prevalence'),
    
    # Graphs for visualization
    dcc.Graph(id='bar-graph'),
    dcc.Graph(id='line-graph'),
    dcc.Graph(id='scatter-plot')
])

# Define callback to update the table and graphs based on user input
@app.callback(
    [Output('data-table', 'children'),
     Output('bar-graph', 'figure'),
     Output('line-graph', 'figure'),
     Output('scatter-plot', 'figure')],
    [Input('country-input', 'value'),
     Input('indicator-dropdown', 'value')]
)
def update_dashboard(selected_country, selected_indicator):
    # Filter data for the selected country
    country_data = data[data['Country'] == selected_country]
    
    # Create the data table
    table_rows = [html.Tr([html.Th(col), html.Td(country_data[col].values[0])]) for col in country_data.columns]
    
    # Create customizable graphs using Plotly Express
    bar_fig = px.bar(data_frame=data, x='Country', y=selected_indicator)
    line_fig = px.line(data_frame=data, x='Year', y=selected_indicator)
    scatter_fig = px.scatter(data_frame=data, x='GDP', y=selected_indicator, color='Region')
    
    return table_rows, bar_fig, line_fig, scatter_fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
