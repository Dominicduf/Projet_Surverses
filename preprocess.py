'''
    Contains some functions to preprocess the data used in the visualisation.
'''
import pandas as pd
import numpy as np

# Correction de la lattitude et de la longitude dans le fichier
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

# Filtrer les données pour le slider
def data_filter(df,min,max):
    df['Date de début du débordement'] = pd.to_datetime(df['Date de début du débordement'])
    df['Année'] = df['Date de début du débordement'].dt.year
    df_filtered = df[(df['Année'] >= min) & (df['Année'] <= max)]
    return df_filtered

# Données pour le line chart
def data_linechart(df,clickdata):
    df = df[['Nom de la station d\'épuration ','Durée de débordement (minutes)','Numéro de l\'ouvrage de surverse','Contexte du débordement', 'Date de début du débordement','Année']]
    if clickdata == None:
        None
    else:
        df=df[df['Nom de la station d\'épuration ']==clickdata]
        
    df_linechart = df.groupby(['Année','Contexte du débordement']).agg({'Durée de débordement (minutes)': 'sum', 'Nom de la station d\'épuration ':'count'}).reset_index()
    df_linechart.rename(columns = {'Nom de la station d\'épuration ':'Fréquence'}, inplace = True)
    df_linechart = df_linechart.sort_values(by=['Contexte du débordement','Année'])
    return df_linechart

# Obtenir l'âge de la station
def age_station(my_df):
    my_df['Year'] = pd.to_datetime(my_df['Date de mise en service']).dt.year
    my_df['Âge'] = 2021 - my_df['Year']
    return my_df

# Obtenir le contexte de débordement ayant la plus longue durée de débordement par station
def contexte_max(my_df):
    my_df=my_df.groupby(['Nom de la station d\'épuration ','Numéro de la station d\'épuration ','Contexte du débordement']).agg({'Durée de débordement (minutes)': 'sum'}).reset_index()
    my_df.rename(columns = {'Contexte du débordement':'Contexte du débordement max'}, inplace = True)
    my_df=my_df.sort_values(by='Durée de débordement (minutes)', ascending=False)
    my_df = my_df.drop_duplicates(subset=['Nom de la station d\'épuration '], keep='first')
    my_df = my_df.drop(['Durée de débordement (minutes)'], axis = 1)
    return my_df

# Données pour le bar chart et la carte
def data_bar_map(my_df_OS, my_df_STEP):
    my_df_OS_group=my_df_OS.groupby(['Nom de la station d\'épuration ','Numéro de la station d\'épuration ']).agg({'Durée de débordement (minutes)': 'sum','Nom de la station d\'épuration ':'count'})
    my_df_OS_group.rename(columns = {'Nom de la station d\'épuration ':'Fréquence'}, inplace = True)
    my_df_OS_group= my_df_OS_group.reset_index()

    my_df_STEP = age_station(my_df_STEP)
    my_df_contexte_max = contexte_max(my_df_OS)
    my_df_STEP = my_df_STEP.merge(my_df_contexte_max, right_on=['Nom de la station d\'épuration ','Numéro de la station d\'épuration '], 
    left_on= ['Nom de la station d\'épuration','Numéro de la station d\'épuration'])

    df_sum = my_df_OS_group.merge(my_df_STEP, right_on=['Nom de la station d\'épuration','Numéro de la station d\'épuration'], 
    left_on= ['Nom de la station d\'épuration ','Numéro de la station d\'épuration '])
    df_sum = df_sum.drop(["Nom de la station d'épuration _y", "Numéro de la station d'épuration _y"], axis = 1)
    df_sum.rename(columns = {"Nom de la station d'épuration _x":'Nom de la station d\'épuration ',"Numéro de la station d'épuration _x":"Numéro de la station d'épuration "}, inplace = True)
    df_sum = df_sum.sort_values(by=['Contexte du débordement max',])
    return df_sum

# Obtenir la position dans le ranking des pires stations
def bar_ranking(df, sort, name):
    col =""
    if sort=="Durée de déversement":
        col = "Durée de débordement (minutes)"
    elif sort == "Fréquence de déversements":
        col = "Fréquence"

    #df_sorted = df.sort_values(by=[col]).reset_index()
    #print(df_sorted.head(10))
    #print(df[df["Nom de la station d'épuration"]==name].index.values[0])
    df["Ranking"] = df[col].rank(method='min', ascending=False)
    
    index = df[df["Nom de la station d'épuration"]==name].index.values[0]
    nb = df.loc[index, "Ranking"]

    return int(nb)


