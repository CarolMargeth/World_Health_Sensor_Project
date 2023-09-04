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
# Define custom category order and labels
custom_category_order = ['MLE', 'FMLE', 'BTSX']  # Specify the desired order
custom_category_labels = {'MLE': 'Men', 'FMLE': 'Women', 'BTSX': 'Both'}  # Specify custom labels
custom_color = 'goldenrod'
aggregated_data = final_prevalence.groupby('Sex')['Prevalence'].mean().reset_index()

fig = px.bar(
    aggregated_data,
    x='Sex',
    y='Prevalence',
    color_discrete_sequence=[custom_color],
    #title='Estimate Average Smoking Prevalence by Sex Category',
    category_orders={'Sex': custom_category_order},  # Set the custom category order
)
fig.update_layout(
    xaxis_title='Sex',
    yaxis_title='Prevalence (%)',
)
# Update the category labels on the x-axis
fig.update_xaxes(categoryorder='array', categoryarray=custom_category_order, title_text='Sex', tickvals=[0, 1, 2], ticktext=[custom_category_labels[category] for category in custom_category_order])


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
    #title='Estimate Smoking Prevalence by Country over the years',
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
    #title='Estimate Average Smoking Prevalence by WHO Region over the time'
)
fig3.update_layout(
    xaxis_title='Year',
    yaxis_title='Prevalence',
)

# Fig component 4
# Scatterplot of Smoking Prevalence vs Premature Deaths

# Sort the 'WHO Region' column alphabetically in your scatter_data DataFrame
scatter_data_sorted = scatter_data.sort_values(by='WHO Region')

fig4 = px.scatter(
    scatter_data_sorted,
    x='Prevalence',
    y='PrematureDeaths/NCD',
    #title='Relation Smoking Prevalence vs Premature Deaths by NCD (proportion among all NCD)',
    labels={'Prevalence': 'Smoking Prevalence', 'PrematureDeaths/NCD': 'Premature Deaths'},
    animation_frame='Year',
    color = 'WHO Region',
    hover_name='Country'  
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
            html.Div([
                html.H3("Average Smoking Prevalence by Sex Category"),
                dcc.Graph(figure=fig),
            ]),
            width=4  # This column takes half of the row width
        ),
        dbc.Col(
            # Component 2 (Right column, first row)
            html.Div([
                html.H3("Smoking Prevalence by Country over the years"),
                dcc.Graph(figure=fig2),
                html.P("Prevalence values for each country since 2000 year and the country’s most recent survey, then project to 2025."),
            ]),
            width=8
        ),
    ]),

    dbc.Row([
        dbc.Col(
            # Component 3 (Left column, second row)
            html.Div([
                html.H3("Average Smoking Prevalence by WHO Region over the time"),
                dcc.Graph(figure=fig3),
            ]),
            width=6
        ),
        dbc.Col(
            # Component 4 (Right column, second row)
            html.Div([
                html.H3("Relation Smoking Prevalence vs Premature Deaths by NCD (proportion among all NCD)"),
                dcc.Graph(figure=fig4),
            ]),
            width=6
        ),
    ]),

    dbc.Row([
    dbc.Col(
        # Component 5 (Third row, single column)
        [
            html.H3('MPOWER Strategy results by country'),
            html.P("Selected the country:"),
            dcc.Dropdown(
                id='country-dropdown',
                options=[{'label': country, 'value': country} for country in final_MPOWER['Country'].unique()],
                value='Canada'
            ),
            
            dash_table.DataTable(
                id='score-table',
                columns = [
                    {'name': 'Year', 'id': 'Year'},
                    {'name': 'Monitoring', 'id': 'Monitoring'},
                    {'name': 'Protecting', 'id': 'Protecting'},
                    {'name': 'Offering', 'id': 'Offering'},
                    {'name': 'Warning', 'id': 'Warning'},
                    {'name': 'Enforcing', 'id': 'Enforcing'},
                    {'name': 'Raising', 'id': 'Raising'},
                ],
            ),
            html.P("Table Description: This table displays the scores for the selected country."),
        ],
        width=6  # Set the width of this column to 6
    ),
    
    dbc.Col(
            # Component 6 (Right column, third row)
            [
                html.H3('The six MPOWER strategies include:'),
                html.Div(
                    dbc.Accordion(
                        [
                            dbc.AccordionItem(
                                "M: Monitor tobacco use and prevention policies",
                                title="M: Monitor tobacco use and prevention policies",
                            ),
                            dbc.AccordionItem(
                                "P: Protect people from tobacco smoke",
                                title="P: Protect people from tobacco smoke",
                            ),
                            dbc.AccordionItem(
                                "O: Offer help to quit smoking",
                                title="O: Offer help to quit smoking",
                            ),
                            dbc.AccordionItem(
                                "W: Warn about the dangers of tobacco",
                                title="W: Warn about the dangers of tobacco",
                            ),
                            dbc.AccordionItem(
                                "E: Enforce bans on tobacco advertising, promotion and sponsorship",
                                title="E: Enforce bans on tobacco advertising, promotion and sponsorship",
                            ),
                            dbc.AccordionItem(
                                "R: Raise taxes on tobacco",
                                title="R: Raise taxes on tobacco",
                            ),
                        ],
                        always_open=True,
                    )
                ),
            ],
            width=6
        ),
    ]),
    # ...
], fluid=True, style={'width': '100%', 'height': '110vh'})








# Define callback to update the table and graphs based on user input

@app.callback(
    Output('score-table', 'data'),
    Input('country-dropdown', 'value')
)
def update_table(selected_country):
    filtered_df = final_MPOWER[final_MPOWER['Country'] == selected_country]

        # Define a mapping from existing column names to desired labels
    column_label_mapping = {
        'M_score': 'Monitoring',
        'P_score': 'Protecting',
        'O_score': 'Offering',
        'W_score': 'Warning',
        'E_score': 'Enforcing',
        'R_score': 'Raising',
    }

     # Rename the columns based on the mapping
    filtered_df.rename(columns=column_label_mapping, inplace=True)
    
    return filtered_df.to_dict('records')

   
# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
