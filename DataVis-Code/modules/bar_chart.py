from dash import html, dcc
import plotly.express as px
from dash.dependencies import Input, Output
from data_processing import data_melted

def layout():
    countries = data_melted['Area'].unique()
    years = sorted(data_melted['Year'].unique())
    visualization_types = ['Grouped Bar Chart', 'Stacked Bar Chart']
    elements = ['Food', 'Feed']

    # hinzufügen der option "All Countries"
    countries = ['All Countries'] + list(countries)

    # definition der kategorisierung der produkte
    category_mapping = {
        'Cereals and Products': ['Cereals - Excluding Beer', 'Wheat and products', 'Rice (Milled Equivalent)', 'Maize and products', 'Barley and products', 'Oats'],
        'Fruits': ['Apples and products', 'Bananas', 'Oranges, Mandarines', 'Grapes and products (excluding wine)'],
        'Vegetables': ['Potatoes and products', 'Carrots and products', 'Tomatoes and products', 'Onions'],
        'Meat and Meat Products': ['Bovine Meat', 'Pigmeat', 'Poultry Meat', 'Mutton & Goat Meat'],
        'Milk and Milk Products': ['Milk - Excluding Butter', 'Cheese', 'Butter and Ghee', 'Cream'],
        'Fish and Seafood': ['Fish, Seafood'],
        'Oils and Fats': ['Soyabean Oil', 'Groundnut Oil', 'Sunflowerseed Oil', 'Cottonseed Oil'],
        'Beverages': ['Coffee and products', 'Tea (including mate)', 'Cocoa Beans and products', 'Wine'],
        'Others': ['Sugar (Raw Equivalent)', 'Honey', 'Spices, Other']
    }

    # erstellung einer umgekehrten zuordnung von item zu kategorie
    item_to_category = {item: category for category, items in category_mapping.items() for item in items}

    # zuordnung der items zu kategorien
    data_melted['Category'] = data_melted['Item'].map(item_to_category)

    # filterung der items, die keiner kategorie zugeordnet sind
    data_melted_filtered = data_melted.dropna(subset=['Category'])

    # erstellung einer liste der kategorien, wobei "Milk and Milk Products" und "Cereals and Products" zuerst stehen, dann alphabetisch sortiert
    categories = ['Milk and Milk Products', 'Cereals and Products'] + sorted([cat for cat in category_mapping.keys() if cat not in ['Milk and Milk Products', 'Cereals and Products']])

    return html.Div([
        html.H3("Production Amounts by Category for a Single Year"),
        html.Div([
            html.Label("Select Country:"),
            dcc.Dropdown(
                id='country-dropdown',
                options=[{'label': country, 'value': country} for country in countries],
                value=['All Countries'],
                multi=True
            )
        ], style={'width': '30%', 'display': 'inline-block'}),
        html.Div([
            html.Label("Select Year:"),
            dcc.Dropdown(
                id='year-dropdown',
                options=[{'label': str(year), 'value': year} for year in years],
                value=years[0]
            )
        ], style={'width': '30%', 'display': 'inline-block'}),
        html.Div([
            html.Label("Select Visualization:"),
            dcc.Dropdown(
                id='visualization-dropdown',
                options=[{'label': viz, 'value': viz} for viz in visualization_types],
                value='Stacked Bar Chart'  # standardwert auf "Stacked Bar Chart" setzen
            )
        ], style={'width': '30%', 'display': 'inline-block'}),
        html.Div([
            html.Label("Select Element:"),
            dcc.Dropdown(
                id='element-dropdown',
                options=[{'label': elem, 'value': elem} for elem in elements],
                value='Food'  # standardwert auf "Food" setzen
            )
        ], style={'width': '30%', 'display': 'inline-block'}),
        html.Div([
            html.Label("Filter out Categories:"),
            dcc.Dropdown(
                id='category-filter',
                options=[{'label': category, 'value': category} for category in categories],
                value=[],
                multi=True
            )
        ], style={'width': '30%', 'display': 'inline-block'}),
        dcc.Graph(id='bar-chart')
    ])

def register_callbacks(app):
    @app.callback(
        Output('bar-chart', 'figure'),
        [Input('country-dropdown', 'value'),
         Input('year-dropdown', 'value'),
         Input('visualization-dropdown', 'value'),
         Input('element-dropdown', 'value'),
         Input('category-filter', 'value')]
    )
    def update_bar_chart(selected_countries, selected_year, selected_visualization, selected_element, filter_categories):
        if 'All Countries' in selected_countries:
            filtered_data = data_melted[(data_melted['Year'] == selected_year) & (data_melted['Element'] == selected_element)]
        else:
            filtered_data = data_melted[(data_melted['Area'].isin(selected_countries)) & (data_melted['Year'] == selected_year) & (data_melted['Element'] == selected_element)]
        
        # filterung der ausgewählten kategorien
        if filter_categories:
            filtered_data = filtered_data[~filtered_data['Category'].isin(filter_categories)]

        # summierung der werte nach kategorie
        grouped_data = filtered_data.groupby(['Category', 'Item']).agg({'Value': 'sum'}).reset_index()

        if selected_visualization == 'Grouped Bar Chart':
            fig = px.bar(grouped_data, x='Category', y='Value', color='Item', barmode='group',
                         title=f'Production Amounts by Category ({selected_element}) in {", ".join(selected_countries)} for {selected_year}',
                         labels={'Value': 'Amount Produced measurd in 1000t', 'Category': 'Category'})
        elif selected_visualization == 'Stacked Bar Chart':
            fig = px.bar(grouped_data, x='Category', y='Value', color='Item', barmode='stack',
                         title=f'Production Amounts by Category ({selected_element}) in {", ".join(selected_countries)} for {selected_year}',
                         labels={'Value': 'Amount Produced measured in 1000t', 'Category': 'Category'})

        # anzeige der werte nur beim hover
        fig.update_traces(texttemplate=None, hovertemplate='%{x}: %{y} measured in 1000t')

        fig.update_layout(transition_duration=500)
        return fig
