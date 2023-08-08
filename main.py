# Estudiante: Luis A, Ramirez G.<br>
# GitHub: ramirezla<br>
# Email: ramirezluisalberto@hotmail.com<br>
# Email: ramirezgluisalberto@gmail.com<br>

import pandas as pd
from wordcloud import WordCloud

from fastapi import FastAPI
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

# Se importa el archivo 'LARG_moviesdataset_reducido_ml_sample_60.csv' con los datos de las peliculas,
# este archivo ya contiene la data limpiada.

ruta_archivo_movies = "./Datasets/LARG_moviesdataset_reducido_ml_sample_60.csv"
LARG_moviesdataset_reducido = pd.read_csv(ruta_archivo_movies)

# Se instancia una variable de tipo FastAPI
app = FastAPI(title='PI_ML_OPS-main', description='Luis A Ramirez G')

# def peliculas_idioma( Idioma: str ): 
# Se ingresa un idioma (como están escritos en el dataset, no hay que traducirlos!). 
# Debe devolver la cantidad de películas producidas en ese idioma.
@app.get('/peliculas_idioma/{idioma}')
def peliculas_idioma(idioma:str):
    try:
        valores = LARG_moviesdataset_reducido[LARG_moviesdataset_reducido['original_language'] == idioma]
        cant_peliculas = int(valores['original_language'].count())
    except (ValueError, SyntaxError):
        pass 
    return {'Idioma indicado':idioma, 'Cantidad encontrada': cant_peliculas}

# def peliculas_duracion( Pelicula: str ): 
# Se ingresa una pelicula. Debe devolver la duracion y el año.
@app.get('/pelicula_duracion_anno/{pelicula}')
def pelicula_duracion_anno(pelicula: str):
    try:
        duracion_min = int(LARG_moviesdataset_reducido[LARG_moviesdataset_reducido['title'] == pelicula]['runtime'])
        anno = int(LARG_moviesdataset_reducido[LARG_moviesdataset_reducido['title'] == pelicula]['release_year'])   # Se cambia el tipo de dato a int para que Json no tenga problemas con el tipo int64
    except (ValueError, SyntaxError):
        pass 
    return {'Nombre Pelicula':pelicula, 'Duracion en minutos':duracion_min, 'Año de estreno':anno}

# def franquicia( Franquicia: str): 
# Se ingresa la franquicia, retornando la cantidad de peliculas, ganancia total y promedio.
@app.get('/franquicia_cant_gana_prom_peliculas/{franquicia}')
def franquicia_cant_gana_prom_peliculas(franquicia:str):
    try:
        cantidad_peliculas = int(LARG_moviesdataset_reducido[LARG_moviesdataset_reducido['belongs_to_collection'] == franquicia]['title'].count())
        ganancia_total = float(LARG_moviesdataset_reducido[LARG_moviesdataset_reducido['belongs_to_collection'] == franquicia]['revenue'].sum())
        ganancia_promedio = 0
        if cantidad_peliculas != 0:
            ganancia_promedio = float(ganancia_total/cantidad_peliculas)
    except (ValueError, SyntaxError):
        pass 
    return {'Titulo franquicia':franquicia, 'Cantidad peliculas':cantidad_peliculas, 'Ganancia Total':ganancia_total, 'Promedio ganancia':ganancia_promedio}

# def peliculas_pais( Pais: str ): 
# Se ingresa un país (como están escritos en el dataset, no hay que traducirlos!), 
# retornando la cantidad de peliculas producidas en el mismo.
@app.get('/peliculas_pais/{pais}')
def peliculas_pais(pais:str):
    try:
        cant_peliculas = int(LARG_moviesdataset_reducido[LARG_moviesdataset_reducido['production_countries'] == pais]['title'].count())
    except (ValueError, SyntaxError):
        pass 
    return {'Pais':pais, 'Cantidad de peliculas que ha producido':cant_peliculas}

# def productoras_exitosas( Productora: str ): 
# Se ingresa la productora, retornando el revenue total y la cantidad de peliculas que realizo.
@app.get('/productoras_exitosas/{productora}')
def productoras_exitosas(productora:str):
    try:
        total_revenue = float(LARG_moviesdataset_reducido[LARG_moviesdataset_reducido['production_companies'] == productora]['revenue'].sum())
        cantidad_peliculas = int(LARG_moviesdataset_reducido[LARG_moviesdataset_reducido['production_companies'] == productora]['revenue'].count())
    except (ValueError, SyntaxError):
        pass 
    return {'Productora':productora, 'Total ingresos': total_revenue,'Cantidad de peliculas':cantidad_peliculas}

# df_split_job = LARG_moviesdataset_reducido['job'].str.split(',')
# df_split_crew = LARG_moviesdataset_reducido['crew'].str.split(',')
# def get_director( nombre_director ): 
# Se ingresa el nombre de un director que se encuentre dentro de un dataset 
# debiendo devolver el éxito del mismo medido a través del retorno. 
# Además, deberá devolver el nombre de cada película con la fecha de lanzamiento, 
# retorno individual, costo y ganancia de la misma, en formato lista.
# @app.get('/get_director/{director}')
# def get_director(director:str):
#     try:
#         lista = []
#         for i, valor in enumerate(df_split_job):
#             for j in range(len(valor)):
#                 if valor[j] == 'Director':
#                     if (df_split_crew[i][j] == director):
#                         lista.append([df_split_crew[i][j], 
#                                     LARG_moviesdataset_reducido['title'][i],
#                                     LARG_moviesdataset_reducido['release_date'][i],
#                                     round(LARG_moviesdataset_reducido['return'][i], 2),
#                                     LARG_moviesdataset_reducido['budget'][i],
#                                     LARG_moviesdataset_reducido['revenue'][i]])
#     except (ValueError, SyntaxError):
#         pass 
#     return lista

@app.get('/get_director/{director}')
def get_director(director:str):
    try:
        df_Director = df_movies_des[df_movies_des['crew'].str.contains(director)]   
        Peliculas_del_Director = df_Director[['title', 'release_year', 'revenue', 'budget']]
        retorno_total_director = 0
        if(Peliculas_del_Director['budget'].sum() != 0):
            retorno_total_director = (Peliculas_del_Director['revenue'].sum() / Peliculas_del_Director['budget'].sum())
        Lista_De_Dicc = Peliculas_del_Director.to_dict('records')        
    except (ValueError, SyntaxError):
        pass 
    return {'Nombre Director':director, 'Relacion de retorno':retorno_total_director, 'Peliculas Dirigidas':Lista_De_Dicc}

# Modelo de recomendacion
# Preprocesamiento de datos
# Convertir columnas relevantes en una sola columna para calcular la similitud.
# Se trabajara con los datos de las columnas: belongs_to_collection, popularity, vote_average, budget, revenue
# del LARG_moviesdataset_reducido
LARG_moviesdataset_reducido['columnas_concatenadas'] = LARG_moviesdataset_reducido['belongs_to_collection'].fillna('') + ' ' + LARG_moviesdataset_reducido['popularity'].astype(str) + ' ' + LARG_moviesdataset_reducido['vote_average'].astype(str) + ' ' + LARG_moviesdataset_reducido['budget'].astype(str) + ' ' + LARG_moviesdataset_reducido['revenue'].astype(str)
# LARG_moviesdataset_reducido_ml['columnas_concatenadas'] = LARG_moviesdataset_reducido_ml['belongs_to_collection'].fillna('') + ' ' + LARG_moviesdataset_reducido_ml['popularity'].astype(str) + ' ' + LARG_moviesdataset_reducido_ml['vote_average'].astype(str)

# Se crea un vector para realizar el calculo de similitud
count_vectorizer = CountVectorizer()
count_matrix = count_vectorizer.fit_transform(LARG_moviesdataset_reducido['columnas_concatenadas'])
cosine_sim = cosine_similarity(count_matrix)

# Se crea la Funcion para la recomendacion
@app.get('/get_recomendacion/{titulo}')
def get_recomendacion(titulo:str):
    try:
        index = LARG_moviesdataset_reducido[LARG_moviesdataset_reducido['title'] == titulo].index[0]
        similar_scores = list(enumerate(cosine_sim[index]))
        similar_scores = sorted(similar_scores, key=lambda x: x[1], reverse=True)
        similar_movies = [LARG_moviesdataset_reducido.iloc[i[0]]['title'] for i in similar_scores[1:6]]
    except (ValueError, SyntaxError):
        pass 
    return similar_movies