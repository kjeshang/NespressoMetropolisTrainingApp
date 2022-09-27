from dash import Dash, html
import dash_bootstrap_components as dbc

import index

app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY]);

app.layout = html.Div([index.pageLayout]);

if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)