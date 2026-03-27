import time
import numpy as np
import matplotlib.pyplot as plt




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
    tamaños = [10**k for k in range(2, 6)]  # 100, 1000, 10000, 100000
    tiempos_binaria = []
    tiempos_ternaria = []

    for n in tamaños:
        lista = list(range(n))
        objetivo = n - 1  # peor caso

        # ---- Binaria ----
        inicio = time.time()
        for _ in range(1000):  # repetir para medir mejor
            busqueda_binaria(lista, objetivo)
        fin = time.time()
        tiempos_binaria.append(fin - inicio)

        # ---- Ternaria ----
        inicio = time.time()
        for _ in range(1000):
            busqueda_ternaria(lista, objetivo)
        fin = time.time()
        tiempos_ternaria.append(fin - inicio)

    # ---- Gráfica ----
    plt.plot(tamaños, tiempos_binaria, marker='o', label='Binaria')
    plt.plot(tamaños, tiempos_ternaria, marker='s', label='Ternaria')
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
        intercambio = False  # bandera
        
        for i in range(n - j - 1):
            # comparar por apellido (última palabra)
            apellido_i = lista[i].split()[-1].lower()
            apellido_j = lista[i+1].split()[-1].lower()
            
            if apellido_i > apellido_j:
                lista[i], lista[i+1] = lista[i+1], lista[i]
                intercambio = True
        
        if not intercambio:
            break  # ya está ordenado
    
    return lista




######################################################
# Función patrón para buscar una paralabra en un texto
#######################################################


def patron_fb(texto, patron):
    m = len(patron)
    n = len(texto)
    for i in range(n-(m-1)):
        for j in range(m):
            if patron[j] == texto[i+j]:
                if j == m-1:
                    return i
                else:
                    continue
            else:
                break
    return -1




#########################################
#Algorimo Boyer-Moore 
#########################################


def boyer_moore(texto, patron):
    m = len(patron)
    n = len(texto)
    last = {}
    for j in range(m):
        last[patron[j]]=j
    k = m-1
    i = m-1
    while(i<n):
        if patron[k] == texto[i]:
            if(k == 0):
                return i
            k -= 1
            i -= 1
        else:
            if texto[i] in patron:
                j = last[texto[i]]
                if j > k:
                    i = i + (m-k)
                else:
                    i = i + (m - j+1)
            else:
                i = i + k
            k = m-1