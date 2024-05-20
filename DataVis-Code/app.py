from dash import Dash
import dash_bootstrap_components as dbc
from layout import create_layout
from callbacks import register_callbacks

# erstelle eine Dash-Anwendung
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
app.title = "FAO Data Visualization Dashboard by Aris Hofmann"  # setze den Titel der App

# setze das Layout der App
app.layout = create_layout()
# registriere die Callbacks
register_callbacks(app)

# setze die HTML-Struktur der App
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%} 
        <style>
            .custom-tabs .nav-link {
                font-size: 14px;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# starte den Server, wenn dieses Skript direkt ausgeführt wird
if __name__ == '__main__':
    app.run_server(debug=True)
