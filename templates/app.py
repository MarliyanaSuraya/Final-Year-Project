from re import template
import pandas as pd
import io
import requests
from flask import Flask, render_template, request, redirect, url_for
import plotly.express as px
import numpy as np

app = Flask(__name__)

historical_data_drive_link = 'https://drive.google.com/uc?id=1ERrk3hay3_VmkZ8otlg6swr590hx8yEm'
predicted_data_drive_link = 'https://drive.google.com/uc?id=1GiTaMNu7DIimApf1qDDelzPWX2IbS5rh'

# Load historical data
#historical_data = pd.read_excel(r'C:\Users\marliyana\FYP Codes\Project folder\data\Combined-Dataset.xlsx')

# Load predicted data
#predicted_data = pd.read_excel(r'C:\Users\marliyana\FYP Codes\Project folder\data\marli-future-prediction.xlsx')

# Function to load historical data
def load_historical_data():
    # Download data from Google Drive link
    download_url = f'https://drive.google.com/uc?id=1ERrk3hay3_VmkZ8otlg6swr590hx8yEm'
    response = requests.get(download_url)
    content = io.BytesIO(response.content)

    # Read historical data from the downloaded content
    historical_data = pd.read_excel(content, engine='openpyxl')


    return historical_data

# Function to load predicted data
def load_predicted_data():
    # Download data from Google Drive link
    download_url = f'https://drive.google.com/uc?id=1GiTaMNu7DIimApf1qDDelzPWX2IbS5rh'
    response = requests.get(download_url)
    content = io.BytesIO(response.content)

    # Read predicted data from the downloaded content
    predicted_data = pd.read_excel(content)

    # Additional data loading and processing logic...

    return predicted_data

@app.route('/')
def index():

    # Load historical data
    historical_data = load_historical_data()
    # Get unique country names for checkbox
    country_names = historical_data['Country name'].unique()

    return render_template('index.html', country_names=country_names)

@app.route('/visualization', methods=['POST','GET'])
def visualization():
    # Get selected countries from the form
    selected_countries = request.form.getlist('country')

    # Load historical data
    historical_data = load_historical_data()

     # Load predicted data
    predicted_data = load_predicted_data()

    # Filter data for the selected countries
    selected_countries_data = historical_data[historical_data['Country name'].isin(selected_countries)]

    # Filter data for the predicted years
    predicted_years_data = predicted_data[predicted_data['Country name'].isin(selected_countries)]

    # Create visualizations
    fig_population = px.line(selected_countries_data, x='Year', y='Population', color='Country name', title='Population Over Time')
    fig_death_rate = px.line(selected_countries_data, x='Year', y='Death Rate', color='Country name', title='Death Rate Over Time')
    fig_birth_rate = px.line(selected_countries_data, x='Year', y='Birth Rate', color='Country name', title='Birth Rate Over Time')
    fig_migration_trend = px.line(selected_countries_data, x='Year', y='Migration Trend', color='Country name', title='Migration Trend Over Time')

    fig_predicted_population = px.line(predicted_years_data, x='Year', y='Predicted Population', color='Country name', title='Predicted Population (2022-2027)')

    fig_population.update_layout(
    paper_bgcolor = "#46005F",
    font = dict(color = '#FFFFFF'),
    xaxis=dict( 
        rangeselector=dict( 
            buttons=list([ 
                dict(count=1, 
                     step="day", 
                     stepmode="backward"), 
            ]) 
        ), 
        rangeslider=dict( 
            visible=True,
        ),
    ) ,
)
    

    fig_death_rate.update_layout(
    paper_bgcolor = "#46005F",
    font = dict(color = '#FFFFFF'),
    xaxis=dict( 
        rangeselector=dict( 
            buttons=list([ 
                dict(count=1, 
                     step="day", 
                     stepmode="backward"), 
            ]) 
        ), 
        rangeslider=dict( 
            visible=True,
        ), 
    ) 
    )

    fig_birth_rate.update_layout( 
    paper_bgcolor = "#46005F",
    font = dict(color = '#FFFFFF'),
    xaxis=dict( 
        rangeselector=dict( 
            buttons=list([ 
                dict(count=1, 
                     step="day", 
                     stepmode="backward"), 
            ]) 
        ), 
        rangeslider=dict( 
            visible=True,
        ), 
    ) 
    )
    
    fig_migration_trend.update_layout(
    paper_bgcolor = "#46005F",
    font = dict(color = '#FFFFFF'), 
    xaxis=dict( 
        rangeselector=dict( 
            buttons=list([ 
                dict(count=1, 
                     step="day", 
                     stepmode="backward"), 
            ]) 
        ), 
        rangeslider=dict( 
            visible=True,
        ), 
    ) 
    )

    fig_predicted_population.update_layout( 
    paper_bgcolor = "#46005F",
    font = dict(color = '#FFFFFF'),
    xaxis=dict( 
        rangeselector=dict( 
            buttons=list([ 
                dict(count=1, 
                     step="day", 
                     stepmode="backward"), 
            ]) 
        ), 
        rangeslider=dict( 
            visible=True,
        ), 
    ) 
    )

    return render_template(
        'visualization.html',
        fig_population=fig_population.to_html(full_html=False),
        fig_death_rate=fig_death_rate.to_html(full_html=False),
        fig_birth_rate=fig_birth_rate.to_html(full_html=False),
        fig_migration_trend=fig_migration_trend.to_html(full_html=False),
        fig_predicted_population=fig_predicted_population.to_html(full_html=False),
        selected_countries=selected_countries, 
        historical_data=historical_data,
        predicted_data=predicted_data
    )

@app.route('/visualization2', methods=['GET', 'POST'])
def visualization2():
    # Get selected countries from the URL
    selected_countries = request.args.get('country').split(',')
    print("Selected countries:", selected_countries)

    # Load historical data
    historical_data = load_historical_data()

     # Load predicted data
    predicted_data = load_predicted_data()

    # Filter data for the selected countries
    selected_countries_data = historical_data[historical_data['Country name'].isin(selected_countries)]

    # Filter data for the predicted years
    predicted_years_data = predicted_data[predicted_data['Country name'].isin(selected_countries)]

    # Create visualizations
    fig_population = px.line(selected_countries_data, x='Year', y='Population', color='Country name', title='Population Over Time')
    fig_death_rate = px.line(selected_countries_data, x='Year', y='Death Rate', color='Country name', title='Death Rate Over Time')
    fig_birth_rate = px.line(selected_countries_data, x='Year', y='Birth Rate', color='Country name', title='Birth Rate Over Time')
    fig_migration_trend = px.line(selected_countries_data, x='Year', y='Migration Trend', color='Country name', title='Migration Trend Over Time')

    fig_predicted_population = px.line(predicted_years_data, x='Year', y='Predicted Population', color='Country name', title='Predicted Population (2022-2027)')

    fig_population.update_layout( 
    paper_bgcolor = "#46005F",
    font = dict(color = '#FFFFFF'),
    xaxis=dict( 
        rangeselector=dict( 
            buttons=list([ 
                dict(count=1, 
                     step="day", 
                     stepmode="backward"), 
            ]) 
        ), 
        rangeslider=dict( 
            visible=True,
        ),
    ) ,
)
    

    fig_death_rate.update_layout( 
    paper_bgcolor = "#46005F",
    font = dict(color = '#FFFFFF'),
    xaxis=dict( 
        rangeselector=dict( 
            buttons=list([ 
                dict(count=1, 
                     step="day", 
                     stepmode="backward"), 
            ]) 
        ), 
        rangeslider=dict( 
            visible=True,
        ), 
    ) 
    )

    fig_birth_rate.update_layout( 
    paper_bgcolor = "#46005F",
    font = dict(color = '#FFFFFF'),
    xaxis=dict( 
        rangeselector=dict( 
            buttons=list([ 
                dict(count=1, 
                     step="day", 
                     stepmode="backward"), 
            ]) 
        ), 
        rangeslider=dict( 
            visible=True,
        ), 
    ) 
    )
    
    fig_migration_trend.update_layout( 
    paper_bgcolor = "#46005F",
    font = dict(color = '#FFFFFF'),
    xaxis=dict( 
        rangeselector=dict( 
            buttons=list([ 
                dict(count=1, 
                     step="day", 
                     stepmode="backward"), 
            ]) 
        ), 
        rangeslider=dict( 
            visible=True,
        ), 
    ) 
    )

    fig_predicted_population.update_layout( 
    paper_bgcolor = "#46005F",
    font = dict(color = '#FFFFFF'),
    xaxis=dict( 
        rangeselector=dict( 
            buttons=list([ 
                dict(count=1, 
                     step="day", 
                     stepmode="backward"), 
            ]) 
        ), 
        rangeslider=dict( 
            visible=True,
        ), 
    ) 
    )

    return render_template(
        'visualization.html',
        fig_population=fig_population.to_html(full_html=False),
        fig_death_rate=fig_death_rate.to_html(full_html=False),
        fig_birth_rate=fig_birth_rate.to_html(full_html=False),
        fig_migration_trend=fig_migration_trend.to_html(full_html=False),
        fig_predicted_population=fig_predicted_population.to_html(full_html=False),
        selected_countries=selected_countries, 
        historical_data=historical_data,
        predicted_data=predicted_data
    )

@app.route('/choropleth', methods=['GET', 'POST'])
def choropleth():

    # Get selected countries from the URL
    selected_countries = request.args.get('country').split(',')

    # Load historical data
    historical_data = load_historical_data()

     # Load predicted data
    predicted_data = load_predicted_data()

    # Filter data for the selected countries
    selected_countries_data = historical_data[historical_data['Country name'].isin(selected_countries)]

    # Filter data for the predicted years
    predicted_years_data = predicted_data[predicted_data['Country name'].isin(selected_countries)]

    # Create a choropleth map
    fig_population_map = px.choropleth(
        selected_countries_data,
        locations='Country name',
        locationmode='country names',
        color='Population',
        hover_name='Country name',
        color_continuous_scale='purpor',
        title='Population Over Time',
        animation_frame="Year", 
        animation_group="Country name",  
    ).update_traces(
        colorbar=dict(outlinewidth=0, ticks='outside', ticklen=3)
    ).update_geos(
        projection_type="orthographic",
        showland=True, landcolor="#50C878",
        showocean=True, oceancolor="#82EEFD",
        bgcolor = "#46005F",
        framecolor = "#444", 
        lataxis_showgrid = True,
        lataxis_gridcolor = "#A15B9E",
        lonaxis_showgrid = True,
        lonaxis_gridcolor = "#A15B9E",
        projection_rotation=dict(lon=30, lat=40, roll=0),
        showframe = True,
    ).update_layout(
        width=600, 
        height=600 ,
        paper_bgcolor = "#46005F",
        font = dict(color = '#FFFFFF')
    ) 

    

     # Create a choropleth map
    fig_birth_map = px.choropleth(
        selected_countries_data,
        locations='Country name',
        locationmode='country names',
        color='Birth Rate',
        hover_name='Country name',
        color_continuous_scale='purpor',
        title='Birth Rate Over Time',
        animation_frame="Year", 
        animation_group="Country name",
     ).update_traces(
        colorbar=dict(outlinewidth=0, ticks='outside', ticklen=3)
    ).update_geos(
        projection_type="orthographic",
        showland=True, landcolor="#50C878",
        showocean=True, oceancolor="#82EEFD",
        bgcolor = "#46005F",
        framecolor = "#444", 
        lataxis_showgrid = True,
        lataxis_gridcolor = "#A15B9E",
        lonaxis_showgrid = True,
        lonaxis_gridcolor = "#A15B9E",
        projection_rotation=dict(lon=30, lat=40, roll=0),
        showframe = True,
    ).update_layout(
        width=600, 
        height=600 ,
        paper_bgcolor = "#46005F",
        font = dict(color = '#FFFFFF')
    )  

     # Create a choropleth map
    fig_death_map = px.choropleth(
        selected_countries_data,
        locations='Country name',
        locationmode='country names',
        color='Death Rate',
        hover_name='Country name',
        color_continuous_scale='purpor',
        title='Death Rate Over Time',
        animation_frame="Year",
        animation_group="Country name",
     ).update_traces(
        colorbar=dict(outlinewidth=0, ticks='outside', ticklen=3)
    ).update_geos(
        projection_type="orthographic",
        showland=True, landcolor="#50C878",
        showocean=True, oceancolor="#82EEFD",
        bgcolor = "#46005F",
        framecolor = "#444", 
        lataxis_showgrid = True,
        lataxis_gridcolor = "#A15B9E",
        lonaxis_showgrid = True,
        lonaxis_gridcolor = "#A15B9E",
        projection_rotation=dict(lon=30, lat=40, roll=0),
        showframe = True,
    ).update_layout(
        width=600, 
        height=600 ,
        paper_bgcolor = "#46005F",
        font = dict(color = '#FFFFFF')
    )  

    fig_migration_map = px.choropleth(
        selected_countries_data,
        locations='Country name',
        locationmode='country names',
        color='Migration Trend',
        hover_name='Country name',
        color_continuous_scale='purpor',
        title='Migration Trend Over Time',
        animation_frame="Year", 
        animation_group="Country name",
     ).update_traces(
        colorbar=dict(outlinewidth=0, ticks='outside', ticklen=3)
    ).update_geos(
        projection_type="orthographic",
        showland=True, landcolor="#50C878",
        showocean=True, oceancolor="#82EEFD",
        bgcolor = "#46005F",
        framecolor = "#444", 
        lataxis_showgrid = True,
        lataxis_gridcolor = "#A15B9E",
        lonaxis_showgrid = True,
        lonaxis_gridcolor = "#A15B9E",
        projection_rotation=dict(lon=30, lat=40, roll=0),
        showframe = True,
    ).update_layout(
        width=600, 
        height=600 ,
        paper_bgcolor = "#46005F",
        font = dict(color = '#FFFFFF')
    ) 

    fig_predict_map = px.choropleth(
        predicted_years_data,
        locations='Country name',
        locationmode='country names',
        color='Predicted Population',
        hover_name='Country name',
        color_continuous_scale='purpor',
        title='Predicted Population (2022-2027)',
        animation_frame="Year", 
        animation_group="Country name",
     ).update_traces(
        colorbar=dict(outlinewidth=0, ticks='outside', ticklen=3)
    ).update_geos(
        projection_type="orthographic",
        showland=True, landcolor="#50C878",
        showocean=True, oceancolor="#82EEFD",
        bgcolor = "#46005F",
        framecolor = "#444", 
        lataxis_showgrid = True,
        lataxis_gridcolor = "#A15B9E",
        lonaxis_showgrid = True,
        lonaxis_gridcolor = "#A15B9E",
        projection_rotation=dict(lon=30, lat=40, roll=0),
        showframe = True,
    ).update_layout(
        width=600, 
        height=600 ,
        paper_bgcolor = "#46005F",
        font = dict(color = '#FFFFFF')
    ) 

    return render_template(
        'choropleth.html',
        fig_population_map=fig_population_map.to_html(full_html=False, auto_play = False),
        fig_birth_map=fig_birth_map.to_html(full_html=False, auto_play = False),
        fig_death_map=fig_death_map.to_html(full_html=False, auto_play = False),
        fig_migration_map=fig_migration_map.to_html(full_html=False, auto_play = False),
        fig_predict_map=fig_predict_map.to_html(full_html=False, auto_play = False),
        selected_countries=selected_countries
    )

@app.route('/scatter', methods=['GET', 'POST'])
def scatter():

    # Get selected countries from the URL
    selected_countries = request.args.get('country').split(',')

    # Load historical data
    historical_data = load_historical_data()

     # Load predicted data
    predicted_data = load_predicted_data()

    # Filter data for the selected countries
    selected_countries_data = historical_data[historical_data['Country name'].isin(selected_countries)]

    # Filter data for the predicted years
    predicted_years_data = predicted_data[predicted_data['Country name'].isin(selected_countries)]

    # Create visualizations
    fig_population_scatter = px.scatter(selected_countries_data, x='Year', y='Population', color='Country name', title='Population Over Time')
    fig_death_rate_scatter = px.scatter(selected_countries_data, x='Year', y='Death Rate', color='Country name', title='Death Rate Over Time')
    fig_birth_rate_scatter = px.scatter(selected_countries_data, x='Year', y='Birth Rate', color='Country name', title='Birth Rate Over Time')
    fig_migration_trend_scatter = px.scatter(selected_countries_data, x='Year', y='Migration Trend', color='Country name', title='Migration Trend Over Time')

    fig_predicted_population_scatter = px.scatter(predicted_years_data, x='Year', y='Predicted Population', color='Country name', title='Predicted Population (2022-2027)')

    fig_population_scatter.update_layout(
    paper_bgcolor = "#46005F",
    font = dict(color = '#FFFFFF'),
    xaxis=dict( 
        rangeselector=dict( 
            buttons=list([ 
                dict(count=1, 
                     step="day", 
                     stepmode="backward"), 
            ]) 
        ), 
        rangeslider=dict( 
            visible=True,
        ),
    ) ,
)
    

    fig_death_rate_scatter.update_layout( 
    paper_bgcolor = "#46005F",
    font = dict(color = '#FFFFFF'),
    xaxis=dict( 
        rangeselector=dict( 
            buttons=list([ 
                dict(count=1, 
                     step="day", 
                     stepmode="backward"), 
            ]) 
        ), 
        rangeslider=dict( 
            visible=True,
        ), 
    ) 
    )

    fig_birth_rate_scatter.update_layout( 
    paper_bgcolor = "#46005F",
    font = dict(color = '#FFFFFF'),
    xaxis=dict( 
        rangeselector=dict( 
            buttons=list([ 
                dict(count=1, 
                     step="day", 
                     stepmode="backward"), 
            ]) 
        ), 
        rangeslider=dict( 
            visible=True,
        ), 
    ) 
    )
    
    fig_migration_trend_scatter.update_layout(
    paper_bgcolor = "#46005F",
    font = dict(color = '#FFFFFF'),
    xaxis=dict( 
        rangeselector=dict( 
            buttons=list([ 
                dict(count=1, 
                     step="day", 
                     stepmode="backward"), 
            ]) 
        ), 
        rangeslider=dict( 
            visible=True,
        ), 
    ) 
    )

    fig_predicted_population_scatter.update_layout(
    paper_bgcolor = "#46005F",
    font = dict(color = '#FFFFFF'),
    xaxis=dict( 
        rangeselector=dict( 
            buttons=list([ 
                dict(count=1, 
                     step="day", 
                     stepmode="backward"), 
            ]) 
        ), 
        rangeslider=dict( 
            visible=True,
        ), 
    ) 
    )

    return render_template(
        'scatter.html',
        fig_population_scatter=fig_population_scatter.to_html(full_html=False),
        fig_death_rate_scatter=fig_death_rate_scatter.to_html(full_html=False),
        fig_birth_rate_scatter=fig_birth_rate_scatter.to_html(full_html=False),
        fig_migration_trend_scatter=fig_migration_trend_scatter.to_html(full_html=False),
        fig_predicted_population_scatter=fig_predicted_population_scatter.to_html(full_html=False),
        selected_countries=selected_countries, 
        historical_data=historical_data,
        predicted_data=predicted_data
    )

def calculate_population_growth_rate(population_1950, population_2021):
    growth_rate = ((population_2021 - population_1950) / population_1950) * 100
    growth = population_2021 - population_1950
    return growth, growth_rate

@app.route('/analysis', methods=['GET', 'POST'])
def analysis():
    # Get selected countries from the URL
    selected_countries = request.args.get('country').split(',')

    # Load historical data
    historical_data = load_historical_data()

    # Filter data for the selected countries
    selected_countries_data = historical_data[historical_data['Country name'].isin(selected_countries)]
    # Perform analysis
    # Calculate population growth rate for each country
    population_growth_rates = []
    for country in selected_countries:
        country_data = selected_countries_data[selected_countries_data['Country name'] == country]
        population_1950 = country_data.loc[country_data['Year'] == 1950, 'Population'].values[0]
        population_2021 = country_data.loc[country_data['Year'] == 2021, 'Population'].values[0]
        growth_rate = calculate_population_growth_rate(population_1950, population_2021)
        population_growth_rates.append((country, growth_rate))

    population_growth_rates = []
    for country in selected_countries:
        country_data = selected_countries_data[selected_countries_data['Country name'] == country]
        population_1950 = country_data.loc[country_data['Year'] == 1950, 'Population'].values[0]
        population_2021 = country_data.loc[country_data['Year'] == 2021, 'Population'].values[0]
        growth = calculate_population_growth_rate(population_1950, population_2021)
        population_growth_rates.append((country, growth))

    # Calculate correlation coefficients for each selected country
    correlation_coefficients = []
    for country, (growth, growth_rate) in population_growth_rates:
        country_data = selected_countries_data[selected_countries_data['Country name'] == country]
        population_rate = country_data['Population'].values
        birth_rate = country_data['Birth Rate'].values
        death_rate = country_data['Death Rate'].values
        migration_trend = country_data['Migration Trend'].values
        growth_rate = growth_rate

        correlation_birth_growth = np.corrcoef(birth_rate, population_rate)[0, 1]
        correlation_death_growth = np.corrcoef(death_rate, population_rate)[0, 1]
        correlation_migration_growth = np.corrcoef(migration_trend, population_rate)[0, 1]
        correlation_coefficients.append((country, correlation_birth_growth, correlation_death_growth, correlation_migration_growth))

    print(correlation_coefficients)

    return render_template(
        'analysis.html',
        selected_countries=selected_countries,
        population_growth_rates=population_growth_rates,
        correlation_coefficients=correlation_coefficients,
    )




if __name__ == '__main__':
    app.run(debug=True)


