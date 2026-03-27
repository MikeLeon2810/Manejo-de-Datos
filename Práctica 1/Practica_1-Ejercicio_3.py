#Practica_1-Ejercicio_3
def merge_sort(lista, inicio=0, fin=None):
    if fin is None:
        fin = len(lista) - 1

    if inicio >= fin:
        return

    medio = (inicio + fin) // 2

    merge_sort(lista, inicio, medio)
    merge_sort(lista, medio + 1, fin)

    i = inicio
    j = medio + 1

    while i <= medio and j <= fin:
        if lista[i] <= lista[j]:
            i += 1
        else:
            temp = lista[j]
            k = j
            while k > i:
                lista[k] = lista[k-1]
                k -= 1
            lista[i] = temp

            i += 1
            medio += 1
            j += 1

lista = [5,-99,-21, 0,18000,-710, 2, 65, 10,3]
merge_sort(lista)
print(lista)           