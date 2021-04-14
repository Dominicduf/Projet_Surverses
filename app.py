
# -*- coding: utf-8 -*-

'''
    File name: app.py
    Author: Dominic Dufour, Antoine Rincent, Daniel Lussier-Seguin
    Course: INF8808
    Python Version: 3.8

    This file is the entry point for our dash app.
'''


import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State

import pandas as pd

import preprocess
import viz
import os

#from template import create_template
#from modes import MODES


app = dash.Dash(__name__)
app.title = 'Surverses'

os_path = os.path.abspath("./OS_clean.csv")
step_path = os.path.abspath("./STEP.csv")

dataframe_OS = pd.read_csv(os_path)
dataframe_STEP = pd.read_csv(step_path)

dataframe_STEP = preprocess.correction_lat_long(dataframe_STEP)
dataframe_merged = preprocess.valeur_total(dataframe_OS, dataframe_STEP)
dataframe_année = preprocess.valeur_année(dataframe_OS)

app.layout = html.Div(className='content', children=[
    html.Header(children=[
        html.H1('Déversement des eaux non-traités dans les cours d\'eau du Québec'),
        html.H2('Texte d\'introduction')
    ]),
    html.Div(
            className='panel-div',
            style={
                'justifyContent': 'center',
                'alignItems': 'center'},
            children=[
                html.Div(id='panel', style={
                    'visibility': 'visible',
                    'border': '1px solid black',
                    'padding': '10px'},
                         children=[
                             html.Div(id='marker-title', style={
                                 'fontSize': '24px'}, children="Manipulation de la carte"),
                             html.Div([dcc.RangeSlider(
                                    id='my-range-slider',
                                    min=2011,
                                    max=2019,
                                    step=1,
                                    value=[2011, 2019],
                                    marks={
                                    2011: {'label': '2011'},
                                    2013: {'label': '2013'},
                                    2015: {'label': '2015'},
                                    2017: {'label': '2017'},
                                    2019: {'label': '2019'}
                                    },
                                ),]),
                             html.Div(id='theme', style={'fontSize': '20px'},
                                    children="Couleur des points"
                                 ),
                             html.Div(
                                 dcc.RadioItems(
                                    options=[
                                        {'label': 'Cause principale de déversement', 'value': 'cause'},
                                        {'label': 'Âge des stations', 'value': 'age'},
                                    ],
                                    value='cause',
                                    labelStyle={'display': 'block'}
                                )),
                                    html.Div(style={'fontSize': '20px'},
                                    children="Taille des points"
                                 ),
                             html.Div(
                                 dcc.RadioItems(
                                    options=[
                                        {'label': 'Durée de déversement', 'value': 'duree'},
                                        {'label': 'Fréquence de déversements', 'value': 'freq'},
                                    ],
                                    value='duree',
                                    labelStyle={'display': 'block'}
                                )),
                                 ])]),
    html.Div(className='viz-container', children=[
        dcc.Graph(
            id='map',
            className='graph',
            figure=viz.map(dataframe_merged),
            config=dict(
                scrollZoom=True,
                showTips=False,
                showAxisDragHandles=False,
                doubleClick=False,
                displayModeBar=False
            )
        )]),
    html.Div(className='viz-container2', children=[
        dcc.Graph(
            id='line-chart',
            className='graph',
            figure=viz.line_chart(dataframe_année),
            config=dict(
                scrollZoom=False,
                showTips=False,
                showAxisDragHandles=False,
                doubleClick=False,
                displayModeBar=False
            )
        )
    ])
])