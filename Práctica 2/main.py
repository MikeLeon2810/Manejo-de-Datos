from funciones import  busqueda_binaria, busqueda_ternaria, generar_reporte, boyer_moore, bubble_sort_optimizado, comparar_tiempos, leer_archivo, escribir_archivo, buscar_mayusculas, cuenta_palabras



def eje_3():

    #Ejercicio 3:
    # Leer datos del archivo
    lista = leer_archivo("data/comentarios.txt")

    lista = bubble_sort_optimizado(lista)
    
    escribir_archivo("data/comentarios.txt", lista)

    reporte = generar_reporte(lista)

    return reporte

def eje_4():
    resultado = buscar_mayusculas("data/quijote_fragmento.txt")
    return resultado


def eje_5():
    frecuencias, mayor_frec, mayor_alfa, menor_alfa = cuenta_palabras("data/prueba.txt")
    return frecuencias, mayor_frec, mayor_alfa, menor_alfa



def main():
    #Ejercicio 1:
    print("=== Ejercicio 1 ===")
    print("El Ejercicio 1, el código de la busqueda ternaria está en funciones.py")
    print("\n")  # Separador entre ejercicios


    #Ejercicio 2:
    # Comparar tiempos de ejecución de las búsquedas
    print("=== Ejercicio 2 ===")
    print("Comparando tiempos de búsqueda binaria y ternaria atrvés de la siguiente gráfica:")
    print("¿Cuál es mejor en cuanto al timepo de ejecución?")
    print("R: La binaria es mejor ya que, (como se ve en la figura) realiza menos comparaciones, ergo tarda menor tiempo en encontrar el elemento objetivo.")
    comparar_tiempos() 
    print("\n")  # Separador entre ejercicios

    #Ejercicio 3:
    print("=== Ejercicio 3 ===")
    reporte = eje_3()
    print("Reporte de implicados en plagio:")
    for nombre in reporte:
        print(nombre)

    print("\n")  # Separador entre ejercicios


    #Ejercicio 4:
    print("=== Ejercicio 4 ===")
    resultado = eje_4()
    print(resultado)



    print("\n")  # Separador entre ejercicios

    #Ejercicio 5:
    print("=== Ejercicio 5 ===")
    frecuencias, mayor_frec, mayor_alfa, menor_alfa = eje_5()
    print("Frecuencias:", frecuencias)
    print("Mayor frecuencia:", mayor_frec)
    print("Mayor alfabético:", mayor_alfa)
    print("Menor alfabético:", menor_alfa)



if __name__ == "__main__":
    main()        
