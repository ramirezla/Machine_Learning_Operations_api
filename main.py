# Estudiante: Luis A, Ramirez G.<br>
# GitHub: ramirezla<br>
# Email: ramirezluisalberto@hotmail.com<br>
# Email: ramirezgluisalberto@gmail.com<br>

import pandas as pd
from wordcloud import WordCloud

from fastapi import FastAPI
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

# ruta_archivo_movies = "./Datasets/LARG_moviesdataset_reducido_ml_sample_50.csv"
# ruta_archivo_movies = "./Datasets/LARG_moviesdataset_reducido.csv"
ruta_archivo_movies = "./Datasets/LARG_moviesdtaset_full.csv"

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
    return {'Idioma':idioma, 'Cantidad de peliculas': cant_peliculas}

# def peliculas_duracion( Pelicula: str ): 
# Se ingresa una pelicula. Debe devolver la duracion y el año.
@app.get('/pelicula_duracion_anno/{pelicula}')
def pelicula_duracion_anno(pelicula: str):
    try:
        duracion_min = int(LARG_moviesdataset_reducido[LARG_moviesdataset_reducido['title'] == pelicula]['runtime'])
        anno = int(LARG_moviesdataset_reducido[LARG_moviesdataset_reducido['title'] == pelicula]['release_year'])   # Se cambia el tipo de dato a int para que Json no tenga problemas con el tipo int64
    except (ValueError, SyntaxError):
        pass 
    return {'Pelicula':pelicula, 'Duracion en minutos':duracion_min, 'Año de estreno':anno}

# def franquicia( Franquicia: str): 
# Se ingresa la franquicia, retornando la cantidad de peliculas, ganancia total y promedio.
@app.get('/franquicia_cant_gana_prom_peliculas/{franquicia}')
def franquicia_cant_gana_prom_peliculas(franquicia:str):
    try:
        cantidad_peliculas = int(LARG_moviesdataset_reducido[LARG_moviesdataset_reducido['belongs_to_collection'] == franquicia]['title'].count())
        ganancia_total = round(float(LARG_moviesdataset_reducido[LARG_moviesdataset_reducido['belongs_to_collection'] == franquicia]['revenue'].sum()),2)
        ganancia_promedio = 0
        if cantidad_peliculas != 0:
            ganancia_promedio = round(float(ganancia_total/cantidad_peliculas),2)
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
@app.get('/get_director/{director}')
def get_director(director:str):
    try:
        df_Director = LARG_moviesdataset_reducido[LARG_moviesdataset_reducido['crew'].str.contains(director)]   
        Peliculas_del_Director = df_Director[['title', 'release_year', 'revenue', 'budget']]
        retorno_total_director = 0
        if(Peliculas_del_Director['budget'].sum() != 0):
            retorno_total_director = (Peliculas_del_Director['revenue'].sum() / Peliculas_del_Director['budget'].sum())
        Lista_De_Dicc = Peliculas_del_Director.to_numpy().tolist()       
    except (ValueError, SyntaxError):
        pass 
    return {'Nombre Director':director, 'Relacion de retorno':retorno_total_director, 'Pelicula, Año, Ingreso, Presupuesto':Lista_De_Dicc}

# Modelo de recomendacion
# Preprocesamiento de datos
# Convertir columnas relevantes en una sola columna para calcular la similitud.

# Se trabajara con los datos de las columnas: belongs_to_collection, popularity, vote_average, budget, revenue
# del LARG_moviesdataset_reducido
# LARG_moviesdataset_reducido['columnas_concatenadas'] = LARG_moviesdataset_reducido['belongs_to_collection'].fillna('') + ' ' + LARG_moviesdataset_reducido['popularity'].astype(str) + ' ' + LARG_moviesdataset_reducido['vote_average'].astype(str) + ' ' + LARG_moviesdataset_reducido['budget'].astype(str) + ' ' + LARG_moviesdataset_reducido['revenue'].astype(str)

# Se trabajara con los datos de las columnas: belongs_to_collection, popularity, genres, cast, vote_count
# del LARG_moviesdataset_reducido
# LARG_moviesdataset_reducido['columnas_concatenadas'] = LARG_moviesdataset_reducido['popularity'].astype(str) + ' ' + LARG_moviesdataset_reducido['genres'].astype(str) + ' ' + LARG_moviesdataset_reducido['cast'].astype(str) + ' ' + LARG_moviesdataset_reducido['vote_count'].astype(str)

@app.get('/get_recomendacion/{titulo}')
def get_recomendacion(pelicula:str):
    # Crear un objeto CountVectorizer para convertir las características en vectores
    vectorizer = CountVectorizer(analyzer='word', lowercase=True, token_pattern=r'\w+')

    # Concatena todas las caracteristicas que deseo evaluar
    cadena_todas_caracteristicas = LARG_moviesdataset_reducido['genres'].fillna('') + ' ' + LARG_moviesdataset_reducido['crew'].astype(str) + ' ' + LARG_moviesdataset_reducido['cast'].astype(str) + ' ' + LARG_moviesdataset_reducido['release_year'].astype(str)
    # Obtener la matriz de documentos término-frecuencia (DTM) a partir de las características
    matrix_todas_caracteristicas = vectorizer.fit_transform(cadena_todas_caracteristicas)

    # Obtener las características de la película que le gustó al usuario
    cadena_pelicula_caracteristicas = LARG_moviesdataset_reducido.loc[LARG_moviesdataset_reducido['title'] == pelicula, 'genres'].iloc[0] + ' ' + LARG_moviesdataset_reducido.loc[LARG_moviesdataset_reducido['title'] == pelicula, 'crew'].iloc[0] + ' ' + LARG_moviesdataset_reducido.loc[LARG_moviesdataset_reducido['title'] == pelicula, 'cast'].iloc[0] + ' ' + LARG_moviesdataset_reducido.loc[LARG_moviesdataset_reducido['title'] == pelicula, 'release_year'].iloc[0].astype(str)
    # Obtener la matriz de documentos término-frecuencia (DTM) a partir de las características
    matrix_pelicula_caracteristica = vectorizer.transform([cadena_pelicula_caracteristicas])

    # Calcular la similitud del coseno entre la película que le gustó al usuario y todas las demás películas
    similitudes = cosine_similarity(matrix_pelicula_caracteristica, matrix_todas_caracteristicas)

    # Obtener los índices de las películas más similares
    similitudes_indices = similitudes.argsort()[0][-6:-1]

    # Obtener los títulos de las películas más similares
    similitudes_peliculas = LARG_moviesdataset_reducido.loc[similitudes_indices, 'title'].tolist()

    return similitudes_peliculas    