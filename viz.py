'''
    Contains some functions related to the creation of the bar chart.
    The bar chart displays the data either as counts or as percentages.
'''

import plotly.graph_objects as go
import plotly.io as pio
import plotly.express as px


def map(df, mode_size, mode_color):
    '''
        Initializes the Graph Object figure used to display the bar chart.
        Sets the template to be used to "simple_white" as a base with
        our custom template on top. Sets the title to 'Lines per act'

        Returns:
            fig: The figure which will display the bar chart
    '''
    # TODO : Update the template to include our new theme and set the title
    if (mode_size =='Durée de déversement') & (mode_color =='cause'):
        fig = px.scatter_mapbox(df, lat='Latitude de l\'émissaire', lon='Longitude de l\'émissaire', size='Durée de débordement (minutes)', color='Contexte du débordement max',
                   size_max=15, zoom=2.6, mapbox_style='open-street-map', center=dict(lat=53 , lon =-70))
    elif (mode_size =='Durée de déversement') & (mode_color =='age'):
        fig = px.scatter_mapbox(df, lat='Latitude de l\'émissaire', lon='Longitude de l\'émissaire', size='Durée de débordement (minutes)', color='Âge',
                   size_max=15, zoom=2.6, mapbox_style='open-street-map', center=dict(lat=53 , lon =-70))
    elif (mode_size =='Fréquence de déversements') & (mode_color =='cause'):
        fig = px.scatter_mapbox(df, lat='Latitude de l\'émissaire', lon='Longitude de l\'émissaire', size='Fréquence', color ='Contexte du débordement max',
                   size_max=15, zoom=2.6, mapbox_style='open-street-map', center=dict(lat=53 , lon =-70))
    elif (mode_size =='Fréquence de déversements') & (mode_color =='age'):
        fig = px.scatter_mapbox(df, lat='Latitude de l\'émissaire', lon='Longitude de l\'émissaire', size='Fréquence', color ='Âge',
                   size_max=15, zoom=2.6, mapbox_style='open-street-map', center=dict(lat=53 , lon =-70))  
    fig.update_layout(height=725, width=1000)
    fig.layout.paper_bgcolor ="rgb(209, 222, 224)"
    return fig

def line_chart(df, mode):
    if mode =='Durée de déversement':
        fig = px.line(df, x='Année', y='Durée de débordement (minutes)', color='Contexte du débordement')
    elif mode =='Fréquence de déversements':
        fig = px.line(df, x='Année', y='Fréquence', color='Contexte du débordement')
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="top",
        xanchor="left",
        y=-0.15
    ))
    fig.layout.paper_bgcolor ="rgb(209, 222, 224)"
    return fig

def bar_chart(df,mode):
    if mode =='Durée de déversement':
        df_sorted = df.sort_values(by=['Durée de débordement (minutes)'])
        fig = px.bar(df_sorted, x='Nom de la station d\'épuration ', y='Durée de débordement (minutes)')
    elif mode =='Fréquence de déversements':
        df_sorted = df.sort_values(by=['Fréquence'])
        fig = px.bar(df_sorted, x='Nom de la station d\'épuration ', y='Fréquence') 
    fig.update_xaxes(visible=False)
    fig.layout.paper_bgcolor ="rgb(209, 222, 224)"
    return fig