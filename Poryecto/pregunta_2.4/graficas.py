import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import mysql.connector

# Configuración de tu base de datos local en Codespaces
config = {
    'user': 'root',
    'password': 'root',
    'host': 'localhost',
    'database': 'sistema_paqueteria'
}

# --- 1. Gráfica de pastel: Entregas por socio ---
def grafica_pastel_socios(conn):
    query = """
        SELECT s.nombre_socio, COUNT(e.id_entrega) as total_entregas
        FROM entrega e
        JOIN socio s ON e.id_socio = s.id_socio
        GROUP BY s.nombre_socio;
    """
    df = pd.read_sql(query, conn)
    
    plt.figure(figsize=(8, 8))
    plt.pie(df['total_entregas'], labels=df['nombre_socio'], autopct='%1.1f%%', startangle=140, colors=sns.color_palette('pastel'))
    plt.title('Porcentaje de Entregas por Socio')
    
    # Guardar imagen en lugar de mostrarla
    plt.savefig('grafica_1_pastel_socios.png', bbox_inches='tight')
    plt.close()
    print("✅ Gráfica 1 generada: grafica_1_pastel_socios.png")

# --- 2. Gráfica de puntos: Peso vs Precio para el socio fedez ---
def grafica_puntos_fedex(conn):
    query = """
        SELECT p.peso, e.costo
        FROM entrega e
        JOIN paquete p ON e.id_paquete = p.id_paquete
        JOIN socio s ON e.id_socio = s.id_socio
        WHERE s.nombre_socio = 'fedex';
    """
    df = pd.read_sql(query, conn)
    
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x='peso', y='costo', color='crimson', alpha=0.6)
    plt.title('Peso del Paquete vs Precio de la Entrega (Socio: fedex)')
    plt.xlabel('Peso del Paquete (kg)')
    plt.ylabel('Precio de Entrega (Costo)')
    plt.grid(True, linestyle='--', alpha=0.7)
    
    plt.savefig('grafica_2_puntos_fedex.png', bbox_inches='tight')
    plt.close()
    print("✅ Gráfica 2 generada: grafica_2_puntos_fedez.png")

# --- 3. Gráfica comparativa: Distancia vs Precio por región ---
def grafica_comparativa_region(conn):
    query = """
        SELECT r.distancia_km, e.costo, rg.region
        FROM entrega e
        JOIN rutas r ON e.id_ruta = r.id_rutas
        JOIN region rg ON r.id_region = rg.id_region;
    """
    df = pd.read_sql(query, conn)
    
    plt.figure(figsize=(12, 7))
    sns.scatterplot(data=df, x='distancia_km', y='costo', hue='region', palette='Set2', alpha=0.7)
    plt.title('Comportamiento de Distancia vs Precio de Entrega por Región')
    plt.xlabel('Distancia (km)')
    plt.ylabel('Precio de Entrega (Costo)')
    plt.legend(title='Región')
    plt.grid(True, linestyle='--', alpha=0.7)
    
    plt.savefig('grafica_3_comparativa_region.png', bbox_inches='tight')
    plt.close()
    print("✅ Gráfica 3 generada: grafica_3_comparativa_region.png")

# ==========================================
# Ejecución Principal
# ==========================================
if __name__ == '__main__':
    try:
        conn = mysql.connector.connect(**config)
        print("Generando reportes gráficos...")
        
        grafica_pastel_socios(conn) # 1. Gráfica de pastel que muestre las entregas realizadas por cada socio[cite: 84].
        grafica_puntos_fedex(conn)  # 2. Gráfica de puntos del peso vs precio para fedez[cite: 85].
        grafica_comparativa_region(conn) # 3. Gráfica comparativa de distancia vs precio por región[cite: 86].
        
        print("\n¡Todas las gráficas se han guardado exitosamente en tu explorador de archivos!")
    except Exception as e:
        print(f"Error al generar las gráficas: {e}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            conn.close()