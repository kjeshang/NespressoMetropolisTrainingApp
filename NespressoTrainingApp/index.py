# Setup ---------------------------------------------------
import pandas as pd
import numpy as np
from time import time

from wordcloud import WordCloud

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer, TfidfTransformer
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity
from sklearn.feature_selection import chi2
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
from sklearn.pipeline import Pipeline

import plotly.express as px
from dash import dcc, html, Input, Output, State, callback, dash_table
import dash_bootstrap_components as dbc

# Import the data -----------------------------------------
df = pd.read_csv("data/PreparedCoffeeData.csv", index_col=False);

# Create elements of the webpage --------------------------
heading = html.H2(
    children='Nespresso Metropolis Training App',
    style={'textAlign':'left', "margin-left":"20px", "margin-top":"25px"}
);

image_path = "https://nestle-nespresso.com/sites/site.prod.nestle-nespresso.com/files/styles/crop_freeform/public/MONOGRAM%20BLACK_0.jpg?itok=QmU2ExCh";

logoImage = html.Img(src=image_path, style={'height':'75%', 'width':'55%', "padding":"0", "display":"inline-flex"});

machineTypeFilter = [
    html.P("Machine Type", style={"font-weight":"bold"}),
    dcc.RadioItems(
        id="machine-type-filter",
        options=[{"label":x, "value":x} for x in df["Type"].unique().tolist()],
        value="Vertuo",
        inline=True,
        inputStyle={"margin-right":"5px", "margin-left":"15px"}
    )
];

servingFilter = [
    html.P("Serving", style={"font-weight":"bold"}),
    dcc.Dropdown(
        id="serving-filter",
        options=[{"label":x, "value":x} for x in df["Serving"].unique().tolist()],
        value=df["Serving"].unique().tolist(),
        multi=True
    )
];

nlpParameters = [
    # Number of Recommendations
    dbc.Row(children=[
        dbc.Col(children=[
            html.P("Number of Recommendations", style={"font-weight":"bold"})
        ]),
        dbc.Col(children=[
            dbc.Input(id="numRec", type="number", min=1, max=len(df), step=1, value=10)
        ])
    ]),
    # Minimum Document Frequency
    dbc.Row(children=[
        dbc.Col(children=[
            html.P("Minimum Document Frequency", style={"font-weight":"bold"}),
        ]),
        dbc.Col(children=[
            dbc.Input(id="min_df", type="number", min=0, value=2)
        ])
    ]),
    # Maximum Document Frequency
    dbc.Row(children=[
        dbc.Col(children=[
            html.P("Maximum Document Frequency", style={"font-weight":"bold"})
        ]),
        dbc.Col(children=[
            dbc.Input(id="max_df", type="number", min=0, value=0.95)
        ])
    ]),
    # Maximum Features
    dbc.Row(children=[
        dbc.Col(children=[
            html.P("Maximum Features", style={"font-weight":"bold"})
        ]),
        dbc.Col(children=[
            dbc.Input(id="max_features", type="number", min=0, step="1", value=50)
        ])
    ]),
    # stop_words = "english"
    html.Br(),
    # N Gram Range
    dbc.Row(children=[
        dbc.Col(children=[
            html.P("N Gram Range", style={"font-weight":"bold"})
        ]),
        dbc.Col(children=[
            dcc.RangeSlider(1, 3, 1, value=[1,2], id="ngram_range")
        ]),
    ]),
    html.Br(),
    # Sublinear Term Frequency Scaling
    dbc.Row(id="sublinear_tf-parameter",children=[
        dbc.Col(children=[
            html.P("Sublinear Term Frequency Scaling", style={"font-weight":"bold"})
        ]),
        dbc.Col(children=[
            dcc.Dropdown(
                id="sublinear_tf",
                options=[
                    {"label":"True", "value":True},
                    {"label":"False", "value":False}
                ],
                value=True,
                clearable=False
            )
        ])
    ]),
    # html.Br(),
    # Analyzer Type
    dbc.Row(id="analyzer-parameter", children=[
        dbc.Col(
            html.P("Analyzer Type", style={"font-weight":"bold"})
        ),
        dbc.Col(
            dcc.Dropdown(
                id="analyzer",
                options=[{"label":x, "value":x} for x in ["word","char","char_wb"]],
                value="word",
                clearable=False
            )
        )
    ]),
    # token_pattern = r"\b[a-zA-Z]{3,}\b"
];

parameterOptions = [
    dbc.Button(
        "Parameter Options", 
        id="open-parameter-options", 
        n_clicks=0,
        style={"margin-top":"10px"}
    ),
    dbc.Offcanvas(
        html.Div(children=nlpParameters),
        id="parameter-options",
        title="Parameter Options",
        is_open=False,
        placement="end",
        scrollable=True
    )
];

techniqueSelector = [
    html.P("Text Mining Technique", style={"font-weight":"bold"}),
    dcc.RadioItems(
        id="technique-selector",
        options=[
            {"label":"TF-IDF", "value":0},
            {"label":"Bag of Words", "value":1}
        ],
        value=0,
        inline=True,
        inputStyle={"margin-right":"5px", "margin-left":"15px"},
        style={"display":"inline-flex"}
    ),
    dbc.Button(
        "Parameter Options", 
        id="open-parameter-options", 
        n_clicks=0,
        style={"margin-left":"20px", "display":"inline-flex"}
    ),
    dbc.Offcanvas(
        html.Div(children=nlpParameters),
        id="parameter-options",
        title="Parameter Options",
        is_open=False,
        placement="end",
        scrollable=True
    )
];

# Page Layout ---------------------------------------------
pageStructure = [
    dbc.Row(children=[
        dbc.Col(children=logoImage, width=3),
        dbc.Col(children=heading, width=9)
    ], style={"margin-bottom":"-50px"}),
    # html.Br(),
    dbc.Row(children=[
        # Machine Type
        dbc.Col(children=[
            dbc.Card(children=[
                dbc.CardBody(children=machineTypeFilter)
            ])
        ], width=3),
        # Serving
        dbc.Col(children=[
            dbc.Card(children=[
                dbc.CardBody(children=servingFilter)
            ])
        ], width=5),
        # Technique Selector
        dbc.Col(children=[
            dbc.Card(children=[
                dbc.CardBody(children=techniqueSelector)
            ])
        ], width=4)
    ]),
    html.Br(),

];

pageLayout = dbc.Container(children=pageStructure, fluid=True);

# Callbacks ------------------------------------------------
@callback(
    Output("parameter-options", "is_open"),
    Input("open-parameter-options", "n_clicks"),
    [State("parameter-options", "is_open")],
)
def toggle_nlpParameter(n1, is_open):
    if n1:
        return not is_open
    return is_open

@callback(
    Output("sublinear_tf-parameter", "style"),
    Output("analyzer-parameter", "style"),
    [Input("technique-selector", "value")]
)
def get_uniqueParameterOptions(techniqueSelected):
    if techniqueSelected == 1:
        return {"display":"none"}, {"display":"flex"};
    else:
        return {"display":"flex"}, {"display":"none"};