import os
import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime

"""
Configuramos las rutas para conectar a la Base de Datos,
generamos los archivos de CSV y auditoría en la fase de limpieza y preprocesamiento de Datos.
"""
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RUTA_DB = os.path.join(BASE_DIR, "static", "db", "ingestion.db")

# CSV de datos limpios
RUTA_CSV_LIMPIO = os.path.join(BASE_DIR, "static", "xlsx", "Tabla_Datos_Limpios.csv")

# CSV de datos sucios para muestra
RUTA_CSV_SUCIO = os.path.join(BASE_DIR, "static", "xlsx", "Tabla_Datos_Sucios.csv")

# Auditoría de Preprocesamiento y Limpieza
RUTA_AUDITORIA = os.path.join(BASE_DIR, "static", "auditoria", "Informe_Limpieza.txt")

def cargar_datos_desde_db():
    """
    Cargamos los datos de la tabla 'covid_data' desde la base de datos SQLite.
    
    Retorna:
        DataFrame con los datos extraídos.
    """
    conexion = sqlite3.connect(RUTA_DB)
    df = pd.read_sql_query("SELECT * FROM covid_data", conexion)
    conexion.close()
    return df

def exportar_datos_sucios(df_sucio):
    """
    Exportamos el DataFrame sucio a un archivo CSV para tener un registro
    de cómo quedaron los datos antes de la limpieza.
    """
    df_sucio.to_csv(RUTA_CSV_SUCIO, index=False)
    print(f"\nArchivo CSV de Datos Sucios Generado en: {RUTA_CSV_SUCIO}")

def guardar_tabla_sucia_en_db(df_sucio):
    """
    Guardamos la tabla sucia en la base de datos bajo el nombre 'covid_data_dirty'.
    Con la finalidad de tener un registro de la tabla sucia antes de limpiar.
    """
    conexion = sqlite3.connect(RUTA_DB)
    conexion.execute("DROP TABLE IF EXISTS covid_data_dirty;")
    df_sucio.to_sql("covid_data_dirty", conexion, if_exists="replace", index=False)
    conexion.close()
    print("\nTabla 'covid_data_dirty' creada en la Base de Datos con los Datos Sucios.\n")

def simular_datos_sucios(df):
    """
    A partir del DataFrame original, simulamos la generación de datos "sucios" (DELTA),
    realizando las siguientes operaciones:
    
      1. Duplicar un 20% de los registros (añadiendo duplicados).
      2. Introducir valores nulos en columnas numéricas 
         (p.ej. 'positive', 'death', 'hospitalizedCurrently', 'totalTestResults').
      3. Crear una columna 'registro_nulo' con valores faltantes (tipo 'object').
      4. Forzar error de tipo en 'positive' y 'death', convirtiendo algunos valores a cadena.
      5. Duplicar columnas ('date', 'positive', 'death') y crear columnas "columna_inutil_1", "columna_inutil_2".
      6. Crear una 'fecha_sucia' duplicada con un 5% de valores nulos.
    """
    df_sucio = df.copy()
    
    # 1. Duplicamos un 20% de los registros
    filas_duplicadas = df_sucio.sample(frac=0.20, random_state=42)
    df_sucio = pd.concat([df_sucio, filas_duplicadas], ignore_index=True)
    
    # 2. Introducimos valores nulos en las columnas numéricas
    columnas_numericas = ['positive', 'death', 'hospitalizedCurrently', 'totalTestResults']
    for col in columnas_numericas:
        indices = df_sucio.sample(frac=0.08, random_state=42).index  # 8% nulos
        df_sucio.loc[indices, col] = None

    # 3. Creamos la columna 'registro_nulo' como objeto para simular valores faltantes
    df_sucio['registro_nulo'] = pd.Series(np.nan, index=df_sucio.index, dtype=object)
    indices_regnull = df_sucio.sample(frac=0.25, random_state=42).index  # 25% de valores
    df_sucio.loc[indices_regnull, 'registro_nulo'] = "Dato Faltante"
    
    # 4. Forzamos error de tipo en 'positive' y 'death': convertir algunos valores a cadena
    for col in ['positive', 'death']:
        indices_error_tipo = df_sucio.sample(frac=0.07, random_state=42).index  # 7% a string
        df_sucio.loc[indices_error_tipo, col] = df_sucio.loc[indices_error_tipo, col].astype(str)
    
    # 5. Creamos columnas duplicadas e inservibles
    df_sucio['fecha_duplicada'] = df_sucio['date']
    df_sucio['positive_duplicada'] = df_sucio['positive']
    df_sucio['death_duplicada'] = df_sucio['death']
    df_sucio['columna_inutil_1'] = "valor_repetido_en_todos_1"
    df_sucio['columna_inutil_2'] = "valor_repetido_en_todos_2"
    
    # 6. Creamos 'fecha_sucia' con un 5% de valores nulos
    df_sucio['fecha_sucia'] = df_sucio['date']
    indices_datesucias = df_sucio.sample(frac=0.05, random_state=42).index 
    df_sucio.loc[indices_datesucias, 'fecha_sucia'] = None
    
    return df_sucio

def operaciones_de_limpieza(df_sucio):
    """
    Aplicamos una serie de operaciones de limpieza y transformación sobre los datos "sucios".
    Las operaciones realizadas son:
    
      - Estadísticas antes de limpiar (nulos, duplicados, etc.).
      - Eliminación de duplicados.
      - Conversión de columnas numéricas a valores numéricos, convirtiendo errores a NaN.
      - Imputación de valores nulos en las columnas numéricas usando la mediana.
      - Relleno de la columna 'registro_nulo' con "Sin Dato".
      - Eliminación de columnas duplicadas o innecesarias.
      - Creación de columnas de auditoría (anio_auditoria, mes_auditoria, dia_auditoria, fecha_completa_auditoria).
      - Renombrado de columnas a nombres en español.
      - Cálculo de 'tasa_positividad' y 'tasa_mortalidad'.
      - Eliminación final de duplicados para asegurar que no queden registros idénticos.
      - Estadísticas después de limpiar (nulos, duplicados, etc.).
    """
    detalles_auditoria = []

    # ====== Estadísticas antes de limpiar ======
    cantidad_inicial = len(df_sucio)
    duplicados_inicial = cantidad_inicial - len(df_sucio.drop_duplicates())
    nulos_inicial = df_sucio.isnull().sum().to_dict()

    detalles_auditoria.append("=== ESTADO INICIAL DE LA TABLA SUCIA ===")
    detalles_auditoria.append(f"Registros Iniciales: {cantidad_inicial}")
    detalles_auditoria.append(f"Duplicados Iniciales: {duplicados_inicial}")
    detalles_auditoria.append(f"Nulos Iniciales (Por Columna): {nulos_inicial}")
    detalles_auditoria.append("")

    # 1. Eliminamos registros duplicados
    df_limpio = df_sucio.drop_duplicates().copy()
    duplicados_eliminados = cantidad_inicial - len(df_limpio)
    detalles_auditoria.append(f"Duplicados Eliminados: {duplicados_eliminados}")

    # 2. Convertimos columnas a numérico y rellenamos valores nulos con la mediana
    columnas_numericas = ['positive', 'death', 'hospitalizedCurrently', 'totalTestResults']
    for columna in columnas_numericas:
        df_limpio.loc[:, columna] = pd.to_numeric(df_limpio[columna], errors='coerce')
        mediana = df_limpio[columna].median()
        df_limpio.loc[:, columna] = df_limpio[columna].fillna(mediana)
        detalles_auditoria.append(f"Valores Nulos en '{columna}' Imputados con la Mediana: {mediana}")

    # 3. Rellenamos valores nulos en 'registro_nulo' con "Sin Dato"
    df_limpio.loc[:, 'registro_nulo'] = df_limpio['registro_nulo'].fillna("Sin Dato")
    detalles_auditoria.append("Valores Nulos en 'registro_nulo' Rellenados con 'Sin Dato'")

    # 4. Eliminamos las columnas duplicadas e innecesarias
    columnas_a_eliminar = [
        'fecha_duplicada', 'positive_duplicada', 'death_duplicada',
        'columna_inutil_1', 'columna_inutil_2', 'registro_nulo',
        'fecha_sucia' 
    ]
    columnas_eliminadas = []
    for col in columnas_a_eliminar:
        if col in df_limpio.columns:
            df_limpio.drop(columns=[col], inplace=True)
            columnas_eliminadas.append(col)
    
    if columnas_eliminadas:
        detalles_auditoria.append(f"Columnas Eliminadas por ser Duplicadas e Innecesarias: {', '.join(columnas_eliminadas)}")
    else:
        detalles_auditoria.append("No se Encontraron Columnas Duplicadas o Innecesarias para Eliminar.")

    # 5. Asignamos la fecha y hora actuales para la auditoría
    fecha_actual = datetime.now()
    anio = fecha_actual.strftime("%Y")
    mes = fecha_actual.strftime("%m")
    dia = fecha_actual.strftime("%d")
    fecha_completa = fecha_actual.strftime("%Y-%m-%d %H:%M:%S")
    
    df_limpio.loc[:, 'anio_auditoria'] = anio
    df_limpio.loc[:, 'mes_auditoria'] = mes
    df_limpio.loc[:, 'dia_auditoria'] = dia
    detalles_auditoria.append(f"Columnas 'anio_auditoria', 'mes_auditoria' y 'dia_auditoria' Establecidas a la Fecha Actual: {anio}-{mes}-{dia}")
    
    df_limpio.loc[:, 'fecha_completa_auditoria'] = fecha_completa
    detalles_auditoria.append(f"Columna 'fecha_completa_auditoria' Establecida a la Fecha y Hora Actual: {fecha_completa}")

    # 6. Renombramos columnas a nombres en español
    df_limpio = df_limpio.rename(columns={
        'date': 'fecha',
        'positive': 'casos_positivos',
        'death': 'fallecidos',
        'hospitalizedCurrently': 'hospitalizados',
        'totalTestResults': 'total_resultados',
        'positiveIncrease': 'incremento_positivos',
        'deathIncrease': 'incremento_fallecidos',
        'lastModified': 'ultima_modificacion'
    })
    detalles_auditoria.append("Columnas Renombradas a Índices en Español")

    # 7. Calculamos la columna 'tasa_positividad'
    df_limpio.loc[:, 'tasa_positividad'] = df_limpio.apply(
        lambda x: (x['casos_positivos'] / x['total_resultados'] * 100)
                  if x['total_resultados'] and x['total_resultados'] > 0 else 0,
        axis=1
    )
    detalles_auditoria.append("Columna 'tasa_positividad' Calculada como (casos_positivos/total_resultados)*100")

    # 8. Calculamos la columna 'tasa_mortalidad'
    df_limpio.loc[:, 'tasa_mortalidad'] = df_limpio.apply(
        lambda x: (x['fallecidos'] / x['casos_positivos'] * 100)
                  if x['casos_positivos'] and x['casos_positivos'] > 0 else 0,
        axis=1
    )
    detalles_auditoria.append("Columna 'tasa_mortalidad' Calculada como (fallecidos/casos_positivos)*100")

    # 9. Eliminamos duplicados finales para asegurar que no queden registros idénticos
    registros_antes = len(df_limpio)
    df_limpio = df_limpio.drop_duplicates()
    duplicados_final = registros_antes - len(df_limpio)
    detalles_auditoria.append(f"Duplicados Finales Eliminados: {duplicados_final}")

    # ====== Estadísticas después de limpiar ======
    cantidad_final = len(df_limpio)
    nulos_final = df_limpio.isnull().sum().to_dict()

    detalles_auditoria.append("")
    detalles_auditoria.append("=== ESTADO FINAL DE LA TABLA LIMPIA ===")
    detalles_auditoria.append(f"Registros Finales: {cantidad_final}")
    detalles_auditoria.append(f"Nulos Finales (por columna): {nulos_final}")

    return df_limpio, detalles_auditoria

def exportar_datos_limpios(df_limpio, detalles_auditoria):
    """
    Exportamos el DataFrame limpio a un archivo CSV y generamos el informe de auditoría en un archivo de texto.
    
    Parámetros:
        df_limpio: DataFrame con los datos limpios.
        detalles_auditoria: Lista de mensajes que describen el proceso de limpieza.
    """
    df_limpio.to_csv(RUTA_CSV_LIMPIO, index=False)
    
    with open(RUTA_AUDITORIA, "w", encoding="utf-8") as archivo:
        archivo.write("\n".join(detalles_auditoria))
    
    print(f"\nArchivo CSV de Datos Limpios Generado en: {RUTA_CSV_LIMPIO}")
    print(f"\nArchivo de Auditoría Generado en: {RUTA_AUDITORIA}")

def actualizar_tabla_limpia(df_limpio):
    """
    Creamos o actualizamos la tabla 'covid_data_cleaned' en la base de datos SQLite con el DataFrame limpio.
    
    Parámetros:
        df_limpio: DataFrame con los datos limpios.
    """
    conexion = sqlite3.connect(RUTA_DB)
    conexion.execute("DROP TABLE IF EXISTS covid_data_cleaned;")
    df_limpio.to_sql("covid_data_cleaned", conexion, if_exists="replace", index=False)
    conexion.close()
    print("\nTabla 'covid_data_cleaned' Creada/Actualizada en la Base de Datos con los Datos Limpios.\n")

def main():
    """
    Función principal que orquesta el proceso completo:
      1. Carga los datos desde la base de datos.
      2. Simula la generación de datos sucios (20% duplicados).
      3. Exporta el DataFrame sucio a CSV.
      4. Guarda la tabla sucia en la base de datos (covid_data_dirty).
      5. Aplica las operaciones de limpieza y transformación.
      6. Exporta el DataFrame limpio a CSV y genera un informe de auditoría (antes y después).
      7. Actualiza la base de datos con la nueva tabla de datos limpios (covid_data_cleaned).
    """
    print("\nIniciando Proceso de Limpieza y Preprocesamiento de Datos...\n")

    # 1. Cargamos datos desde la base de datos
    df = cargar_datos_desde_db()
    print(f"Datos Extraídos de la Base de Datos: {len(df)} Registros\n")

    # 2. Simulamos datos sucios (DELTA)
    df_sucio = simular_datos_sucios(df)
    print(f"\nDatos Sucios Simulados: {len(df_sucio)} Registros (Incluye Duplicados y Valores Nulos)\n")

    # 3. Exportamos los datos sucios a CSV
    exportar_datos_sucios(df_sucio)

    # 4. Guardamos la tabla sucia en la base de datos
    guardar_tabla_sucia_en_db(df_sucio)

    # 5. Aplicamos operaciones de limpieza y transformación
    df_limpio, detalles_auditoria = operaciones_de_limpieza(df_sucio)
    print("\nOperaciones de Limpieza y Transformación Aplicadas\n")

    # 6. Exportamos los datos limpios y generamos el informe de auditoría
    exportar_datos_limpios(df_limpio, detalles_auditoria)

    # 7. Actualizamos la base de datos con la nueva tabla de datos limpios
    actualizar_tabla_limpia(df_limpio)

    print("\n¡Preprocesamiento y Limpieza de Datos Completado con Éxito!\n")

if __name__ == "__main__":
    main()