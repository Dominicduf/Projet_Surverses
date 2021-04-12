'''
    Contains some functions to preprocess the data used in the visualisation.
'''
import pandas as pd
import numpy as np

def correction_lat_long(my_df_STEP):
    my_df_STEP['Latitude de l\'émissaire']=my_df_STEP['Latitude de l\'émissaire'].str.replace(',' , '')
    my_df_STEP['Longitude de l\'émissaire']=my_df_STEP['Longitude de l\'émissaire'].str.replace(',' , '')

    lat = []
    long = []
    for i in np.arange(0,my_df_STEP.shape[0]):
        s_lat=my_df_STEP.iloc[i]['Latitude de l\'émissaire']
        s_long=my_df_STEP.iloc[i]['Longitude de l\'émissaire']
        s_lat = s_lat[:2] + '.' + s_lat[2:]
        s_long = s_long[:3] + '.' + s_long[3:]
        lat.append(s_lat)
        long.append(s_long)

    my_df_STEP['Latitude de l\'émissaire']=pd.DataFrame(lat).astype(float)
    my_df_STEP['Longitude de l\'émissaire']=pd.DataFrame(long).astype(float)
    return my_df_STEP

def valeur_total(my_df_OS, my_df_STEP):
    my_df_OS_group=my_df_OS.groupby(['Nom de la station d\'épuration ']).agg({'Durée de débordement (minutes)': 'sum'}).reset_index()
    my_df_STEP = my_df_STEP[['Nom de la station d\'épuration','Latitude de l\'émissaire','Longitude de l\'émissaire']]

    df_sum = my_df_OS_group.merge(my_df_STEP, right_on='Nom de la station d\'épuration', left_on= 'Nom de la station d\'épuration ')
    return df_sum