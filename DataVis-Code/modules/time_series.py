from dash import html, dcc
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import pandas as pd  # <-- import-statement hinzugefügt
from data_processing import data_melted

# funktion für das layout der seite
def layout():
    # einzigartige elemente und länder aus den daten extrahieren
    elements = data_melted['Element'].unique()
    countries = ['All Countries'] + sorted(data_melted['Area'].unique())
    return html.Div([
        html.H3("Zeitreihen-Visualisierung"),
        html.Div([
            html.Label("Select Element:"),
            # dropdown-menü für die elemente
            dcc.Dropdown(
                id='element-dropdown-ts',
                options=[{'label': elem, 'value': elem} for elem in elements],
                value=elements[0]  # standardwert ist das erste element
            )
        ], style={'width': '30%', 'display': 'inline-block'}),
        html.Div([
            html.Label("Select Countries:"),
            # dropdown-menü für die länder, mehrfachauswahl erlaubt
            dcc.Dropdown(
                id='country-dropdown-ts',
                options=[{'label': country, 'value': country} for country in countries],
                value=['All Countries'],  # standardwert ist "alle länder"
                multi=True
            )
        ], style={'width': '30%', 'display': 'inline-block'}),
        dcc.Graph(id='time-series-chart')  # graph für das zeitreihendiagramm
    ])

# funktion zur registrierung der callbacks
def register_callbacks(app):
    @app.callback(
        Output('time-series-chart', 'figure'),
        [Input('element-dropdown-ts', 'value'),
         Input('country-dropdown-ts', 'value')]
    )
    def update_figure(selected_element, selected_countries):
        # daten filtern nach ausgewähltem element
        filtered_data = data_melted[data_melted['Element'] == selected_element]

        # daten gruppieren nach jahr und land, summe der werte berechnen
        data_agg = filtered_data.groupby(['Year', 'Area'])['Value'].sum().reset_index()

        # gesamtwerte für jedes land berechnen
        country_totals = data_agg.groupby('Area')['Value'].sum().reset_index()

        # länder sortieren nach gesamtwert
        sorted_countries = sorted(country_totals['Area'].values)

        # kategorien für die länder setzen und daten sortieren
        data_agg['Area'] = pd.Categorical(data_agg['Area'], categories=sorted_countries, ordered=True)
        data_agg = data_agg.sort_values(by=['Year', 'Area'])

        fig = go.Figure()

        # wenn "alle länder" ausgewählt ist, zeitreihen für alle länder hinzufügen
        if 'All Countries' in selected_countries:
            for country in sorted_countries:
                country_data = data_agg[data_agg['Area'] == country]
                fig.add_trace(go.Scatter(x=country_data['Year'], y=country_data['Value'], mode='lines', name=country, fill='tozeroy'))
        else:
            # zeitreihen nur für ausgewählte länder hinzufügen
            for country in selected_countries:
                country_data = data_agg[data_agg['Area'] == country]
                fig.add_trace(go.Scatter(x=country_data['Year'], y=country_data['Value'], mode='lines', name=country, fill='tozeroy'))

        # layout des diagrams anpassen
        fig.update_layout(
            title_text=f"die {selected_element} zeitreihen-visualisierung zeigt die jährlichen veränderungen der nahrungsmittelproduktion in den ausgewählten ländern ab 1962.",
            xaxis_title="jahr",
            yaxis_title="produzierte menge in 1000t"
        )

        return fig
