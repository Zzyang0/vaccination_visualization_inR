import dash
from dash import dcc, html, Input, Output, State
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta
import numpy as np

# Load the datasets with their original URL
vac_data_url = "https://raw.githubusercontent.com/IrisDin/vaccination_visulization_inR/main/country_vaccinations.csv"
vac_type_data_url = "https://raw.githubusercontent.com/IrisDin/vaccination_visulization_inR/main/country_vaccinations_by_manufacturer.csv"

try:
    vac_data = pd.read_csv(vac_data_url)
    vac_type_data = pd.read_csv(vac_type_data_url)
    print("Data loaded successfully!")
except Exception as e:
    print(f"Error loading data: {e}")
    print("Using sample data...")
    # Create sample data
    vac_data = pd.DataFrame({
        'country': ['China', 'US', 'India'],
        'date': pd.date_range(start='2021-01-01', periods=3),
        'daily_vaccinations': [1000000, 500000, 800000],
        'total_vaccinations': [3000000, 1500000, 2400000],
        'people_fully_vaccinated': [2000000, 1000000, 1600000]
    })
    
    vac_type_data = pd.DataFrame({
        'location': ['China', 'US', 'India'],
        'date': pd.date_range(start='2021-01-01', periods=3),
        'vaccine': ['Pfizer', 'Moderna', 'AstraZeneca'],
        'total_vaccinations': [1000000, 500000, 800000]
    })
    vac_type_data = vac_type_data.rename(columns={'location': 'country'})

# Data pre-processing
vac_type_data['date'] = pd.to_datetime(vac_type_data['date'])
vac_data['date'] = pd.to_datetime(vac_data['date'])

# Initialize the Dash app with the minty theme (similar to bslib's minty theme)
app = dash.Dash(
    __name__, 
    external_stylesheets=[
        'https://bootswatch.com/5/minty/bootstrap.min.css',
        'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.1/css/all.min.css'
    ]
)

# Expose the server variable for gunicorn
server = app.server

# App layout with tabs similar to the Shiny navbarPage
app.layout = html.Div([
    html.H1("COVID-19 Vaccination Analysis", className="p-3 bg-primary text-white text-center"),
    
    dcc.Tabs([
        # Introduction Tab
        dcc.Tab(label="Introduction", children=[
            html.Div([
                html.Img(src="https://publichealth.jhu.edu/sites/default/files/styles/article_feature/public/2021-07/carrying-equity-in-covid-19-vaccination-forward.png?h=f2862316&itok=C9sfEOAv", 
                         height=400, width=700),
                html.H1("Purpose/Importance:"),
                html.P("The COVID-19 pandemic has led to the dramatic loss of human life and presents unprecedented challenges to not only public health, but also individual health more importantly. Though, people who had Covid recovered, still Covid do have potential sequelae to the different organs. Thus, it is crucial and urgent to get vaccinated and make it universally accessible to ensure a safe condition for the general public. The pandemic is far from over, and vaccines are our best bet on staying safe. As more and more people get vaccinated, the community immunity, also individual community would both improve and further secure the invade of the virus. Our main issue is the inconvenience that covid brings to people's lives. This issue is very important because it relates to the long-term impact of covid on humans. To address this issue, we will conduct an in-depth analysis of people's willingness and brand of vaccination.",
                      style={"fontSize": 20}),
                html.Br(),
                html.H1("Main questions🤔:"),
                html.P("Question 1: To see the trend of people getting vaccinated around the world by analyzing different vaccine brand being used worldwide.",
                       style={"fontSize": 20}),
                html.Br(),
                html.P("Question 2: Daily vaccination trend in different country and in different period of time.",
                       style={"fontSize": 20}),
                html.Br(),
                html.P("Question 3: To visualize the distribution of vaccinated population in a world map.",
                       style={"fontSize": 20}),
                html.Br(),
                html.H1("About the dataset:"),
                html.P("We found the dataset from the Kaggle site which was collected from the authoritative organization Our World in Data GitHub repository specifically for the covid-19, and it is still continuing to update. There are two files of the dataset, one contains locations, also includes vaccination sources' information. The second file is information about the manufacturers like Moderna and Pfizer. From the comprehensive vaccination information in different countries, people can see the total number of people who get vaccinated in their country which might let them feel safe. Also, from the vaccination information, people can also visualize which country does not access adequate medical resources(vaccinations) that further provided them with help and facilitated the progress to ending the global pandemic.",
                       style={"fontSize": 20}),
                html.A("Visit kaggle Website to check our data", href="https://www.kaggle.com/gpreda/covid-world-vaccination-progress", target="_blank"),
                html.Br(),
                html.H1("limitations🦠:"),
                html.Br(),
                html.P("After viewing the dataset, we found out several limitations and problems of the dataset. To begin with, there is a lot of missing values in the front part of the dataset. However, when we scroll down the dataset, there are only a small amount of missing values remaining. To sum up, the missing values only made up a small proportion of the whole dataset. We think we can change the distribution of the missing value after filtering and sorting the dataset by using R. Also, another potential problem with the dataset is that there are over 70000 rows of the dataset which contain all different countries' vaccination information. This is a large dataset that might be hard to process and filter the core information and pattern we want. The potential solution we came up with is that we need to further explore our research question and drop the information or data we do not need. We need to clean and condense our dataset in order to get better visualization. In addition, we think it is necessary for us to add more features to the dataset for better analysis. For example, merging the vaccine type feature can help us better visualize the usage for different brands' vaccination like Pfizer or Moderna in different areas.",
                       style={"fontSize": 20}),
            ], className="container p-4")
        ], className="p-4"),
        
        # Vaccine Types Tab
        dcc.Tab(label="Vaccine types used in the world", children=[
            html.Div([
                html.Div([
                    html.Div([
                        html.H4("Select vaccine"),
                        dcc.Dropdown(
                            id='vac-type-dropdown',
                            options=[{'label': v, 'value': v} for v in vac_type_data['vaccine'].unique()],
                            value=['Moderna'],
                            multi=True
                        ),
                    ], className="col-md-3"),
                    
                    html.Div([
                        dcc.Graph(id='vac-type-plot'),
                        html.H1("Description/Analysis of the visualization📊:"),
                        html.Br(),
                        html.P("The reason why we construct the vaccine used in the world, to be more specific, classified by the brand of the vaccine throughout the world, is to see what's the trend of people getting vaccinated worldwide, and reveals the people's awareness of self-protection. Meanwhile, we can spot among all these different kinds of vaccines, which one is most prevalent after all. From the graphs generated, it is very obvious, considering all the countries as a whole, more and more people getting vaccinated global-wise, an increasing pattern, though there are some sag occurring. Another insight we can extract from the graph is that the most popular vaccines would be Pfizer/BioNtech, Moderna, and Pfizer is the one used most frequently.",
                               style={"fontSize": 23}),
                    ], className="col-md-9"),
                ], className="row")
            ], className="container p-4")
        ], className="p-4"),
        
        # Daily Vaccination Trend Tab
        dcc.Tab(label="Daily vaccination trend", children=[
            html.Div([
                html.Div([
                    html.Div([
                        html.H4("Select country"),
                        dcc.Dropdown(
                            id='country-dropdown',
                            options=[{'label': c, 'value': c} for c in vac_data['country'].unique()],
                            value=['China'],
                            multi=True
                        ),
                        html.Br(),
                        html.H4("Date range"),
                        dcc.DatePickerRange(
                            id='date-picker-range',
                            start_date=datetime(2021, 10, 1),
                            end_date=datetime(2021, 12, 31),
                            min_date_allowed=vac_data['date'].min(),
                            max_date_allowed=vac_data['date'].max()
                        ),
                    ], className="col-md-3"),
                    
                    html.Div([
                        dcc.Graph(id='line-daily-plot'),
                        html.H1("Description/Analysis of the visualization📊:"),
                        html.Br(),
                        html.P("The reason why we produce this visualization is to provide our audiences with an overview of the world's vaccination distribution. We offer several vaccination related variables for people to select and view. It is quite obvious that China has the highest daily vaccination and the most vaccinated population in the world.",
                               style={"fontSize": 23}),
                    ], className="col-md-9"),
                ], className="row")
            ], className="container p-4")
        ], className="p-4"),
        
        # Maps Tab
        dcc.Tab(label="Maps", children=[
            html.Div([
                html.Div([
                    html.Div([
                        html.H4("Different vaccination feature distribution"),
                        dcc.Dropdown(
                            id='map-feature-dropdown',
                            options=[
                                {'label': 'Daily Vaccinations', 'value': 'daily_vaccinations'},
                                {'label': 'Total Vaccinations', 'value': 'total_vaccinations'},
                                {'label': 'People Fully Vaccinated', 'value': 'people_fully_vaccinated'}
                            ],
                            value='daily_vaccinations'
                        ),
                    ], className="col-md-3"),
                    
                    html.Div([
                        dcc.Graph(id='map-plot'),
                        html.H1("Description/Analysis of the visualization📊:"),
                        html.Br(),
                        html.P("The visualization shown in the figure above provides a clearer and more specific understanding of the global acceptance rate of the vaccine dose. From the figure above, it can be seen that India has the most places for daily vaccination, while China's full vacation is the highest. But it is clear that the total number of people vaccinated nationwide is still low.",
                               style={"fontSize": 23}),
                    ], className="col-md-9"),
                ], className="row")
            ], className="container p-4")
        ], className="p-4"),
        
        # Summary/Takeaways Tab
        dcc.Tab(label="Summary/Takeaways", children=[
            html.Div([
                html.Img(src="https://www.hopkinsmedicine.org/-/media/images/health/1_-conditions/coronavirus/vaccine3.ashx?la=en&hash=E14E7B4842E409C6FC40A8659B1B68F3529C0841", 
                         height=450, width=700),
                html.H1("Specific takeaways💉："),
                html.P("First takeaway: There is an increasing pattern of vaccine types being used in the world and more and more people are getting vaccinated, which shows that people's self-protection awareness is increased as time goes by. Beyond this trend, it is obivious that Pfizer/BioNtech and Moderna are the top two brands that being used most frequently. By the end of Jan, 2022, more than 600 millions of people have taken the vaccine from Pfizer/BioNtech, which is the most popular brand all over the world.",
                       style={"fontSize": 20}),
                html.P("Second takeaway: The daily vaccination trend of the U.S. seems steady as time passes and has been kept under 5 millions per day. Compared with the U.S., Chinese daily vaccination rate has been constantly increased from under 5 millions per day to over 10 millions per day. This comparison proves that American people are not taking vaccination as seriously as Chinese do. Moreover, even though the daily vaccination number starts to decrease after Jan, 2022, China still has the highest daily vaccination rate than all of the other countries in the world.",
                       style={"fontSize": 20}),
                html.Br(),
                html.P("Third takeaway: China has the most vacccinated population in the world. India is the country that covered with the higest number of daily vaccinations. Since COVID outbreak is relatively early in China, so it is easy to tell that China is the one that takes the pandemic most seriously. As its nearby country, India also took immediate actions to fight against the coronavirus. The spreadout of the pandemic is extremly fast throughout the world. Countries with large population density are more able to be infected and the U.S. has also been influenced severely so it has a relative high vaccinated population as well.",
                       style={"fontSize": 20}),
                html.P("Forth Takeaway: Up to the most recent data, from the overall trend for the daily vaccinations in the country China, United States, and India all shown a decreasing tendency till the February 1st. Although these are the countries with relatively high daily vaccinations in general. Still, due to the gradual loose policy indifferent region, seems like the number of people getting vaccinated is decreasing. Especially in the United States, for instance, wearing a mask is become optional in some regions, and even at the restaurant, no vaccination verification is needed as well. Thus, it could be a crucial factor that leads to the nowadays trend.",
                       style={"fontSize": 20}),
                html.Br(),
                html.H1("Insight💡："),
                html.P("In recent years, the covid-19 pandemic has swept the entire globe and caused a large number of infections and deaths. From the data visualizations we made, we are able to find that China has the highest number of daily vaccinated also has shown the highest number of people fully vaccinated. To some extent, it is the country that most actively prevents and controls the pandemic mostly due to the strict regulations and widespread of vaccinations. And the U.S. also has a relatively high number of daily vaccinations, however, with a low level of people fully vaccinated. It is mostly due to the policy being made within different states and the consciousness of being vaccinated.",
                       style={"fontSize": 20}),
                html.Br(),
                html.H1("Broader implications："),
                html.P("As time passes by, the number of immune is increasing and shows that all human beings can recognize the importance of self-protection. People stick together to fight against the COVID-19 and this tough period of time is a historical moment that should be memorized by all human beings. Things are getting better right now and the world is getting covered by vaccines. So there would be more people being vaccinated in future no matter the daily vaccination trend is steady, increased, or decreased. Overall, the majority chooses to be vaccinated not only for protecting themselves, but also for protecting people they care for.",
                       style={"fontSize": 20}),
            ], className="container p-4")
        ], className="p-4"),
    ], className="p-4")
])

# Callback for Vaccine Types Plot
@app.callback(
    Output('vac-type-plot', 'figure'),
    Input('vac-type-dropdown', 'value')
)
def update_vac_type_plot(selected_vaccines):
    if not selected_vaccines:
        return go.Figure()
    
    filtered_data = vac_type_data[vac_type_data['vaccine'].isin(selected_vaccines)]
    
    # Create a bar chart similar to the ggplot in the Shiny app
    fig = px.bar(
        filtered_data,
        x="date",
        y="total_vaccinations",
        color="vaccine",
        barmode="group",
        facet_col="vaccine",
        labels={"date": "Date", "total_vaccinations": "Total Vaccination"},
        title="Vaccine types used in the world"
    )
    
    fig.update_xaxes(tickangle=90)
    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font={"size": 12},
        height=600
    )
    
    return fig

# Callback for Daily Vaccination Line Plot
@app.callback(
    Output('line-daily-plot', 'figure'),
    [Input('country-dropdown', 'value'),
     Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date')]
)
def update_line_daily_plot(selected_countries, start_date, end_date):
    if not selected_countries:
        return go.Figure()
    
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    
    filtered_data = vac_data[
        (vac_data['country'].isin(selected_countries)) & 
        (vac_data['date'] >= start_date) & 
        (vac_data['date'] <= end_date)
    ]
    
    # Create a line chart
    fig = px.line(
        filtered_data,
        x="date",
        y="daily_vaccinations",
        color="country",
        labels={"date": "Date", "daily_vaccinations": "Daily Vaccinations"},
        title="Daily vaccination trend"
    )
    
    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font={"size": 12},
        height=600
    )
    
    return fig

# Callback for Map Plot
@app.callback(
    Output('map-plot', 'figure'),
    Input('map-feature-dropdown', 'value')
)
def update_map_plot(selected_feature):
    # Process data for the map
    # Group by country and get the most recent data
    processed = vac_data.groupby('country').apply(
        lambda x: x.loc[x['date'].idxmax()]
    ).reset_index(drop=True)
    
    # Create the map
    # Note: Different color scales based on the feature selected
    color_scales = {
        'daily_vaccinations': 'Reds',
        'total_vaccinations': 'Blues',
        'people_fully_vaccinated': 'Greens'
    }
    
    fig = px.choropleth(
        processed,
        locations="country",
        locationmode="country names",
        color=selected_feature,
        hover_name="country",
        color_continuous_scale=color_scales.get(selected_feature, 'Reds'),
        labels={selected_feature: selected_feature.replace('_', ' ').title()},
        title=f"{selected_feature.replace('_', ' ').title()} world map"
    )
    
    fig.update_layout(
        geo=dict(
            showframe=False,
            showcoastlines=True,
            projection_type='natural earth'
        ),
        height=600
    )
    
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
