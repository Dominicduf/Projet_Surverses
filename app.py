
# -*- coding: utf-8 -*-

'''
    File name: app.py
    Author: Dominic Dufour, Antoine Rincet, Daniel Lussier-Seguin
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

#from template import create_template
#from modes import MODES


app = dash.Dash(__name__)
app.title = 'TP2 | INF8808'



dataframe_OS = pd.read_csv('d:/Python Projects/INF8808/Projet surverse/OS_clean.csv')
dataframe_STEP = pd.read_csv('d:/Python Projects/INF8808/Projet surverse/STEP.csv')

dataframe_STEP = preprocess.correction_lat_long(dataframe_STEP)
dataframe_merged = preprocess.valeur_total(dataframe_OS, dataframe_STEP)
dataframe_année = preprocess.valeur_année(dataframe_OS)

app.layout = html.Div(className='content', children=[
    html.Header(children=[
        html.H1('Déversement des eaux non-traités dans les cours d\'eau du Québec'),
        html.H2('Texte d\'introduction')
    ]),
    html.Main(className='viz-container', children=[
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
        ),
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