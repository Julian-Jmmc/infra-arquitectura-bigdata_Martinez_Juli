import os
import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime


# Configuración de rutas
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RUTA_DB = os.path.join(BASE_DIR, "static", "db", "ingestion.db")
RUTA_CSV = os.path.join(BASE_DIR, "static", "xlsx", "datos_limpios.csv")
RUTA_AUDITORIA = os.path.join(BASE_DIR, "static", "auditoria", "informe_limpieza.txt")


def cargar_datos_desde_db():
    """
    Carga los datos de la tabla 'covid_data' desde la base de datos SQLite.
   
    Retorna:
        DataFrame con los datos extraídos.
    """
    conexion = sqlite3.connect(RUTA_DB)
    df = pd.read_sql_query("SELECT * FROM covid_data", conexion)
    conexion.close()
    return df


def simular_datos_sucios(df):
    """
    A partir del DataFrame original, simulamos la generación de datos "sucios" (DELTA),
    realizando las siguientes operaciones:
   
      1. Duplicar un 10% de los registros (añadiendo duplicados).
      2. Introducir valores nulos en algunas columnas numéricas.
      3. Crear la columna 'registro_nulo' con valores faltantes (tipo 'object').
      4. Forzar error de tipo en la columna 'positive', convirtiendo algunos valores a cadena.
      5. Duplicar columnas completas ('date' y 'positive') y crear una columna "columna_inutil"
         para luego demostrar cómo se eliminan en la limpieza.
   
    Parámetros:
        df: DataFrame original.
   
    Retorna:
        DataFrame con los datos "sucios".
    """
    df_sucio = df.copy()
   
    # 1. Duplicar un 10% de los registros
    filas_duplicadas = df_sucio.sample(frac=0.1, random_state=42)
    df_sucio = pd.concat([df_sucio, filas_duplicadas], ignore_index=True)
   
    # 2. Introducir valores nulos en columnas numéricas
    for columna in ['positive', 'death', 'hospitalizedCurrently']:
        indices = df_sucio.sample(frac=0.05, random_state=42).index
        df_sucio.loc[indices, columna] = None


    # 3. Crear la columna 'registro_nulo' como objeto para simular valores faltantes
    df_sucio['registro_nulo'] = pd.Series(np.nan, index=df_sucio.index, dtype=object)
    indices = df_sucio.sample(frac=0.2, random_state=42).index
    df_sucio.loc[indices, 'registro_nulo'] = "Dato Faltante"
   
    # 4. Forzar error de tipo en 'positive': convertir algunos valores a cadena
    indices = df_sucio.sample(frac=0.05, random_state=42).index
    df_sucio.loc[indices, 'positive'] = df_sucio.loc[indices, 'positive'].astype(str)
   
    # 5. Crear columnas duplicadas e inútiles
    df_sucio['fecha_duplicada'] = df_sucio['date']               # Duplicamos la columna 'date'
    df_sucio['positive_duplicada'] = df_sucio['positive']        # Duplicamos la columna 'positive'
    df_sucio['columna_inutil'] = "valor_repetido_en_todos"       # Columna sin información relevante
   
    return df_sucio


def operaciones_de_limpieza(df_sucio):
    """
    Aplicamos una serie de operaciones de limpieza y transformación sobre los datos "sucios".
    Las operaciones realizadas son:
   
      - Eliminación de duplicados (se crea una copia para evitar advertencias de pandas).
      - Conversión de columnas numéricas (p.ej. 'positive', 'death', 'hospitalizedCurrently')
        a valores numéricos, convirtiendo errores a NaN.
      - Imputación de valores nulos en las columnas numéricas usando la mediana.
      - Relleno de la columna 'registro_nulo' con "Sin Dato" donde falte información.
      - Eliminación de columnas duplicadas o innecesarias ('fecha_duplicada', 'positive_duplicada',
        'columna_inutil' y 'registro_nulo').
      - Creación de columnas de auditoría utilizando la fecha y hora actuales:
            * 'anio', 'mes' y 'dia' con la fecha actual.
            * 'fecha_completa' con la fecha y hora en formato "YYYY-MM-DD HH:MM:SS".
      - Renombrado de columnas a nombres en español.
      - Cálculo de las columnas:
            * 'tasa_positividad': (casos_positivos / total_resultados) * 100.
            * 'tasa_mortalidad': (fallecidos / casos_positivos) * 100.
   
    Parámetros:
        df_sucio: DataFrame con los datos "sucios".
   
    Retorna:
        Una tupla (df_limpio, detalles_auditoria), donde:
          - df_limpio es el DataFrame limpio y transformado.
          - detalles_auditoria es una lista de mensajes con el detalle de cada operación realizada.
    """
    detalles_auditoria = []


    # 1. Contabilizamos registros iniciales
    cantidad_inicial = len(df_sucio)
    detalles_auditoria.append(f"Registros iniciales: {cantidad_inicial}")


    # 2. Eliminamos registros duplicados (creamos una copia para evitar advertencias)
    df_limpio = df_sucio.drop_duplicates().copy()
    duplicados_eliminados = cantidad_inicial - len(df_limpio)
    detalles_auditoria.append(f"Duplicados eliminados: {duplicados_eliminados}")


    # 3. Convertimos columnas a numérico y rellenamos valores nulos con la mediana
    for columna in ['positive', 'death', 'hospitalizedCurrently']:
        df_limpio.loc[:, columna] = pd.to_numeric(df_limpio[columna], errors='coerce')
        mediana = df_limpio[columna].median()
        df_limpio.loc[:, columna] = df_limpio[columna].fillna(mediana)
        detalles_auditoria.append(f"Valores nulos en '{columna}' imputados con la mediana: {mediana}")


    # 4. Rellenamos valores nulos en 'registro_nulo' con "Sin Dato"
    # (Si no deseas conservar esta columna, la eliminaremos después)
    df_limpio.loc[:, 'registro_nulo'] = df_limpio['registro_nulo'].fillna("Sin Dato")
    detalles_auditoria.append("Valores nulos en 'registro_nulo' rellenados con 'Sin Dato'")


    # 5. Eliminamos las columnas duplicadas e innecesarias
    columnas_a_eliminar = ['fecha_duplicada', 'positive_duplicada', 'columna_inutil', 'registro_nulo']
    columnas_eliminadas = []
    for col in columnas_a_eliminar:
        if col in df_limpio.columns:
            df_limpio.drop(columns=[col], inplace=True)
            columnas_eliminadas.append(col)
   
    if columnas_eliminadas:
        detalles_auditoria.append(f"Columnas eliminadas por ser duplicadas/innecesarias: {', '.join(columnas_eliminadas)}")
    else:
        detalles_auditoria.append("No se encontraron columnas duplicadas o innecesarias para eliminar.")


    # 6. Asignamos la fecha y hora actuales para la auditoría
    fecha_actual = datetime.now()
    anio = fecha_actual.strftime("%Y")
    mes = fecha_actual.strftime("%m")
    dia = fecha_actual.strftime("%d")
    fecha_completa = fecha_actual.strftime("%Y-%m-%d %H:%M:%S")
   
    df_limpio.loc[:, 'anio'] = anio
    df_limpio.loc[:, 'mes'] = mes
    df_limpio.loc[:, 'dia'] = dia
    detalles_auditoria.append(f"Columnas 'anio', 'mes' y 'dia' establecidas a la fecha actual: {anio}-{mes}-{dia}")
   
    df_limpio.loc[:, 'fecha_completa'] = fecha_completa
    detalles_auditoria.append(f"Columna 'fecha_completa' establecida a la fecha y hora actual: {fecha_completa}")


    # 7. Renombramos columnas a nombres en español
    df_limpio = df_limpio.rename(columns={
        'date': 'fecha',
        'positive': 'casos_positivos',
        'death': 'fallecidos',
        'hospitalizedCurrently': 'hospitalizados',
        'totalTestResults': 'total_resultados',
        'positiveIncrease': 'incremento_positivos',
        'deathIncrease': 'incremento_fallecidos'
    })
    detalles_auditoria.append("Columnas renombradas a índices en español")


    # 8. Calculamos la columna 'tasa_positividad'
    df_limpio.loc[:, 'tasa_positividad'] = df_limpio.apply(
        lambda x: (x['casos_positivos'] / x['total_resultados'] * 100)
                  if x['total_resultados'] and x['total_resultados'] > 0 else 0,
        axis=1
    )
    detalles_auditoria.append("Columna 'tasa_positividad' calculada como (casos_positivos/total_resultados)*100")


    # 9. Calculamos la columna 'tasa_mortalidad'
    df_limpio.loc[:, 'tasa_mortalidad'] = df_limpio.apply(
        lambda x: (x['fallecidos'] / x['casos_positivos'] * 100)
                  if x['casos_positivos'] and x['casos_positivos'] > 0 else 0,
        axis=1
    )
    detalles_auditoria.append("Columna 'tasa_mortalidad' calculada como (fallecidos/casos_positivos)*100")


    # 10. Registramos la cantidad final de registros
    cantidad_final = len(df_limpio)
    detalles_auditoria.append(f"Registros finales: {cantidad_final}")


    return df_limpio, detalles_auditoria


def exportar_datos_limpios(df_limpio, detalles_auditoria):
    """
    Exporta el DataFrame limpio a un archivo CSV y genera un informe de auditoría en un archivo de texto.
   
    Parámetros:
        df_limpio: DataFrame con los datos limpios.
        detalles_auditoria: Lista de mensajes que describen el proceso de limpieza.
    """
    df_limpio.to_csv(RUTA_CSV, index=False)
   
    with open(RUTA_AUDITORIA, "w") as archivo:
        archivo.write("\n".join(detalles_auditoria))
   
    print(f"Archivo CSV de datos limpios generado en: {RUTA_CSV}")
    print(f"Archivo de auditoría generado en: {RUTA_AUDITORIA}")


def actualizar_tabla_limpia(df_limpio):
    """
    Crea o actualiza la tabla 'covid_data_cleaned' en la base de datos SQLite con el DataFrame limpio.
   
    Parámetros:
        df_limpio: DataFrame con los datos limpios.
    """
    conexion = sqlite3.connect(RUTA_DB)
    conexion.execute("DROP TABLE IF EXISTS covid_data_cleaned;")
    df_limpio.to_sql("covid_data_cleaned", conexion, if_exists="replace", index=False)
    conexion.close()
    print("Tabla 'covid_data_cleaned' creada en la base de datos con los datos limpios.")


def main():
    """
    Función principal que orquesta el proceso completo:
      1. Carga los datos desde la base de datos.
      2. Simula la generación de datos sucios.
      3. Aplica las operaciones de limpieza y transformación.
      4. Exporta el DataFrame limpio a CSV y genera un informe de auditoría.
      5. Actualiza la base de datos con la nueva tabla de datos limpios.
    """
    print("Iniciando proceso de limpieza y preprocesamiento de datos...")


    # 1. Cargar datos desde la base de datos
    df = cargar_datos_desde_db()
    print(f"Datos extraídos de la base de datos: {len(df)} registros")


    # 2. Simular datos sucios (DELTA)
    df_sucio = simular_datos_sucios(df)
    print(f"Datos sucios simulados: {len(df_sucio)} registros (incluye duplicados y valores nulos)")


    # 3. Aplicar operaciones de limpieza y transformación
    df_limpio, detalles_auditoria = operaciones_de_limpieza(df_sucio)
    print("Operaciones de limpieza y transformación aplicadas")


    # 4. Exportar los datos limpios y generar el informe de auditoría
    exportar_datos_limpios(df_limpio, detalles_auditoria)


    # 5. Actualizar la base de datos con la nueva tabla de datos limpios
    actualizar_tabla_limpia(df_limpio)


    print("Proceso de limpieza completado exitosamente.")


if __name__ == "__main__":
    main()
