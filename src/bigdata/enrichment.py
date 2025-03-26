import os
import sqlite3
import pandas as pd
import requests
from datetime import datetime

# Rutas y Configuraciones
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Ruta de la Base de Datos
RUTA_BD = os.path.join(BASE_DIR, "static", "db", "ingestion.db")

# Ruta del Nuevo Archivo CSV de Delitos Informáticos
RUTA_DELITOS_INFORMATICOS_CSV = os.path.join(BASE_DIR, "static", "xlsx", "Delitos_Informaticos.csv")

# Ruta Donde se Guardarán los Datos Enriquecidos
RUTA_DATOS_ENRIQUECIDOS = os.path.join(BASE_DIR, "static", "xlsx", "datos_enriquecidos.csv")

# Ruta Donde se Guardará el Reporte de Enriquecimiento
RUTA_REPORTE_ENRIQUECIMIENTO = os.path.join(BASE_DIR, "static", "auditoria", "reporte_enriquecimiento.txt")

# URL de la API del Inventario Anual de Bovinos en Antioquia 
URL_INVENTARIO_BOVINOS_API = "https://www.datos.gov.co/resource/fy9z-8zxt.json"

# Creamos los directorios si no existen
os.makedirs(os.path.dirname(RUTA_DATOS_ENRIQUECIDOS), exist_ok=True)
os.makedirs(os.path.dirname(RUTA_REPORTE_ENRIQUECIMIENTO), exist_ok=True)

# 1. Lectura de Datos

def cargar_dataset_limpio_desde_bd():
    """
    Cargamos el dataset limpio (covid_data_cleaned) generado en la Actividad 2,
    almacenado en la base de datos (ingestion.db).
    """
    print("Cargando dataset base limpio desde la base de datos (covid_data_cleaned)...")
    conexion = sqlite3.connect(RUTA_BD)
    df_limpio = pd.read_sql_query("SELECT * FROM covid_data_cleaned", conexion)
    conexion.close()
    print(f"Dataset limpio cargado: {len(df_limpio)} registros.")
    return df_limpio

def leer_delitos_informaticos_csv():
    """
    Leemos el archivo CSV de Delitos Informáticos y renombramos columnas para unificar criterios.
    Se renombra 'MUNICIPIO_HECHO' a 'municipio' para poder unir con la fuente de Bovinos.
    """
    print("Leyendo archivo CSV de Delitos Informáticos...")
    df_informaticos = pd.read_csv(RUTA_DELITOS_INFORMATICOS_CSV)
    print(f"Delitos Informáticos leídos: {len(df_informaticos)} registros.")

    # Renombramos columnas a minúsculas y renombramos 'MUNICIPIO_HECHO' a 'municipio'
    df_informaticos.rename(columns={
        'CRIMINALIDAD': 'criminalidad',
        'ES_ARCHIVO': 'es_archivo',
        'ES_PRECLUSIÓN': 'es_preclusion',
        'ESTADO': 'estado',
        'ETAPA_CASO': 'etapa_caso',
        'LEY': 'ley',
        'PAÍS_HECHO': 'pais_hecho',
        'DEPARTAMENTO_HECHO': 'departamento_hecho',
        'MUNICIPIO_HECHO': 'municipio',  # clave de unión 
        'SECCIONAL': 'seccional',
        'AÑO_HECHOS': 'a_o_hechos',
        'AÑO_ENTRADA': 'a_o_entrada',
        'AÑO_DENUNCIA': 'a_o_denuncia',
        'DELITO': 'delito',
        'GRUPO_DELITO': 'grupo_delito',
        'CONSUMADO': 'consumado',
        'TOTAL_PROCESOS': 'total_procesos'
    }, inplace=True)
    
    # Eliminamos espacios extra en la clave de unión
    df_informaticos['municipio'] = df_informaticos['municipio'].str.strip()
    return df_informaticos

def leer_inventario_bovinos_api():
    """
    Leemos la API JSON del Inventario Anual de Bovinos en Antioquia.
    Devolvemos un DataFrame con los datos y rellenamos los valores nulos en
    las columnas de pasto (pasto_mejorado, pasto_natural, pasto_corte y en Total Pastos)
    usando la mediana. Se renombra 'MUNICIPIO' a 'municipio' y 'Total Pastos (ha)' a 'total_pastos'.
    """
    print("Consultando API de Inventario Anual de Bovinos en Antioquia...")
    try:
        respuesta = requests.get(URL_INVENTARIO_BOVINOS_API)
        respuesta.raise_for_status()
        datos_json = respuesta.json()
        df_bovinos = pd.DataFrame(datos_json)
        print(f"Inventario Bovinos desde API: {len(df_bovinos)} registros.\n")

        # Renombramos 'MUNICIPIO' a 'municipio' y eliminamos espacios
        if 'MUNICIPIO' in df_bovinos.columns:
            df_bovinos.rename(columns={'MUNICIPIO': 'municipio'}, inplace=True)
        if 'municipio' in df_bovinos.columns:
            df_bovinos['municipio'] = df_bovinos['municipio'].astype(str).str.strip()

        # Renombramos 'Total Pastos (ha)' a 'total_pastos' para facilitar el manejo
        if 'Total Pastos (ha)' in df_bovinos.columns:
            df_bovinos.rename(columns={'Total Pastos (ha)': 'total_pastos'}, inplace=True)

        # Convertimos a numérico y rellenamos nulos con la mediana en las columnas de pasto y total_pastos
        columnas_imputar = ["pasto_mejorado", "pasto_natural", "pasto_corte", "total_pastos"]
        for col in columnas_imputar:
            if col in df_bovinos.columns:
                df_bovinos[col] = pd.to_numeric(df_bovinos[col], errors="coerce")
                mediana = df_bovinos[col].median()
                df_bovinos[col] = df_bovinos[col].fillna(mediana)

        return df_bovinos
    except Exception as e:
        print(f"Error al leer la API de Inventario Bovinos: {e}")
        return pd.DataFrame()

# 2. Integración de Fuentes Externas mediante Merge

def integrar_fuentes_externas(df_info, df_bovinos):
    """
    Integramos los DataFrames de Delitos Informáticos e Inventario Bovinos utilizando merge
    sobre la columna 'municipio'. Se realiza un inner join para conservar solo los registros coincidentes.
    """
    # Verificamos que ambas fuentes tengan la columna 'municipio'
    if 'municipio' not in df_info.columns:
        raise KeyError("El DataFrame de Delitos Informáticos no contiene la columna 'municipio'")
    if 'municipio' not in df_bovinos.columns:
        raise KeyError("El DataFrame de Inventario Bovinos no contiene la columna 'municipio'")
    
    # Realizamos el merge entre los dos DataFrames externos
    df_externos = pd.merge(df_info, df_bovinos, on="municipio", how="inner")
    return df_externos

def generar_reporte_enriquecimiento(df_base, df_info, df_bovinos, df_externos, df_final):
    """
    Generamos un reporte de auditoría que documenta:
      - Cantidad de registros y columnas en cada dataset original.
      - Cantidad de registros y columnas del dataset integrado (resultado del merge y concatenación).
      - Observaciones sobre la integración realizada.
    """
    reporte = []
    reporte.append("===== INFORME DE ENRIQUECIMIENTO DE DATOS =====")
    reporte.append(f"Fecha/Hora de Enriquecimiento: {datetime.now()}")
    reporte.append("")

    reporte.append("=== Dataset Base (EA2 - COVID Limpio) ===")
    reporte.append(f"  - Registros: {len(df_base)}")
    reporte.append(f"  - Columnas: {list(df_base.columns)}")
    reporte.append("")

    reporte.append("=== Delitos Informáticos (CSV) ===")
    reporte.append(f"  - Registros: {len(df_info)}")
    reporte.append(f"  - Columnas: {list(df_info.columns)}")
    reporte.append("")

    reporte.append("=== Inventario Anual de Bovinos (API) ===")
    reporte.append(f"  - Registros: {len(df_bovinos)}")
    reporte.append(f"  - Columnas: {list(df_bovinos.columns)}")
    reporte.append("")

    reporte.append("=== Fuentes Externas Integradas (Merge por 'municipio') ===")
    reporte.append(f"  - Registros: {len(df_externos)}")
    reporte.append(f"  - Columnas: {list(df_externos.columns)}")
    reporte.append("")

    reporte.append("=== Dataset Final Enriquecido ===")
    reporte.append(f"  - Registros (filas): {len(df_final)}")
    reporte.append(f"  - Columnas totales: {list(df_final.columns)}")
    reporte.append("")

    reporte.append("Observaciones:")
    reporte.append("  - Se integraron las fuentes externas (Delitos Informáticos e Inventario Bovinos) usando merge sobre la columna 'municipio'.")
    reporte.append("  - El dataset base (COVID limpio) no posee clave geográfica, por lo que se realizó una concatenación horizontal con una muestra representativa (444 filas) del dataset resultante de la integración de las fuentes externas.")
    reporte.append("  - Las columnas 'pasto_mejorado', 'pasto_natural', 'pasto_corte' y 'total_pastos' fueron convertidas a numérico y sus valores nulos imputados con la mediana.")
    
    return "\n".join(reporte)

# 3. Función Principal

def main():
    """
    Orquesta el proceso completo de enriquecimiento de datos:
      1. Carga del dataset base (COVID limpio).
      2. Lectura de Delitos Informáticos (CSV).
      3. Lectura del Inventario Anual de Bovinos (API).
      4. Integración de las fuentes externas mediante merge sobre 'municipio'.
      5. Concatenación horizontal de la muestra (444 filas) del dataset base con la muestra integrada de fuentes externas.
      6. Exportación del dataset final a CSV y generación de un reporte de auditoría en TXT.
    """
    print("\n=== Iniciando Proceso de Enriquecimiento (EA3) ===")

    # 1. Cargamos el dataset base (COVID limpio)
    df_base = cargar_dataset_limpio_desde_bd()

    # 2. Leemos los Delitos Informáticos (CSV)
    df_info = leer_delitos_informaticos_csv()

    # 3. Leemos el Inventario Anual de Bovinos (API)
    df_bovinos = leer_inventario_bovinos_api()

    # 4. Integramos las fuentes externas (merge sobre 'municipio')
    df_externos = integrar_fuentes_externas(df_info, df_bovinos)

    # Tomamos una muestra representativa de 444 filas de cada fuente
    df_base_444 = df_base.head(444).reset_index(drop=True)
    df_externos_444 = df_externos.head(444).reset_index(drop=True)

    # 5. Concatemanos horizontalmente el dataset base con la integración de fuentes externas
    df_final = pd.concat([df_base_444, df_externos_444], axis=1)

    # 6. Exportamos a CSV el dataset final enriquecido
    df_final.to_csv(RUTA_DATOS_ENRIQUECIDOS, index=False)
    print(f"Dataset enriquecido exportado en: {RUTA_DATOS_ENRIQUECIDOS}\n")

    # 7. Generamos el reporte de auditoría
    reporte = generar_reporte_enriquecimiento(df_base, df_info, df_bovinos, df_externos, df_final)
    with open(RUTA_REPORTE_ENRIQUECIMIENTO, "w", encoding="utf-8") as archivo_reporte:
        archivo_reporte.write(reporte)
    print(f"Reporte de enriquecimiento generado en: {RUTA_REPORTE_ENRIQUECIMIENTO}\n")

    print("=== Proceso de Enriquecimiento Finalizado ===\n")

if __name__ == "__main__":
    main()