import flask
import os
import dash
import dash_bootstrap_components as dbc
from random import randint

external_stylesheets = [dbc.themes.DARKLY]

server = flask.Flask(__name__)
server.secret_key = os.environ.get('secret_key', str(randint(0, 1000000)))
app = dash.Dash(__name__,server=server,external_stylesheets=external_stylesheets)