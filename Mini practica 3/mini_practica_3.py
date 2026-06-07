
import numpy as np
import matplotlib.pyplot as plt
import time


# ==========================================================
# FUNCIONES DE ORDENAMIENTO
# ==========================================================

##############################################
# Bubble-sort
##############################################
def bubble_sort(lista):

    n = len(lista)

    for j in range(1, n):

        for i in range(n - j):

            if lista[i] > lista[i + 1]:

                aux = lista[i]
                lista[i] = lista[i + 1]
                lista[i + 1] = aux

    return lista


##############################################
#  Insertion-sort
##############################################
def insertion_sort(lista):

    n = len(lista)

    for i in range(1, n):

        j = i

        while j > 0:

            if lista[j - 1] > lista[j]:

                lista[j - 1], lista[j] = lista[j], lista[j - 1]

            else:
                break

            j = j - 1

    return lista


##############################################
# Función auxiliar Quick-sort
##############################################
def acomoda_pivote(lista, izq, der):

    pivote = izq

    while der > izq:

        if pivote == izq:

            if lista[pivote] < lista[der]:

                der -= 1

            else:

                lista[pivote], lista[der] = lista[der], lista[pivote]

                pivote = der

                izq += 1

        elif pivote == der:

            if lista[pivote] > lista[izq]:

                izq += 1

            else:

                lista[pivote], lista[izq] = lista[izq], lista[pivote]

                pivote = izq

                der -= 1

    return pivote


##############################################
# Algoritmo Quick-sort
##############################################
def quick_sort(lista, izq, der):

    if izq >= der:
        return

    piv = acomoda_pivote(lista, izq, der)

    quick_sort(lista, izq, piv - 1)

    quick_sort(lista, piv + 1, der)


##############################################
# Función auxiliar Merge-sort
##############################################
def mezclar(l1, l2):

    i = 0
    j = 0

    r = []

    while i <= len(l1) - 1 and j <= len(l2) - 1:

        if l1[i] <= l2[j]:

            r.append(l1[i])

            i += 1

        else:

            r.append(l2[j])

            j += 1

    if i == len(l1):

        r.extend(l2[j:])

    elif j == len(l2):

        r.extend(l1[i:])

    return r


##############################################
# Algoritmo Merge-sort
##############################################
def merge_sort(lista):

    n = len(lista)

    if n <= 1:

        return lista

    else:

        m = n // 2

        l1 = lista[0:m]

        l2 = lista[m:]

        return mezclar(
            merge_sort(l1),
            merge_sort(l2)
        )


# ==========================================================
# FUNCIONES AUXILIARES
# ==========================================================

##############################################
# Leer archivo de enteros
##############################################
def leer_archivo_enteros(nombre_archivo):

    datos = []

    with open(nombre_archivo, "r") as archivo:

        for linea in archivo:

            linea = linea.strip()

            if linea != "":

                numeros = list(
                    map(int, linea.split(","))
                )

                datos.append(numeros)

    return datos


##############################################
# Medir tiempo de ejecución
##############################################
def medir_tiempo(funcion, lista):

    copia = lista.copy()

    inicio = time.perf_counter()

    funcion(copia)

    fin = time.perf_counter()

    return fin - inicio


##############################################
# Medir tiempo Quick-sort
##############################################
def medir_tiempo_quick(lista):

    copia = lista.copy()

    inicio = time.perf_counter()

    quick_sort(copia, 0, len(copia) - 1)

    fin = time.perf_counter()

    return fin - inicio


# ==========================================================
# EJERCICIO 1
# ==========================================================

def ejercicio_1(nombre_archivo):

    datos = leer_archivo_enteros(nombre_archivo)

    tamanios = []

    tiempos_bubble = []
    tiempos_insertion = []
    tiempos_quick = []
    tiempos_merge = []

    for lista in datos:

        tamanios.append(len(lista))

        # Bubble-sort
        tiempo = medir_tiempo(
            bubble_sort,
            lista
        )

        tiempos_bubble.append(tiempo)

        # Insertion-sort
        tiempo = medir_tiempo(
            insertion_sort,
            lista
        )

        tiempos_insertion.append(tiempo)

        # Quick-sort
        tiempo = medir_tiempo_quick(lista)

        tiempos_quick.append(tiempo)

        # Merge-sort
        inicio = time.perf_counter()

        merge_sort(lista.copy())

        fin = time.perf_counter()

        tiempos_merge.append(fin - inicio)

    # ------------------------------------------------------
    # Graficar resultados
    # ------------------------------------------------------

    plt.figure(figsize=(10, 6))

    plt.plot(
        tamanios,
        tiempos_bubble,
        marker="o",
        label="Bubble Sort"
    )

    plt.plot(
        tamanios,
        tiempos_insertion,
        marker="o",
        label="Insertion Sort"
    )

    plt.plot(
        tamanios,
        tiempos_quick,
        marker="o",
        label="Quick Sort"
    )

    plt.plot(
        tamanios,
        tiempos_merge,
        marker="o",
        label="Merge Sort"
    )

    plt.title(
        "Comparación de algoritmos de ordenamiento"
    )

    plt.xlabel("Tamaño de entrada")
    plt.ylabel("Tiempo de ejecución")
    plt.grid()
    plt.legend()
    plt.show()


# ==========================================================
# EJERCICIO 2
# ==========================================================

def ejercicio_2(nombre_archivo):

    locaciones = [
        "RPT", "VAL", "ROS", "KIL",
        "SHA", "BIR", "DUB", "CLA",
        "MUL", "CLO", "BEL", "MAL"
    ]

    # ------------------------------------------------------
    # Leer archivo
    # ------------------------------------------------------

    datos = np.loadtxt(nombre_archivo)

    velocidades = datos[:, 3:]

    # ------------------------------------------------------
    # a) Graficar series
    # ------------------------------------------------------

    plt.figure(figsize=(12, 6))

    for i in range(12):

        plt.plot(
            velocidades[:, i],
            label=locaciones[i]
        )

    plt.title(
        "Velocidades de viento por locación"
    )

    plt.xlabel("Observación")
    plt.ylabel("Velocidad")
    plt.legend()
    plt.grid()
    plt.show()

    # ------------------------------------------------------
    # b) Estadísticas generales
    # ------------------------------------------------------

    maximo = np.max(velocidades)

    minimo = np.min(velocidades)

    promedio = np.mean(velocidades)

    desviacion = np.std(velocidades)

    print("\n===================================")
    print(" ESTADÍSTICAS GENERALES ")
    print("===================================")

    print(f"Máximo: {maximo}")

    print(f"Mínimo: {minimo}")

    print(f"Promedio: {promedio}")

    print(f"Desviación estándar: {desviacion}")

    # ------------------------------------------------------
    # c) Estadísticas por locación
    # ------------------------------------------------------

    maximos = np.max(velocidades, axis=0)

    minimos = np.min(velocidades, axis=0)

    promedios = np.mean(velocidades, axis=0)

    desviaciones = np.std(velocidades, axis=0)

    x = np.arange(len(locaciones))

    ancho = 0.2

    plt.figure(figsize=(14, 6))

    plt.bar(
        x - 1.5 * ancho,
        maximos,
        width=ancho,
        label="Máximo"
    )

    plt.bar(
        x - 0.5 * ancho,
        minimos,
        width=ancho,
        label="Mínimo"
    )

    plt.bar(
        x + 0.5 * ancho,
        promedios,
        width=ancho,
        label="Promedio"
    )

    plt.bar(
        x + 1.5 * ancho,
        desviaciones,
        width=ancho,
        label="Desv. Est."
    )

    plt.xticks(x, locaciones)

    plt.title(
        "Estadísticas por locación"
    )

    plt.xlabel("Locación")

    plt.ylabel("Velocidad")

    plt.legend()

    plt.grid()

    plt.show()


# ==========================================================
# EJERCICIO 3
# ==========================================================

def ejercicio_3(
    monto_inicial,
    retorno_anual,
    volatilidad,
    tiempo,
    simulaciones=100
):

    # ------------------------------------------------------
    # Generar retornos aleatorios
    # ------------------------------------------------------

    retornos = np.random.normal(
        retorno_anual,
        volatilidad,
        (tiempo, simulaciones)
    )

    # ------------------------------------------------------
    # Crear matriz de escenarios
    # ------------------------------------------------------

    escenarios = np.zeros(
        (tiempo + 1, simulaciones)
    )

    escenarios[0] = monto_inicial

    # ------------------------------------------------------
    # Simular inversión
    # ------------------------------------------------------

    for i in range(1, tiempo + 1):

        escenarios[i] = (
            escenarios[i - 1]
            * (1 + retornos[i - 1])
        )

    # ------------------------------------------------------
    # Mejor y peor escenario
    # ------------------------------------------------------

    finales = escenarios[-1]

    mejor = np.argmax(finales)

    peor = np.argmin(finales)

    # ------------------------------------------------------
    # Graficar escenarios
    # ------------------------------------------------------

    plt.figure(figsize=(12, 6))

    for i in range(simulaciones):

        if i == mejor:

            plt.plot(
                escenarios[:, i],
                linewidth=3,
                label="Mejor escenario"
            )

        elif i == peor:

            plt.plot(
                escenarios[:, i],
                linewidth=3,
                label="Peor escenario"
            )

        else:

            plt.plot(
                escenarios[:, i],
                alpha=0.4
            )

    plt.title(
        "Simulación de portafolio de inversión"
    )

    plt.xlabel("Años")

    plt.ylabel("Monto")

    plt.grid()

    plt.legend()

    plt.show()


# ==========================================================
# MAIN
# ==========================================================

def main():



    # ------------------------------------------------------
    # EJERCICIO 1
    # ------------------------------------------------------

    print("\nEjecutando ejercicio 1...")

    ejercicio_1("datos.txt")

    # ------------------------------------------------------
    # EJERCICIO 2
    # ------------------------------------------------------

    print("\nEjecutando ejercicio 2...")

    ejercicio_2("wind.data")

    # ------------------------------------------------------
    # EJERCICIO 3
    # ------------------------------------------------------

    print("\nEjecutando ejercicio 3...")

    ejercicio_3(
        monto_inicial=50000,
        retorno_anual=0.08,
        volatilidad=0.15,
        tiempo=20
    )


# ==========================================================
# EJECUCIÓN PRINCIPAL
# ==========================================================

if __name__ == "__main__":

    main()