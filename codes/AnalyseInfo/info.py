import pandas as pd
import collections
from collections import Counter

# Read the csv file into a dataframe.
df_serie = pd.read_csv("C:\\Users\\stosc\\Documents\\ESME\\Ingé2_2019-2020\\S2\\UE1\\DataTools\\Projet\series_data.csv",
                      header=0, index_col=0)

'''
    Moyenne du nombre de saison par série
'''
print(df_serie['Number_of_season'].mean())


'''
    Reccupération de la langue la plus utilisée et des occurences des 3 plus communes
'''
print(df_serie['Language'].value_counts().idxmax())
redondant_language=collections.Counter(df_serie['Language']).most_common(3)
print(redondant_language)


'''
    Reccupération du format d'épisode et du type les plus communs
'''
redondant_format=collections.Counter(df_serie['Number_of_episodes']).most_common(3)
print(redondant_format)

redondant_type=collections.Counter(df_serie['Type']).most_common(3)
print(redondant_type)


'''
       Reccupération des 10 acteurs les plus cotés sur le top 10
'''
list_actors=[]

for n in range(len(df_serie["Actors"])) :
    clean_column = df_serie.iloc[n, 5]
    clean= clean_column.replace('[','')
    clean = clean.replace(']','')
    clean = clean.replace("'","")
    clean = clean.replace(",","")
    #Split strings element to list : get actors.
    liste = clean.split("\\n")

    for element in liste:
        if element!='':
            list_actors.append(element)
        

list_actors
redondant_actors=collections.Counter(list_actors).most_common(10)
print(redondant_actors)


'''
       Reccupération du genre qui marche le mieux 
'''
list_genre=[]

for n in range(len(df_serie["Genre"])) :
    clean_column = df_serie.iloc[n, 1]
    clean= clean_column.replace('[','')
    clean = clean.replace(']','')
    clean = clean.replace("'","")
    clean = clean.replace(",","")
    #Split strings element to list : get actors.
    liste = clean.split("\\n")

    for element in liste:
        if element!='':
            list_genre.append(element)
        
redondant_genre=collections.Counter(list_genre).most_common(3)
print(redondant_genre)


'''
       Reccupération des créateurs de plusieurs séries. 
'''
list_creators=[]

for n in range(len(df_serie["Creators"])) :
    clean_column = str(df_serie.iloc[n, 6])
    clean= clean_column.replace('[','')
    clean = clean.replace(']','')
    clean = clean.replace("'","")
    clean = clean.replace(",","")
    #Split strings element to list : get actors.
    liste = clean.split("\\n")

    for element in liste:
        if element!='':
            list_creators.append(element)


redondant_creators=collections.Counter(list_creators).most_common(6)
print(redondant_creators)


'''
       Reccupération des origines de série les plus courantes. 
'''
list_origin=[]

for n in range(len(df_serie["Origin"])) :
    clean_column = df_serie.iloc[n, 7]
    clean= clean_column.replace('[','')
    clean = clean.replace(']','')
    clean = clean.replace("'","")
    clean = clean.replace(",","")
    #Split strings element to list : get actors.
    liste = clean.split("\\n")

    for element in liste:
        if element!='':
            list_origin.append(element)
        
redondant_origin=collections.Counter(list_origin).most_common(2)
print(redondant_origin)


'''
       Reccupération des certifications. 
'''
list_certification=[]

for n in range(len(df_serie["Origin"])) :
    clean_column = str(df_serie.iloc[n, 9])
    clean= clean_column.replace('[','')
    clean = clean.replace(']','')
    clean = clean.replace("'","")
    clean = clean.replace(",","")
    #Split strings element to list : get actors.
    liste = clean.split("\\n")

    for element in liste:
        if element!='':
            if element!='nan':
                list_certification.append(element)
        
list_certification

redondant_certification=collections.Counter(list_certification).most_common(2)
print(redondant_certification)