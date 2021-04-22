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
songFile = 'subsamples-small/context_content_features-small.csv'
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
        controller.loadData(cont,songFile)
        print(type(cont))
        print(cont.keys())
        print(lt.size(cont['songs']))
        print(om.size(cont['instrumentalness']))

    elif int(inputs[0]) == 2:
        #req 1
        pass

    elif int(inputs[0]) == 3:
        #Req 2
        pass
    
    elif int(inputs[0]) == 4:
        #req 3
        pass

    elif int(inputs[0]) == 5:
        #req 4
        pass

    elif int(inputs[0]) == 6:
        #req 5
        pass

    elif int(inputs[0]) == 0:
        running = False
        print("Adios!")
sys.exit(0)
