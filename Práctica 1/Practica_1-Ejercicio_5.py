
def cuenta_unos(n):
    contador = 0

    for i in range(n + 1):
        contador += str(i).count('1')

    return contador

print(cuenta_unos(130))
