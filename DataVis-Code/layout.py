from dash import html, dcc
import dash_bootstrap_components as dbc

def create_layout():
    layout = dbc.Container([
        html.H1("FAO Data Visualization Dashboard", className="text-center my-4"),
        dbc.Tabs([
            dbc.Tab(label="Temporal Changes in Production Quantities", tab_id="lollipop-chart-tab"),
            dbc.Tab(label="Categorized Production Quantities", tab_id="bar-chart-tab"),
            dbc.Tab(label="World Map", tab_id="world-map-tab"),
            dbc.Tab(label="Food vs. Feed Production", tab_id="pie-chart-tab"),
            dbc.Tab(label="Production Changes", tab_id="time-series-tab"),
        ], id="tabs", active_tab="lollipop-chart-tab", className="custom-tabs"),
        html.Div(id="tab-content")
    ], fluid=True)
    return layout
