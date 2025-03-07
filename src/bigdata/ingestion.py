import os
import sqlite3
import requests
import pandas as pd
import datetime


# Configuramos las Rutas para la Base de Datos, el Archivo de Excel y la Auditoría
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "static", "db", "ingestion.db")
XLSX_PATH = os.path.join(BASE_DIR, "static", "xlsx", "ingestion.xlsx")
AUDIT_PATH = os.path.join(BASE_DIR, "static", "auditoria", "ingestion.txt")


# Nos Aseguramos que las Carpetas de Almacenamiento Existan
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
os.makedirs(os.path.dirname(XLSX_PATH), exist_ok=True)
os.makedirs(os.path.dirname(AUDIT_PATH), exist_ok=True)


def extraer_datos_api():
    """Obtenemos los Datos Históricos del COVID-19 en EE.UU. Desde una API"""
    url = "https://api.covidtracking.com/v1/us/daily.json"
    try:
        response = requests.get(url)
        response.raise_for_status() # Lanzamos Error si la Respuesta no es Exitosa
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ Error al Extraer los Datos del API: {e}")
        raise


def crear_db():
    """Creamos la Base de Datos SQLite y la Tabla si no Existe"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS covid_data (
                hash TEXT PRIMARY KEY,
                date INTEGER,
                positive INTEGER,
                death INTEGER,
                hospitalizedCurrently INTEGER,
                totalTestResults INTEGER,
                positiveIncrease INTEGER,
                deathIncrease INTEGER,
                lastModified TEXT
            );
        """)
        conn.commit()
        return conn
    except sqlite3.Error as e:
        print(f"❌ Error al Crear la Base de Datos: {e}")
        raise


def insertar_datos(conn, datos):
    """Guardamos los Datos Obtenidos en la Base de Datos"""
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM covid_data;")  # Limpiamos la Tabla Antes de Insertar Nuevos Datos
       
        for registro in datos:
            cursor.execute("""
                INSERT INTO covid_data (
                    hash,
                    date,
                    positive,
                    death,
                    hospitalizedCurrently,
                    totalTestResults,
                    positiveIncrease,
                    deathIncrease,
                    lastModified
                ) VALUES (?,?,?,?,?,?,?,?,?)
            """, (
                registro.get("hash"),
                registro.get("date"),
                registro.get("positive"),
                registro.get("death"),
                registro.get("hospitalizedCurrently"),
                registro.get("totalTestResults"),
                registro.get("positiveIncrease"),
                registro.get("deathIncrease"),
                registro.get("lastModified")
            ))
        conn.commit()
    except sqlite3.Error as e:
        print(f"❌ Error al Insertar Datos: {e}")
        raise


def generar_archivo_muestra(conn):
    """Creamos un Archivo de Excel con 50 Registros de Muestra"""
    try:
        query = """
            SELECT
                date,
                positive,
                death,
                hospitalizedCurrently,
                totalTestResults,
                positiveIncrease,
                deathIncrease
            FROM covid_data
            ORDER BY date DESC
            LIMIT 50
        """
        df = pd.read_sql_query(query, conn)
        df["timestamp"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        df.to_excel(XLSX_PATH, index=False)
        print(f"Archivo de Excel Generado en: {XLSX_PATH}")
    except Exception as e:
        print(f"❌ Error al Generar el Archivo de Excel: {e}")
        raise


def generar_auditoria(api_datos, conn):
    """Generamos un Pequeño Informe de Auditoría Comparando la API y la Base de Datos"""
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM covid_data;")
        count_db = cursor.fetchone()[0]
        count_api = len(api_datos)
       
        auditoria = (
            f"Registros COVID-19 Extraidos: {count_api}\n"
            f"Registros en DB: {count_db}\n"
            f"Consistencia: {'OK' if count_api == count_db else 'ERROR'}\n"
            f"Ultima Fecha Registrada: {api_datos[0]['date'] if api_datos else 'N/A'}\n"
            f"Total Casos Positivos: {api_datos[0]['positive'] if api_datos else 'N/A'}\n"
            f"Total Fallecidos: {api_datos[0]['death'] if api_datos else 'N/A'}\n"
            f"Fecha/Hora Auditoria: {datetime.datetime.now()}\n"
        )
       
        with open(AUDIT_PATH, "w") as f:
            f.write(auditoria)
        print(f"Auditoría Generada en: {AUDIT_PATH}")
    except Exception as e:
        print(f"❌ Error al Generar la Auditoría: {e}")
        raise


def main():
    """Orquestamos el Flujo de Extracción, Almacenamiento y Auditoría de Datos"""
    try:
        print("Comenzando la Ingesta de Datos de COVID-19...")
       
        api_datos = extraer_datos_api()
        print(f"¡Datos obtenidos! Se han obtenido {len(api_datos)} Registros Históricos del COVID-19 en EE.UU")


        conn = crear_db()
        insertar_datos(conn, api_datos)
        print("Los Datos del COVID-19 se han Almacenado en la Base de  Datos SQLite")


        generar_archivo_muestra(conn)
        generar_auditoria(api_datos, conn)
       
        conn.close()
        print("¡Proceso Finalizado con Éxito!")
    except Exception as e:
        print(f"❌ Error en el Proceso Principal: {e}")
        raise


if __name__ == "__main__":
    main()