# Setup ---------------------------------------------------
from dash import Dash, dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc
import sys

sys.path.append(".")
from app import app
from app import server
from apps import home_page
from apps import about_page
from apps import NLP_page
from apps import explore_page

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
    html.Div(id="page-content", children=[])
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
if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)

# if __name__ == '__main__':
#     app.run_server(debug=True)