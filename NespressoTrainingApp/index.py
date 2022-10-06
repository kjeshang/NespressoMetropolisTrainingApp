# Setup ---------------------------------------------------
from dash import Dash, dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc
import sys

sys.path.append(".")
from app import app
from apps import home
from apps import coffee_page

# Create elements of the webpage --------------------------
heading = html.H2(
    children='Nespresso Metropolis Training App',
    style={'textAlign':'left', "margin-left":"20px", "margin-top":"25px"}
);

image_path = "https://nestle-nespresso.com/sites/site.prod.nestle-nespresso.com/files/styles/crop_freeform/public/MONOGRAM%20BLACK_0.jpg?itok=QmU2ExCh";

logoImage = html.Img(src=image_path, style={'height':'75%', 'width':'55%', "padding":"0", "display":"inline-flex"});

navigation = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Coffee", href="/coffee_page")),
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
        return home.homePageLayout;
    # TF-IDF & BoW
    elif pathname == "/coffee_page":
        return coffee_page.pageLayout;
    # Page Error
    else:
        return "404 Page Error! Please choose a link";

# Run the Dash application ----------------------------------
if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)