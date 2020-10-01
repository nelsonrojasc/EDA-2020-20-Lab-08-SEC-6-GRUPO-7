"""
 * Copyright 2020, Departamento de sistemas y Computación
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
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
from App import model
from DISClib.DataStructures import listiterator as it
import datetime
import csv

# from DISClib.ADT import orderedmap as om
# from DISClib.ADT import map as m
"""
El controlador se encarga de mediar entre la vista y el modelo.
Existen algunas operaciones en las que se necesita invocar
el modelo varias veces o integrar varias de las respuestas
del modelo en una sola respuesta.  Esta responsabilidad
recae sobre el controlador.
"""

# ___________________________________________________
#  Inicializacion del catalogo
# ___________________________________________________

def greaterFunction(el1,el2):
    if el1 > el2:
        return 1
    elif el1 < el2:
        return -1
    return 0 

def init(accidentsfile):
    """
    Llama la funcion de inicializacion del modelo.
    """
    analyzer = {'dateTree': model.newTree(greaterFunction),
                'locationTree': model.newTree(greaterFunction),
                'rawAccidents': loadData(accidentsfile)}
    return analyzer


# ___________________________________________________
#  Funciones para la carga de datos y almacenamiento
#  de datos en los modelos
# ___________________________________________________

def loadData(accidentsfile):
    """
    Carga los datos de los archivos CSV en el modelo
    """
    lst = model.newList(cmpfunction=greaterFunction)
    with open(cf.data_dir + accidentsfile,encoding="utf-8") as csvfile:
        accident_data = csv.DictReader(csvfile,delimiter=',')
        # print(accident_data.)
        i=1
        p=1
        for accident in accident_data:
            if i%8787 == 0:
            # if i%29743 == 0:
                print(" " + str(p) + "%" + " completado",end='\r')
                p+=1
            # print(i,end='\r')
            model.addListAccident(lst,accident)
            i+=1
    print (" 100%" +" completado\n")
    return lst


def fillDataTree(analyzer):
    iterator = it.newIterator(analyzer['rawAccidents'])
    dates = {}
    i = 1
    while it.hasNext(iterator):
        accident = it.next(iterator)
        if accident['Start_Time'][:10] not in dates:
            dates[accident['Start_Time'][:10]] = [accident]
        else:
            dates[accident['Start_Time'][:10]].append(accident)
    
    print("Creando y organizando un árbol...")
    i=0
    p=1
    for date in dates:
        model.addTreeNode(analyzer['dateTree'],date,dates[date])
    print (" 100%" +" completado\n")
# ___________________________________________________
#  Funciones para consultas
# ___________________________________________________

def getAccident(tree,key):
    return model.getTreeKey(tree,key)['value']

def getAllDates(tree):
    return model.getTreeAllKeys(tree)

def filterSeverityIndividual(tree,date):
    result = getAccident(tree,date)
    severity = {"1":0,
                "2":0,
                "3":0,
                "4":0}
    for accident in result:
        severity[accident['Severity']] += 1
    return severity
