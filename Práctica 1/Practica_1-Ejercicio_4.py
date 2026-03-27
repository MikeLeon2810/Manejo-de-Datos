def posibles_combinaciones(lista, r, inicio=0, comb=None):
    if comb is None:
        comb = []

    if len(comb) == r:
        print(comb)
        return

    for i in range(inicio, len(lista)):
        comb.append(lista[i])
        posibles_combinaciones(lista, r, i + 1, comb)
        comb.pop()
posibles_combinaciones([1,2,3,4,5],3)        