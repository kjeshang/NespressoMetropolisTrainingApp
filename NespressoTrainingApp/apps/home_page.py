# Setup --------------------------------------------------------
import pandas as pd
from dash import Dash, dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc

# Import the data -----------------------------------------
# df = pd.read_csv("data/PreparedCoffeeData.csv", index_col=False);

# Create elements of the webpage -------------------------------

image_path = "https://wallpapercave.com/wp/wp2046655.jpg";

homeImage = html.Img(src=image_path, style={'height':'80%', 'width':'100%', "padding":"0", "display":"inline-flex"});

title = [
    html.H3("Welcome to the Nespresso Metropolis Training App!", className="display-5"),
    html.P("By Kunal Ajaykumar Jeshang", className="lead"),
];

# items = [];
# for i in df.index:
#     items.append({
#         "key":i,
#         "src":df.loc[i, "Capsule & Sleeve Image Link"],
#         "header":df.loc[i, "Name"],
#         "caption":df.loc[i, "Type"] + " - " + df.loc[i, "Category"]
#     });

# carousel = dbc.Carousel(
#     items=items,
#     controls=False,
#     indicators=False,
#     interval=2000,
#     ride="carousel",
# );

# Page Layout --------------------------------------------------

homePageStructure = [
    html.Br(),
    # dbc.Row(children=[
    #     dbc.Col(children=title),
    #     dbc.Col(children=homeImage)
    # ]),
    dbc.Row(children=title),
    dbc.Row(children=homeImage)
    # dbc.Row(children=carousel)
];

homePageLayout = dbc.Container(children=homePageStructure, fluid=True);