
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
#server = app.server
app.title = 'Surverses'

#os_path = os.path.abspath("D:/Python Projects/INF8808/Projet_Surverses/OS_clean.csv")
#step_path = os.path.abspath("D:/Python Projects/INF8808/Projet_Surverses/STEP.csv")

os_path = os.path.abspath("OS_clean.csv")
step_path = os.path.abspath("STEP.csv")

dataframe_OS = pd.read_csv(os_path)
dataframe_STEP = pd.read_csv(step_path)

dataframe_STEP = preprocess.correction_lat_long(dataframe_STEP)
dataframe_OS_init = preprocess.data_filter(dataframe_OS,2011,2019)

app.layout = html.Div(className='content', children=[
    html.Header(children=[
        html.H1('Déversement des eaux non-traités dans les cours d\'eau du Québec'),
        html.H2('Texte d\'introduction')
    ]),
    html.Div(className='viz-container', children=[
    dcc.Graph(
        id='map',
        config=dict(
            scrollZoom=True,
            showTips=False,
            showAxisDragHandles=False,
            doubleClick=False,
            displayModeBar=False
        )
    )], style={'width':'66%', 'display': 'inline-block'}),
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
                             html.Div([
                                    html.Div(id='slider-drag-output', style={'margin-top': '00px'}),
                                    dcc.RangeSlider(
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
                                    }
                                ),]),
                             html.Div(id='theme', style={'fontSize': '20px', 'margin-top': '0px', 'width':'49%', 'display': 'inline-block'},
                                    children=["Couleur des disques"]
                                 ),
                             html.Div(style={'fontSize': '20px', 'margin-top': '0px', 'width':'49%', 'display': 'inline-block'},
                                    children="Taille des disques"
                                 ),
                             html.Div(
                                 dcc.RadioItems(
                                    id='pts-color',
                                    options=[
                                        {'label': 'Cause principale de déversement', 'value': 'cause'},
                                        {'label': 'Âge des stations', 'value': 'age'},
                                    ],
                                    value='cause',
                                    labelStyle={'display': 'block'}
                                ), style={'width':'49%', 'display': 'inline-block'}),
                             html.Div(
                                 dcc.RadioItems(
                                    id='pts-size',
                                    options= [{'label': i, 'value': i} for i in ['Durée de déversement', 'Fréquence de déversements']],
                                    value='Durée de déversement',
                                    labelStyle={'display': 'block'}
                                ), style={'width':'49%', 'display': 'inline-block'}),
                                 ]),
    html.Div(className='viz-container2', children=[
        dcc.Graph(id='line-chart',
                config=dict(
                scrollZoom=False,
                showTips=False,
                showAxisDragHandles=False,
                doubleClick=False,
                displayModeBar=False)
        )
    ], style={'width':'33%', 'display': 'inline-block'}),
    html.Div(className='viz-container3', children=[
        dcc.Graph(
            id='bar-chart',
            config=dict(
                scrollZoom=True,
                showTips=False,
                showAxisDragHandles=False,
                doubleClick=False,
                displayModeBar=False
            )
        )
    ], style={'width':'33%', 'display': 'inline-block'})
    ]),
])
@app.callback(
    [Output('line-chart', 'figure'),Output('bar-chart', 'figure'),
    Output('map', 'figure')],
    [Input('pts-size', 'value'),Input('pts-color', 'value'),Input('my-range-slider', 'value')
    ,Input('map','clickData')]
    )
def update_graph(pts_size,pts_color,slider,clickdata):
    
    dataframe_OS = preprocess.data_filter(dataframe_OS_init,slider[0],slider[1])
    dataframe_linechart = preprocess.data_linechart(dataframe_OS)
    dataframe_barmap = preprocess.data_bar_map(dataframe_OS, dataframe_STEP)

    name = ""
    classement = 0
    if clickdata==None:
        None
    else:
        name = clickdata["points"][0]["hovertext"]
        classement = preprocess.bar_ranking(dataframe_barmap, pts_size, name)
        name = name.replace("Station", "station")

    figure_line=viz.line_chart(dataframe_linechart, pts_size, name)
    figure_bar=viz.bar_chart(dataframe_barmap, pts_size, name, classement)
    figure_map=viz.map(dataframe_barmap, pts_size,pts_color)

    return [figure_line, figure_bar, figure_map]

#if __name__ == '__main__':
   # app.run_server(debug=True)