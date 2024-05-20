from dash import html, dcc
import plotly.express as px
from dash.dependencies import Input, Output
import pandas as pd
from data_processing import data_melted

# funktion für das layout der seite
def layout():
    # liste der länder mit "alle länder" am anfang
    countries = ['All Countries'] + sorted(data_melted['Area'].unique())
    # liste der jahre sortiert
    years = sorted(data_melted['Year'].unique())
    return html.Div([
        html.H3("nahrungsmittel- vs futterproduktion torten-diagramm"),
        html.Div([
            html.Label("Select Country:"),
            # dropdown-menü für die länder
            dcc.Dropdown(
                id='country-dropdown-pie',
                options=[{'label': country, 'value': country} for country in countries],
                value='All Countries'  # standardwert ist "alle länder"
            )
        ], style={'width': '45%', 'display': 'inline-block'}),
        html.Div([
            html.Label("Select Year:"),
            # dropdown-menü für die jahre
            dcc.Dropdown(
                id='year-dropdown-pie',
                options=[{'label': str(year), 'value': year} for year in years],
                value=years[0]  # standardwert ist das erste jahr in der liste
            )
        ], style={'width': '45%', 'display': 'inline-block'}),
        dcc.Graph(id='pie-chart')  # graph für das tortendiagramm
    ])

# funktion zur registrierung der callbacks
def register_callbacks(app):
    @app.callback(
        Output('pie-chart', 'figure'),
        [Input('country-dropdown-pie', 'value'),
         Input('year-dropdown-pie', 'value')]
    )
    def update_pie_chart(selected_country, selected_year):
        # daten filtern nach ausgewähltem jahr
        filtered_data = data_melted[data_melted['Year'] == selected_year]
        
        # daten weiter filtern nach ausgewähltem land, wenn nicht "alle länder" ausgewählt ist
        if selected_country != 'All Countries':
            filtered_data = filtered_data[filtered_data['Area'] == selected_country]

        # wenn keine daten vorhanden sind, ein leeres tortendiagramm anzeigen
        if filtered_data.empty:
            fig = px.pie(
                names=['No Data'],
                values=[1],
                title=f'Food vs Feed Production for {selected_country} in {selected_year}'
            )
            fig.update_traces(marker=dict(colors=['lightgrey']), textinfo='none')
            fig.update_layout(annotations=[dict(text='No Data Available',
                                                x=0.5, y=0.5, font_size=20, showarrow=False)])
            return fig

        # daten gruppieren nach "Element" und summieren der "Value"
        grouped_data = filtered_data.groupby('Element').agg({'Value': 'sum', 'Unit': 'first'}).reset_index()

        # tortendiagramm erstellen
        fig = px.pie(
            grouped_data,
            names='Element',
            values='Value',
            title=f'Food vs Feed Production for {selected_country} in {selected_year}',
            hole=0.4  # donutförmiges diagramm
        )

        # annotationen hinzufügen, um werte mit einheiten anzuzeigen
        fig.update_traces(textposition='inside', textinfo='percent+label+value', hovertemplate='%{label}: %{value} %{customdata[0]}<extra></extra>', customdata=grouped_data[['Unit']])

        return fig

