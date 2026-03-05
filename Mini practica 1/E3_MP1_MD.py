# 1) Función que lee el archivo y calcula estadísticas
def leer_deportes(nombre_archivo):
    datos = {}   # deporte -> [contador, suma_edades, suma_años]

    with open(nombre_archivo, "r") as f:
        for linea in f:
            # separar los datos
            nombre, edad, deporte, años = linea.strip().split(", ")
            edad = int(edad)
            años = int(años)

            # si el deporte no existe, lo creamos
            if deporte not in datos:
                datos[deporte] = [0, 0, 0]

            # acumulamos datos
            datos[deporte][0] += 1        # número de estudiantes
            datos[deporte][1] += edad     # suma de edades
            datos[deporte][2] += años    # suma de años entrenando

    # calcular promedio de edades
    for deporte in datos:
        count, suma_edades, suma_años = datos[deporte]
        promedio = suma_edades // count
        datos[deporte] = [count, promedio, suma_años]

    return datos


# 2) Función que guarda los resultados en un archivo
def guardar_resultados(datos, nombre_salida):
    with open(nombre_salida, "w") as f:
        f.write("Deporte, numero_deportistas, promedio_edad, total_años\n")
        for deporte, (n, prom, total) in datos.items():
            f.write(f"{deporte}, {n}, {prom}, {total}\n")


# ===== PROGRAMA PRINCIPAL =====
if __name__ == '__main__':

 datos = leer_deportes("deportes.txt")

 # imprimir estilo diccionario
 for deporte, valores in datos.items():
    print(f"{deporte}: {valores}")

 # guardar en archivo
 guardar_resultados(datos, "resultado.txt")