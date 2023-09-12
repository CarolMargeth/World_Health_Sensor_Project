# World_Health_Sensor_Project

This project isn't just about ETL processes; it takes a broader approach. It starts by pulling data from The Global Health Observatory OData API, then delves into data analysis using various data science techniques. Afterward, it culminates in creating an interactive application or dashboard and deploying it using cloud services. 

## About The Global Health Observatory API

The GHO data repository serves as the World Health Organization's (WHO) portal to health-related statistics concerning its 194 Member States. The GHO is constructed using a technology called RESTful web service. REST stands for Representational State Transfer, which is an architectural style used to design networked applications. In this context, GHO uses RESTful web services as the underlying technology to provide access to its data.

## About the Project Name

Initially, I named the project the "World Health Sensor Project" because I aimed to work with reliable and comprehensive global health data. As I progressed, I narrowed my focus to tobacco-related data. However, the project has the potential for expansion to include analysis and communication of various other global health topics and indicators found in the GHO repository.

## Project steps

1. Select the Data Source: Determine the specific API that provides the data needed for the analysis. Explore available public datasets. Determine the analysis goals.

2. Understand the API: Study the documentation of the OData API to understand its endpoints, query parameters, and how to retrieve data. Identify the available resources, data models, and relationships between entities.

3. Retrieve and Preprocess Data: Use the OData API to fetch the required data based on the analysis goals. Apply data preprocessing steps like cleaning, filtering, and transforming the data as necessary to prepare it for analysis.

4. Analyze the Data: Utilize data science techniques and libraries such as pandas, stats to perform exploratory data analysis (EDA), statistical analysis and visualizations. Extract meaningful insights and identify patterns or correlations in the data. Select the appropriate visualization tool like Matplotlib, Seaborn, or Plotly to create interactive and informative visualizations.

5. Design the application/dashboard: Design the user interface and layout of the dashboard using Dash library. Create an intuitive and user-friendly dashboard that allows users to interact with the visualizations, apply filters, and explore the data dynamically. Iterate on the design and make improvements based on user input and additional data analysis requirements.

6. Deploy the Dashboard: Host the dashboard on a web server or a cloud platform to make it accessible online. This involves deploying it as a web application utilizing AWS cloud hosting services. Test and Iterate: Test the functionality and usability of the dashboard, seeking feedback from potential users. 

## Application description

As I explained, after connecting with GHO API, the exploration derived in the building of the dashboard: ** "Global Tobacco Insights: Visualizing Smoking Trends, Health Consequences, and Control Policies" ** a dashboard that display important information about Smoking Prevalence by sex, countries and WHO regions, the relationship between smoking rates and premature deaths caused by non-communicable diseases (NCDs), and the efforts being undertaken by the countries to accomplish the MPOWER strategy. 

[Access the dashboard here](http://18.216.161.201:8050/)

## Repository structure

- Find the project workflow and the summarized version in the World Health Sensor Project and WHSP_summarized Notebooks.
- Find the application script to display the dashboard, the description of the dashboard and final datasets in Application folder.
- Explore some plots built during the exploration and preprocessing stages in the Visualizations folder.

## Sources

- [Global Health Observatory](https://www.who.int/data/gho/info/gho-odata-api)
- [GHO OData API](https://www.who.int/data/gho/info/gho-odata-api)
- [World Health Organization - MPOWER measures](https://www.who.int/initiatives/mpower)
- [Canada's Tobacco Strategy](https://www.canada.ca/en/health-canada/services/publications/healthy-living/canada-tobacco-strategy.html)

## Contact information
    Author: Carol Calderon
    Email: cmcalderonr1093@gmail.com
    Linkedln: https://www.linkedin.com/in/carolcalderon/

## Acknowledgments
- Dash Python User Guide: Dash is the original low-code framework for rapidly building data apps in Python. [Learn more here](https://dash.plotly.com/)
- Dash Bootstrap Components: dash-bootstrap-components is a library of Bootstrap components for Plotly Dash, that makes it easier to build consistently styled apps with complex, responsive layouts. [Learn more here](https://dash-bootstrap-components.opensource.faculty.ai/)
- Rahul Agarwal [How to Deploy a Streamlit App using an Amazon Free ec2 instance?](https://towardsdatascience.com/how-to-deploy-a-streamlit-app-using-an-amazon-free-ec2-instance-416a41f69dc3)
