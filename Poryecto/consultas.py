import mysql.connector


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

    cursor.execute(query)
    return cursor.fetchall()


# ==========================================================
# CONSULTA 2
# ¿Cuál es el vehículo más usado en las rutas
# de la región north?
# ==========================================================

def vehiculo_mas_usado_north(cursor):

    query = """
    SELECT v.tipo,
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

    cursor.execute(query)
    return cursor.fetchall()


# ==========================================================
# CONSULTA 3
# Muestra las entregas que se hayan retrasado
# con clima stormy
# ==========================================================

def entregas_retrasadas_stormy(cursor):

    query = """
    SELECT *
    FROM entrega
    WHERE retraso = 'yes'
      AND clima = 'stormy';
    """

    cursor.execute(query)
    return cursor.fetchall()


# ==========================================================
# CONSULTA 4
# Entregas realizadas en una van por DHL
# ==========================================================

def entregas_van_dhl(cursor):

    query = """
    SELECT e.*
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

    cursor.execute(query)
    return cursor.fetchall()


# ==========================================================
# CONSULTA 5
# Entregas con calificación 1 realizadas por
# xpressbees en la región east
# ==========================================================

def entregas_calificacion_xpressbees_east(cursor):

    query = """
    SELECT e.*
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

    cursor.execute(query)
    return cursor.fetchall()


# ==========================================================
# PROGRAMA PRINCIPAL
# ==========================================================

if __name__ == "__main__":

    conn = mysql.connector.connect(**config_mysql)
    cursor = conn.cursor()

    print("=== CONEXIÓN EXITOSA A MYSQL ===")


    # CONSULTA 1
    resultado1 = rutas_entre_50_y_100(cursor)

    print("\nCONSULTA 1")
    print("Rutas entre 50 y 100 km:", len(resultado1))
    print("Primeros 3 registros:")
    print(resultado1[:3])


    # CONSULTA 2
    resultado2 = vehiculo_mas_usado_north(cursor)

    print("\nCONSULTA 2")
    print("Vehículo más usado en North:")
    print(resultado2)


    # CONSULTA 3
    resultado3 = entregas_retrasadas_stormy(cursor)

    print("\nCONSULTA 3")
    print("Entregas retrasadas con clima stormy:", len(resultado3))
    print("Primeros 3 registros:")
    print(resultado3[:3])


    # CONSULTA 4
    resultado4 = entregas_van_dhl(cursor)

    print("\nCONSULTA 4")
    print("Entregas realizadas en van por DHL:", len(resultado4))
    print("Primeros 3 registros:")
    print(resultado4[:3])


    # CONSULTA 5
    resultado5 = entregas_calificacion_xpressbees_east(cursor)

    print("\nCONSULTA 5")
    print("Entregas con calificación 1, xpressbees, región east:", len(resultado5))
    print("Primeros 3 registros:")
    print(resultado5[:3])


    cursor.close()
    conn.close()

    print("\nConexión cerrada correctamente.")

