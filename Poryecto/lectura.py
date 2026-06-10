import pandas as pd


# ==========================================================
# CARGA DE DATOS
# ==========================================================

def leer_datos(nombre_archivo):
    return pd.read_csv(nombre_archivo)


# ==========================================================
# PREGUNTA 1
# ¿Cuáles son todos los tipos de paquetes, vehículos,
# modos de entrega, regiones, condiciones climáticas
# y socios registrados?
# ==========================================================

def obtener_valores_unicos(df):

    return pd.DataFrame({
        "socios": pd.Series(sorted(df["delivery_partner"].unique())),
        "tipos_paquete": pd.Series(sorted(df["package_type"].unique())),
        "tipos_vehiculo": pd.Series(sorted(df["vehicle_type"].unique())),
        "modos_entrega": pd.Series(sorted(df["delivery_mode"].unique())),
        "regiones": pd.Series(sorted(df["region"].unique())),
        "condiciones_climaticas": pd.Series(sorted(df["weather_condition"].unique()))
    })


# ==========================================================
# PREGUNTA 2
# ¿Cuál es el tipo de paquete más enviado y cuál el menos?
# ==========================================================

def paquete_mas_y_menos_enviado(df):

    conteo = df["package_type"].value_counts()

    return pd.DataFrame({
        "categoria": ["Más enviado", "Menos enviado"],
        "tipo_paquete": [
            conteo.idxmax(),
            conteo.idxmin()
        ],
        "cantidad": [
            conteo.max(),
            conteo.min()
        ]
    })


# ==========================================================
# PREGUNTA 3
# ¿Cuántos envíos se realizaron por región?
# ==========================================================

def envios_por_region(df):

    return (
        df.groupby("region")
          .size()
          .reset_index(name="cantidad_envios")
          .sort_values("cantidad_envios", ascending=False)
    )


# ==========================================================
# PREGUNTA 4
# Promedio, máximo, mínimo y desviación estándar
# de las distancias de entrega
# ==========================================================

def estadisticas_distancia(df):

    return pd.DataFrame({
        "promedio": [df["distance_km"].mean()],
        "maximo": [df["distance_km"].max()],
        "minimo": [df["distance_km"].min()],
        "desviacion_estandar": [df["distance_km"].std()]
    })


# ==========================================================
# PREGUNTA 5
# Por cada tipo de vehículo:
# peso promedio, peso máximo y peso mínimo
# ==========================================================

def estadisticas_peso_por_vehiculo(df):

    return (
        df.groupby("vehicle_type")["package_weight_kg"]
          .agg(
              promedio="mean",
              maximo="max",
              minimo="min"
          )
          .reset_index()
          .sort_values("vehicle_type")
    )


# ==========================================================
# PROGRAMA PRINCIPAL
# ==========================================================

def main():

    df = leer_datos("delivery_logistics.csv")

    pregunta1 = obtener_valores_unicos(df)
    pregunta2 = paquete_mas_y_menos_enviado(df)
    pregunta3 = envios_por_region(df)
    pregunta4 = estadisticas_distancia(df)
    pregunta5 = estadisticas_peso_por_vehiculo(df)

    

    print("\n" )
    print("PREGUNTA 1")
    print("Tipos de paquetes, vehículos, modos de entrega, regiones,")
    print("condiciones climáticas y socios registrados.")
    print(pregunta1)


    print("\n" )
    print("PREGUNTA 2")
    print("Tipo de paquete más enviado y menos enviado.")
    print(pregunta2)


    print("\n" )
    print("PREGUNTA 3")
    print("Cantidad de envíos por región.")
    print(pregunta3)


    print("\n" )
    print("PREGUNTA 4")
    print("Estadísticas descriptivas de la distancia de entrega.")
    print(pregunta4)


    print("\n" )
    print("PREGUNTA 5")
    print("Peso promedio, máximo y mínimo por tipo de vehículo.")
    print(pregunta5)


if __name__ == "__main__":
    main()