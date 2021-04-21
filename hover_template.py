'''
    Provides the templates for the tooltips.
'''


def map_hover_template():
    '''
        Sets the template for the hover tooltips on the neighborhoods.

        The label is simply the name of the neighborhood in font 'Oswald'.

        Returns:
            The hover template.
    '''
    # TODO : Generate the hover template
    string = "<b><span style=\"font-family:Oswald\">%{customdata[0]}</span><b><extra></extra><br>"\
    "<b>Durée de débordement (minutes):<b> %{customdata[2]}<br>"\
    "<b>Fréquence:<b> %{customdata[3]}<br>"\
    "<b>Date de mise en service:<b> %{customdata[16]}<br>"\
    "<b>Taille de la station d'épuration:<b> %{customdata[14]}<br>"\
    "<b>Lac/Cours d'eau (milieu récepteur):<b> %{customdata[23]}<br>"\
    "<b>Nom du bassin primaire:<b> %{customdata[24]}"
    "<extra></extra>"
    return string