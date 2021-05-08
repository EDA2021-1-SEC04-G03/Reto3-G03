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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.ADT import orderedmap as om
assert cf
import datetime
import random

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos

contenttuple=("instrumentalness","liveness","speechiness","danceability","valence","loudness","tempo","acousticness","energy")

def newAnalyzer():
    """ Inicializa el analizador

    Crea una lista vacia para guardar todos los crimenes
    Se crean indices (Maps) por los siguientes criterios:
    -Fechas

    Retorna el analizador inicializado.
    """
    analyzer = {'events': None,
               'artists': None,
               'tracks': None,
               'sentiments': None,
               'hashtagsbytrack':None}

    analyzer['events'] = lt.newList('ARRAY_LIST')

    analyzer['sentiments'] = lt.newList('ARRAY_LIST')

    #hay que ordenar por track
    analyzer['hashtagsbytrack'] = mp.newMap(31000,
                                   maptype='PROBING',
                                   comparefunction=None)

    analyzer['artists'] = mp.newMap(11000,
                                   maptype='PROBING',
                                   comparefunction=None)

    analyzer['tracks'] = mp.newMap(31000,
                                   maptype='PROBING',
                                   comparefunction=None)
    
    for content in contenttuple:
        analyzer[content] = om.newMap(omaptype='RBT',
                                      comparefunction=compareFloat)
    
    return analyzer

# Funciones para agregar informacion al catalogo

def addEvent(analyzer, event):
    """
    Se adiciona un video a la lista de videos
    """
    lt.addLast(analyzer['events'], event)
    addArtist(analyzer, event['artist_id'], event)
    addTrack(analyzer, event['track_id'], event)
    for content in contenttuple:
        updateDateIndex(analyzer[content], event, content)

def addSentiment (analyzer, sentiment):
    lt.addLast(analyzer['sentiments'], sentiment)
    return

def addHashtags (analyzer, sentiment):
    addTrackbyHashtag(analyzer, sentiment['track_id'], sentiment)
    return

def addTrackbyHashtag(analyzer, track_id, event):
    """
    Esta función adiciona un video a la lista de videos de la misma categoría.
    """
    tracks = analyzer['hashtagsbytrack']
    existtrack = mp.contains(tracks, track_id)
    if existtrack:
        entry = mp.get(tracks, track_id)
        track = me.getValue(entry)
    else:
        track = newTrack(track_id)
        mp.put(tracks, track_id, track)
    lt.addLast(track['events'], event)

def addArtist(analyzer, artist_id, event):
    """
    Esta función adiciona un video a la lista de videos de la misma categoría.
    """
    artists = analyzer['artists']
    existartist = mp.contains(artists, artist_id)
    if existartist:
        entry = mp.get(artists, artist_id)
        artist = me.getValue(entry)
    else:
        artist = newArtist(artist_id)
        mp.put(artists, artist_id, artist)
    lt.addLast(artist['events'], event)

def addTrack(analyzer, track_id, event):
    """
    Esta función adiciona un video a la lista de videos de la misma categoría.
    """
    tracks = analyzer['tracks']
    existtrack = mp.contains(tracks, track_id)
    if existtrack:
        entry = mp.get(tracks, track_id)
        track = me.getValue(entry)
    else:
        track = newTrack(track_id)
        mp.put(tracks, track_id, track)
    lt.addLast(track['events'], event)

def updateDateIndex(map, event, content_name):
    """

    """
    content = float(event[content_name])
    entry = om.get(map, content)
    if entry is None:
        floatentry = newDataEntry(event)
        om.put(map, content, floatentry)
    else:
        floatentry = me.getValue(entry)
    lt.addLast(floatentry['lst'], event)
    return map

def newDataEntry(crime):
    """
    Crea una entrada en el indice por fechas, es decir en el arbol
    binario.
    """
    entry = {'lst': None}

    entry['lst'] = lt.newList('SINGLE_LINKED', compareFloat)
    return entry

# Funciones para creacion de datos

def newArtist(name):
    """
    Crea una nueva estructura para modelar los videos de un autor
    y su promedio de ratings. Se crea una lista para guardar los
    libros de dicho autor.
    """
    artist = {'name': "",
              "events": None}
    artist['name'] = name
    artist['events'] = lt.newList('ARRAY_LIST', None)
    return artist

def newTrack(name):
    """
    Crea una nueva estructura para modelar los videos de un autor
    y su promedio de ratings. Se crea una lista para guardar los
    libros de dicho autor.
    """
    track = {'name': "",
              "events": None}
    track['name'] = name
    track['events'] = lt.newList('ARRAY_LIST', None)
    return track

# Funciones de consulta

def getContentByRange(analyzer, initialDate, finalDate, content):
    """
    Retorna el numero de crimenes en un rago de fechas.
    """
    lst = om.values(analyzer[content], initialDate, finalDate)
    return lst

def getIntersectedList(cont, parametro1, parametro2, rangoInicial1, rangoFinal1, rangoInicial2, rangoFinal2):
    intersectedList = lt.newList('ARRAY_LIST')

    list1=getContentByRange(cont, rangoInicial1, rangoFinal1, parametro1)
    list2=getContentByRange(cont, rangoInicial2, rangoFinal2, parametro2)

    for lstindex in lt.iterator(list1):
        for element in lt.iterator(lstindex['lst']):
            notFound=True
            for lstindex2 in lt.iterator(list2):
                for element2 in lt.iterator(lstindex2['lst']):
                    if element==element2:
                        notFound=False
                        lt.addLast(intersectedList, element)
                        break
                if notFound==False:
                    break
    
    return intersectedList

def getNumberOfEvents(lst):
    numberElements = 0
    for lstindex in lt.iterator(lst):
        numberElements += lt.size(lstindex['lst'])
    return numberElements

def getRandomTracks(lst, number):
    randomTracks = lt.newList('ARRAY_LIST')
    for x in range(number):
        lt.addLast(randomTracks, lt.getElement(lst, random.randint(0,lt.size(lst))))
    return randomTracks

def get10TrackHashtags(cont, uniqueTracks, numberOfRandomTracks):
    uniqueTracksList = mp.keySet(uniqueTracks['tracks'])
    randomTracks = getRandomTracks(uniqueTracksList, numberOfRandomTracks)
    results=[]
    
    for track_id in lt.iterator(randomTracks):
        existtrack = mp.contains(cont['hashtagsbytrack'], track_id)
        if existtrack:
            entry = mp.get(cont['hashtagsbytrack'], track_id)
            hashtaglist = me.getValue(entry)
            hashtagTempList=[]
            for hashtag in lt.iterator(hashtaglist['events']):
                if hashtag['hashtag'].lower() not in hashtagTempList:
                    hashtagTempList.append(hashtag['hashtag'].lower())
            contador=0
            sumVader=0
            for hashtag in hashtagTempList:
                for elemento in lt.iterator(cont['sentiments']):
                    if elemento['hashtag']==hashtag and elemento['vader_avg']!='':
                        print(hashtag)
                        sumVader+=float(elemento['vader_avg'])
                        contador+=1
                        break
            if contador!=0:
                promedio=sumVader/contador
            else:
                promedio=0
            results.append([track_id,len(hashtagTempList),promedio])
        else:
            print("No existe!")
            #track = newTrack(track_id)
            #mp.put(tracks, track_id, track)
    return results

def obtainUniqueArtists(lst):
    uniqueArtists = {'artists': None}
    uniqueArtists['artists'] = mp.newMap(31000,
                                   maptype='PROBING',
                                   comparefunction=None)
    
    for lstindex in lt.iterator(lst):
        for event in lt.iterator(lstindex['lst']):
            addArtist(uniqueArtists, event['artist_id'], event)
    return artistsSize(uniqueArtists)

def obtainUniqueTracks(lst):
    uniqueTracks = {'tracks': None}
    uniqueTracks['tracks'] = mp.newMap(11000,
                                   maptype='PROBING',
                                   comparefunction=None)

    for event in lt.iterator(lst):
        addTrack(uniqueTracks, event['track_id'], event)
    return uniqueTracks

def eventsSize(analyzer):
    """
    Número de libros en el catago
    """
    return lt.size(analyzer['events'])

def artistsSize(analyzer):
    """
    Numero de autores en el catalogo
    """
    return mp.size(analyzer['artists'])

def tracksSize(analyzer):
    """
    Numero de autores en el catalogo
    """
    return mp.size(analyzer['tracks'])

def indexHeight(analyzer, content):
    """
    Altura del arbol
    """
    return om.height(analyzer[content])


def indexSize(analyzer, content):
    """
    Numero de elementos en el indice
    """
    return om.size(analyzer[content])

# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento

def compareFloat(num1, num2):
    """
    Compara dos fechas
    """
    if (num1 == num2):
        return 0
    elif (num1 > num2):
        return 1
    else:
        return -1

def compareIds(id1, id2):
    """
    Compara dos crimenes
    """
    if (i1 == i2):
        return 0
    elif i1 > i2:
        return 1
    else:
        return -1


def compareDates(date1, date2):
    """
    Compara dos fechas
    """
    if (date1 == date2):
        return 0
    elif (date1 > date2):
        return 1
    else:
        return -1


def compareOffenses(offense1, offense2):
    """
    Compara dos tipos de crimenes
    """
    offense = me.getKey(offense2)
    if (offense1 == offense):
        return 0
    elif (offense1 > offense):
        return 1
    else:
        return -1

def getArtists(lst,number):
    artistList = []
    counter = 0
    for i in lt.iterator(lst):
        artistList.append(i['lst']['first']['info']['artist_id'])
        counter+=1
        if(counter == number):
            break
    return artistList

def timeToSeconds(time):
    seconds = (float(time[0])*3600.0)+(float(time[1])*60.0)+(float(time[2]))
    return seconds

def generoPorHora(catalog,min,max,genresInfo):
    generoResults = {'total':0,'genreLists':[]}
    min = timeToSeconds(min)
    max = timeToSeconds(max)

    for genero in genresInfo:
        genreListFinal = lt.newList('ARRAY_LIST')
        tempoRange = genresInfo[genero]
        genreList = getContentByRange(catalog,tempoRange[0],tempoRange[1],'tempo')
        for lstindex in lt.iterator(genreList):
            for event in lt.iterator(lstindex['lst']):
                dateTime = event['created_at'].split()
                timeOfDay = dateTime[1].split(':')
                time_of_event = timeToSeconds(timeOfDay)
                if time_of_event>=min and time_of_event<=max:
                    lt.addLast(genreListFinal, event)
        
        generoResults['genreLists'].append([genero,genreListFinal,lt.size(genreListFinal)])
        generoResults['total']+= lt.size(genreListFinal)
    generoResults['genreLists'].sort(key=lambda x:x[2],reverse=True)
    return generoResults