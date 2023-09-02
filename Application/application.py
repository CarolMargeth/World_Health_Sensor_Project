# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.


# Import packages
import dash
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px


# Load the datasets into DataFrames
final_prevalence = pd.read_csv('final_prevalence.csv')
final_premature_deaths = pd.read_csv('final_premature_deaths.csv')
final_MPOWER = pd.read_csv('finaL_MPOWER.csv')
scatter_data = pd.read_csv('scatter_data.csv')

# Figures

# Fig component 1
aggregated_data = final_prevalence.groupby('Sex')['Prevalence'].mean().reset_index()

fig = px.bar(
    aggregated_data,
    x='Sex',
    y='Prevalence',
    color=None,
    title='Estimate Average Smoking Prevalence by Sex Category',
)
fig.update_layout(
    xaxis_title='Sex',
    yaxis_title='Prevalence (%)',
)

# Fig component 2
# Sort the dataframe by 'TimeDimensionValue' in ascending order
aggregated_data2 = final_prevalence.sort_values('Year')

fig2 = px.choropleth(
    aggregated_data2,
    locations='Country',  # Column with country names
    locationmode='country names',  # Set location mode to country names
    color='Prevalence',  
    hover_name='Country',  # Hover text will show country name
    animation_frame='Year',  # Animation frame based on year
    color_continuous_scale='Viridis_r',  # Color scale
    title='Estimate Smoking Prevalence by Country over the years',
)
fig2.update_geos(
    showcoastlines=True,
    coastlinecolor='RebeccaPurple',
    showland=True,
    landcolor='LightGrey',
    showocean=True,
    oceancolor='LightBlue',
    projection_type='orthographic',  # Projection type
)
fig2.update_layout(
    geo=dict(showframe=False, showcoastlines=False),
    coloraxis_colorbar=dict(title='Prevalence (%)'),
)

# Fig component 3
# Group by WHO Region and Year and calculate the mean of Prevalence

average_numeric_value_over_years = final_prevalence.groupby(['WHO Region', 'Year'])['Prevalence'].mean().reset_index()

pivot_table = pd.pivot_table(
    average_numeric_value_over_years,
    values='Prevalence',
    index='Year',
    columns='WHO Region',
    aggfunc='mean'
)
pivot_table.reset_index(inplace=True)
fig3 = px.line(
    pivot_table,
    x='Year',
    y=pivot_table.columns[1:],  
    title='Estimate Average Smoking Prevalence by WHO Region over the time'
)
fig3.update_layout(
    xaxis_title='Year',
    yaxis_title='Prevalence',
)

# Fig component 4
# Scatterplot of Smoking Prevalence vs Premature Deaths
fig4 = px.scatter(
    scatter_data,
    x='Prevalence',
    y='PrematureDeaths/NCD',
    title='Relation Smoking Prevalence vs Premature Deaths by NCD (proportion among all NCD)',
    labels={'Prevalence': 'Smoking Prevalence', 'PrematureDeaths/NCD': 'Premature Deaths'},
    animation_frame='Year',
    color = 'WHO Region' 
)
# Set fixed axis ranges
fig4.update_xaxes(range=[0, 100])
fig4.update_yaxes(range=[0, 100])






# Create the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SPACELAB])

# Define the layout of the app
app.layout = dbc.Container([
    # Title Row
    dbc.Row([
        dbc.Col(
            html.H1("Global Tobacco Insights: Visualizing Smoking Trends, Control Policies, and Health Related Problems", className="text-center"),
            width={"size": 12}  # Center the title within the container
        ),
    ]),

    dbc.Row([
        dbc.Col(
            # Component 1 (Left column, first row)
            dcc.Graph(figure=fig),
            width=5  # This column takes half of the row width
        ),
        dbc.Col(
            # Component 2 (Right column, first row)
            dcc.Graph(figure=fig2),
            width=7
        ),
    ]),

    dbc.Row([
        dbc.Col(
            # Component 3 (Left column, second row)
            dcc.Graph(figure=fig3),
            width=6
        ),
        dbc.Col(
            # Component 4 (Right column, second row)
            dcc.Graph(figure=fig4),
            width=6
        ),
    ]),

    dbc.Row([
        dbc.Col(
            # Component 5 (Left column, third row)
            dcc.Dropdown(
            id='country-dropdown',
            options=[{'label': country, 'value': country} for country in final_MPOWER['Country'].unique()],
            value=final_MPOWER['Country'].iloc[0]
            )
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
        ),
        dbc.Col(
            # Component 6 (Right column, third row)
            html.Div("Component 6"),
            width=6
        ),
    ]),
], fluid=True)

# Define callback to update the table and graphs based on user input

@app.callback(
    Output('score-table', 'data'),
    Input('country-dropdown', 'value')
)
def update_table(selected_country):
    filtered_df = final_MPOWER[final_MPOWER['Country'] == selected_country]
    return filtered_df.to_dict('records')


    # Filter data for the selected country

    # Create the data table
    
    # Create customizable graphs using Plotly Express
   
   
# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
