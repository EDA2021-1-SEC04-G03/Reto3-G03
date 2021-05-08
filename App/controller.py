"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

from DISClib.ADT.list import size
import config as cf
import model
import csv
import time
import tracemalloc

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros

def init():
    """
    Llama la funcion de inicializacion  del modelo.
    """
    # catalog es utilizado para interactuar con el modelo
    analyzer = model.newAnalyzer()
    return analyzer

# Funciones para la carga de datos

def loadData(analyzer):
    """
    Carga los datos de los archivos CSV en el modelo
    """

    loadEvents(analyzer)
    loadHashtags(analyzer)
    loadSentiments(analyzer)
    return

def loadEvents(analyzer):
    crimesfile = cf.data_dir + 'context_content_features/context_content_features-80pct.csv'
    input_file = csv.DictReader(open(crimesfile, encoding="utf-8"),
                                delimiter=",")
    for crime in input_file:
        model.addEvent(analyzer, crime)
    return analyzer

def loadSentiments(analyzer):
    sentimentsfile = cf.data_dir + 'sentiment_values.csv'
    input_file = csv.DictReader(open(sentimentsfile, encoding="utf-8"),
                                delimiter=",")
    for sentiment in input_file:
        model.addSentiment(analyzer, sentiment)
    return analyzer

def loadHashtags(analyzer):
    hastagsfile = cf.data_dir + 'user_track_hashtag_timestamp/user_track_hashtag_timestamp-80pct.csv'
    input_file = csv.DictReader(open(hastagsfile, encoding="utf-8"),
                                delimiter=",")
    for hashtag in input_file:
        model.addHashtags(analyzer, hashtag)
    return analyzer

# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo

def getContentByRange(analyzer, initialDate, finalDate, content):
    """
    Retorna el total de crimenes en un rango de fechas
    """
    return model.getContentByRange(analyzer, initialDate,
                                  finalDate, content)

def getIntersectedList(cont, parametro1, parametro2, rangoInicial1, rangoFinal1, rangoInicial2, rangoFinal2):
    return model.getIntersectedList(cont, parametro1, parametro2, rangoInicial1, rangoFinal1, rangoInicial2, rangoFinal2)

def getNumberOfEvents(lst):
    """
    Retorna el total de crimenes en un rango de fechas
    """
    return model.getNumberOfEvents(lst)

def getTrackHashtags(cont, uniqueTracks, numberOfRandomTracks):
    return model.get10TrackHashtags(cont, uniqueTracks, numberOfRandomTracks)

def getRandomTracks(lst, number):
    return model.getRandomTracks(lst, number)

def obtainUniqueArtists(lst):
    return model.obtainUniqueArtists(lst)

def obtainUniqueTracks(lst):
    return model.obtainUniqueTracks(lst)

def indexHeight(analyzer, content):
    """
    Altura del indice (arbol)
    """
    return model.indexHeight(analyzer, content)


def indexSize(analyzer, content):
    """
    Numero de nodos en el arbol
    """
    return model.indexSize(analyzer, content)

def eventsSize(catalog):
    """
    Numero de libros cargados al catalogo
    """
    return model.eventsSize(catalog)

def artistsSize(catalog):
    """
    Numero de autores cargados al catalogo
    """
    return model.artistsSize(catalog)

def tracksSize(catalog):
    """
    Numero de autores cargados al catalogo
    """
    return model.tracksSize(catalog)

def genres_search(catalog, generosList, genresInfo,artistsBool):
    '''
    Buscar por generos
    '''
    generoResults = {'total':0}

    for genero in generosList:
        tempoRange = genresInfo[genero]
        genreList = model.getContentByRange(catalog,tempoRange[0],tempoRange[1],'tempo')
        generoResults[genero] = {'listens':model.getNumberOfEvents(genreList),'artists':model.obtainUniqueArtists(genreList)}
        if artistsBool == True:
            generoResults[genero]['10arts'] = model.getArtists(genreList,10)
        generoResults['total'] += generoResults[genero]['listens']
    
    return generoResults

def generoPorHora(catalog,min,max,genresInfo):
    return model.generoPorHora(catalog,min,max,genresInfo)


# ======================================
# Funciones para medir tiempo y memoria
# ======================================

def getTime():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def getMemory():
    """
    toma una muestra de la memoria alocada en instante de tiempo
    """
    return tracemalloc.take_snapshot()


def deltaMemory(start_memory, stop_memory):
    """
    calcula la diferencia en memoria alocada del programa entre dos
    instantes de tiempo y devuelve el resultado en bytes (ej.: 2100.0 B)
    """
    memory_diff = stop_memory.compare_to(start_memory, "filename")
    delta_memory = 0.0

    # suma de las diferencias en uso de memoria
    for stat in memory_diff:
        delta_memory = delta_memory + stat.size_diff
    # de Byte -> kByte
    delta_memory = delta_memory/1024.0
    return delta_memory

def initiateCalculation():
    delta_time = -1.0
    delta_memory = -1.0

    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()
    return start_time, start_memory

def finishCalculation(start_time, start_memory):
    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)
    return delta_time, delta_memory