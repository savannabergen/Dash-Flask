# Import packages
from dash import Dash, html, dash_table, Output, Input, dcc
import pandas as pd
import dash_bootstrap_components as dbc
import dash_auth
import plotly.express as px

# Incorporate data
df = pd.read_csv('Infrastructure_Plan_Funding_20240720.csv')
VALID_USERNAME = {
    'hello':'world'
}

# Initialize the app
def create_dash_application(flask_app):
    dash_app = Dash(__name__,
            server=flask_app,
            title='Example Dash login',
            update_title='Loading...', suppress_callback_exceptions=True, url_base_pathname="/Dash/", external_stylesheets=[dbc.themes.SOLAR])
    # App layout
    stack = html.Div([
             html.H4('City of Winnipeg Infrastructure Funding', className='display-3'),
             html.P(id='table_out'), 
                         dash_table.DataTable(
                                id='table',
                                data=df.to_dict('records'),
                                columns=[{'id': c, 'name': c} for c in df.columns],
                                page_size=100, 
                                style_table={'height': '600px', 'overflowY': 'auto'},
                                style_cell={'overflow': 'hidden',
                                            'textOverflow': 'ellipsis',
                                                'maxWidth': 0},
                                style_header=dict(backgroundColor="white", color="black"),
                                style_data=dict(backgroundColor="lightgrey")
                                ),
                                    ]),
    
    dash_app.layout = dbc.Container(stack)

    @dash_app.callback(
        Output('table_out', 'children'), 
        Input('table', 'active_cell'))
    def update_graphs(active_cell):
        if active_cell:
            cell_data = df.iloc[active_cell['row']][active_cell['column_id']]
            return f"Data: \"{cell_data}\" from table cell: {active_cell}"
        return "Click the table"

    return dash_app









