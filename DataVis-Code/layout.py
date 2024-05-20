from dash import html, dcc
import dash_bootstrap_components as dbc

# funktion zur erstellung des layouts
def create_layout():
    layout = dbc.Container([
        # überschrift des dashboards
        html.H1("FAO Data Visualization Dashboard", className="text-center my-4"),
        # tabs für die verschiedenen diagramme
        dbc.Tabs([
            dbc.Tab(label="Zeitliche Veränderungen der Produktionsmengen", tab_id="lollipop-chart-tab"),
            dbc.Tab(label="Kategorisierte Produktionsmengen", tab_id="bar-chart-tab"),
            dbc.Tab(label="Weltkarte", tab_id="world-map-tab"),
            dbc.Tab(label="Nahrungsmittel vs. Futterproduktion", tab_id="pie-chart-tab"),
            dbc.Tab(label="Produktionsänderungen", tab_id="time-series-tab"),
        ], id="tabs", active_tab="lollipop-chart-tab", className="custom-tabs"),
        # container für den inhalt des aktiven tabs
        html.Div(id="tab-content")
    ], fluid=True)
    return layout
