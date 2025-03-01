import os
import json
import sqlite3
import requests
import pandas as pd
import datetime


# Configuración de rutas
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "static", "db", "ingestion.db")
XLSX_PATH = os.path.join(BASE_DIR, "static", "xlsx", "ingestion.xlsx")
AUDIT_PATH = os.path.join(BASE_DIR, "static", "auditoria", "ingestion.txt")


# Asegurar carpetas
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
os.makedirs(os.path.dirname(XLSX_PATH), exist_ok=True)
os.makedirs(os.path.dirname(AUDIT_PATH), exist_ok=True)


def extraer_datos_api():
    """Extrae datos del API de COVID-19"""
    url = "https://api.covidtracking.com/v1/us/daily.json"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ Error al extraer datos del API: {e}")
        raise


def crear_db():
    """Crea la base de datos y tabla para COVID-19"""
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
        print(f"❌ Error al crear la base de datos: {e}")
        raise


def insertar_datos(conn, datos):
    """Inserta datos de COVID-19 en la DB"""
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM covid_data;")
       
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
        print(f"❌ Error al insertar datos: {e}")
        raise


def generar_archivo_muestra(conn):
    """Genera muestra en Excel con datos relevantes"""
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
        print(f"Archivo de muestra generado en: {XLSX_PATH}")
    except Exception as e:
        print(f"❌ Error al generar muestra: {e}")
        raise


def generar_auditoria(api_datos, conn):
    """Auditoría comparativa COVID-19"""
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM covid_data;")
        count_db = cursor.fetchone()[0]
        count_api = len(api_datos)
       
        auditoria = (
            f"Registros COVID extraídos: {count_api}\n"
            f"Registros en DB: {count_db}\n"
            f"Consistencia: {'OK' if count_api == count_db else 'ERROR'}\n"
            f"Última fecha registrada: {api_datos[0]['date'] if api_datos else 'N/A'}\n"
            f"Total casos positivos: {api_datos[0]['positive'] if api_datos else 'N/A'}\n"
            f"Total fallecidos: {api_datos[0]['death'] if api_datos else 'N/A'}\n"
            f"Fecha/Hora auditoría: {datetime.datetime.now()}\n"
        )
       
        with open(AUDIT_PATH, "w") as f:
            f.write(auditoria)
        print(f"Auditoría generada en: {AUDIT_PATH}")
    except Exception as e:
        print(f"❌ Error en auditoría: {e}")
        raise


def main():
    try:
        print("Iniciando ingesta de datos COVID...")
       
        api_datos = extraer_datos_api()
        print(f"Datos obtenidos: {len(api_datos)} registros históricos")


        conn = crear_db()
        insertar_datos(conn, api_datos)
        print("Datos COVID almacenados en DB")


        generar_archivo_muestra(conn)
        generar_auditoria(api_datos, conn)
       
        conn.close()
        print("Proceso completado exitosamente")
    except Exception as e:


        print(f"❌ Error en proceso principal: {e}")
        raise


if __name__ == "__main__":
    main()