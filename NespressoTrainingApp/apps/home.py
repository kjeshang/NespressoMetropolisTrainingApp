# Setup --------------------------------------------------------
from dash import Dash, dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc

# Create elements of the webpage -------------------------------
message = html.H1("Hello");

# Page Layout --------------------------------------------------
homePageStructure = [
    message
];

homePageLayout = dbc.Container(children=homePageStructure, fluid=True);