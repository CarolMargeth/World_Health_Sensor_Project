# Create the project environment and Run this app with `python application.py` in your terminal and
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
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX]) #LUX, FLATLY, 

# Define the navbar
navbar = dbc.NavbarSimple(
    brand=html.Div([html.I(className="fas fa-chart-bar"), " World Health Sensor Project"]),  # Bar chart icon
    brand_href="https://github.com/CarolMargeth/World_Health_Sensor_Project",
    color="darkblue",
    dark=True,
)

# Define the layout of the app
app.layout = dbc.Container([
    #Navigation bar
    navbar,
    
    # Add space after the navigation bar
    html.Div(style={"height": "30px"}),

    # Title Row
    dbc.Row([
        dbc.Col(
            html.H1("Global Tobacco Insights: Visualizing Smoking Trends, Control Policies, and Health Related Problems", className="text-center"),
            width={"size": 12}  # Center the title within the container
        ),
    ]),

    # Add space after the navigation bar
    html.Div(style={"height": "30px"}),

    dbc.Row([
        dbc.Col(
            html.Div([
                html.H5("Average Smoking Prevalence by Sex Category", className="text-center"),
                dcc.Graph(figure=fig),
            ]),
            width=4  # This column takes half of the row width
        ),
        dbc.Col(
            # Component 2 (Right column, first row)
            html.Div([
                html.H5("Smoking Prevalence by Country over the years", className="text-center"),
                dcc.Graph(figure=fig2),
                html.P("Prevalence values for each country since 2000 year and the country’s most recent survey, then project to 2025.", className="text-center"),
            ]),
            width=8
        ),
    ],
        style={"margin-bottom": "30px"}  # Add space between these two rows
    ),

    dbc.Row([
        dbc.Col(
            # Component 3 (Left column, second row)
            html.Div([
                html.H5("Average Smoking Prevalence by WHO Region over the time", className="text-center"),
                dcc.Graph(figure=fig3),
            ]),
            width=6
        ),
        dbc.Col(
            # Component 4 (Right column, second row)
            html.Div([
                html.H5("Relation Smoking Prevalence vs Premature Deaths by NCD (proportion among all NCD)", className="text-center"),
                dcc.Graph(figure=fig4),
            ]),
            width=6
        ),
    ],
        style={"margin-bottom": "30px"}  # Add space between these two rows
    ),

    dbc.Row([
        dbc.Col(
            # Component 6 (Right column, third row)
            [
                html.H5('MPOWER strategies'),
                html.P("Click over each strategy to learn more about it:"),
                html.Div(
                    dbc.Accordion(
                        [
                            dbc.AccordionItem(
                                [
                                    html.P("This involves tracking and assessing tobacco use trends, as well as the effectiveness of tobacco control policies and programs. Monitoring helps policymakers make informed decisions based on data."),
                                    html.P("Score 0: Little to no monitoring of tobacco use and control policies."),
                                    html.P("Score 1: Limited monitoring with minimal data collection and analysis."),
                                    html.P("Score 2: Basic monitoring with some data collection and analysis."),
                                    html.P("Score 3: Moderate monitoring with regular data collection and analysis."),
                                    html.P("Score 4: Good monitoring with comprehensive data collection and analysis."),
                                    html.P("Score 5: Excellent monitoring with up-to-date, comprehensive, and widely available data on tobacco use and control policies."),
                                ],
                             title="M: Monitor tobacco use and prevention policies",    
                            ),
                            dbc.AccordionItem(
                                [
                                    html.P("This involves protecting people from secondhand smoke exposure in public places and workplaces. Smoke-free policies are a key component of this strategy."),
                                    html.P("Score 0: No significant protection measures in place."),
                                    html.P("Score 1: Limited protection with restrictions in some public places or workplaces."),
                                    html.P("Score 2: Basic protection with restrictions in most public places and workplaces."),
                                    html.P("Score 3: Moderate protection with widespread smoke-free policies."),
                                    html.P("Score 4: Good protection with comprehensive smoke-free laws and strong enforcement."),
                                    html.P("Score 5: Excellent protection with comprehensive, strictly enforced smoke-free laws in all public places and workplaces."),
                                ],
                                title="P: Protect people from tobacco smoke",
                            ),
                            dbc.AccordionItem(
                                [
                                    html.P("This involves providing support and assistance to individuals trying to quit smoking. Access to cessation services is essential for this strategy."),
                                    html.P("Score 0: No support or assistance available for individuals trying to quit."),
                                    html.P("Score 1: Limited support with minimal access to cessation services."),
                                    html.P("Score 2: Basic support with some access to counseling and medications."),
                                    html.P("Score 3: Moderate support with widespread access to cessation services."),
                                    html.P("Score 4: Good support with comprehensive cessation programs and access."),
                                    html.P("Score 5: Excellent support with readily available and accessible cessation services."),
                                ],
                                title="O: Offer help to quit smoking",
                            ),
                            dbc.AccordionItem(
                                [
                                    html.P("This involves raising awareness about the dangers of tobacco use through public health campaigns and effective warning labels on tobacco products."),
                                    html.P("Score 0: No awareness campaigns or warning labels on tobacco products."),
                                    html.P("Score 1: Limited awareness campaigns or basic warning labels."),
                                    html.P("Score 2: Basic public health campaigns and warning labels."),
                                    html.P("Score 3: Moderate public health campaigns and effective warning labels."),
                                    html.P("Score 4: Good public health campaigns and strong warning labels."),
                                    html.P("Score 5: Excellent public health campaigns and highly effective warning labels that cover a large portion of tobacco packaging."),
                                ],
                                title="W: Warn about the dangers of tobacco",
                            ),
                            dbc.AccordionItem(
                                [
                                    html.P("This involves prohibiting tobacco advertising, promotion, and sponsorship to reduce the attractiveness of tobacco products."),
                                    html.P("Score 0: No bans or significant presence of tobacco advertising, promotion, and sponsorship."),
                                    html.P("Score 1: Limited bans with some restrictions on advertising."),
                                    html.P("Score 2: Basic bans on some forms of advertising, promotion, and sponsorship."),
                                    html.P("Score 3: Moderate bans with comprehensive restrictions on advertising, promotion, and sponsorship."),
                                    html.P("Score 4: Good bans with strong enforcement of restrictions."),
                                    html.P("Score 5: Excellent bans with complete prohibition and strict enforcement of all forms of tobacco advertising, promotion, and sponsorship."),
                                ],
                                title="E: Enforce bans on tobacco advertising, promotion and sponsorship",
                            ),
                            dbc.AccordionItem(
                                [
                                    html.P("This involves increasing the taxes on tobacco products to reduce affordability and discourage tobacco consumption."),
                                    html.P("Score 0: Minimal or no taxes on tobacco products."),
                                    html.P("Score 1: Low taxes with little impact on tobacco affordability."),
                                    html.P("Score 2: Basic taxes that somewhat increase tobacco prices."),
                                    html.P("Score 3: Moderate taxes that make tobacco less affordable."),
                                    html.P("Score 4: Good taxes with substantial price increases."),
                                    html.P("Score 5: Excellent taxes with high prices that significantly discourage tobacco consumption."),
                                ],
                                title="R: Raise taxes on tobacco",
                            ),
                        ],
                        start_collapsed=True,
                        flush=True,
                    )
                ),
            ],
            width=6
        ),
        dbc.Col(
            # Component 5 (Third row, single column)
            [
                html.H5('MPOWER Results by country'),
                html.P("Selecte the country:"),
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
    ],
    style={"margin-bottom": "40px"}  # Add space between the rows
    ),

    html.Div(style={"height": "30px"}),

    # New Row
    dbc.Row([
        # Column for References
        dbc.Col([
            html.H4("References"),
            html.A("The Global Health Observatory OData API", href="https://www.who.int/data/gho/info/gho-odata-api", target="_blank"),
            html.Br(),
            html.A("The Global Health Observatory", href="https://www.who.int/data/gho/data/indicators/indicator-details/GHO/gho-tobacco-control-monitor-current-tobaccouse-tobaccosmoking-cigarrettesmoking-agestd-tobagestdcurr", target="_blank"),
            html.Br(),
            html.A("WHO POWER initiative", href="https://www.who.int/initiatives/mpower", target="_blank"),

        ]),
        
        # Column for Resources
        dbc.Col([
            html.H4("About this project"),
            # Add links 
            html.P("Learn more about this project:"),
            html.A("Git Hub Repository", href="https://github.com/CarolMargeth/World_Health_Sensor_Project"),
        ]),

        # Column for Author Information
        dbc.Col([
            html.H4("About the author"),
            html.P("Author: Carol Calderon"),
            html.A("Let's connect through Linkedln!", href="https://www.linkedin.com/in/carolcalderon/"),
            html.P("Email: cmcalderonr1093@gmail.com"),        
        ]),
    ]),
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
