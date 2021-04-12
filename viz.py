'''
    Contains some functions related to the creation of the bar chart.
    The bar chart displays the data either as counts or as percentages.
'''

import plotly.graph_objects as go
import plotly.io as pio
import plotly.express as px


def map(df):
    '''
        Initializes the Graph Object figure used to display the bar chart.
        Sets the template to be used to "simple_white" as a base with
        our custom template on top. Sets the title to 'Lines per act'

        Returns:
            fig: The figure which will display the bar chart
    '''
    # TODO : Update the template to include our new theme and set the title

    fig = px.scatter_mapbox(df, lat='Latitude de l\'émissaire', lon='Longitude de l\'émissaire', size='Durée de débordement (minutes)',
                   size_max=15, zoom=2.6, mapbox_style='open-street-map', center=dict(lat=53 , lon =-70))
    fig.update_layout(height=725, width=1000)
    return fig