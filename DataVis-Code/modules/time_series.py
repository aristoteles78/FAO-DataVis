from dash import html, dcc
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import pandas as pd  # <-- Add this import statement
from data_processing import data_melted

def layout():
    elements = data_melted['Element'].unique()
    countries = ['All Countries'] + sorted(data_melted['Area'].unique())
    return html.Div([
        html.H3("Time Series Visualization"),
        html.Div([
            html.Label("Select Element:"),
            dcc.Dropdown(
                id='element-dropdown-ts',
                options=[{'label': elem, 'value': elem} for elem in elements],
                value=elements[0]
            )
        ], style={'width': '30%', 'display': 'inline-block'}),
        html.Div([
            html.Label("Select Countries:"),
            dcc.Dropdown(
                id='country-dropdown-ts',
                options=[{'label': country, 'value': country} for country in countries],
                value=['All Countries'],
                multi=True
            )
        ], style={'width': '30%', 'display': 'inline-block'}),
        dcc.Graph(id='time-series-chart')
    ])

def register_callbacks(app):
    @app.callback(
        Output('time-series-chart', 'figure'),
        [Input('element-dropdown-ts', 'value'),
         Input('country-dropdown-ts', 'value')]
    )
    def update_figure(selected_element, selected_countries):
        filtered_data = data_melted[data_melted['Element'] == selected_element]

        data_agg = filtered_data.groupby(['Year', 'Area'])['Value'].sum().reset_index()

        country_totals = data_agg.groupby('Area')['Value'].sum().reset_index()

        sorted_countries = sorted(country_totals['Area'].values)

        data_agg['Area'] = pd.Categorical(data_agg['Area'], categories=sorted_countries, ordered=True)
        data_agg = data_agg.sort_values(by=['Year', 'Area'])

        fig = go.Figure()

        if 'All Countries' in selected_countries:
            for country in sorted_countries:
                country_data = data_agg[data_agg['Area'] == country]
                fig.add_trace(go.Scatter(x=country_data['Year'], y=country_data['Value'], mode='lines', name=country, fill='tozeroy'))
        else:
            for country in selected_countries:
                country_data = data_agg[data_agg['Area'] == country]
                fig.add_trace(go.Scatter(x=country_data['Year'], y=country_data['Value'], mode='lines', name=country, fill='tozeroy'))

        fig.update_layout(
            title_text=f"The {selected_element} time series visualization represents the annual changes in food production values across selected countries from 1962 onward.",
            xaxis_title="Year",
            yaxis_title=f"Amount produced in 1000t"
        )

        return fig
