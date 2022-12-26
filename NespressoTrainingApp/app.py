# Setup ---------------------------------------------------
import dash
from dash import Dash, dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc
import sys
import flask
import os

from random import randint

sys.path.append(".")
from apps import home_page
from apps import about_page
from apps import NLP_page
from apps import explore_page

# Instantiate Dash App ------------------------------------

# server = flask.Flask(__name__)
# server.secret_key = os.environ.get('secret_key', str(randint(0, 1000000)))

external_stylesheets = [dbc.themes.DARKLY];
app = dash.Dash(__name__,
                meta_tags=[
                    {'name': 'viewport', 'content': 'width=device-width, initial-scale=1.0, maximum-scale=1.2, minimum-scale=0.5,'}],
                external_stylesheets=external_stylesheets
            )

server = app.server
app.config.suppress_callback_exceptions = True

# Create elements of the webpage --------------------------
heading = html.H2(
    children='Nespresso Metropolis Training App',
    style={'textAlign':'left', "margin-left":"20px", "margin-top":"25px"}
);

navigation = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("About", href="/about_page")),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem('Explore', href='/explore_page'),
                dbc.DropdownMenuItem('NLP', href='/NLP_page')
            ],
            nav=True,
            in_navbar=True,
            label='Coffee'
        )
    ],
    brand="Nespresso Metropolis Training App",
    brand_href="/",
    color="secondary",
    dark=True
);

# Page Layout ---------------------------------------------
app.layout = html.Div([
    dcc.Location(id="url", refresh=False),
    navigation,
    html.Br(),
    html.Div(id="page-content", children=[]),
    html.Footer([
        dcc.Markdown(
        '''
        Please visit the official [Nespresso Canada Website](https://www.nespresso.com/ca/en/) for more information
        ''', style={"text-align":"center"})
    ])
]);

# Callbacks -----------------------------------------------
@callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    # Home
    if pathname == "/":
        return home_page.homePageLayout;
    # About Page
    if pathname == "/about_page":
        return about_page.aboutPageLayout;
    # Explore Page
    elif pathname == '/explore_page':
        return explore_page.pageLayout;
    # NLP Page
    elif pathname == "/NLP_page":
        return NLP_page.pageLayout;
    # Page Error
    else:
        return "404 Page Error! Please choose a link";

# Run the Dash application ----------------------------------
# if __name__ == '__main__':
#     app.run_server(debug=True, use_reloader=False)

if __name__ == '__main__':
    app.run_server(debug=False)