# Estudiante: Luis A, Ramirez G.<br>
# GitHub: ramirezla<br>
# Email: ramirezluisalberto@hotmail.com<br>
# Email: ramirezgluisalberto@gmail.com<br>

# Versiones paquetes utilizados: <br>
# OS: Linux x64 3.10.0-1160.92.1.el7.x8_64<br>
# Visual Studio Code 1.80.1<br>
# Python 3.6.8<br>
# fastapi             0.83.0
# pip                 21.3.1
# matplotlib          3.3.4
# numpy               1.19.5
# pandas              1.1.5
# pip                 21.3.1
# seaborn             0.11.2
# sklearn             0.0.post1
# uvicorn             0.16.0

import pandas as pd
import numpy as np
import ast
import math

import matplotlib.pyplot as plt
import seaborn as sns

from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

# Se importa el archivo 'LARG_moviesdataset_reducido.csv' con los datos de las peliculas,
# este archivo ya contiene la data limpiada.
ruta_archivo_movies = "./Datasets/LARG_moviesdataset_reducido.csv"
LARG_moviesdataset_reducido = pd.read_csv(ruta_archivo_movies)

# Se instancia una variable de tipo FastAPI
app = FastAPI()

# def peliculas_idioma( Idioma: str ): 
# Se ingresa un idioma (como están escritos en el dataset, no hay que traducirlos!). 
# Debe devolver la cantidad de películas producidas en ese idioma.
df_split_job = LARG_moviesdataset_reducido['job'].str.split(',')
df_split_crew = LARG_moviesdataset_reducido['crew'].str.split(',')
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

# def get_director( nombre_director ): 
# Se ingresa el nombre de un director que se encuentre dentro de un dataset 
# debiendo devolver el éxito del mismo medido a través del retorno. 
# Además, deberá devolver el nombre de cada película con la fecha de lanzamiento, 
# retorno individual, costo y ganancia de la misma, en formato lista.
@app.get('/get_director/{director}')
def get_director(director:str):
    try:
        lista = []
        for i, valor in enumerate(df_split_job):
            for j in range(len(valor)):
                if valor[j] == 'Director':
                    if (df_split_crew[i][j] == director):
                        lista.append([df_split_crew[i][j], 
                                    LARG_moviesdataset_reducido['title'][i],
                                    LARG_moviesdataset_reducido['release_date'][i],
                                    round(LARG_moviesdataset_reducido['return'][i], 2),
                                    LARG_moviesdataset_reducido['budget'][i],
                                    LARG_moviesdataset_reducido['revenue'][i]])
    except (ValueError, SyntaxError):
        pass 
    return lista