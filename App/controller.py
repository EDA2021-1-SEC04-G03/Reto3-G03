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
    crimesfile = cf.data_dir + 'context_content_features/context_content_features-small.csv'
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
    hastagsfile = cf.data_dir + 'user_track_hashtag_timestamp/user_track_hashtag_timestamp-small.csv'
    input_file = csv.DictReader(open(hastagsfile, encoding="utf-8"),
                                delimiter=",")
    for hashtag in input_file:
        #model.addHashtags(analyzer, hashtag)
        pass
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

    
