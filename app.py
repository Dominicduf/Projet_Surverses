
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

def init_app_layout(figure):
    '''
        Generates the HTML layout representing the app.

        Args:
            figure: The figure to display.
        Returns:
            The HTML structure of the app's web page.
    '''
    return html.Div(className='content', children=[
        html.Header(children=[
            html.H1('Déversement des eaux non-traités dans les cours d\'eau du Québec'),
            html.H2('Texte d\'introduction')
        ]),
        html.Main(children=[
            html.Div(className='viz-container', children=[
                dcc.Graph(
                    figure=figure,
                    config=dict(
                        scrollZoom=True,
                        showTips=False,
                        showAxisDragHandles=False,
                        doubleClick=False,
                        displayModeBar=False
                    ),
                    className='map',
                    id='line-chart'
                )
            ])
        ])
    ])


fig = viz.map(dataframe_merged)
app.layout = init_app_layout(fig)
