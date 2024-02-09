# Import necessary libraries
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Load the data using pandas
data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv')

# Initialize the Dash app
app = dash.Dash(__name__)

# Set the title of the dashboard
app.title = "Automobile Statistics Dashboard"

# Create the dropdown menu options
dropdown_options = [
    {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
    {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
]

# List of years 
year_list = [i for i in range(1980, 2024, 1)]

# Create the layout of the app
app.layout = html.Div([
    # Header title
    html.H1(app.title, style={"textAlign": "center", "color": "#503D36", "font-size": 24}),
    # Dropdowns for selecting statistics and year
    html.Div([
        html.Label("Select Statistics :"),
        dcc.Dropdown(
            id='dropdown-statistics',
            options=dropdown_options,
            value='Select Statistics',
            placeholder='Select a report type',
            style={"width": "80%", "padding": "3px", "font-size": "20px", "textAlign": "center"}
        )
    ]),
    html.Div(dcc.Dropdown(
        id='select-year',
        options=[{'label': i, 'value': i} for i in year_list],
        value='Select Year',
        style={"width": "80%", "padding": "3px", "font-size": "20px", "textAlign": "center"}
    )),
    # Container for displaying output (graphs)
    html.Div(id='output-container', className='chart-grid', style={"display": "flex"})
])

# Callback to update the select-year dropdown's disabled property
@app.callback(
    Output(component_id='select-year', component_property='disabled'),
    Input(component_id='dropdown-statistics', component_property='value')
)
def update_input_container(selected_statistics):
    if selected_statistics == 'Yearly Statistics':
        return False
    else:
        return True

# Callback for plotting
@app.callback(
    Output(component_id='output-container', component_property='children'),
    [Input(component_id='select-year', component_property='value'), Input(component_id='dropdown-statistics', component_property='value')]
)
def update_output_container(selected_year, selected_statistics):
    if selected_statistics == 'Recession Period Statistics':
        # Filter the data for recession periods
        recession_data = data[data['Recession'] == 1]
        
        # Plot 1: Average Automobile Sales fluctuation over Recession Period
        chart1 = dcc.Graph(
            figure=px.line(recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index(), 
                           x='Year', y='Automobile_Sales', title="Average Automobile Sales fluctuation over Recession Period")
        )
        
        # Plot 2: Average number of vehicles sold by vehicle type
        chart2 = dcc.Graph(
            figure=px.bar(recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index(), 
                          x="Vehicle_Type", y='Automobile_Sales', title="Average number of vehicles sold by vehicle type")
        )
        
        # Plot 3: Total expenditure share by vehicle type during recessions
        chart3 = dcc.Graph(
            figure=px.pie(recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index(), 
                          values='Advertising_Expenditure', names='Vehicle_Type', title='Total expenditure share by vehicle type during recessions')
        )
        
        # Plot 4: Effect of Unemployment Rate on Vehicle Type and Sales
        chart4 = dcc.Graph(
            figure=px.bar(recession_data.groupby(['Vehicle_Type', 'unemployment_rate'])['Automobile_Sales'].mean().reset_index(), 
                          x='unemployment_rate', y='Automobile_Sales', color='Vehicle_Type', title='Effect of Unemployment Rate on Vehicle Type and Sales')
        )

        return [html.Div(className='chart-item', children=[chart1, chart2]), 
                html.Div(className='chart-item', children=[chart3, chart4])]
    
    elif selected_statistics == 'Yearly Statistics' and selected_year != 'Select Year':
        yearly_data = data[data['Year'] == selected_year]
        
        # Plot 1: Yearly Automobile sales
        chart1 = dcc.Graph(
            figure=px.line(data.groupby('Year')['Automobile_Sales'].mean().reset_index(), 
                           x='Year', y="Automobile_Sales", title='Yearly Automobile sales')
        )
        
        # Plot 2: Monthly Automobile sales
        chart2 = dcc.Graph(
            figure=px.line(yearly_data, x="Month", y="Automobile_Sales", title="Monthly Automobile sales")
        )
        
        # Plot 3: Average Vehicles Sold by Vehicle Type in the selected year
        chart3 = dcc.Graph(
            figure=px.bar(yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index(), 
                          x='Vehicle_Type', y='Automobile_Sales', title=f'Average Vehicles Sold by Vehicle Type in the year {selected_year}')
        )
        
        # Plot 4: Total expenditure share by vehicle type
        chart4 = dcc.Graph(
            figure=px.pie(yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index(), 
                          values='Advertising_Expenditure', names='Vehicle_Type', title='Total expenditure share by vehicle type')
        )

        return [html.Div(className='chart-item', children=[chart1, chart2]), 
                html.Div(className='chart-item', children=[chart3, chart4])]
    
    else:
        return None

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)
