from dash import Dash, html, dcc
import dash
import plotly.express as px

# Template from Plotly
px.defaults.template = 'ggplot2'
external_css = ["https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"]

from dash import Dash, html, dcc
import dash
dash_app = Dash(__name__, use_pages=True, pages_folder="pages", external_stylesheets=external_css, server=app, url_base_pathname='/pathname/')

dash.register_page("home", path='/', layout=html.Div('Home Page'))
dash.register_page("analytics", layout=html.Div('Analytics'))

dash_app.layout = html.Div([
    html.Div([
        html.Div(
            dcc.Link(f"{page['name']} - {page['path']}", href=page["relative_path"], className="btn btn-dark")
        ) for page in dash.page_registry.values()
    ]),
    dash.page_container,
], className="form-group")

if __name__ == '__main__':
    dash_app.run(debug=True)