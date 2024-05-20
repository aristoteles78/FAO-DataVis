from dash import Input, Output
import modules.lollipop_chart as lollipop_chart
import modules.bar_chart as bar_chart
import modules.world_map as world_map
import modules.pie_chart as pie_chart
import modules.time_series as time_series

def register_callbacks(app):
    @app.callback(
        Output('tab-content', 'children'),
        [Input('tabs', 'active_tab')]
    )
    def render_tab_content(active_tab):
        if active_tab == "lollipop-chart-tab":
            return lollipop_chart.layout()
        elif active_tab == "bar-chart-tab":
            return bar_chart.layout()
        elif active_tab == "world-map-tab":
            return world_map.layout()
        elif active_tab == "pie-chart-tab":
            return pie_chart.layout()
        elif active_tab == "time-series-tab":
            return time_series.layout()

    lollipop_chart.register_callbacks(app)
    bar_chart.register_callbacks(app)
    world_map.register_callbacks(app)
    pie_chart.register_callbacks(app)
    time_series.register_callbacks(app)
