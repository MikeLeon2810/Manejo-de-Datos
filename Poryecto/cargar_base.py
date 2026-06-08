import pandas as pd
import mysql.connector
from itertools import islice


def lectura_de_tablas_unicas():
    src_df = pd.read_csv("./delivery_logistics.csv")
    socio_u = src_df[["delivery_partner"]].dropna().drop_duplicates().reset_index(drop=True)
    socio_u = socio_u.rename(columns={"delivery_partner": "nombre"})
    vehiculo_u = src_df[["vehicle_type"]].dropna().drop_duplicates().reset_index(drop=True)
    vehiculo_u= vehiculo_u.rename(columns={"vehicle_type": "tipo"})
    region_u = src_df[["region"]].dropna().drop_duplicates().reset_index(drop=True)
    region_u= region_u.rename(columns={"region": "region"})
    paquete_u = src_df[["package_type", "package_weight_kg"]].dropna().drop_duplicates().reset_index(drop=True)
    paquete_u= paquete_u.rename(columns={"package_type": "tipo", "package_weight_kg": "peso"})
    return {
        #"socio": socio_u,
        "vehiculo": vehiculo_u,
        "region": region_u,
        #"paquete": paquete_u
        }

def preparar_tabla_con_foreign_keys(
    df_source: pd.DataFrame,
    columnas: dict,
    relaciones: dict,
    normalizar_texto: bool = True,
    convertir_nulls: bool = False
) -> pd.DataFrame:
    """
    Prepara un DataFrame para cargar a SQL, seleccionando columnas normales
    y reemplazando columnas descriptivas por foreign keys tomadas desde
    el índice de los DataFrames relacionales.

    columnas:
        {
            "columna_origen": "columna_final_sql"
        }

    relaciones:
        {
            "nombre_logico_relacion": {
                "df": df_catalogo,
                "source_col": "columna_en_df_source",
                "match_col": "columna_en_df_catalogo",
                "final_col": "nombre_fk_final",
                "id_offset": 1
            }
        }
    """

    df = df_source.copy()

    # 1. Seleccionar y renombrar columnas normales
    columnas_origen = list(columnas.keys())

    faltantes = [col for col in columnas_origen if col not in df.columns]

    if faltantes:
        raise ValueError(f"Columnas normales faltantes en df_source: {faltantes}")

    df_final = df[columnas_origen].rename(columns=columnas).copy()

    # 2. Procesar relaciones
    for nombre_relacion, config in relaciones.items():

        df_rel = config["df"].copy()

        source_col = config["source_col"]
        match_col = config["match_col"]
        final_col = config["final_col"]
        id_offset = config.get("id_offset", 1)

        if source_col not in df.columns:
            raise ValueError(
                f"La columna source_col='{source_col}' no existe en df_source "
                f"para la relación '{nombre_relacion}'."
            )

        if match_col not in df_rel.columns:
            raise ValueError(
                f"La columna match_col='{match_col}' no existe en el catálogo "
                f"de la relación '{nombre_relacion}'."
            )

        # Importante: resetear índice para que index + 1 coincida con SQL
        df_rel = df_rel.reset_index(drop=True)

        # Crear FK desde el índice
        df_rel = df_rel[[match_col]].copy()
        df_rel["__fk_id"] = df_rel.index + id_offset

        # Crear auxiliares para comparar
        df_aux = df[[source_col]].copy()

        df_aux["__match_source"] = df_aux[source_col]
        df_rel["__match_rel"] = df_rel[match_col]

        if normalizar_texto:
            df_aux["__match_source"] = (
                df_aux["__match_source"]
                .astype(str)
                .str.strip()
                .str.lower()
            )

            df_rel["__match_rel"] = (
                df_rel["__match_rel"]
                .astype(str)
                .str.strip()
                .str.lower()
            )

        # Validar duplicados en catálogo
        duplicados = (
            df_rel[df_rel["__match_rel"].duplicated(keep=False)][match_col]
            .drop_duplicates()
            .tolist()
        )

        if duplicados:
            raise ValueError(
                f"Hay valores duplicados en el catálogo '{nombre_relacion}': {duplicados}"
            )

        # Merge para traer FK
        df_match = df_aux.merge(
            df_rel[["__match_rel", "__fk_id"]],
            left_on="__match_source",
            right_on="__match_rel",
            how="left",
            validate="m:1"
        )

        # Validar valores sin match
        sin_match = (
            df_match[df_match["__fk_id"].isna()][source_col]
            .drop_duplicates()
            .tolist()
        )

        if sin_match:
            raise ValueError(
                f"Valores sin match para la relación '{nombre_relacion}' "
                f"usando source_col='{source_col}' y match_col='{match_col}': {sin_match}"
            )

        # Agregar FK al resultado final
        df_final[final_col] = df_match["__fk_id"].astype(int).values

    if convertir_nulls:
        df_final = df_final.astype(object).where(pd.notna(df_final), None)

    return df_final

def cargar_dataframes_mysql(tablas: dict, config_mysql: dict, batch_size: int = 1000):
    """
    tablas:
        dict con estructura:
        {
            "nombre_tabla_mysql": dataframe,
            "otra_tabla_mysql": otro_dataframe
        }
    """

    conn = mysql.connector.connect(**config_mysql)
    cursor = conn.cursor()

    try:
        for nombre_tabla, df in tablas.items():

            if df.empty:
                print(f"Tabla '{nombre_tabla}' vacía. Se omite.")
                continue

            # Copia para no modificar el original
            df_insert = df.copy()

            # Convertir NaN / NaT a None para MySQL
            df_insert = df_insert.astype(object).where(pd.notna(df_insert), None)

            columnas = list(df_insert.columns)

            columnas_sql = ", ".join(f"{col}" for col in columnas)
            placeholders = ", ".join(["%s"] * len(columnas))

            sql = f"""
                INSERT INTO {nombre_tabla} ({columnas_sql})
                VALUES ({placeholders})
            """

            def chunks(iterable, size):
                iterator = iter(iterable)
                while True:
                    batch = list(islice(iterator, size))
                    if not batch:
                        break
                    yield batch

            filas = df_insert.itertuples(index=False, name=None)

            total = 0

            for batch in chunks(filas, batch_size):
                cursor.executemany(sql, batch)
                conn.commit()
                total += cursor.rowcount

            print(f"Tabla '{nombre_tabla}' cargada. Filas insertadas: {total}")

    except Exception as e:
        conn.rollback()
        raise e

    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    config_mysql = {
        "host": "localhost",
        "user": "root",
        "password": "darkuniverse_08",
        "database": "sistema_paqueteria",
        "port": 3306
    }

    src_df = pd.read_csv("./delivery_logistics.csv")
    rutas_raw = src_df[["distance_km", "expected_time_hours", "region", "vehicle_type"]]
    tablas = lectura_de_tablas_unicas()

    rutas = preparar_tabla_con_foreign_keys(
        rutas_raw,
        columnas = {
            "vehicle_type": "tipo",
            "distance_km": "distancia",
            "expected_time_hours": "tiempo_esperado"
        },
        relaciones={
        "region": {
            "df": tablas["region"],
            "source_col": "region",
            "match_col": "region",
            "final_col": "id_region",
            "id_offset": 1
        },
        "vehiculo": {
            "df": tablas["vehiculo"],
            "source_col": "vehicle_type",
            "match_col": "tipo",
            "final_col": "id_vehiculo",
            "id_offset": 1
        }
    })
    
    cargar_dataframes_mysql(tablas=tablas, config_mysql=config_mysql)