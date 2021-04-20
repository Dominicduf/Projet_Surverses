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
        fig = px.scatter_mapbox(df, lat='Latitude de l\'émissaire', lon='Longitude de l\'émissaire', size='Durée de débordement (minutes)', color='Contexte du débordement max', hover_name="Nom de la station d'épuration",
                   size_max=15, zoom=3.75, mapbox_style='open-street-map', center=dict(lat=53 , lon =-74))
    elif (mode_size =='Durée de déversement') & (mode_color =='age'):
        fig = px.scatter_mapbox(df, lat='Latitude de l\'émissaire', lon='Longitude de l\'émissaire', size='Durée de débordement (minutes)', color='Âge', hover_name="Nom de la station d'épuration",
                   size_max=15, zoom=3.75, mapbox_style='open-street-map', center=dict(lat=53 , lon =-74))
    elif (mode_size =='Fréquence de déversements') & (mode_color =='cause'):
        fig = px.scatter_mapbox(df, lat='Latitude de l\'émissaire', lon='Longitude de l\'émissaire', size='Fréquence', color ='Contexte du débordement max', hover_name="Nom de la station d'épuration",
                   size_max=15, zoom=3.75, mapbox_style='open-street-map', center=dict(lat=53 , lon =-74))
    elif (mode_size =='Fréquence de déversements') & (mode_color =='age'):
        fig = px.scatter_mapbox(df, lat='Latitude de l\'émissaire', lon='Longitude de l\'émissaire', size='Fréquence', color ='Âge', hover_name="Nom de la station d'épuration",
                   size_max=15, zoom=3.75, mapbox_style='open-street-map', center=dict(lat=53 , lon =-74))  
    fig.update_layout(height=800, width=1100)
    fig.layout.paper_bgcolor ="rgb(209, 222, 224)"
    return fig

def line_chart(df, mode):
    titre = "Comparaison des causes de déversement en fonction de "
    if mode =='Durée de déversement':
        titre += "la durée des déversements"
        fig = px.line(df, x='Année', y='Durée de débordement (minutes)', color='Contexte du débordement', title=titre)
    elif mode =='Fréquence de déversements':
        titre += "la fréquence des déversements"
        fig = px.line(df, x='Année', y='Fréquence', color='Contexte du débordement', title=titre)
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="top",
        xanchor="left",
        y=-0.15
    ))
    fig.layout.paper_bgcolor ="rgb(209, 222, 224)"
    return fig

def bar_chart(df,mode):
    titre = "Classement des pires stations selon "
    if mode =='Durée de déversement':
        titre += "la durée des déversements"
        df_sorted = df.sort_values(by=['Durée de débordement (minutes)'])
        fig = px.bar(df_sorted, x='Nom de la station d\'épuration ', y='Durée de débordement (minutes)', title=titre)
    elif mode =='Fréquence de déversements':
        titre += "la fréquence des déversements"
        df_sorted = df.sort_values(by=['Fréquence'])
        fig = px.bar(df_sorted, x='Nom de la station d\'épuration ', y='Fréquence', title=titre) 
    fig.update_xaxes(visible=False)
    fig.layout.paper_bgcolor ="rgb(209, 222, 224)"
    return fig