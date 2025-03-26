---

# infra-arquitectura-bigdata_Martinez_Juli
 🚀

<div align="center">
  <h1>Infraestructura y Arquitectura para Big Data</h1>
  <h2>
    Proyecto Integrador
    <br><br>
    Parte 1 EA1 - Ingestión de Datos desde un API 📊  
    ㅤ <br><br>
    Parte 2 EA2 - Preprocesamiento y Limpieza de Datos simulando una Plataforma de Big Data en la Nube 🔍🚀
    ㅤ <br><br>
    Parte 3 EA3 - Enriquecimiento de Datos simulando una Plataforma de Big Data en la Nube 🌐📈
  </h2>
</div>

---

Este proyecto es un flujo completo de datos de **COVID-19** que abarca desde la ingesta hasta el preprocesamiento, limpieza y enriquecimiento. En la fase **EA1**, se extraen datos históricos desde la API pública del **COVID Tracking Project** 😷, se almacenan en **SQLite** 💾, se genera un archivo **Excel** de muestra 📈 y se crea un reporte de auditoría 📋. Además, se implementa un flujo de integración continua en **GitHub Actions** 🤖 que automatiza la ejecución del script y la construcción de la imagen Docker. 🐳

---

> **Importante:**  
> El COVID Tracking Project finalizó la recolección de datos el **7 de marzo de 2021** 📆, por lo que la información disponible es histórica y no se actualiza más allá de esa fecha.

---

En la **fase 2** de este proyecto, 🔍 a partir de los datos obtenidos se simulan condiciones de "datos sucios" mediante la duplicación de registros 📑, la inserción de valores nulos ⚠️, la forzada conversión de tipos 🔄 y la creación de columnas adicionales ➕. Posteriormente, se aplican operaciones de limpieza y transformación: se eliminan duplicados 🗑️, se convierten columnas a formatos numéricos (imputando valores nulos con la mediana) 🔢, se eliminan columnas redundantes ✂️, se añaden columnas de auditoría (fecha y hora) ⏰, se renombran las columnas a nombres en español 📝 y se calculan indicadores clave como la tasa de positividad 📊 y la tasa de mortalidad ⚰️. Como resultado, se genera un archivo CSV con los datos limpios y otro con los datos sucios para muestra 📂, se crea un informe de auditoría detallado 📋 y se actualiza la base de datos con 2 tablas nuevas la tabla limpia y la tabla sucia 🗄️.

---

En la **fase 3 (EA3)**, 🌐 se enriquece el dataset base integrando datos externos de delitos informáticos y un inventario anual de bovinos en Antioquia, procesando y unificando esta información con el dataset limpio de COVID-19 para generar un conjunto de datos más completo y útil para análisis.

---

## 1. Descripción General 🌟

### EA1 – Ingesta de Datos
Este proyecto realiza las siguientes tareas:

* 📥 **Descarga de datos:**  
  Descarga datos históricos de COVID-19 de los EE.UU. desde la API del COVID Tracking Project.
  - **Página web del API:**  
    [https://covidtracking.com/data/api](https://covidtracking.com/data/api)
  - **Formato JSON:**  
    [https://api.covidtracking.com/v1/us/daily.json](https://api.covidtracking.com/v1/us/daily.json)
  - **Formato CSV (opcional):**  
    [https://api.covidtracking.com/v1/us/daily.csv](https://api.covidtracking.com/v1/us/daily.csv)
  - **Recurso adicional:**  
    [Las mejores APIs públicas para practicar](https://ed.team/blog/las-mejores-apis-publicas-para-practicar)

* 🗄️ **Base de datos SQLite:**  
  Crea (o actualiza) una base de datos para almacenar la información.

* 📊 **Generación de archivo Excel:**  
  Genera un archivo Excel con los últimos 50 registros a modo de muestra.

* 📝 **Informe de auditoría:**  
  Crea un informe de auditoría (archivo de texto) comparando la cantidad de registros en la API y en la base de datos.

* 🚀 **Automatización:**  
  Automatiza la ejecución de la ingesta y la construcción de la imagen Docker a través de GitHub Actions.

---

Al finalizar, tendrás:

* 🗃️ Una base de datos ingestion.db.
* 📑 Un archivo Excel ingestion.xlsx con 50 registros en la carpeta xlsx.
* 📜 Un archivo de auditoría ingestion.txt con un resumen de los datos procesados.
* 🤖 Un pipeline en GitHub Actions que ejecuta estos pasos automáticamente.

---

## 2. Acerca de la API (COVID Tracking Project) 📡

El COVID Tracking Project fue una iniciativa que recopiló datos de COVID-19 en EE.UU. hasta el **7 de marzo de 2021**. A partir de esa fecha, la recolección de datos se detuvo y la información quedó congelada como un registro histórico. Algunas consideraciones importantes:

* **URL Base:**  
  [https://api.covidtracking.com](https://api.covidtracking.com)
* **Endpoint de Datos Históricos (JSON):**  
  [https://api.covidtracking.com/v1/us/daily.json](https://api.covidtracking.com/v1/us/daily.json)
  - *También disponible en CSV:*  
    [https://api.covidtracking.com/v1/us/daily.csv](https://api.covidtracking.com/v1/us/daily.csv)
* **Formato de Respuesta:**  
  JSON
* **Licencia:**  
  CC BY 4.0 https://covidtracking.com/about-data/license

**Campos Principales:**
* date: Fecha del reporte
* positive: Casos positivos acumulados
* death: Fallecimientos confirmados o probables
* hospitalizedCurrently: Hospitalizados
* totalTestResults: Número total de tests reportados
* positiveIncrease: Nuevos casos
* deathIncrease: Nuevas muertes
* lastModified: Última fecha/hora de actualización

---

## 3. EA2 – Limpieza y Preprocesamiento de Datos  
A partir de la base de datos generada en EA1 se simulan "datos sucios" y se aplican las siguientes operaciones:

* **Simulación de datos sucios:**  
  - 🔁 **Duplicación de un 20% de registros.**
  - ⚠️ **Inserción de valores nulos en columnas numéricas.**
  - ➕ **Creación de columnas adicionales** (por ejemplo, 'registro_nulo', columnas duplicadas como 'fecha_duplicada', 'positive_duplicada', 'death_duplicada', 'columna_inutil_1', 'columna_inutil_2' y 'fecha_sucia').
  - 🔄 **Forzado error de tipo** en las columnas 'positive' y 'death' (convirtiendo un 7% de los valores a cadena).

* **Limpieza y transformación:**  
  - 🗑️ **Eliminación de duplicados.**
  - 🔢 **Conversión de columnas a tipos numéricos** e imputación de valores nulos con la mediana.
  - 🧹 **Relleno de valores faltantes** en 'registro_nulo' con "Sin Dato".
  - ✂️ **Eliminación de columnas inservibles y duplicadas** (como 'fecha_duplicada', 'positive_duplicada', 'death_duplicada', 'columna_inutil_1', 'columna_inutil_2' y 'fecha_sucia').
  - ⏰ **Generación de nuevas columnas de auditoría:**  
    Se añaden columnas 'anio_auditoria', 'mes_auditoria', 'dia_auditoria' y 'fecha_completa_auditoria' con la fecha y hora actuales (por ejemplo, 2025-03-10 y 2025-03-10 13:48:16).
  - 📝 **Renombrado de columnas a nombres en español.**
  - 📊 **Cálculo de indicadores clave:**  
    - **Tasa de positividad:** Calculada como (casos_positivos / total_resultados) * 100.  
    - **Tasa de mortalidad:** Calculada como (fallecidos / casos_positivos) * 100.

* **Auditoría del Proceso de Limpieza:**  
  Se genera un informe de auditoría que detalla el estado de los datos antes y después de la limpieza

* **Salida:**  
  - 📁 **Archivos CSV:** Se generan 2 archivos uno con los datos limpios y otro con los datos sucios (Tabla_Datos_Limpios.csv, Tabla_Datos_Sucios.csv).  
  - 📋 **Informe de auditoría detallado:** Se crea el archivo Informe_Limpieza.txt.  
  - 🗄️ **Actualización de la base de datos:** Se agrega la nueva tabla covid_data_cleaned y también se agrega covid_data_dirty para muestra de los datos sucios.

---

## 4. EA3 – Enriquecimiento de Datos 🔍📊  

En esta fase se integra información adicional proveniente de fuentes externas para complementar los datos de COVID-19. En particular, se realiza lo siguiente:  

### 🌍 Fuentes Externas:  
- **🖥️ Delitos Informáticos (CSV):** https://www.datos.gov.co/Justicia-y-Derecho/Delitos-Informaticos-V1/wxd8-ucns/about_data  
  Se extrae información de un archivo CSV, renombrando y normalizando sus columnas (por ejemplo, se renombra `MUNICIPIO_HECHO` a `municipio`).  

- **🐄📡 Inventario Anual de Bovinos (API):** https://www.datos.gov.co/resource/fy9z-8zxt.json
- https://www.datos.gov.co/Agricultura-y-Desarrollo-Rural/Inventario-anual-de-Bovinos-en-Antioquia-desde-200/fy9z-8zxt/about_data
  Se consulta una API que provee información sobre bovinos en Antioquia.  
  - 🔄 Se renombra la columna `MUNICIPIO` a `municipio` y se normalizan espacios y formatos.  
  - 🌿 Se procesan las columnas relacionadas con pastos: `pasto_mejorado`, `pasto_natural`, `pasto_corte` y `Total Pastos (ha)` (renombrada a `total_pastos`).  
  - 🛠️ Los valores nulos en estas columnas se imputan con la mediana de cada una, garantizando así que la información no presente huecos que afecten el análisis.  

### 🔗 Integración (Merge):  
- Se realiza un **`merge` (inner join)** entre las dos fuentes externas utilizando la columna común `municipio` 🏙️, lo que permite conservar únicamente los registros que coinciden en ambas fuentes.  

### 📌 Integración con el Dataset Base:  
- 📊 Dado que el dataset base de COVID-19 (EA2) no posee una clave geográfica en común, se toma una muestra representativa de **444 filas** tanto del dataset base como del resultado de la integración de las fuentes externas.  
- 🏗️ Finalmente, se concatena horizontalmente la muestra de COVID-19 con la muestra integrada, generando el dataset final enriquecido.  

### 📁 Evidencias Generadas:  
- **📜 Archivo CSV Enriquecido:**  
  Se genera un archivo con el dataset final que contiene tanto la información original de COVID-19 como los datos enriquecidos de las fuentes externas.  
- **📄 Reporte de Auditoría:**  
  Se crea un informe (archivo TXT) que detalla la cantidad de registros y columnas en cada fuente, las operaciones de merge realizadas, y se especifica que las columnas relacionadas con pastos, incluida `total_pastos`, fueron procesadas para imputar valores nulos con la mediana.  

---

## 5. Requerimientos Previos ✅

Antes de ejecutar el proyecto, asegúrate de contar con:

* 🐍 **Python 3.9 o superior** (se recomienda 3.13.2).
* 🌍 **Git** (para clonar el repositorio).
* 🐳 **(Opcional) Docker**, si deseas ejecutar el proyecto en contenedor.
* 🔗 **Conexión a Internet** para descargar los datos.
* 🤖 **Cuenta en GitHub** (para la automatización con GitHub Actions).

---

## 6. Clonar o Descargar el Proyecto 📂

### 🔹 Clonar con Git  
Ejecuta el siguiente comando en tu terminal:  

```bash
git clone https://github.com/Alexis-Machado/infra-arquitectura-bigdata_Alexis_Machado.git
```

---

> **Nota:**  
> Las carpetas auditoria/, db/ y xlsx/ se crean vacías en el repositorio, pero el código las poblará en tiempo de ejecución.  
> No te preocupes si las ves vacías inicialmente. 🗂️

---

## 7. Creación y Activación de un Entorno Virtual (Recomendado) 🛠️

Para mantener organizadas las dependencias del proyecto y evitar conflictos con otras instalaciones de Python, se recomienda usar un entorno virtual.

### 🔹 Crear el entorno virtual  
Ejecuta el siguiente comando dentro de la carpeta del proyecto:  

```bash
python -m venv venv
```

🔹 Activar el entorno virtual

🔹 En Windows 🖥️

```bash
venv\Scripts\activate
```

🔹 En Linux/Mac 💻

```bash
source venv/bin/activate
```

🔹 Verificar la activación ✅  
Si el entorno se activó correctamente, deberías ver **(venv)** al inicio de tu línea de comandos.

---

## 8. Instalación de Dependencias y Uso de setup.py 📦

Para ejecutar el proyecto correctamente y facilitar su instalación, es necesario instalar las bibliotecas requeridas o utilizar setup.py.

### 🔹 Instalación de dependencias  

Ejecuta los siguientes comandos en la raíz del proyecto (asegúrate de tener el entorno virtual activo si lo estás usando):  

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

Esto instalará todas las bibliotecas necesarias para el proyecto (por ejemplo: requests, pandas, openpyxl, etc.). ✅

## 🔹 Recomendado Uso de setup.py (Empaquetado e Instalación)

El proyecto incluye un setup.py que permite instalarlo como un paquete Python local.

El archivo setup.py ahora está actualizado para reflejar la versión EA2

```python
from setuptools import setup, find_packages

setup(
    name="infra-arquitectura-bigdata_Alexis_Machado",
    version="3.0.0",
    author="Jhon Alexis Machado Rodriguez",
    author_email="jmachadoa12@gmail.com",
    description="EA3 Proyecto Integrador: Enriquecimiento de Datos simulando una Plataforma de Big Data en la Nube. 🔍🚀",
    py_modules=["EA3_Enriquecimiento_de_Datos_simulando_una_Plataforma_de_Big_Data_en_la_Nube"],
    install_requires=[
        'requests',
        "pandas",
        "openpyxl"
    ]
)

```

Asegúrate de estar en el directorio raíz del proyecto (donde está setup.py).  
Para instalarlo, ejecuta:

```bash
pip install -e .
```

Esto instalará el paquete en tu entorno Python y permitirá modificar el código sin necesidad de reinstalarlo.

---

## 9. Ejecución del Proyecto (Local) 🚀

### Ejecutar Ingesta (EA1)

Para ejecutar el primer paso del proyecto, asegúrate de tener el entorno virtual activo (si lo estás utilizando) o haber instalado las dependencias globalmente. Luego, ejecuta el script principal: 

```bash
python src/bigdata/ingestion.py
```

*El script descargará los datos, los almacenará en SQLite, generará el archivo Excel y el informe de auditoría correspondiente.*<br><br>

### 🔹 Ejemplo de salida en consola
Al ejecutar el script, verás un proceso similar a este:

```bash
Comenzando la Ingesta de Datos de COVID-19...
¡Datos obtenidos! Se han obtenido 420 Registros Históricos del COVID-19 en EE.UU
Los Datos del COVID-19 se han Almacenado en la Base de Datos SQLite
Archivo de Excel Generado en: ...\src\bigdata\static\xlsx\ingestion.xlsx
Auditoría Generada en: ...\src\bigdata\static\auditoria\ingestion.txt
¡Proceso Finalizado con Éxito!
```

#### 🔹 Archivos generados al finalizar

✔ Base de datos SQLite:  
📂 Se creará (o actualizará) el archivo ingestion.db en src/bigdata/static/db/.

✔ Archivo Excel de muestra:  
📊 Se generará un archivo ingestion.xlsx con 50 registros en src/bigdata/static/xlsx/.

✔ Informe de auditoría:  
📝 Un archivo ingestion.txt estará disponible en src/bigdata/static/auditoria/.

¡Listo! El proceso de ingesta y almacenamiento de datos ha sido completado con éxito. 🎉

---

### Ejecutar Limpieza y Preprocesamiento (EA2)

Para ejecutar la fase de limpieza y preprocesamiento, asegúrate de haber completado la ingesta (EA1) y de tener el entorno virtual activo (o las dependencias instaladas globalmente). Luego, ejecuta el siguiente comando:

```bash
python src/bigdata/cleaning.py
```

*El script realizará lo siguiente:*

* 📥 **Carga de datos:** Extrae los datos desde ingestion.db.
* 🔁 **Simulación de datos "sucios":**  
  - Duplicación de un **20%** de registros.  
  - Inserción de valores nulos en columnas numéricas.  
  - Creación de columnas adicionales (por ejemplo, 'registro_nulo', columnas duplicadas y 'fecha_sucia').  
  - Forzado error de tipo en 'positive' y 'death' (7% de los valores convertidos a cadena).
* 🧹 **Limpieza y transformación:**  
  - Eliminación de duplicados.  
  - Conversión de columnas a tipos numéricos, imputando valores nulos con la mediana.  
  - Relleno de valores faltantes en 'registro_nulo' con "Sin Dato".  
  - Eliminación de columnas inservibles (duplicadas y de error).  
  - Generación de nuevas columnas de auditoría con la fecha y hora actuales.  
  - Renombrado de columnas a nombres en español.  
  - Cálculo de indicadores: tasa de positividad y tasa de mortalidad.
* 📋 **Auditoría del proceso:**  
  Se genera un informe de auditoría que detalla el estado inicial y final del proceso de limpieza

### 🔹 Ejemplo de salida en consola

Al ejecutar el script, verás un proceso similar a este:

```bash
Iniciando Proceso de Limpieza y Preprocesamiento de Datos...
Datos Extraídos de la Base de Datos: 420 Registros
Datos Sucios Simulados: 504 Registros (Incluye Duplicados y Valores Nulos)
Archivo CSV de Datos Sucios Generado en: .../src/bigdata/static/xlsx/Tabla_Datos_Sucios.csv
Tabla 'covid_data_dirty' creada en la Base de Datos con los Datos Sucios.
Operaciones de Limpieza y Transformación Aplicadas
Archivo CSV de datos limpios generado en: .../src/bigdata/static/xlsx/Tabla_Datos_Limpios.csv
Archivo de auditoría generado en: .../src/bigdata/static/auditoria/Informe_Limpieza.txt
Tabla 'covid_data_cleaned' Creada/Actualizada en la Base de Datos con los Datos Limpios.
¡Preprocesamiento y Limpieza de Datos Completado con Éxito!
```

#### 🔹 Archivos generados al finalizar

✔ **CSV de datos limpios:**  
📂 Se generará el archivo Tabla_Datos_Limpios.csv en src/bigdata/static/xlsx/.

✔ **CSV de datos sucios:**  
📂 Se generará el archivo Tabla_Datos_Sucios.csv en src/bigdata/static/xlsx/.

✔ **Informe de auditoría de limpieza:**  
📝 Se creará el archivo Informe_Limpieza.txt en src/bigdata/static/auditoria/.

✔ **Actualización de la base de datos:**  
🗃️ Se agregarán las nuevas tablas covid_data_cleaned y covid_data_dirty  en src/bigdata/static/db/ingestion.db.

¡Listo! El proceso de limpieza y preprocesamiento se ha completado con éxito. 🎉

---

### Ejecutar Enriquecimiento (EA3)

Para ejecutar la fase de enriquecimiento, asegúrate de haber completado las fases EA1 y EA2, y de tener el entorno virtual activo (o las dependencias instaladas globalmente). Luego, ejecuta el siguiente comando:

```bash
python src/bigdata/enrichment.py
```

*El script realizará lo siguiente:*

- 📥 **Carga del dataset base:** Extrae los datos limpios desde `ingestion.db` (tabla `covid_data_cleaned`).
- 📂 **Lectura de fuentes externas:**  
  - Carga el archivo CSV de Delitos Informáticos (`Delitos_Informaticos.csv`) y renombra columnas (ejemplo: `MUNICIPIO_HECHO` a `municipio`).  
  - Consulta la API de Inventario Anual de Bovinos en Antioquia, renombra `MUNICIPIO` a `municipio`, procesa columnas de pastos (`pasto_mejorado`, `pasto_natural`, `pasto_corte`, `total_pastos`) e imputa valores nulos con la mediana.
- 🔗 **Integración de fuentes externas:** Realiza un `merge` (inner join) entre las fuentes externas usando la columna `municipio`.
- ➕ **Integración con el dataset base:** Toma una muestra de 444 filas del dataset base y del resultado del merge, y los concatena horizontalmente.
- 📤 **Exportación:** Genera un archivo CSV enriquecido (`datos_enriquecidos.csv`) y un reporte de auditoría (`reporte_enriquecimiento.txt`).

### 🔹 Ejemplo de salida en consola

Al ejecutar el script, verás un proceso similar a este:

```bash
=== Iniciando Proceso de Enriquecimiento (EA3) ===
Cargando dataset base limpio desde la base de datos (covid_data_cleaned)...
Dataset limpio cargado: 444 registros.
Leyendo archivo CSV de Delitos Informáticos...
Delitos Informáticos leídos: 56502 registros.
Consultando API de Inventario Anual de Bovinos en Antioquia...
Inventario Bovinos desde API: 1000 registros.

Dataset enriquecido exportado en: ..\src\bigdata\static\xlsx\datos_enriquecidos.csv

Reporte de enriquecimiento generado en: ..\src\bigdata\static\auditoria\reporte_enriquecimiento.txt

=== Proceso de Enriquecimiento Finalizado ===
```

#### 🔹 Archivos generados al finalizar

✔ **CSV enriquecido:**  
📂 Se generará el archivo `datos_enriquecidos.csv` en `src/bigdata/static/xlsx/`.

✔ **Informe de auditoría de enriquecimiento:**  
📝 Se creará el archivo `reporte_enriquecimiento.txt` en `src/bigdata/static/auditoria/`.

¡Listo! El proceso de enriquecimiento se ha completado con éxito. 🎉

---

## 10. Ejecución del Proyecto con Docker 🐳 (Opcional)

El **Dockerfile** ha sido actualizado para ejecutar los tres scripts (ingesta, limpieza y enriquecimiento):

```dockerfile
# Usamos la imagen oficial de Python 3.9 como base
FROM python:3.9

# Definimos el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiamos el archivo de dependencias (requirements.txt) al contenedor
COPY requirements.txt .

# Instalamos las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el código fuente al contenedor dentro del directorio /app/src
COPY src/ ./src

# Ejecutamos en secuencia el script de ingesta de EA1, luego el de preprocesamiento y limpieza de EA2 y por último el de enriquecimiento de EA3
CMD ["sh", "-c", "python src/bigdata/ingestion.py && python src/bigdata/cleaning.py && python src/bigdata/enrichment.py"]

```

### Construir la imagen Docker

Si prefieres ejecutar todo dentro de un contenedor Docker, sigue estos pasos:

Crear la imagen Docker (en la raíz del proyecto, donde está el Dockerfile):

```bash
docker build -t bigdata-ingestion .
```

### Ejecutar el contenedor

```bash
docker run --name bigdata_container bigdata-ingestion
```

Este comando creará un contenedor llamado `bigdata_container` que ejecutará los scripts `ingestion.py`, `cleaning.py` y `enrichment.py` en secuencia.

<br>

Para ver los archivos generados (base de datos, Excel, CSV, auditorías) dentro del contenedor, puedes montar un volumen o copiar los archivos al host. Por ejemplo, para montar el directorio actual al contenedor:

```bash
docker run -v ${PWD}/src/bigdata/static:/app/src/bigdata/static bigdata-ingestion
```

Si el contenedor ya se ejecutó y deseas copiar los archivos generados manualmente a tu sistema local, usa:

```bash
docker cp bigdata_container:/app/src/bigdata/static ./src/bigdata/static
```

Después de la ejecución, deberías ver los siguientes archivos en `src/bigdata/static/`:

* **DB:** `db/ingestion.db` (incluye las tablas `covid_data_cleaned` y `covid_data_dirty`).
* **Excel:** `xlsx/ingestion.xlsx`
* **CSV de datos limpios y sucios:** `xlsx/Tabla_Datos_Limpios.csv` | `xlsx/Tabla_Datos_Sucios.csv`
* **CSV enriquecido:** `xlsx/datos_enriquecidos.csv`
* **Auditorías:**  
  - `auditoria/ingestion.txt` (de ingesta)  
  - `auditoria/Informe_Limpieza.txt` (de limpieza)  
  - `auditoria/reporte_enriquecimiento.txt` (de enriquecimiento)

¡Listo! Ahora tienes tu proyecto ejecutándose en Docker con todos los archivos generados correctamente. 🚀

---

## 11. Automatización con GitHub Actions 🤖

Este proyecto incluye un flujo de trabajo en `.github/workflows/main.yml` que automatiza:

* 📥 **Ingestión de Datos desde un API**: Ejecuta el script `ingestion.py` (EA1).
* 🔄 **Preprocesamiento y Limpieza de Datos**: Ejecuta el script `cleaning.py` (EA2).
* 🌐 **Enriquecimiento de Datos**: Ejecuta el script `enrichment.py` (EA3).
* 📤 **Commit automático**: Guarda los cambios en la base de datos, Excel, CSV y auditorías si hay modificaciones.
* 🐳 **Construcción y ejecución de Docker**: Crea y ejecuta la imagen del contenedor.<br><br>

### 🔹 11.1 Estructura del Flujo de Trabajo

El archivo de configuración `.github/workflows/main.yml` tiene el siguiente contenido actualizado:

```yaml
name: ETL Pipeline Automation

on:
  push:
    branches:
      - main

jobs:
  ingestion:
    runs-on: ubuntu-latest

    steps:
      - name: 🛎️ Checkout del repositorio
        uses: actions/checkout@v3

      - name: 🔄 Rebase antes de ingestar
        run: |
          git pull --rebase origin main

      - name: 🐍 Configurar Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'

      - name: 📦 Instalar dependencias
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: 🚀 Ejecutar script de ingesta (EA1)
        run: python src/bigdata/ingestion.py

      - name: 🚀 Ejecutar script de limpieza (EA2)
        run: python src/bigdata/cleaning.py

      - name: 🚀 Ejecutar script de enriquecimiento (EA3)
        run: python src/bigdata/enrichment.py

      - name: 📂 Configurar Git
        run: |
          git config --global user.name "github-actions[bot]"
          git config --global user.email "github-actions[bot]@users.noreply.github.com"

      - name: 📤 Hacer commit de los cambios
        run: |
          git add .
          git commit -m "Actualización Automática de Datos (EA1, EA2 y EA3) ✅🎉" || echo "No hay cambios para commitear"
          git push https://${{ secrets.GITHUB_TOKEN }}@github.com/Alexis-Machado/infra-arquitectura-bigdata_Alexis_Machado.git
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

  docker-build:
    needs: ingestion
    runs-on: ubuntu-latest

    steps:
      - name: 🛎️ Checkout del repositorio
        uses: actions/checkout@v3

      - name: 🐳 Construir y ejecutar contenedor Docker
        run: |
          docker build -t bigdata-ingestion .
          docker run --rm bigdata-ingestion
```

Esta configuración automatiza la ingesta, limpieza y enriquecimiento de datos, realizando un commit automático si hay cambios y, finalmente, construyendo y ejecutando un contenedor Docker.

Cada vez que se realice un push a la rama `main`, se ejecutarán de forma secuencial los scripts de ingesta (EA1), limpieza (EA2) y enriquecimiento (EA3), seguido de la construcción y ejecución del contenedor Docker.

---

### 🔹 11.2 Explicación del Flujo

🎯 **Evento de disparo:**

Cada vez que se hace un push a la rama `main`, se ejecutan los siguientes jobs:

* **📥 Checkout del repositorio:** Se descarga el repositorio.  
* **🐍 Configuración de Python:** Se configura Python 3.9.  
* **📦 Instalación de dependencias:** Se instalan las dependencias indicadas en `requirements.txt`.  
* **🚀 Ejecución del script de ingesta (EA1):**  
  Se ejecuta `ingestion.py`, el cual descarga los datos de COVID-19, los almacena en SQLite, genera un archivo Excel y un informe de auditoría.  
* **🔄 Ejecución del script de limpieza (EA2):**  
  A continuación, se ejecuta `cleaning.py`, que carga los datos, simula datos "sucios", aplica las operaciones de limpieza y transformación, exporta los CSV con los datos limpios y sucios, genera un informe de auditoría de limpieza y actualiza la base de datos con las nuevas tablas `covid_data_cleaned` y `covid_data_dirty`.  
* **🌐 Ejecución del script de enriquecimiento (EA3):**  
  Luego, se ejecuta `enrichment.py`, que integra datos externos (Delitos Informáticos e Inventario Bovinos), los combina con una muestra del dataset limpio de COVID-19, y genera un CSV enriquecido y un reporte de auditoría.  
* **📝 Configuración de Git:** Se configuran los datos de Git para realizar commits automáticos desde GitHub Actions.  
* **📤 Commit automático:** Se realiza un commit de los cambios generados (nuevos datos, Excel, auditorías, CSV, etc.) si existen, y se hace push al repositorio.

🐳 **docker-build** (depende de ingestion)  
* **📥 Checkout del repositorio:** Se descarga el repositorio.  
* **🛠️ Construcción de la imagen Docker:** Se ejecuta `docker build` para construir la imagen.  
* **🚢 Ejecución del contenedor Docker:** Se ejecuta `docker run`, lo que lanza un contenedor que ejecuta secuencialmente los scripts de ingesta (EA1), limpieza (EA2) y enriquecimiento (EA3).

<br><br>

🚀 ¡Listo! Con este flujo de trabajo, la ingesta de datos, el preprocesamiento, la limpieza, el enriquecimiento y la construcción del contenedor Docker se ejecutarán automáticamente cada vez que subas cambios al repositorio. 🎉

---

### 🔹 11.3 Cómo Personalizarlo 🔧

Cambiar la rama en la que se dispara el flujo:

Si deseas que la automatización se ejecute en otra rama, edita:

```yaml
on:
  push:
    branches:
      - main
```

📌 Ajustar la versión de Python:

Si necesitas otra versión de Python, cambia:

```yaml
with:
  python-version: '3.9'
```

🔗 Configurar la URL del repositorio:  
Asegúrate de que el paso `git push` apunte a tu repositorio:

```yaml
git push https://${{ secrets.GITHUB_TOKEN }}@github.com/TU_USUARIO/TU_REPO.git main
```

📊 Ver logs y resultados:

Para revisar la ejecución, dirígete a la pestaña **Actions** en tu repositorio de GitHub.
<br><br>

🚀 ¡Listo! Con este flujo de trabajo automatizado, la ingesta de datos, el preprocesamiento, la limpieza, el enriquecimiento y la construcción del contenedor Docker se ejecutarán automáticamente cada vez que realices un push al repositorio. 🎉

---

## 12. Conclusión 🎯

Con este proyecto se integra un pipeline completo de ETL para datos de COVID-19:

* **Extracción (EA1):**  
  Descarga de datos desde la API del COVID Tracking Project, almacenamiento en SQLite y generación de reportes (Excel y auditoría). 📥💾📊📋

* **Transformación y Limpieza (EA2):**  
  Simulación de datos sucios, limpieza, transformación, exportación de los CSV con datos limpios y sucios, generación de un informe de auditoría detallado y actualización de la base de datos (nuevas tablas `covid_data_cleaned` y `covid_data_dirty`). 🔄🧹📈📁📝

* **Enriquecimiento (EA3):**  
  Integración de datos externos (Delitos Informáticos e Inventario Bovinos), combinación con el dataset limpio de COVID-19, generación de un dataset enriquecido y un reporte de auditoría. 🌐📈📝

* **Automatización:**  
  Integración con GitHub Actions 🤖 y ejecución en contenedores Docker 🐳.
<br><br>

¡Felicidades! Has implementado exitosamente un sistema de ingesta, limpieza y enriquecimiento de datos, simulando una plataforma Big Data en la nube. 🎉

---

## 13. Autores

<div align="center">
  <img src="https://www.iudigital.edu.co/images/11.-IU-DIGITAL.png" alt="IU Digital" width="350">

  ━━━━━━━━━━━━━━━━━━━━━━━

  <h1>📋 Evidencia de Aprendizaje 3<br>
  <sub>Enriquecimiento de Datos simulando una Plataforma de Big Data en la Nube<sub></h1>
  <h3>Parte 1, 2 y 3 del Proyecto Integrador</h3>

  ━━━━━━━━━━━━━━━━━━━━━━━

  ### 👥 **Integrantes**
  **Jhon Alexis Machado Rodríguez**  
  **Julián José Martínez Camacho**

  ━━━━━━━━━━━━━━━━━━━━━━━

  #### 🎓 **Ingeniería de Software y Datos**  
  #### 🏛️ Institución Universitaria Digital de Antioquia  
  #### 📅 Semestre 9°  
  #### 📦 Infraestructura y arquitectura para Big Data  
  #### 🔖 PREICA2501B010112  
  #### 👨‍🏫🏫 andres felipe callejas  

  ━━━━━━━━━━━━━━━━━━━━━━━

  **🗓 26 de Marzo del 2025**  

</div>

---