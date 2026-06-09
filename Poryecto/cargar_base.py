from itertools import islice
import pandas as pd
import mysql.connector


# ============================================================
# Validaciones
# ============================================================

def validar_columnas(df, columnas, contexto):
    faltantes = [col for col in columnas if col not in df.columns]

    if faltantes:
        raise ValueError(f"Columnas faltantes en {contexto}: {faltantes}")


def validar_sin_nulos(df, contexto):
    nulos = df.isna().sum()
    nulos = nulos[nulos > 0]

    if not nulos.empty:
        raise ValueError(f"Hay nulos en {contexto}:\n{nulos}")


# ============================================================
# Limpieza mínima de fuente
# ============================================================

def limpiar_texto(s):
    return (
        s.astype("string")
        .str.strip()
    )


def limpiar_numero(s, nombre_columna):
    texto = (
        s.astype("string")
        .str.strip()
        .str.replace(",", ".", regex=False)
    )

    extraido = texto.str.extract(r"([-+]?\d*\.?\d+)")[0]
    numero = pd.to_numeric(extraido, errors="coerce")

    if numero.isna().any():
        ejemplos = s[numero.isna()].drop_duplicates().head(20).tolist()

        raise ValueError(
            f"La columna '{nombre_columna}' generó nulos al convertir a número. "
            f"Ejemplos: {ejemplos}"
        )

    return numero


def normalizar_fuente(df):
    df = df.copy()

    columnas_requeridas = [
        "delivery_partner",
        "package_type",
        "vehicle_type",
        "delivery_mode",
        "region",
        "weather_condition",
        "distance_km",
        "package_weight_kg",
        "delivery_time_hours",
        "expected_time_hours",
        "delayed",
        "delivery_status",
        "delivery_rating",
        "delivery_cost",
    ]

    validar_columnas(df, columnas_requeridas, "df fuente")

    columnas_texto = [
        "delivery_partner",
        "package_type",
        "vehicle_type",
        "delivery_mode",
        "region",
        "weather_condition",
        "delayed",
        "delivery_status",
    ]

    for col in columnas_texto:
        df[col] = limpiar_texto(df[col])

    columnas_numericas = [
        "distance_km",
        "package_weight_kg",
        "delivery_time_hours",
        "expected_time_hours",
        "delivery_rating",
        "delivery_cost",
    ]

    for col in columnas_numericas:
        df[col] = limpiar_numero(df[col], col)

    validar_sin_nulos(df[columnas_requeridas], "df fuente normalizado")

    return df


# ============================================================
# 1. Crear tabla normalizada de únicos
# ============================================================

def normalizar_seccion_unicos(df, columnas, id_col):
    """
    Crea una tabla normalizada a partir de valores únicos.

    columnas:
        {
            "columna_origen": "columna_final"
        }

    El ID se crea únicamente desde el índice de pandas.
    """

    columnas_origen = list(columnas.keys())

    validar_columnas(df, columnas_origen, f"normalizar_seccion_unicos({id_col})")

    tabla = (
        df[columnas_origen]
        .copy()
        .drop_duplicates()
        .rename(columns=columnas)
        .reset_index(drop=True)
    )

    validar_sin_nulos(tabla, f"tabla normalizada {id_col}")

    tabla.insert(0, id_col, tabla.index + 1)

    return tabla


# ============================================================
# 2. Relacionar tablas
# ============================================================

def como_lista(x):
    if isinstance(x, str):
        return [x]

    return list(x)


def llave_match(s):
    """
    Normaliza solo para comparar.
    No crea IDs.
    No cambia valores finales.
    """

    if pd.api.types.is_numeric_dtype(s):
        return pd.to_numeric(s, errors="coerce").round(10)

    return (
        s.astype("string")
        .str.strip()
        .str.casefold()
    )


def obtener_fk(df_source, tabla_unicos, source_cols, match_cols, id_col, nombre_relacion):
    """
    Toma IDs ya creados en tabla_unicos y los asigna al df_source.
    """

    source_cols = como_lista(source_cols)
    match_cols = como_lista(match_cols)

    validar_columnas(df_source, source_cols, f"df_source relación {nombre_relacion}")
    validar_columnas(tabla_unicos, match_cols + [id_col], f"tabla_unicos relación {nombre_relacion}")

    if len(source_cols) != len(match_cols):
        raise ValueError(
            f"source_cols y match_cols deben tener la misma longitud en '{nombre_relacion}'."
        )

    left = df_source[source_cols].copy()
    right = tabla_unicos[match_cols + [id_col]].copy()

    validar_sin_nulos(left, f"llaves fuente relación {nombre_relacion}")
    validar_sin_nulos(right, f"llaves catálogo relación {nombre_relacion}")

    left["__orden"] = range(len(left))

    key_cols = []

    for i, (source_col, match_col) in enumerate(zip(source_cols, match_cols)):
        key = f"__key_{i}"

        left[key] = llave_match(left[source_col])
        right[key] = llave_match(right[match_col])

        key_cols.append(key)

    duplicados = right[right.duplicated(key_cols, keep=False)]

    if not duplicados.empty:
        ejemplos = duplicados[match_cols + [id_col]].drop_duplicates().head(20)

        raise ValueError(
            f"Hay duplicados en la tabla relacionada '{nombre_relacion}':\n{ejemplos}"
        )

    merged = left.merge(
        right[key_cols + [id_col]],
        on=key_cols,
        how="left",
        validate="m:1",
        sort=False
    )

    sin_match = merged[merged[id_col].isna()]

    if not sin_match.empty:
        indices = sin_match["__orden"]

        ejemplos = (
            df_source.iloc[indices][source_cols]
            .drop_duplicates()
            .head(20)
        )

        raise ValueError(
            f"No hubo match para la relación '{nombre_relacion}'. "
            f"Ejemplos:\n{ejemplos}"
        )

    merged = merged.sort_values("__orden")

    return merged[id_col].astype("int64").reset_index(drop=True)


def relacionar_tablas(df_source, columnas, relaciones=None, id_col=None):
    """
    Crea una tabla final.

    columnas:
        {
            "columna_origen": "columna_final"
        }

    relaciones:
        {
            "nombre": {
                "tabla": tabla_unicos,
                "source_cols": "...",
                "match_cols": "...",
                "id_col": "...",
                "final_col": "..."
            }
        }

    id_col:
        Si se pasa, crea el ID de esta tabla desde el índice de pandas.
    """

    if relaciones is None:
        relaciones = {}

    columnas_origen = list(columnas.keys())

    validar_columnas(df_source, columnas_origen, "columnas directas en relacionar_tablas")

    df_final = (
        df_source[columnas_origen]
        .copy()
        .rename(columns=columnas)
        .reset_index(drop=True)
    )

    if id_col is not None:
        df_final.insert(0, id_col, df_final.index + 1)

    for nombre_relacion, config in relaciones.items():
        df_final[config["final_col"]] = obtener_fk(
            df_source=df_source,
            tabla_unicos=config["tabla"],
            source_cols=config["source_cols"],
            match_cols=config["match_cols"],
            id_col=config["id_col"],
            nombre_relacion=nombre_relacion
        )

    validar_sin_nulos(df_final, "tabla generada en relacionar_tablas")

    return df_final


# ============================================================
# 3. Construcción de tablas según tu modelo
# ============================================================

def crear_tablas_relacionales(path_csv):
    df = pd.read_csv(path_csv)
    df = normalizar_fuente(df)

    # =====================================================
    # Tablas catálogo
    # =====================================================

    paquete = normalizar_seccion_unicos(
        df,
        columnas={
            "package_type": "tipo",
            "package_weight_kg": "peso",
        },
        id_col="id_paquete"
    )

    socio = normalizar_seccion_unicos(
        df,
        columnas={
            "delivery_partner": "nombre",
        },
        id_col="id_socio"
    )

    region = normalizar_seccion_unicos(
        df,
        columnas={
            "region": "region",
        },
        id_col="id_region"
    )

    vehiculo = normalizar_seccion_unicos(
        df,
        columnas={
            "vehicle_type": "tipo",
        },
        id_col="id_vehiculo"
    )

    # =====================================================
    # Tabla auxiliar de rutas únicas
    # Aquí se crea id_rutas desde índice pandas.
    # Esta tabla auxiliar NO se carga a MySQL.
    # =====================================================

    rutas_unicos = normalizar_seccion_unicos(
        df,
        columnas={
            "region": "region",
            "vehicle_type": "vehicle_type",
            "expected_time_hours": "expected_time_hours",
            "distance_km": "distance_km",
        },
        id_col="id_rutas"
    )

    # =====================================================
    # Tabla rutas final
    # rutas(id_rutas, id_region, id_vehiculo, tiempo_esperado, distancia)
    # =====================================================

    rutas = relacionar_tablas(
        df_source=rutas_unicos,
        columnas={
            "id_rutas": "id_rutas",
            "expected_time_hours": "tiempo_esperado",
            "distance_km": "distancia",
        },
        relaciones={
            "region": {
                "tabla": region,
                "source_cols": "region",
                "match_cols": "region",
                "id_col": "id_region",
                "final_col": "id_region",
            },
            "vehiculo": {
                "tabla": vehiculo,
                "source_cols": "vehicle_type",
                "match_cols": "tipo",
                "id_col": "id_vehiculo",
                "final_col": "id_vehiculo",
            },
        }
    )

    rutas = rutas[
        [
            "id_rutas",
            "id_region",
            "id_vehiculo",
            "tiempo_esperado",
            "distancia",
        ]
    ]

    # =====================================================
    # Tabla entrega final
    # entrega(id_entrega, id_ruta, id_paquete, id_socio, modo,
    #         tiempo_entrega, retraso, clima, costo, calificacion)
    #
    # id_entrega se crea desde el índice pandas.
    # NO se usa delivery_id.
    # =====================================================

    entrega = relacionar_tablas(
        df_source=df,
        id_col="id_entrega",
        columnas={
            "delivery_mode": "modo",
            "delivery_time_hours": "tiempo_entrega",
            "delayed": "retraso",
            "weather_condition": "clima",
            "delivery_cost": "costo",
            "delivery_rating": "calificacion",
        },
        relaciones={
            "rutas": {
                "tabla": rutas_unicos,
                "source_cols": [
                    "region",
                    "vehicle_type",
                    "expected_time_hours",
                    "distance_km",
                ],
                "match_cols": [
                    "region",
                    "vehicle_type",
                    "expected_time_hours",
                    "distance_km",
                ],
                "id_col": "id_rutas",
                "final_col": "id_rutas",
            },
            "paquete": {
                "tabla": paquete,
                "source_cols": [
                    "package_type",
                    "package_weight_kg",
                ],
                "match_cols": [
                    "tipo",
                    "peso",
                ],
                "id_col": "id_paquete",
                "final_col": "id_paquete",
            },
            "socio": {
                "tabla": socio,
                "source_cols": "delivery_partner",
                "match_cols": "nombre",
                "id_col": "id_socio",
                "final_col": "id_socio",
            },
        }
    )

    entrega = entrega[
        [
            "id_entrega",
            "id_rutas",
            "id_paquete",
            "id_socio",
            "modo",
            "tiempo_entrega",
            "retraso",
            "clima",
            "costo",
            "calificacion",
        ]
    ]

    tablas = {
        "paquete": paquete,
        "socio": socio,
        "region": region,
        "vehiculo": vehiculo,
        "rutas": rutas,
        "entrega": entrega,
    }

    for nombre, tabla in tablas.items():
        validar_sin_nulos(tabla, f"tabla {nombre}")

    return tablas


def valor_mysql(x):
    """
    Convierte valores de pandas/numpy a valores aceptables por mysql.connector.
    """

    if pd.isna(x):
        return None

    if hasattr(x, "item"):
        return x.item()

    return x


def generar_batches(iterable, batch_size):
    iterator = iter(iterable)

    while True:
        batch = list(islice(iterator, batch_size))

        if not batch:
            break

        yield batch


def truncar_tablas_mysql(cursor, tablas):
    """
    Limpia las tablas respetando llaves foráneas.
    Se truncan en orden inverso porque entrega depende de rutas,
    rutas depende de region y vehiculo, etc.
    """

    cursor.execute("SET FOREIGN_KEY_CHECKS = 0")

    for nombre_tabla in reversed(list(tablas.keys())):
        cursor.execute(f"TRUNCATE TABLE `{nombre_tabla}`")

    cursor.execute("SET FOREIGN_KEY_CHECKS = 1")


def cargar_dataframes_mysql(
    tablas: dict[str, pd.DataFrame],
    config_mysql: dict,
    batch_size: int = 1000,
    truncate: bool = False
) -> None:
    """
    Carga un diccionario de DataFrames a MySQL usando mysql.connector.

    tablas:
        {
            "paquete": df_paquete,
            "socio": df_socio,
            "region": df_region,
            "vehiculo": df_vehiculo,
            "rutas": df_rutas,
            "entrega": df_entrega,
        }

    Importante:
    El orden del diccionario debe respetar las dependencias:
    primero catálogos, luego rutas, luego entrega.
    """

    conn = mysql.connector.connect(**config_mysql)
    cursor = conn.cursor()

    try:
        if truncate:
            truncar_tablas_mysql(cursor, tablas)

        for nombre_tabla, df in tablas.items():

            if df.empty:
                print(f"Tabla '{nombre_tabla}' vacía. Se omite.")
                continue

            columnas = list(df.columns)

            columnas_sql = ", ".join(f"`{col}`" for col in columnas)
            placeholders = ", ".join(["%s"] * len(columnas))

            sql = f"""
                INSERT INTO `{nombre_tabla}` ({columnas_sql})
                VALUES ({placeholders})
            """

            filas = (
                tuple(valor_mysql(v) for v in fila)
                for fila in df.itertuples(index=False, name=None)
            )

            total = 0

            for batch in generar_batches(filas, batch_size):
                cursor.executemany(sql, batch)
                total += cursor.rowcount

            print(f"Tabla '{nombre_tabla}' cargada. Filas insertadas: {total}")

        conn.commit()

    except Exception as e:
        conn.rollback()
        raise e

    finally:
        cursor.close()
        conn.close()

# ============================================================
# Ejecución
# ============================================================

if __name__ == "__main__":

    config_mysql = {
        "host": "localhost",
        "user": "root",
        "password": "darkuniverse_08",
        "database": "sistema_paqueteria",
        "port": 3306,
    }

    tablas = crear_tablas_relacionales("./delivery_logistics.csv")

    for nombre, tabla in tablas.items():
        print("\n" + "=" * 60)
        print(nombre)
        print(tabla.head())
        print(tabla.info())

    cargar_dataframes_mysql(
        tablas=tablas,
        config_mysql=config_mysql,
        batch_size=1000,
        truncate=True
    )