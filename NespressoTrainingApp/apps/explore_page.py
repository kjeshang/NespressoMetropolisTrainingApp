# Setup -------------------------------------------------------------
import pandas as pd
import numpy as np

import plotly.express as px
import plotly.graph_objects as go
from dash import dcc, html, Input, Output, State, callback, dash_table
import dash_bootstrap_components as dbc

# Import the data ----------------------------------------------------
df = pd.read_csv('data\PreparedCoffeeData.csv');

# Create Elements of the webpage --------------------------------------

# Machine Type Filter:
machineTypeFilter = [
    html.P("Machine Type", style={"font-weight":"bold"}),
    dcc.Checklist(
        id="machine",
        options=[{"label":x, "value":x} for x in df["Type"].unique().tolist()],
        value=df["Type"].unique().tolist(),
        inline=True,
        inputStyle={"margin-right":"5px", "margin-left":"15px"}
    )
];

# Serving Filter:
servingFilter = [
    html.P("Serving", style={"font-weight":"bold"}),
    dcc.Dropdown(
        id="serving",
        # options=[{"label":x, "value":x} for x in df["Serving"].unique().tolist()],
        # value=df["Serving"].unique().tolist(),
        multi=True
    )
];

# Decaf Coffee Filter:
decafCoffeeFilter = [
    html.P("Include Decaf Coffee?", style={"font-weight":"bold"}),
    dcc.RadioItems(
        id="decaf",
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

# Category Filter:
categoryFilter = [
    html.P("Category", style={"font-weight":"bold"}),
    dcc.Dropdown(
        id="category",
        # options=[{"label":x, "value":x} for x in df["Category"].unique().tolist()],
        # value=df["Category"].unique().tolist(),
        multi=True
    )
];

# Price Type Selector:
priceTypeSelector = [
    html.P('Price Type', style={'font-weight':'bold'}),
    dcc.RadioItems(
        id='priceType',
        options=[
            {'label':'Sleeve Price', 'value':'Sleeve Price'},
            {'label':'Per Capsule Price', 'value':'Per Capsule Price'}
        ],
        value='Sleeve Price',
        inputStyle={"margin-right":"5px", "margin-left":"15px"},
        style={"display":"inline-flex"}
    )   
];

# Intensity Option Type Selector:
intensityOptionTypeSelector = [
    html.P('Intensity Option', style={'font-weight':'bold'}),
    dcc.RadioItems(
        id='intensityOption',
        options=[
            {'label':'Intensity Level', 'value':'Intensity'},
            {'label':'Intensity Classification', 'value':'Intensity Classification'}
        ],
        value='Intensity',
        inputStyle={"margin-right":"5px", "margin-left":"15px"},
        style={"display":"inline-flex"}
    )
];

# EDA Content:
edaContent = html.Div(id='eda-content');

# Page Layout ----------------------------------------------------------
pageStructure = [
    dbc.Row(children=[
        # Machine Type
        dbc.Col(children=[
            dbc.Card(children=[
                dbc.CardBody(children=machineTypeFilter)
            ])
        ], width=3),
        # Decaf Coffee
        dbc.Col(children=[
            dbc.Card(children=[
                dbc.CardBody(children=servingFilter)
            ])
        ], width=7),
        # Serving:
        dbc.Col(children=[
            dbc.Card(children=[
                dbc.CardBody(children=decafCoffeeFilter)
            ])
        ], width=2)
    ], style={"margin-bottom":"15px"}),
    dbc.Row(children=[
        dbc.Col(children=[
            dbc.Card(children=[
                dbc.CardBody(children=categoryFilter)
            ])
        ])
    ], style={"margin-bottom":"15px"}),
    dbc.Row(children=edaContent)
];

pageLayout = dbc.Container(children=pageStructure, fluid=True);

# Callbacks & Functions ------------------------------------------------

# Get Serving Options ****************************************************

@callback(
    Output("serving", "value"),
    Output("serving", "options"),
    [Input("machine", "value")]
)
def get_servingOptions(machine):
    mask = df["Type"].isin(machine);
    servingValue = df[mask]["Serving"].unique().tolist();
    servingOptions = [{"label":x, "value":x} for x in servingValue];
    return servingValue, servingOptions;

# Get Category Options ****************************************************

@callback(
    Output('category', 'value'),
    Output('category', 'options'),
    [Input('machine','value')]
)
def get_categoryOptions(machine):
    mask = df['Type'].isin(machine);
    categoryValue = df[mask]['Category'].unique().tolist();
    categoryOptions = [{"label":x, "value":x} for x in categoryValue];
    return categoryValue, categoryOptions;

# Exploratory Analysis Content *********************************************

@callback(
    Output('eda-content','children'),
    [   
        Input('machine', 'value'),
        Input('serving', 'value'),
        Input('decaf', 'value'),
        Input('category', 'value')
    ]
)
def get_edaContent(machine, serving, decaf, category):
    if ((len(machine) == 0) & (len(serving) == 0)) | (len(category) == 0):
        content = html.P("No Machine Type, Serving and/or Category selected");
    else:
        content = dbc.Accordion(children=[
            # Distribution of Coffee Servings
            dbc.AccordionItem(children=[
                html.Div(id='chart1')
            ], title='Distribution of Coffee Servings', style={'color':'white'}, item_id='1'),
            # Distribution of Coffee Price
            dbc.AccordionItem(children=[
                dbc.Card(children=[
                    dbc.CardBody(children=priceTypeSelector)
                ]),
                html.Div(id='chart2'),
            ], title='Distribution of Coffee Price', style={'color':'white'}, item_id='2'),
            # Distribution of Coffee Intensity
            dbc.AccordionItem(children=[
                dbc.Card(children=[
                    dbc.CardBody(children=intensityOptionTypeSelector)
                ]),
                html.Div(id='chart3'),
            ], title='Distribution of Coffee Intensity', style={'color':'white'}, item_id='3')
        ]);
    return content;

# Distribution of Coffee Servings ******************************

def transformDataAggregation(df_agg):
    labels = [];
    labels.append(df_agg.index.names[0]);
    labels.append(df_agg.index.names[1]);
    labels.append('Count');
    
    data = [];
    for i in range(len(df_agg)):
        row = []
        for j in range(len(df_agg.index[i])):
            # row.append(str(df_agg.index[i][j]));
            row.append(df_agg.index[i][j]);
        row.append(df_agg.values[i]);
        data.append(row);
    return pd.DataFrame(data, columns=labels);

@callback(
    Output('chart1','children'),
    [   
        Input('machine', 'value'),
        Input('serving', 'value'),
        Input('decaf', 'value'),
        Input('category', 'value'),
    ]
)
def get_chart1(machine, serving, decaf, category):
    if decaf == 'Yes':
        mask = (df['Type'].isin(machine)) & (df['Serving'].isin(serving)) & (df['Category'].isin(category));
    else:
        mask = (df['Type'].isin(machine)) & (df['Serving'].isin(serving)) & (df['Category'].isin(category)) & (df['Decaf Coffee?'] != 'Yes');
    if (len(machine) == 2):
        dff = transformDataAggregation(
            df_agg=df[mask].groupby(by=['Serving','Type']).size()
        );
        fig = px.bar(
            dff, 
            x=dff.columns.tolist()[0], 
            y=dff.columns.tolist()[2],
            color=dff.columns.tolist()[1],
            barmode='group',
            template='plotly_dark',
            title='Distribution of Coffee Servings (Vertuo & Original)'
        );
    else:
        dff = df[mask].groupby(by=['Serving']).size();
        if machine[0] == 'Vertuo':
            title = 'Distribution of Vertuo Coffee Servings';
        elif machine[0] == 'Original':
            title = 'Distribution of Original Coffee Servings';
        fig = px.bar(dff, x=dff.index, y=dff.values, title=title, template='plotly_dark');
        fig.update_layout(
            yaxis_title="Count",
        );
    chart = dcc.Graph(figure=fig, config={"displayModeBar":False});
    output = html.Div(children=chart);
    return output;

# Distribution of Coffee Price ******************************************
@callback(
    Output('chart2','children'),
    [   
        Input('machine', 'value'),
        Input('serving', 'value'),
        Input('decaf', 'value'),
        Input('category', 'value'),
        Input('priceType', 'value')
    ]
)
def get_chart2(machine, serving, decaf, category, priceType):
    if decaf == 'Yes':
        mask = (df['Type'].isin(machine)) & (df['Serving'].isin(serving)) & (df['Category'].isin(category));
    else:
        mask = (df['Type'].isin(machine)) & (df['Serving'].isin(serving)) & (df['Category'].isin(category)) & (df['Decaf Coffee?'] != 'Yes');
    if (len(machine) == 2):
        dff = transformDataAggregation(
            df_agg=df[mask].groupby(by=[priceType,'Type']).size()
        );
        dff = dff.sort_values(by=priceType, ascending=True);
        dff[priceType] = dff[priceType].astype(str);
        fig = px.bar(
            dff, 
            x=dff.columns.tolist()[0], 
            y=dff.columns.tolist()[2],
            color=dff.columns.tolist()[1],
            template='plotly_dark',
            title='Distribution of Coffee Price (Vertuo & Original)'
        );
    else:
        dff = df[mask].groupby(by=[priceType]).size();
        # print(dff);
        dff = dff.sort_index();
        dff.index = dff.index.astype(str);
        if machine[0] == 'Vertuo':
            title = 'Distribution of Vertuo Coffee Price';
        elif machine[0] == 'Original':
            title = 'Distribution of Original Coffee Price';
        fig = px.bar(dff, x=dff.index, y=dff.values, title=title, template='plotly_dark');
    fig.update_layout(
        xaxis_title=f'{priceType} ($)',
        yaxis_title="Count",
        xaxis = dict(
            tickformat='%.2f'
        )
    );
    chart = dcc.Graph(figure=fig, config={"displayModeBar":False});
    output = html.Div(children=chart);
    return output;

# Distribution of Coffee Intensity **************************************\
@callback(
    Output('chart3','children'),
    [   
        Input('machine', 'value'),
        Input('serving', 'value'),
        Input('decaf', 'value'),
        Input('category', 'value'),
        Input('intensityOption', 'value')
    ]
)
def get_chart3(machine, serving, decaf, category, intensityOption):
    if decaf == 'Yes':
        mask = (df['Type'].isin(machine)) & (df['Serving'].isin(serving)) & (df['Category'].isin(category));
    else:
        mask = (df['Type'].isin(machine)) & (df['Serving'].isin(serving)) & (df['Category'].isin(category)) & (df['Decaf Coffee?'] != 'Yes');
    if len(machine) == 2:
        dff = transformDataAggregation(
            df_agg=df[mask].groupby(by=[intensityOption,'Type']).size()
        );
        dff = dff.sort_values(by=intensityOption, ascending=True);
        dff[intensityOption] = dff[intensityOption].astype(str);
        fig = px.bar(
            dff, 
            x=dff.columns.tolist()[0], 
            y=dff.columns.tolist()[2],
            color=dff.columns.tolist()[1],
            template='plotly_dark',
            title='Distribution of Coffee Intensity (Vertuo & Original)'
        );
        fig.update_layout(
            xaxis_title=f'{intensityOption}',
            yaxis_title="Count",
            barmode='group'
        );
        if intensityOption == 'Intensity Classification':
            fig.update_xaxes(categoryorder='array', categoryarray= ['Low','Medium','High']);   
    else:
        dff = df[mask].groupby(by=[intensityOption]).size();
        # print(dff);
        dff = dff.sort_index();
        dff.index = dff.index.astype(str);
        if machine[0] == 'Vertuo':
            title = 'Distribution of Vertuo Coffee Price';
        elif machine[0] == 'Original':
            title = 'Distribution of Original Coffee Price';
        fig = px.bar(dff, x=dff.index, y=dff.values, title=title, template='plotly_dark');
        fig.update_layout(
            xaxis_title=f'{intensityOption}',
            yaxis_title="Count",
        );
        if intensityOption == 'Intensity Classification':
           fig.update_xaxes(categoryorder='array', categoryarray= ['Low','Medium','High']);
    chart = dcc.Graph(figure=fig, config={"displayModeBar":False});
    output = html.Div(children=chart);
    return output;