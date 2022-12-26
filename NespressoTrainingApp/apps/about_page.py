# Setup --------------------------------------------------------
from dash import Dash, dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc

# Create elements of the webpage -------------------------------

image_path = "https://nestle-nespresso.com/sites/site.prod.nestle-nespresso.com/files/styles/crop_freeform/public/MONOGRAM%20BLACK_0.jpg?itok=QmU2ExCh";

logoImage = html.Img(src=image_path, style={'height':'85%', 'width':'75%', "padding":"0", "display":"inline-flex"});

message = dcc.Markdown(
    '''
    **_Welcome to the Nespresso Metropolis Training App!_**
    
    This web application was created using the Python programming language as well as the Numpy, Pandas, Scikit-Learn, Plotly, and Dash Libraries. It was created to serve as a referential platform for both new Hires and current Coffee Specialists to better-familiarize themselves regarding the various coffee flavours for the purpose of serving customers with maximum information with the ability to make precise flavour recommendations. This application is essentially a recommendation engine, with various other facets & features, yet is in the guise of a training platform. The information shown on this application was retrieved from the official Nespresso Canada, USA, UK, and Australia websites. There is no internal company information that is displayed in this application.

    This application was created during my Fall 2022 Semester at Douglas College to fulfill the term project requirement of CSIS 3290: Fundamentals of Machine Learning. I would like to thank Prof. Bambang Sarif for supporting me throughout the semester to create this application. Furthermore, I would like to thank Mr. Scott Sorell (Nespresso Metrotown Boutique Manager), Ms. Kashish Bhandari (Bard Team Leader), and Ms. Zoe Jia (Total Quality Management Team Leader) for helping me to better understand the Nespresso product lineup and continually inspiring to become a better Coffee Specialist

    --- Kunal Ajaykumar Jeshang

    '''
);

aboutPageContent = [
    html.P(message, style={'display':'inline-flex'})
];

# Page Layout --------------------------------------------------
aboutPageStructure = [
    html.Br(),
    dbc.Row(children=[
        dbc.Col(children=logoImage, width=5),
        dbc.Col(children=aboutPageContent, width=7)
    ])
];

aboutPageLayout = dbc.Container(children=aboutPageStructure, fluid=True);