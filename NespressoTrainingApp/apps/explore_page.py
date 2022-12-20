# Setup -------------------------------------------------------------
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Input, Output, State, callback, dash_table, dcc, html

# Import the data ----------------------------------------------------
df = pd.read_csv('PreparedCoffeeData.csv');

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
        multi=True,
        style={'color':'black'}
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
        multi=True,
        style={'color':'black'}
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

# Taste Profile Chart Selector:
# tasteProfileChartSelector = [
#     html.P('Select Chart', style={'font-weight':'bold'}),
#     dcc.Dropdown(
#         id='tasteProfileChart',
#         options = [
#             {'label':'Distribution Chart', 'value':'Distribution Chart'},
#             {'label':'Correlation with Intensity', 'value':'Yes'}
#         ],
#         value='Distribution Chart',
#         style={"display":"inline-flex"}
#     )
# ];

# Taste Profile Type Selector:
tasteProfileTypeSelector = [
    html.P('Taste Profile Type', style={'font-weight':'bold'}),
    dcc.RadioItems(
        id='tasteProfileType',
        options = [
            {'label':'Level', 'value':'Level'},
            {'label':'Classification', 'value':'Classification'}
        ],
        value='Level',
        inputStyle={"margin-right":"5px", "margin-left":"15px"},
        style={"display":"inline-flex"}
    )
];

# Milk Selector:
milkSelector = [
    html.P('With Milk?', style={'font-weight':'bold'}),
    dcc.RadioItems(
        id='milk',
        options = [
            {'label':'No', 'value':'No'},
            {'label':'Yes', 'value':'Yes'}
        ],
        value='No',
        inputStyle={"margin-right":"5px", "margin-left":"15px"},
        style={"display":"inline-flex"}
    )
];

# Taste Profile Selector
tasteProfileSelector = [
    html.P('Taste Profile', style={'font-weight':'bold'}),
    dcc.Dropdown(id='tasteProfile', style={'color':'black'}, clearable=False)
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
            ], title='Distribution of Coffee Intensity', style={'color':'white'}, item_id='3'),
            
            # Distribution of Roast by Machine Type & Proportion of Decaffeinated Coffee
            dbc.AccordionItem(children=[
                dbc.Card(children=[
                    html.Div(id='chart5'),
                ]),
            ], title='Distribution of Roast by Machine Type & Proportion of Decaffeinated Coffee', style={'color':'white'}, item_id='5'),

            # Distribution of Taste Profile Level & Correlation with Intensity
            dbc.AccordionItem(children=[
                dbc.Row(children=[
                    dbc.Col(children=[
                        dbc.Card(children=[
                            dbc.CardBody(children=tasteProfileTypeSelector)
                        ])
                    ]),
                    dbc.Col(children=[
                        dbc.Card(children=[
                            dbc.CardBody(children=milkSelector)
                        ])
                    ]),
                    dbc.Col(children=[
                        dbc.Card(children=[
                            dbc.CardBody(children=tasteProfileSelector)
                        ])
                    ]),
                ], style={'margin-bottom':'15px'}),
                html.Div(id='chart4', ),
            ], title='Distribution of Taste Profile & Relationship with Intensity', style={'color':'white'}, item_id='4'),
            
            # Taste Profile Correlation with Intensity
            dbc.AccordionItem(children=[
                dbc.Card(children=[
                    dbc.CardBody(children=milkSelector)
                ]),
                html.Div(id='chart6'),
            ], title='Taste Profile Correlation with Intensity', style={'color':'white'}, item_id='6'),
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

# Distribution of Coffee Intensity **************************************

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

# Distribution of Roast by Machine Type & Proportion of Decaffeinated Coffee *********

@callback(
    Output('chart5', 'children'),
    [
        Input('machine', 'value'),
        Input('serving', 'value'),
        Input('decaf', 'value'),
        Input('category', 'value'),
    ]
)
def get_chart5(machine, serving, decaf, category):
    if decaf == 'Yes':
        mask = (df['Type'].isin(machine)) & (df['Serving'].isin(serving)) & (df['Category'].isin(category));
    else:
        mask = (df['Type'].isin(machine)) & (df['Serving'].isin(serving)) & (df['Category'].isin(category)) & (df['Decaf Coffee?'] != 'Yes');
    df_filter = df[mask];
    # Bar Chart:
    df_agg = df_filter.groupby(by=['Roast Type','Type']).size();
    dff_bar = transformDataAggregation(df_agg);
    fig_bar = px.bar(
        dff_bar,
        x='Count',
        y='Roast Type',
        color='Type',
        barmode='group',
        orientation='h',
        template='plotly_dark',
        title='Distribution of Roast by Machine Type'
    );
    fig_bar.update_yaxes(categoryorder='array', categoryarray= ['Blonde','Medium','Dark']);
    # Pie Chart:
    df_prop = df_filter.groupby(by='Decaf Coffee?').size();
    data = [];
    for i in range(len(df_prop)):
        row = []
        row.append(df_prop.index[i]);
        row.append(df_prop.values[i]);
        data.append(row);
    dff_pie = pd.DataFrame(data, columns=['Decaf Coffee?','Count']);
    fig_pie = px.pie(dff_pie, values='Count', names='Decaf Coffee?', title='Proportion of Decaffeinated Coffee', template='plotly_dark');
    # Output:
    output = html.Div(children=[
        dbc.Row(children=[
            dbc.Col(children=dcc.Graph(figure=fig_bar, config={"displayModeBar":False}), width=8),
            dbc.Col(children=dcc.Graph(figure=fig_pie, config={"displayModeBar":False}), width=4),
        ])
    ]);
    return output;

# Get Taste Profile Options ************************************************

@callback(
    Output('tasteProfile', 'options'),
    Output('tasteProfile', 'value'),
    [
        Input('tasteProfileType', 'value'),
        Input('milk', 'value')
    ]
)
def get_tasteProfileOptions(tasteProfileType, milk):
    if (tasteProfileType == 'Level') & (milk == 'No'):
        options = ['Acidity','Bitterness','Roastness','Body'];
        value = 'Acidity';
    elif (tasteProfileType == 'Level') & (milk == 'Yes'):
        options = ['Milky Taste','Bitterness with Milk','Roastiness with Milk','Creamy Texture'];
        value = 'Milky Taste';
    elif (tasteProfileType == 'Classification') & (milk == 'No'):
        options = ['Acidity Classification','Bitterness Classification','Roastness Classification','Body Classification'];
        value = 'Acidity Classification';
    elif (tasteProfileType == 'Classification') & (milk == 'Yes'):
        options = ['Milky Taste Classification','Bitterness with Milk Classification','Roastiness with Milk Classification','Creamy Texture Classification'];
        value = 'Milky Taste Classification';
    return options, value;

# Distribution of Taste Profile & Relationship with Intensity ************************

@callback(
    Output('chart4', 'children'),
    [
        Input('machine', 'value'),
        Input('serving', 'value'),
        Input('decaf', 'value'),
        Input('category', 'value'),
        Input('tasteProfile', 'value'),
        Input('tasteProfileType', 'value'),
    ]
)
def get_chart4_and_5(machine, serving, decaf, category, tasteProfile, tasteProfileType):
    if decaf == 'Yes':
        mask = (df['Type'].isin(machine)) & (df['Serving'].isin(serving)) & (df['Category'].isin(category));
    else:
        mask = (df['Type'].isin(machine)) & (df['Serving'].isin(serving)) & (df['Category'].isin(category)) & (df['Decaf Coffee?'] != 'Yes');
    df_filter = df[mask];
    # Bar Chart:
    df_agg = df_filter.groupby(by=[tasteProfile]).size();
    data = [];
    for i in range(len(df_agg)):
        row = []
        row.append(df_agg.index[i]);
        row.append(df_agg.values[i]);
        data.append(row);
    dff_agg = pd.DataFrame(data, columns=[tasteProfile,'Count']);
    fig_agg = px.bar(dff_agg, x=tasteProfile, y='Count', template='plotly_dark', title=f'Distribution of {tasteProfile}');
    if tasteProfileType == 'Level':
        # Line Plot:
        df_mean = df_filter.groupby(by=[tasteProfile])['Intensity'].mean();
        data = [];
        for i in range(len(df_mean)):
            row = [];
            row.append(df_mean.index[i]);
            row.append(df_mean.values[i]);
            data.append(row);
        dff_mean = pd.DataFrame(data, columns=[tasteProfile,'Intensity']);
        fig_mean = px.line(dff_mean, x=tasteProfile, y='Intensity', template='plotly_dark', title=f'Relationship between {tasteProfile} and Intensity');
        # output = html.Div(children=[
        #     dbc.Row(children=dcc.Graph(figure=fig_agg, config={"displayModeBar":False})),
        #     dbc.Row(children=dcc.Graph(figure=fig_mean, config={"displayModeBar":False}))
        # ]);
        output = html.Div(children=[
            dbc.Row(children=[
                dbc.Col(children=dcc.Graph(figure=fig_agg, config={"displayModeBar":False}), width=6),
                dbc.Col(children=dcc.Graph(figure=fig_mean, config={"displayModeBar":False}), width=6)
            ])
        ]);
    elif tasteProfileType == 'Classification':
        fig_agg.update_xaxes(categoryorder='array', categoryarray= ['Low','Medium','High']);
        chart = dcc.Graph(figure=fig_agg, config={"displayModeBar":False});
        output = html.Div(children=chart);
    return output;

# Taste Profile Correlation with Intensity ******************************************

@callback(
    Output('chart6', 'children'),
    [
        Input('machine', 'value'),
        Input('serving', 'value'),
        Input('decaf', 'value'),
        Input('category', 'value'),
        Input('milk', 'value')
    ]
)
def get_chart6(machine, serving, decaf, category, milk):
    if decaf == 'Yes':
        mask = (df['Type'].isin(machine)) & (df['Serving'].isin(serving)) & (df['Category'].isin(category));
    else:
        mask = (df['Type'].isin(machine)) & (df['Serving'].isin(serving)) & (df['Category'].isin(category)) & (df['Decaf Coffee?'] != 'Yes');
    df_filter = df[mask];
    if milk == 'No':
        cols = ['Intensity','Acidity','Bitterness','Body','Roastness'];
        title = 'Correlation between Intensity & Taste Profile Levels';
        color_cont = 'amp';
    elif milk == 'Yes':
        cols = ['Intensity','Milky Taste','Bitterness with Milk','Roastiness with Milk','Creamy Texture'];
        title = 'Correlation between Intensity & Taste Profile Levels with Milk';
        color_cont = 'ice';
    dff = df_filter[cols].corr().round(3);
    fig = px.imshow(dff, text_auto=True, aspect='auto', title=title, color_continuous_scale=color_cont, template='plotly_dark');
    chart = dcc.Graph(figure=fig, config={"displayModeBar":False});
    output = html.Div(children=chart);
    return output;