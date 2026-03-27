#Practica 1 - Ejercicio 1


def ordena_positivos(lista):
    # obtener los positivos
    positivos = [x for x in lista if x > 0]

    # ordenarlos
    positivos.sort()

    resultado = []
    i = 0  # índice para recorrer positivos

    for x in lista:
        if x > 0:
            resultado.append(positivos[i])
            i += 1
        else:
            resultado.append(x)

    return resultado

print(ordena_positivos([6, 3, 2, 5, -8, 2, -2]))