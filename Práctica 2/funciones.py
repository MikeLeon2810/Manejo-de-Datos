import timeit
import numpy as np
import matplotlib.pyplot as plt
import re




""""
En este programa se definen las funciones usadas en la practica 2 
de manejo de datos. Estás serán importadas y se ejecutaran en el mainp.py
"""


######################
#Busqueda binaria 
######################

def busqueda_binaria(lista, objetivo):
    left = 0
    right = len(lista) - 1

    while left <= right:
        mid = (left + right) // 2

        if lista[mid] == objetivo:
            return mid
        elif objetivo < lista[mid]:
            right = mid - 1
        else:
            left = mid + 1

    return -1

#######################
#Busqueda ternaria
#######################

def busqueda_ternaria(lista, objetivo):
    left = 0
    right = len(lista) - 1

    while left <= right:
        m1 = left + (right - left) // 3
        m2 = right - (right - left) // 3

        if lista[m1] == objetivo:
            return m1
        if lista[m2] == objetivo:
            return m2

        if objetivo < lista[m1]:
            right = m1 - 1
        elif objetivo > lista[m2]:
            left = m2 + 1
        else:
            left = m1 + 1
            right = m2 - 1

    return -1



########################
#Funcion para comparar los tiemopos de ejecucion de las busquedas y graficar
#los resultados
########################


def comparar_tiempos():
    tamaños = [10**k for k in range(2, 6)]
    tiempos_binaria = []
    tiempos_ternaria = []

    for n in tamaños:
        lista = list(range(n))
        objetivo = n - 1  # peor caso

        # repeat=5 corre 5 veces, tomamos el mínimo
        t_binaria = min(timeit.repeat(
            lambda: busqueda_binaria(lista, objetivo),
            repeat=5, number=1000
        ))
        t_ternaria = min(timeit.repeat(
            lambda: busqueda_ternaria(lista, objetivo),
            repeat=5, number=1000
        ))

        tiempos_binaria.append(t_binaria)
        tiempos_ternaria.append(t_ternaria)

    plt.plot(tamaños, tiempos_binaria, marker='o', label='Binaria')
    plt.plot(tamaños, tiempos_ternaria, marker='s', label='Ternaria')
    plt.xscale('log')  # escala logarítmica para que se vea mejor
    plt.xlabel("Tamaño de la lista")
    plt.ylabel("Tiempo (segundos)")
    plt.title("Comparación de tiempos: Binaria vs Ternaria")
    plt.legend()
    plt.show()

##################
#Algortmo Bubble Sort optimizado para detenerse si no hay untercambios
##########################

def bubble_sort_optimizado(lista):
    n = len(lista)
    
    for j in range(n - 1):
        intercambio = False
        
        for i in range(n - j - 1):
            # separar nombre del comentario
            nombre_i = lista[i].split("|")[0]
            nombre_j = lista[i+1].split("|")[0]
            
            # obtener apellido (antes de la coma)
            apellido_i = nombre_i.split(",")[0].strip().lower()
            apellido_j = nombre_j.split(",")[0].strip().lower()
            
            if apellido_i > apellido_j:
                lista[i], lista[i+1] = lista[i+1], lista[i]
                intercambio = True
        
        if not intercambio:
            break
    
    return lista



#########################################
#Algorimo Boyer-Moore 
#########################################

def boyer_moore(texto, patron):
    m = len(patron)
    n = len(texto)
    
    if m == 0:
        return 0
    
    # Tabla last: última ocurrencia de cada carácter en el patrón
    last = {}
    for j in range(m):
        last[patron[j]] = j
    
    i = m - 1  # índice en el texto
    k = m - 1  # índice en el patrón
    
    while i < n:
        if patron[k] == texto[i]:
            if k == 0:
                return i  # encontrado
            k -= 1
            i -= 1
        else:
            j = last.get(texto[i], -1)  # -1 si no está en el patrón
            i = i + m - min(k, j + 1)   # salto correcto
            k = m - 1  # reiniciar índice del patrón
    
    return -1


##############################
#Funcion para abrir el archivo txt 
##################################
def leer_archivo(nombre_archivo):
    lista = []
    
    with open(nombre_archivo, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            lista.append(linea.strip())
    
    return lista


#######################################
# Función para escribir en el archivo txt
##########################################
def escribir_archivo(nombre_archivo, lista):
    with open(nombre_archivo, "w", encoding="utf-8") as archivo:
        for linea in lista:
            archivo.write(linea + "\n")    



#########################################
# Generar reporte usando Boyer-Moore
#########################################
def generar_reporte(lista):
    implicados = set()  
    
    for linea in lista:
        partes = linea.split("|")
        
        if len(partes) < 2:
            continue
        
        nombre = partes[0].strip()
        comentario = partes[1].strip().lower()
        
        r = boyer_moore(comentario, "plagio")
        
        if r != -1:
            implicados.add(nombre)  # no permite repetidos
    
    return sorted(implicados)  



###################################################################
# Función que busca mayúsculas en el texto y pone en un diccionario
###################################################################

def buscar_mayusculas(nombre_archivo):
    resultado = {}
    
    with open(nombre_archivo, "r", encoding="utf-8") as archivo:
        lineas = archivo.readlines()
    
    for num_linea, linea in enumerate(lineas):
        col = 0
        i = 0
        while i < len(linea):
            # Saltar espacios y obtener columna real
            if linea[i] == ' ' or linea[i] == '\n':
                col += 1
                i += 1
                continue
            
            # Extraer la palabra completa
            palabra = ""
            inicio_col = col
            while i < len(linea) and linea[i] not in (' ', '\n'):
                palabra += linea[i]
                i += 1
                col += 1
            
            # Limpiar signos de puntuación al inicio y al final
            palabra_limpia = palabra.strip('.,;:!?«»¿¡()"\'-—')
            
            # Verificar si empieza con mayúscula
            if palabra_limpia and palabra_limpia[0].isupper():
                if palabra_limpia in resultado:
                    # Si ya existe, agregar la nueva posición
                    if isinstance(resultado[palabra_limpia], list):
                        resultado[palabra_limpia].append((num_linea, inicio_col))
                    else:
                        resultado[palabra_limpia] = [resultado[palabra_limpia], (num_linea, inicio_col)]
                else:
                    resultado[palabra_limpia] = (num_linea, inicio_col)
    
    return resultado


#########################
# Función para contar palabras y obtener estadísticas
#########################

def cuenta_palabras(nombre_archivo):
    with open(nombre_archivo, "r", encoding="utf-8") as archivo:
        texto = archivo.read()
    
    # Separar palabras y limpiar puntuación, convertir a minúsculas
    palabras = re.findall(r"[a-záéíóúüñ]+", texto.lower())
    
    # a) Diccionario con frecuencias
    frecuencias = {}
    for palabra in palabras:
        if palabra in frecuencias:
            frecuencias[palabra] += 1
        else:
            frecuencias[palabra] = 1
    
    # b) Palabra con mayor frecuencia
    mayor_frecuencia = max(frecuencias, key=lambda p: frecuencias[p])
    
    # c) Palabra mayor alfabéticamente
    mayor_alfabetico = min(frecuencias)
    
    # d) Palabra menor alfabéticamente
    menor_alfabetico = max(frecuencias)
    
    return frecuencias, mayor_frecuencia, mayor_alfabetico, menor_alfabetico