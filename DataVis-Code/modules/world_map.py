from dash import html, dcc
import plotly.express as px
from dash.dependencies import Input, Output
from data_processing import data_melted

def layout():
    items = data_melted['Item'].unique()
    elements = data_melted['Element'].unique()
    years = sorted(data_melted['Year'].unique())

    return html.Div([
        html.H3("World Production Map"),
        html.Div([
            html.Label("Select Item:"),
            dcc.Dropdown(
                id='item-dropdown',
                options=[{'label': item, 'value': item} for item in items],
                value=items[0]
            )
        ], style={'width': '30%', 'display': 'inline-block'}),
        html.Div([
            html.Label("Select Start Year:"),
            dcc.Dropdown(
                id='start-year-dropdown',
                options=[{'label': str(year), 'value': year} for year in years],
                value=years[0]
            )
        ], style={'width': '30%', 'display': 'inline-block'}),
        html.Div([
            html.Label("Select End Year:"),
            dcc.Dropdown(
                id='end-year-dropdown',
                options=[{'label': str(year), 'value': year} for year in years],
                value=years[-1]
            )
        ], style={'width': '30%', 'display': 'inline-block'}),
        html.Div([
            html.Label("Select Element:"),
            dcc.Dropdown(
                id='element-dropdown',
                options=[{'label': elem, 'value': elem} for elem in elements],
                value=elements[0]
            )
        ], style={'width': '30%', 'display': 'inline-block'}),
        dcc.Graph(id='world-map', style={'height': '80vh'})  # Set the height of the map
    ])

def register_callbacks(app):
    @app.callback(
        Output('world-map', 'figure'),
        [Input('item-dropdown', 'value'),
         Input('start-year-dropdown', 'value'),
         Input('end-year-dropdown', 'value'),
         Input('element-dropdown', 'value')]
    )
    def update_map(selected_item, start_year, end_year, selected_element):
        filtered_data = data_melted[(data_melted['Item'] == selected_item) & 
                                    (data_melted['Year'] >= start_year) & 
                                    (data_melted['Year'] <= end_year) & 
                                    (data_melted['Element'] == selected_element)]
        
        filtered_data = filtered_data.groupby(['Area', 'iso_alpha', 'Unit'])['Value'].sum().reset_index()
        
        fig = px.choropleth(
            filtered_data,
            locations="iso_alpha",
            locationmode="ISO-3",
            color="Value",
            hover_name="Area",
            hover_data={"Value": True, "Unit": True},
            color_continuous_scale="Reds",
            title=f"{selected_element} Production for {selected_item} ({start_year}-{end_year})",
            template="plotly_white",
            range_color=(0, filtered_data['Value'].max())
        )
        fig.update_geos(showcoastlines=True, coastlinecolor="Black", showland=True, landcolor="white")
        fig.update_layout(height=800)
        return fig
