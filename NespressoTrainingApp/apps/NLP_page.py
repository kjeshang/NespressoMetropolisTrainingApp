# Setup ---------------------------------------------------
from re import M
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
import plotly.graph_objects as go
from dash import dcc, html, Input, Output, State, callback, dash_table
import dash_bootstrap_components as dbc

# import sys
# sys.append(".")
from modules.NLP import get_dataframeNLP, get_recommendationResults, stop_words, token_pattern, get_featureResults

# Import the data -----------------------------------------
df = pd.read_csv("data/PreparedCoffeeData.csv", index_col=False);

# Create elements of the webpage --------------------------

# Machine Type Filter:
machineTypeFilter = [
    html.P("Machine Type", style={"font-weight":"bold"}),
    dcc.Checklist(
        id="machine-type-filter",
        options=[{"label":x, "value":x} for x in df["Type"].unique().tolist()],
        value=df["Type"].unique().tolist(),
        inline=True,
        inputStyle={"margin-right":"5px", "margin-left":"15px"}
    )
];

# Decaf Coffee Filter:
decafCoffeeFilter = [
    html.P("Include Decaf Coffee?", style={"font-weight":"bold"}),
    dcc.RadioItems(
        id="include-decaf",
        options=[
            {"label":"Yes", "value":"Yes"},
            {"label":"No", "value": "No"}
        ],
        value="Yes",
        inline=True,
        inputStyle={"margin-right":"5px", "margin-left":"15px"},
        style={"display":"inline-flex"}
    )
];

# Serving Filter:
servingFilter = [
    html.P("Serving", style={"font-weight":"bold"}),
    dcc.Dropdown(
        id="serving-filter",
        multi=True
    )
];

# Selected Coffee:
selectedCoffee = [
    html.P("Select Coffee", style={"font-weight":"bold"}),
    dcc.Dropdown(
        id="coffee-select",
        searchable=True,
        placeholder="Select a Coffee",
        style={"color":"black"}
    )
];

# NLP Parameters ******************************************************

# TF-IDF/BoW Parameters: 
tfidfBoWParameters = [
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
                clearable=False,
                style={"color":"black"}
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
                clearable=False,
                style={"color":"black"}
            )
        )
    ]),
    # token_pattern = r"\b[a-zA-Z]{3,}\b"
];

# *********************************************************

# Technique Selector:
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
        html.Div(id="nlp-parameters"),
        id="parameter-options",
        title="Parameter Options",
        is_open=False,
        placement="end",
        scrollable=True
    )
];

# Main Content:
mainContent = html.Div(id="main-content");

# Page Layout ---------------------------------------------
pageStructure = [
    dbc.Row(children=[
        # Machine Type
        dbc.Col(children=[
            dbc.Card(children=[
                dbc.CardBody(children=machineTypeFilter)
            ])
        ], width=3),
        # Serving Filter
        dbc.Col(children=[
            dbc.Card(children=[
                dbc.CardBody(children=servingFilter)
            ])
        ], width=7),
        # Decaf Coffee?
        dbc.Col(children=[
            dbc.Card(children=[
                dbc.CardBody(children=decafCoffeeFilter)
            ])
        ], width=2)
    ], style={"margin-bottom":"15px"}),
    dbc.Row(children=[
        # Select Coffee
        dbc.Col(children=[
            dbc.Card(children=[
                dbc.CardBody(children=selectedCoffee)
            ]),
        ], width=3),
        # Serving
        dbc.Col(children=[
            dbc.Card(children=[
                dbc.CardBody(children=techniqueSelector)
            ])
        ], width=9),
    ], style={"margin-bottom":"15px"}),
    # Main Content
    dbc.Row(children=mainContent)
];

pageLayout = dbc.Container(children=pageStructure, fluid=True);

# Callbacks & Functions ------------------------------------------------
# Callback: Toggle Parameter options *********************************
@callback(
    Output("parameter-options", "is_open"),
    Input("open-parameter-options", "n_clicks"),
    [State("parameter-options", "is_open")],
)
def toggle_nlpParameter(n1, is_open):
    if n1:
        return not is_open
    return is_open

# Callback: Retrieve NLP parameters based on technique selected *****
@callback(
    Output("nlp-parameters", "children"),
    [Input("technique-selector", "value")]
)
def getNLPTechniqueParametes(techniqueSelected):
    # TF-IDF or BoW
    if (techniqueSelected == 0) | (techniqueSelected == 1):
        return tfidfBoWParameters;

# Callback: Trigger TF-IDF/BoW unique parameters ********************
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

# Callback: Get Serving Options *********************************
@callback(
    Output("serving-filter", "value"),
    Output("serving-filter", "options"),
    [Input("machine-type-filter", "value")]
)
def get_servingOptions(machineTypeValue):
    mask = df["Type"].isin(machineTypeValue);
    servingValue = df[mask]["Serving"].unique().tolist();
    servingOptions = [{"label":x, "value":x} for x in servingValue];
    return servingValue, servingOptions;

# Callback: Get Coffee Options ***********************************
@callback(
    Output("coffee-select", "options"),
    [
        Input("machine-type-filter", "value"),
        Input("serving-filter", "value"),
        Input("include-decaf", "value")
    ]
)
def get_coffeeOptions(machineTypeValue, servingValue, includeDecafValue):
    if includeDecafValue == "Yes":
        mask = (df["Type"].isin(machineTypeValue)) & (df["Serving"].isin(servingValue));
    else:
        mask = (df["Type"].isin(machineTypeValue)) & (df["Serving"].isin(servingValue)) & (df["Decaf Coffee?"] != "Yes");
    coffeeSelectOptions = [{"label":x, "value":x} for x in df[mask]["Name"].tolist()];
    return coffeeSelectOptions;

# Functions: Get Selected Coffee Information ************************

# Selected Coffee General Details:
def selectedCoffeeGeneralDetails(df, idx):
    # generalDetailCols = ["Serving","Serving Size","Sleeve Price","Ingredients & Allergens","Per Capsule Price","Number of Capsules per Sleeve","Net Weight per Total Number of Capsules","Decaf Coffee?","Other Information"];
    generalDetailCols = ["Sleeve Price","Ingredients & Allergens","Per Capsule Price","Number of Capsules per Sleeve","Net Weight per Total Number of Capsules","Decaf Coffee?","Other Information"];
    
    data = [];
    for col in generalDetailCols:
        if col in ["Sleeve Price", "Per Capsule Price"]:
            row = [col, "${:,.2f}".format(df.loc[idx, col])];
        else:
            row = [col, df.loc[idx, col]];
        data.append(row);
    df_genDetails = pd.DataFrame(data, columns=["Metric","Detail"]);
    
    genDetailsTable = dash_table.DataTable(
        df_genDetails.to_dict('records'), 
        [{"name": i, "id": i} for i in df_genDetails],

        style_header={
        'backgroundColor': 'rgb(30, 30, 30)',
        'color': 'white'
        },
        style_data={
            'backgroundColor': 'rgb(50, 50, 50)',
            'color': 'white'
        },
        style_cell={
            'whiteSpace':'normal',
            'height':'auto'
        },
        style_cell_conditional=[
            {'if': {'column_id': 'Metric'},
            'width': '30%', 'textAlign':'left'},
            {'if': {'column_id': 'Detail'},
            'width': '70%', 'textAlign':'center'},
        ],
        # fill_width=False
    );

    return genDetailsTable; 

# Selected Coffee Information Output:
def selectedCoffeeInformation(df, coffeeSelectValue):
    idx = df[df["Name"] == coffeeSelectValue].index.astype('Int64')[0];
    
    selectedCoffeeInfo = dbc.Card([
        # Type
        dbc.CardHeader(df.loc[idx, "Type"] + " " + df.loc[idx, "Serving"], style={"textAlign":"center"}),
            dbc.Row([
                dbc.Col([
                    # Capsule Image
                    dbc.CardImg(
                        src=df.loc[idx, "Capsule Image Link"],
                        className="img-fluid rounded-start",
                    ),
                    # Category
                    html.P(df.loc[idx, "Category"], style={"textAlign":"center"}),
                ], className="col-md-2"),
                dbc.Col([
                    dbc.Card([
                        # Capsule & Sleeve Image
                        dbc.CardImg(
                            src=df.loc[idx, "Capsule & Sleeve Image Link"],
                            top=True,
                            style={"opacity": 0.3},
                        ),
                        dbc.CardImgOverlay(
                            dbc.CardBody([
                                dbc.Row([
                                    dbc.Col([
                                        # Name
                                        html.H4(
                                            df.loc[idx, "Name"], className="display-5",
                                            style={"textAlign":"left"}
                                        ),
                                        # Headline
                                        html.P(
                                            df.loc[idx, "Headline"], className="lead",
                                            style={"textAlign":"left"}
                                        ),
                                    ], width=8),
                                    dbc.Col([
                                        # Intensity
                                        html.P(
                                            "Intensity", 
                                            style={"textAlign":"right"}
                                        ),
                                        html.H3(
                                            df.loc[idx, "Intensity"], className="display-4",
                                            style={"textAlign":"right", "margin-right":"5px"}
                                        )
                                    ], width=4)
                                ]),
                                html.Hr(className="my-2"),
                                # Caption
                                html.P(df.loc[idx, "Caption"]),
                                # Notes & Best Served As
                                html.P(df.loc[idx, "Notes"] + " notes — best served as " + " " + df.loc[idx, "Best Served As"]),
                                # Taste Description & More Information
                                html.Div([
                                    dbc.Button(
                                        "Taste Description",
                                        id="taste-description-button",
                                        n_clicks=0,
                                        style={"margin-bottom":"10px", "display":"inline-flex"}
                                    ),
                                    dbc.Button(
                                        "More Information",
                                        id="more-information-button",
                                        n_clicks=0,
                                        style={"margin-bottom":"10px", "margin-left":"15px", "display":"inline-flex"}
                                    ),
                                    dbc.Collapse(
                                        selectedCoffeeGeneralDetails(df, idx),
                                        id="more-information",
                                        is_open=False
                                    ),
                                    dbc.Collapse(
                                        html.P(df.loc[idx, "Taste"]),
                                        id="taste-description",
                                        is_open=False
                                    )
                                ])
                            ])
                        ),
                    ], style={"display":"flex"}),
                ], className="col-md-10")
            ]),
        # dbc.CardFooter(df.loc[idx, "Category"], style={"textAlign":"center"})
    ], style={"display":"flex", "max-height":"100%", "max-width":"100%"});

    return selectedCoffeeInfo; 

# Functions: Get Recommendation Content *********************************

# Recommendation Results Table:
def get_recommendationResultsTable(techniqueSelected, df, coffee_select, numRec, min_df, max_df, max_features, stop_words, n_lower, n_upper, sublinear_tf, analyzer, token_pattern):

    dff_rec = get_recommendationResults(techniqueSelected, df, coffee_select, numRec, min_df, max_df, max_features, stop_words, n_lower, n_upper, sublinear_tf, analyzer, token_pattern);

    dashTable = dash_table.DataTable(
        style_cell={
            'whiteSpace':'normal',
            'height':'auto',
            'textAlign':'left'
        },
        style_header={
        'backgroundColor': 'rgb(30, 30, 30)',
        'color': 'white',
        'textAlign':'left'
        },
        style_data={
            'backgroundColor': 'rgb(50, 50, 50)',
            'color': 'white',
        },
        style_cell_conditional=[
            {
                'if': {'column_id': c},
                'textAlign': 'center'
            } for c in ["Intensity","Similarity Score"]
        ],
        data=dff_rec.to_dict('records'),
        columns=[{"name": i, "id": i} for i in dff_rec.columns if i != "id"],
        id="tbl"
    );

    return dashTable;

# BRIEF COFFEE INFORMATION ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

# Brief Coffee Information:
def briefCoffeeInformation(df, coffee_select, selectOrRecommend):
    idx = df[df["Name"] == coffee_select].index.astype('Int64')[0];

    card = dbc.Card([
        dbc.CardHeader(selectOrRecommend + ": " + df.loc[idx, "Type"] + " " + df.loc[idx, "Serving"], style={"textAlign":"center"}),
        dbc.Row([
            dbc.Col([
                    dbc.CardImg(
                    src=df.loc[idx,"Capsule Image Link"], 
                    className="img-fluid rounded-start"
                ),
            ], className="col-md-4"),
            dbc.Col([
                dbc.CardBody([
                    html.H4(df.loc[idx, "Name"], style={"textAlign":"center"}),
                    html.P(df.loc[idx, "Headline"], style={"textAlign":"center", "font-weight":"bold"}),
                    html.Div([
                        html.P("Intensity: " + str(df.loc[idx, "Intensity"])),
                        html.P("Serving Size: " + df.loc[idx, "Serving Size"]),
                        html.P("Notes: " + df.loc[idx, "Notes"])
                    ], style={"margin-left":"20px"})
                ], className='card-text'),
            ], className="col-md-8"),
        ], className="g-0 d-flex align-items-center"),
        dbc.CardFooter(df.loc[idx, "Category"], style={"textAlign":"center"})
    ], style={"margin-top":"10px"});
    
    return card;

# Brief Coffee Information Comparison:
def get_briefCoffeeInformationComparison(df, coffee_select):
    information = html.Div([
        dbc.Row([
            dbc.Col(briefCoffeeInformation(df, coffee_select, "Selected"), width=6),
            dbc.Col(id="recommended-coffee-information", width=6)
        ])
    ]);
    return information;

# TASTE PROFILE ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

# Taste Profile Chart of an individual Coffee flavor:
def tasteProfileChart(df, coffee_select):
    idx = df[df["Name"] == coffee_select].index.astype('Int64')[0];

    if df.loc[idx, "Category"] == "Barista Creations":
        if df.loc[idx, "Name"] == "Bianco Piccolo":
            tasteCols = ["Acidity","Bitterness","Roastness","Body"];
        else:
            tasteCols = ["Milky Taste","Bitterness with Milk","Roastiness with Milk", "Creamy Texture"];
    else:
        tasteCols = ["Acidity","Bitterness","Roastness","Body"];
    
    data = [];
    for col in tasteCols:
        row = [col, df.loc[idx, col]];
        data.append(row);
    df_tasteProfile = pd.DataFrame(data, columns=["Metric","Value"]);

    fig = px.bar(
        df_tasteProfile, 
        x='Metric', 
        y='Value', 
        color='Metric',
        title=df.loc[idx, "Name"] + " Taste Profile",
        template='plotly_dark'
    );
    fig.update_layout(
        yaxis = dict(
            tickmode = 'array',
            tickvals = [0, 1, 2, 3, 4, 5],
        ) 
    );

    chart = dcc.Graph(figure=fig, config={"displayModeBar":False});

    return chart;

# Taste Profile Comparison:
def get_tasteProfileComparison(df, coffee_select, coffee_recommend):
    id_select = df[df["Name"] == coffee_select].index.astype('Int64')[0];
    id_recommend = df[df["Name"] == coffee_recommend].index.astype('Int64')[0];

    tasteCols = ["Acidity","Bitterness","Roastness","Body"];
    tasteCols_barista = ["Milky Taste","Bitterness with Milk","Roastiness with Milk", "Creamy Texture"];

    if (df.loc[id_select, "Category"] != "Barista Creations") & (df.loc[id_recommend, "Category"] != "Barista Creations"):
        data = [];
        for id in [id_select, id_recommend]:
            for col in tasteCols:
                row = [
                    df.loc[id, "Name"],
                    col,
                    df.loc[id, col]
                ];
                data.append(row);
        dfTaste = pd.DataFrame(data, columns=["Coffee","Metric","Value"]);
        fig = px.bar(
            dfTaste, 
            x="Metric", 
            y="Value", 
            color="Coffee", 
            barmode="group",
            template='plotly_dark'
        );
        fig.update_layout(
            yaxis = dict(
                tickmode = 'array',
                tickvals = [0, 1, 2, 3, 4, 5],
            ) 
        );
        tasteProfiles = html.Div([
            html.H5("Taste Profile: " + df.loc[id_select, "Name"] + " vs. " +df.loc[id_recommend, "Name"], style={"textAlign":"center"}),
            dcc.Graph(figure=fig, config={"displayModeBar":False})
        ], style={"margin-top":"10px"});
    
    elif (df.loc[id_select, "Category"] == "Barista Creations") & (df.loc[id_recommend, "Category"] == "Barista Creations"):
        if (df.loc[id_select, "Name"] == "Bianco Piccolo") | (df.loc[id_recommend, "Name"] == "Bianco Piccolo"):
            tasteProfiles = html.Div([
                html.H5("Taste Profile: " + df.loc[id_select, "Name"] + " vs. " +df.loc[id_recommend, "Name"], style={"textAlign":"center"}),
                dbc.Row([
                    dbc.Col([
                        tasteProfileChart(df, coffee_select),
                    ]),
                    dbc.Col([
                        tasteProfileChart(df, coffee_recommend)
                    ]),
                ])
            ], style={"margin-top":"10px"});
        
        else:
            data = [];
            for id in [id_select, id_recommend]:
                for col in tasteCols_barista:
                    row = [
                        df.loc[id, "Name"],
                        col,
                        df.loc[id, col]
                    ];
                    data.append(row);
            dfTaste = pd.DataFrame(data, columns=["Coffee","Metric","Value"]);
            fig = px.bar(
                dfTaste, 
                x="Metric", 
                y="Value", 
                color="Coffee", 
                barmode="group",
                template='plotly_dark'
            );
            fig.update_layout(
                yaxis = dict(
                    tickmode = 'array',
                    tickvals = [0, 1, 2, 3, 4, 5],
                ) 
            );
            tasteProfiles = html.Div([
                html.H5("Taste Profile: " + df.loc[id_select, "Name"] + " vs. " +df.loc[id_recommend, "Name"], style={"textAlign":"center"}),
                dcc.Graph(figure=fig, config={"displayModeBar":False})
            ], style={"margin-top":"10px"});
    
    else:
        tasteProfiles = html.Div([
            html.H5("Taste Profile: " + df.loc[id_select, "Name"] + " vs. " +df.loc[id_recommend, "Name"], style={"textAlign":"center"}),
            dbc.Row([
                dbc.Col([
                    tasteProfileChart(df, coffee_select),
                ], width=6),
                dbc.Col([
                    tasteProfileChart(df, coffee_recommend)
                ], width=6),
            ])
        ], style={"margin-top":"10px"});

    return tasteProfiles;

# WORD CLOUD ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

def wordCloud(df, coffee_select, selectOrRecommend):
    wordcloud = WordCloud(background_color="white", max_words=5000, contour_width=3, contour_color="steelblue");
    mask = df["Name"] == coffee_select;
    idx = df.index[mask].tolist()[0];
    wc = wordcloud.generate(df.loc[idx, "Textual Info"]);
    card = dbc.Card([
        dbc.CardHeader(selectOrRecommend + ": " + df.loc[idx, "Type"] + " " + df.loc[idx, "Serving"], style={"textAlign":"center"}),
        dbc.CardBody([
            dbc.CardBody(html.H5(df.loc[idx, "Name"], style={"textAlign":"center"})),
            dbc.CardImg(src=wc.to_image(), bottom=True)
        ]),
        dbc.CardFooter(df.loc[idx, "Category"], style={"textAlign":"center"})
    ], style={"margin-top":"10px"});
    return card;

def get_wordCloudComparison(df, coffee_select):
    wordClouds = html.Div([
        dbc.Row([
            dbc.Col([
                wordCloud(df, coffee_select, "Selected")
            ]),
            dbc.Col(id='recommended-coffee-wordCloud')
        ])
    ])
    return wordClouds;

# FEATURE RESULTS ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

# Feature Result Chart:
def featureResultChart(techniqueSelected, df_feature, coffee_select):
    if techniqueSelected == 0:
        fig = px.bar(
            df_feature,
            x="TF-IDF",
            y=df_feature.index,
            orientation="h",
            labels={'index':'Terms', 'TF-IDF':'Score'},
            title=f'{coffee_select} Important Features (TF-IDF)',
            template='plotly_dark'
        );
    elif techniqueSelected == 1:
        fig = px.bar(
            df_feature,
            x="Bag of Words",
            y=df_feature.index,
            orientation="h",
            labels={'index':'Terms', 'Bag of Words':'Score'},
            title=f'{coffee_select} Important Features (Bag of Words)',
            template='plotly_dark'
        )
    chart = dcc.Graph(figure=fig, config={"displayModeBar":False});
    return chart;

# Feature Result Comparison:
def get_featureResultComparison(techniqueSelected, df, coffee_select, min_df, max_df, max_features, stop_words, n_lower, n_upper, sublinear_tf, analyzer, token_pattern):
    df_selectedFeatureResult = get_featureResults(techniqueSelected, df, coffee_select, min_df, max_df, max_features, stop_words, n_lower, n_upper, sublinear_tf, analyzer, token_pattern);

    selectedCoffeeFeatureChart = featureResultChart(techniqueSelected, df_selectedFeatureResult, coffee_select);

    featureResult = html.Div([
        dbc.Row([
            dbc.Col(selectedCoffeeFeatureChart, width=6),
            dbc.Col(id='recommended-feature-result-chart', width=6)
        ])
    ]);
    return featureResult;

# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

# Recommendation Content Ouput:
def get_recommendationContent(techniqueSelected, df, coffee_select, numRec, min_df, max_df, max_features, stop_words, n_lower, n_upper, sublinear_tf, analyzer, token_pattern):
    dashTable = get_recommendationResultsTable(techniqueSelected, df, coffee_select, numRec, min_df, max_df, max_features, stop_words, n_lower, n_upper, sublinear_tf, analyzer, token_pattern);

    recommendationContent = html.Div([
        # Recommendations
        html.P(f"Top {numRec} Alternate Recommendations for {coffee_select}"),
        dashTable,
        html.Br(),
        dbc.Tabs([
            # Brief Coffee Information
            dbc.Tab(
                get_briefCoffeeInformationComparison(df, coffee_select),
            label="Brief Coffee Information"),
            # Taste Profile
            dbc.Tab(
                id="taste-profile-comparison", 
            label="Taste Profile"),
            # Word Cloud
            dbc.Tab(
                get_wordCloudComparison(df, coffee_select),
            label="Word Cloud"),
            # Feature Results
            dbc.Tab(
                get_featureResultComparison(techniqueSelected, df, coffee_select, min_df, max_df, max_features, stop_words, n_lower, n_upper, sublinear_tf, analyzer, token_pattern), 
            label="Feature Results")
        ])
    ]);
    return recommendationContent;

# Callback: Get Main Content **************************************************
@callback(
    Output("main-content", "children"),
    [
        # Filter Options
        Input("coffee-select", "value"),
        Input("machine-type-filter", "value"),
        Input("serving-filter", "value"),
        Input("include-decaf", "value"),
        # NLP Parameters
        Input("technique-selector", "value"),
        Input("numRec", "value"),
        Input("min_df", "value"),
        Input("max_df", "value"),
        Input("max_features", "value"),
        Input("ngram_range","value"),
        Input("sublinear_tf", "value"),
        Input("analyzer", "value"),
    ]
)
def get_mainContent(coffeeSelectValue, machineTypeValue, servingValue, includeDecafValue, techniqueSelected, numRec, min_df, max_df, max_features, ngram_range, sublinear_tf, analyzer):
    if includeDecafValue == "Yes":
        mask = (df["Type"].isin(machineTypeValue)) & (df["Serving"].isin(servingValue));
    else:
        mask = (df["Type"].isin(machineTypeValue)) & (df["Serving"].isin(servingValue)) & (df["Decaf Coffee?"] != "Yes");
    
    if (len(machineTypeValue) == 0) & (len(servingValue) == 0):
        mainContent = html.P("No Machine Type and/or Serving selected");
    elif (coffeeSelectValue == None) | (coffeeSelectValue not in df[mask]["Name"].tolist()):
        mainContent = html.P("No Coffee Selected");
    else:
        mainContent = dbc.Accordion([
            # Coffee Information
            dbc.AccordionItem([
                selectedCoffeeInformation(df[mask], coffeeSelectValue)
            ], title="Coffee Information", style={"color":"white"}, item_id="coffeeInformation"),
            # Recommendation
            dbc.AccordionItem([
                get_recommendationContent(
                    techniqueSelected = techniqueSelected, 
                    df = df[mask], 
                    coffee_select=coffeeSelectValue, 
                    numRec = numRec, 
                    min_df = min_df, 
                    max_df = max_df, 
                    max_features = max_features, 
                    stop_words=stop_words, 
                    n_lower=ngram_range[0], 
                    n_upper=ngram_range[1], 
                    sublinear_tf = sublinear_tf, 
                    analyzer = analyzer, 
                    token_pattern=token_pattern)
            ], title="Recommendation", style={"color":"white"}, item_id="recommendation")   
        ], active_item="coffeeInformation");
    return mainContent;

# Callback: Get Selected Coffee Information - More Information *************
# @callback(
#     Output("more-information", "is_open"),
#     Output("more-information-button", "n_clicks"),
#     [Input("more-information-button", "n_clicks")],
#     [State("more-information", "is_open")],
# )
# def toggle_moreCoffeeInformation(n, is_open):
#     # if n:
#     #     return not is_open
#     # return is_open
#     print(n)
#     print(is_open)
#     # n = 0, is_open = False
#     if n == 1:
#         is_open = True;
#     else:
#         is_open = False;
#         n = 0;
#     return is_open, n;

# Callback: Get Selected Coffee Information - General Details & Taste Description **********
@callback(
    Output("more-information", "is_open"),
    Output("more-information-button", "n_clicks"),
    Output("taste-description", "is_open"),
    Output("taste-description-button", "n_clicks"),
    [
        Input("more-information-button", "n_clicks"),
        Input("taste-description-button", "n_clicks")
    ],
    [
        State("more-information", "is_open"),
        State("taste-description", "is_open")
    ],
)
def toggle_moreCoffeeInformationAndTasteDescription(n_more, n_taste, is_open_more, is_open_taste):
    if (n_more == 1) & (n_taste == 0):
        is_open_more = True;
    elif (n_more == 0) & (n_taste == 1):
        is_open_taste = True;
    else:
        n_more = 0;
        is_open_more = False;
        n_taste = 0;
        is_open_taste = False;
    return is_open_more, n_more, is_open_taste, n_taste;


# Callback: Recommended Coffee Output ************************
@callback(
    Output("recommended-coffee-information", "children"),
    Output("taste-profile-comparison", "children"),
    Output("recommended-coffee-wordCloud", "children"),
    Output("recommended-feature-result-chart", "children"),
    [
        Input("tbl", "active_cell"),
        # Filter Options
        Input("coffee-select", "value"),
        Input("machine-type-filter", "value"),
        Input("serving-filter", "value"),
        Input("include-decaf", "value"),
        # NLP Parameters
        Input("technique-selector", "value"),
        # Input("numRec", "value"),
        Input("min_df", "value"),
        Input("max_df", "value"),
        Input("max_features", "value"),
        Input("ngram_range","value"),
        Input("sublinear_tf", "value"),
        Input("analyzer", "value"),
    ]
)
def get_recommendedCoffeeContent(active_cell, coffeeSelectValue, machineTypeValue, servingValue, includeDecafValue, techniqueSelected, min_df, max_df, max_features, ngram_range, sublinear_tf, analyzer):
    if includeDecafValue == "Yes":
        mask = (df["Type"].isin(machineTypeValue)) & (df["Serving"].isin(servingValue));
    else:
        mask = (df["Type"].isin(machineTypeValue)) & (df["Serving"].isin(servingValue)) & (df["Decaf Coffee?"] != "Yes");

    if (bool(active_cell) == True):
        row_id = active_cell.get("row_id");
        recommendedCoffee = df.loc[row_id, "Name"];

        # Recommended Coffee Brief Information
        briefInfo = briefCoffeeInformation(
            df = df[mask],
            coffee_select = df.loc[row_id, "Name"],
            selectOrRecommend = "Recommended"
        );

        # Taste Profile Comparison
        tasteProfiles = get_tasteProfileComparison(
            df = df[mask], 
            coffee_select = coffeeSelectValue, 
            coffee_recommend = recommendedCoffee
        );

        # Recommended Coffee Word Cloud
        cloud = wordCloud(
            df = df[mask],
            coffee_select = df.loc[row_id, "Name"],
            selectOrRecommend = "Recommended"
        );

        # Recommended Coffee Feature Result
        df_recommendedFeatureResult = get_featureResults(
            techniqueSelected=techniqueSelected, 
            df = df[mask], 
            coffee_select=df.loc[row_id, "Name"], 
            min_df=min_df, 
            max_df=max_df, 
            max_features=max_features, 
            stop_words=stop_words, 
            n_lower=ngram_range[0], 
            n_upper=ngram_range[1], 
            sublinear_tf=sublinear_tf, 
            analyzer=analyzer, 
            token_pattern=token_pattern
        );
        featureChart = featureResultChart(
            techniqueSelected=techniqueSelected, 
            df_feature=df_recommendedFeatureResult, 
            coffee_select=recommendedCoffee
        );

    else:
        briefInfo = html.P("No Recommended Coffee Selected");
        tasteProfiles = html.Div(tasteProfileChart(df[mask], coffeeSelectValue));
        cloud = html.P("No Recommended Coffee Selected");
        featureChart = html.P("No Recommended Coffee Selected");
    return briefInfo, tasteProfiles, cloud, featureChart;

