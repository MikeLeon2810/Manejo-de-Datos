import mysql.connector
import pandas as pd


# ==========================================================
# CONFIGURACIÓN DE LA CONEXIÓN
# ==========================================================

config_mysql = {
        "host": "localhost",
        "user": "root",
        "password": "darkuniverse_08",
        "database": "sistema_paqueteria",
        "port": 3306,
    }


# ==========================================================
# FUNCIÓN AUXILIAR
# ==========================================================

def ejecutar_consulta_df(cursor, query):

    cursor.execute(query)

    columnas = [columna[0] for columna in cursor.description]

    return pd.DataFrame(
        cursor.fetchall(),
        columns=columnas
    )


# ==========================================================
# CONSULTA 1
# ¿Cuáles son las rutas cuya distancia se encuentra
# entre los 50 km y 100 km?
# ==========================================================

def rutas_entre_50_y_100(cursor):

    query = """
    SELECT *
    FROM rutas
    WHERE distancia BETWEEN 50 AND 100;
    """

    return ejecutar_consulta_df(cursor, query)


# ==========================================================
# CONSULTA 2
# ¿Cuál es el vehículo más usado en la región north?
# ==========================================================

def vehiculo_mas_usado_north(cursor):

    query = """
    SELECT
        v.tipo AS vehiculo,
        COUNT(*) AS total_rutas
    FROM rutas r
    JOIN region rg
        ON r.id_region = rg.id_region
    JOIN vehiculo v
        ON r.id_vehiculo = v.id_vehiculo
    WHERE rg.region = 'north'
    GROUP BY v.tipo
    ORDER BY total_rutas DESC
    LIMIT 1;
    """

    return ejecutar_consulta_df(cursor, query)


# ==========================================================
# CONSULTA 3
# Entregas retrasadas con clima stormy
# ==========================================================

def entregas_retrasadas_stormy(cursor):

    query = """
    SELECT *
    FROM entrega
    WHERE retraso = 'yes'
      AND clima = 'stormy';
    """

    return ejecutar_consulta_df(cursor, query)


# ==========================================================
# CONSULTA 4
# Entregas realizadas en vehículo van por DHL
# ==========================================================

def entregas_van_dhl(cursor):

    query = """
    SELECT
        e.id_entrega,
        s.nombre AS socio,
        v.tipo AS vehiculo,
        e.modo,
        e.clima,
        e.costo,
        e.calificacion
    FROM entrega e
    JOIN socio s
        ON e.id_socio = s.id_socio
    JOIN rutas r
        ON e.id_rutas = r.id_rutas
    JOIN vehiculo v
        ON r.id_vehiculo = v.id_vehiculo
    WHERE v.tipo = 'van'
      AND s.nombre = 'dhl';
    """

    return ejecutar_consulta_df(cursor, query)


# ==========================================================
# CONSULTA 5
# Entregas con calificación 1 realizadas por
# XpressBees en la región East
# ==========================================================

def entregas_calificacion_xpressbees_east(cursor):

    query = """
    SELECT
        e.id_entrega,
        s.nombre AS socio,
        rg.region,
        e.modo,
        e.clima,
        e.costo,
        e.calificacion
    FROM entrega e
    JOIN socio s
        ON e.id_socio = s.id_socio
    JOIN rutas r
        ON e.id_rutas = r.id_rutas
    JOIN region rg
        ON r.id_region = rg.id_region
    WHERE e.calificacion = 1
      AND s.nombre = 'xpressbees'
      AND rg.region = 'east';
    """

    return ejecutar_consulta_df(cursor, query)


# ==========================================================
# PROGRAMA PRINCIPAL
# ==========================================================

if __name__ == "__main__":

    conn = mysql.connector.connect(**config_mysql)
    cursor = conn.cursor()

    print("=== CONEXIÓN EXITOSA A MYSQL ===")

    print("\nAVISO:")
    print("Las consultas pueden devolver cientos o miles de registros.")
    print("Por motivos de legibilidad, este programa muestra únicamente un resumen")
    print("y los primeros registros encontrados.")
    print("Si desea visualizar la consulta completa, utilice MySQL Workbench.")


    # ======================================================
    # CONSULTA 1
    # ======================================================

    resultado1 = rutas_entre_50_y_100(cursor)

    print("\n" + "=" * 60)
    print("CONSULTA 1")
    print("Rutas entre 50 y 100 km:", len(resultado1))
    print("\nPrimeras 5 filas:")
    print(resultado1.head())


    # ======================================================
    # CONSULTA 2
    # ======================================================

    resultado2 = vehiculo_mas_usado_north(cursor)

    print("\n" + "=" * 60)
    print("CONSULTA 2")
    print("Vehículo más usado en la región North:")
    print(resultado2)


    # ======================================================
    # CONSULTA 3
    # ======================================================

    resultado3 = entregas_retrasadas_stormy(cursor)

    print("\n" + "=" * 60)
    print("CONSULTA 3")
    print("Entregas retrasadas con clima stormy:", len(resultado3))
    print("\nPrimeras 5 filas:")
    print(resultado3.head())


    # ======================================================
    # CONSULTA 4
    # ======================================================

    resultado4 = entregas_van_dhl(cursor)

    print("\n" + "=" * 60)
    print("CONSULTA 4")
    print("Entregas realizadas en vehículo tipo van por DHL:", len(resultado4))
    print("\nPrimeras 5 filas:")
    print(resultado4.head())


    # ======================================================
    # CONSULTA 5
    # ======================================================

    resultado5 = entregas_calificacion_xpressbees_east(cursor)

    print("\n" + "=" * 60)
    print("CONSULTA 5")
    print("Entregas con calificación 1 realizadas por XpressBees en la región East:", len(resultado5))
    print("\nPrimeras 5 filas:")
    print(resultado5.head())


    cursor.close()
    conn.close()

    print("\nConexión cerrada correctamente.")