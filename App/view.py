"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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

import config as cf
import sys
import controller
from DISClib.ADT import list as lt
from DISClib.ADT import orderedmap as om
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("")
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Caracterizar las reproducciones")
    print("3- Encontrar música para festejar")
    print('4- Encontrar música para estudiar')
    print('5- Estudiar los géneros musicales')
    print('6- Indicar el género musical más escuchado en el tiempo')
    print("0- Salir")
    print('-------------------------------------')

catalog = None
genres={
    "reggae":(60,90),
    "down-tempo":(70,100),
    "chill-out":(90,120),
    "hip-hop":(85,115),
    "jazz and funk":(120,125),
    "pop":(100,130),
    "r&b":(60,80),
    "rock":(110,140),
    "metal":(100,160)
}

"""
Menu principal
"""
running = True
while running:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("Cargando información de los archivos ....")
        cont = controller.init()
        controller.loadData(cont)
        print('Eventos cargados: ' + str(controller.eventsSize(cont)))
        print('Artistas únicos cargados: ' + str(controller.artistsSize(cont)))
        print('Pistas de audio únicas cargados: ' + str(controller.tracksSize(cont)))

        for pos in (0,1,2,3,4):
            dicc=lt.getElement(cont['events'],pos)
            print("\nPosición:",pos)
            for key in dicc:
                print(key+": "+dicc[key], end=", ")
            print("")
        
        size=lt.size(cont['events'])

        for pos in (4,3,2,1,0):
            dicc=lt.getElement(cont['events'],size-pos)
            print("\nPosición:",size-pos)
            for key in dicc:
                print(key+": "+dicc[key], end=", ")
            print("")

    elif int(inputs[0]) == 2:
        #req 1
        print("\nBuscando eventos basados en una caracteristica de contenido en un rango determinado: ")
        rangoInicial = float(input("Rango inicial: "))
        rangoFinal = float(input("Rango final: "))
        content=input("Contenido a buscar: ").lower()

        list = controller.getContentByRange(cont, rangoInicial, rangoFinal, content)
        total = controller.getNumberOfEvents(list)
        artists = controller.obtainUniqueArtists(list)

        print("\nEl total de eventos en el rango es de: " + str(total))
        print("El total de artistas unicos en el rango es de: " + str(artists))

    elif int(inputs[0]) == 3:
        #Req 2
        print("\nEncontrando pistas que pueden utilizarse en una fiesta: ")
        rangoInicial1 = float(input("Rango inicial energy: "))
        rangoFinal1 = float(input("Rango final energy: "))
        rangoInicial2 = float(input("Rango inicial danceability: "))
        rangoFinal2 = float(input("Rango final danceability: "))

        print("\nBuscando...\n")

        list = controller.getIntersectedList(cont,'energy','danceability',rangoInicial1,rangoFinal1,rangoInicial2,rangoFinal2)
        tracks = controller.obtainUniqueTracks(list)
        randomTracks = controller.getRandomTracks(list,5)

        print("El total de pistas unicas en los eventos es de: " + str(controller.tracksSize(tracks)))

        print("Algunas pistas aleatorias:")
        for track in lt.iterator(randomTracks):
            print("{} con energy de {} y danceability de {}".format(track["track_id"],track["energy"],track["danceability"]))

    
    elif int(inputs[0]) == 4:
        #req 3
        print("\nEncontrando pistas que pueden utilizarse en periodos de estudio: ")
        rangoInicial1 = float(input("Rango inicial instrumentalness: "))
        rangoFinal1 = float(input("Rango final instrumentalness: "))
        rangoInicial2 = float(input("Rango inicial tempo: "))
        rangoFinal2 = float(input("Rango final tempo: "))

        print("\nBuscando...\n")

        list = controller.getIntersectedList(cont,'instrumentalness','tempo',rangoInicial1,rangoFinal1,rangoInicial2,rangoFinal2)
        tracks = controller.obtainUniqueTracks(list)
        randomTracks = controller.getRandomTracks(list,5)

        print("El total de pistas unicas en los eventos es de: " + str(controller.tracksSize(tracks)))

        print("Algunas pistas aleatorias:")
        for track in lt.iterator(randomTracks):
            print("{} con instrumentalness de {} y tempo de {}".format(track["track_id"],track["instrumentalness"],track["tempo"]))

    elif int(inputs[0]) == 5:
        #req 4
        print("Buscando canciones y artistas por género:")
        generos = input("Indique los generos que quiere buscar:").split(",")

        for genero in generos:
            if genero.lower() not in genres:
                print("\nEncontramos un nuevo genero, {}, por favor indique:".format(genero))
                rangoInicial = float(input("Valor mínimo del Tempo del nuevo género musical: "))
                rangoFinal = float(input("Valor máximo del Tempo del nuevo género musical: "))
                genres[genero.lower()]=(rangoInicial,rangoFinal)
        
        #falta buscar por tempo e imprimir en pantalla
        #los filtros para buscar por valor unico se usan en los req 2 y 3

    elif int(inputs[0]) == 6:
        #req 5
        pass

    elif int(inputs[0]) == 0:
        running = False
        print("Adios!")
sys.exit(0)
