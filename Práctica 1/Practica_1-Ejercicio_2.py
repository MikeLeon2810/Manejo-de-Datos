#Pratica 1 - Ejercicio 2
def selection_sort(lista):
    n = len(lista)

    for i in range(n):
        min_index = i

        for j in range(i + 1, n):
            if lista[j] < lista[min_index]:
                min_index = j

        lista[i], lista[min_index] = lista[min_index], lista[i]

    return lista

print(selection_sort([5,0, 2, 65, 10,-65,-1, 21]))