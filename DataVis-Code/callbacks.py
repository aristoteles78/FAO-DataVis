from dash import Input, Output
import modules.lollipop_chart as lollipop_chart
import modules.bar_chart as bar_chart
import modules.world_map as world_map
import modules.pie_chart as pie_chart
import modules.time_series as time_series

# funktion zur registrierung der callbacks
def register_callbacks(app):
    @app.callback(
        Output('tab-content', 'children'),
        [Input('tabs', 'active_tab')]
    )
    # funktion zum rendern des inhalts der tabs basierend auf dem aktiven tab
    def render_tab_content(active_tab):
        if active_tab == "lollipop-chart-tab":
            return lollipop_chart.layout()  # layout für lollipop-chart-tab
        elif active_tab == "bar-chart-tab":
            return bar_chart.layout()  # layout für bar-chart-tab
        elif active_tab == "world-map-tab":
            return world_map.layout()  # layout für world-map-tab
        elif active_tab == "pie-chart-tab":
            return pie_chart.layout()  # layout für pie-chart-tab
        elif active_tab == "time-series-tab":
            return time_series.layout()  # layout für time-series-tab

    # registrierung der callbacks für die einzelnen module
    lollipop_chart.register_callbacks(app)
    bar_chart.register_callbacks(app)
    world_map.register_callbacks(app)
    pie_chart.register_callbacks(app)
    time_series.register_callbacks(app)
