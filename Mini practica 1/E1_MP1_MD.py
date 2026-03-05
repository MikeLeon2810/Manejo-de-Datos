#Ejercico 1
#Escribe la función expandir(datos) que recibe una cadena de datos formado por bases y
#cantidades (se asume válido, las cantidades van de 1 a 9) y retorna la secuencia correspon-
#diente.
#Ejemplo: Entrada: “A1T2C1A5T1C1A1G3” Salida: ATTCAAAAATCAGGG

def expandir(datos):
    resultado =""

    for i in range(0, len(datos),2):
        base = datos[i] #letra
        cantidad= int(datos[i+1]) #numero
        resultado += base * cantidad

    return resultado


if __name__ == '__main__':
    datos = "A1T2C1A5T1C1A1G3"
    salida = expandir(datos)
    print(salida)