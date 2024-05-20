from dash import html, dcc
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import pandas as pd
from data_processing import data_melted, all_years

# funktion zum erstellen des layouts der line-chart-seite
def layout():
    elements = data_melted['Element'].unique()
    change_types = ['Highest', 'Lowest']
    return html.Div([
        html.H3("Line Chart of Change Rates"),
        html.Div([
            html.Label("Select Change Type:"),
            dcc.Dropdown(
                id='change-type-dropdown',
                options=[{'label': change_type, 'value': change_type} for change_type in change_types],
                value='Highest'
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
        dcc.Graph(id='line-chart'),
        html.Div(id='explanation', style={'padding': '20px', 'font-size': '16px'})
    ])

# funktion zum registrieren der callbacks
def register_callbacks(app):
    @app.callback(
        [Output('line-chart', 'figure'),
         Output('explanation', 'children')],
        [Input('change-type-dropdown', 'value'),
         Input('element-dropdown', 'value')]
    )
    def update_line_chart(change_type, selected_element):
        # filtere die daten basierend auf dem ausgewählten element und jahr ab 1962
        filtered_data = data_melted[(data_melted['Element'] == selected_element) & (data_melted['Year'] >= 1962)].copy()

        # funktion zum ermitteln der länder mit der höchsten oder niedrigsten änderungsrate
        def get_top_countries(group, change_type):
            valid_entries = group.dropna(subset=['ChangeRate'])
            if valid_entries.empty:
                return pd.Series({'Year': group['Year'].iloc[0], 'Area': 'No data', 'ChangeRate': None})
            if change_type == 'Highest':
                top_entry = valid_entries.loc[valid_entries['ChangeRate'].idxmax()]
            else:
                top_entry = valid_entries.loc[valid_entries['ChangeRate'].idxmin()]
            return pd.Series({'Year': top_entry['Year'], 'Area': top_entry['Area'], 'ChangeRate': top_entry['ChangeRate']})

        # ermitteln der top-länder pro jahr
        top_countries = filtered_data.groupby('Year').apply(lambda x: get_top_countries(x, change_type)).reset_index(drop=True)

        # zusammenführen der top-länder mit allen jahren
        top_countries = all_years.merge(top_countries, on='Year', how='left')

        # erstellen des linien diagrams
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=top_countries['Year'],
            y=top_countries['ChangeRate'],
            mode='lines+markers',  # linien und marker anzeigen
            text=top_countries['Area'],
            hoverinfo='text',
            marker=dict(size=10, color='red'),
            line=dict(color='gray', dash='dash'),  # gestrichelte linie
            showlegend=False
        ))

        fig.update_layout(
            title=f"{change_type} Change Rate in {selected_element} Production",
            xaxis_title='Year',
            yaxis_title='Change Rate',
            height=600
        )

        explanation = (
            "The change rate is calculated as the percentage change in total value from one year to the next. "
            "For each year, the country with the highest (or lowest) change rate is displayed."
        )

        return fig, explanation
