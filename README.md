# infra-arquitectura-bigdata_Martinez_Julian 🚀

<div align="center">
  <h1>Infraestructura y Arquitectura para Big Data</h1>
  <h2>Proyecto Integrador: Parte 1 EA1 - Ingestión de Datos desde un API 📊</h2>
</div>

---

Este proyecto es un flujo de ingesta de datos del **COVID-19** desde la API pública del **COVID Tracking Project** 😷, con almacenamiento en **SQLite** 💾, generación de un archivo **Excel** de muestra 📈 y un reporte de auditoría 📋. Además, cuenta con un flujo de integración continua en **GitHub Actions** 🤖 que automatiza la ejecución del script y la construcción de la imagen Docker 🐳.

---

> **Importante:**  
> El COVID Tracking Project finalizó la recolección de datos el **7 de marzo de 2021** 📆, por lo que la información disponible es histórica y no se actualiza más allá de esa fecha.

---

## 1. Descripción General 🌟

Este proyecto realiza las siguientes tareas:

- 📥 **Descarga de datos:**  
  Descarga datos históricos de COVID-19 de los EE.UU. desde la API del COVID Tracking Project.
  - **Página web del API:**  
    [https://covidtracking.com/data/api](https://covidtracking.com/data/api)
  - **Formato JSON:**  
    [https://api.covidtracking.com/v1/us/daily.json](https://api.covidtracking.com/v1/us/daily.json)
  - **Formato CSV (opcional):**  
    [https://api.covidtracking.com/v1/us/daily.csv](https://api.covidtracking.com/v1/us/daily.csv)
  - **Recurso adicional:**  
    [Las mejores APIs públicas para practicar](https://ed.team/blog/las-mejores-apis-publicas-para-practicar)

- 🗄️ **Base de datos SQLite:**  
  Crea (o actualiza) una base de datos para almacenar la información.

- 📊 **Generación de archivo Excel:**  
  Genera un archivo Excel con los últimos 50 registros a modo de muestra.

- 📝 **Informe de auditoría:**  
  Crea un informe de auditoría (archivo de texto) comparando la cantidad de registros en la API y en la base de datos.

- 🚀 **Automatización:**  
  Automatiza la ejecución de la ingesta y la construcción de la imagen Docker a través de GitHub Actions.

---

Al finalizar, tendrás:

- 🗃️ Una base de datos `ingestion.db`.
- 📑 Un archivo Excel `ingestion.xlsx` con 50 registros en la carpeta `xlsx`.
- 📜 Un archivo de auditoría `ingestion.txt` con un resumen de los datos procesados.
- 🤖 Un pipeline en GitHub Actions que ejecuta estos pasos automáticamente.

---

## 2. Acerca de la API (COVID Tracking Project) 📡

El COVID Tracking Project fue una iniciativa que recopiló datos de COVID-19 en EE.UU. hasta el **7 de marzo de 2021**. A partir de esa fecha, la recolección de datos se detuvo y la información quedó congelada como un registro histórico. Algunas consideraciones importantes:

- **URL Base:**  
  [https://api.covidtracking.com](https://api.covidtracking.com)
- **Endpoint de Datos Históricos (JSON):**  
  [https://api.covidtracking.com/v1/us/daily.json](https://api.covidtracking.com/v1/us/daily.json)
  - *También disponible en CSV:*  
    [https://api.covidtracking.com/v1/us/daily.csv](https://api.covidtracking.com/v1/us/daily.csv)
- **Formato de Respuesta:**  
  JSON
- **Licencia:**  
  CC BY 4.0 https://covidtracking.com/about-data/license

**Campos Principales:**
- `date`: Fecha del reporte
- `positive`: Casos positivos acumulados
- `death`: Fallecimientos confirmados o probables
- `hospitalizedCurrently`: Hospitalizados
- `totalTestResults`: Número total de tests reportados
- `positiveIncrease`: Nuevos casos
- `deathIncrease`: Nuevas muertes
- `lastModified`: Última fecha/hora de actualización

---

## 3. Requerimientos Previos ✅

Antes de ejecutar el proyecto, asegúrate de contar con los siguientes requisitos:

- 🐍 **Python 3.9 o superior (Recomendado: 3.13.2)** instalado en tu sistema.
- 🌍 **Git** instalado (para clonar el repositorio, aunque puedes descargar el ZIP directamente).
- 🐳 **(Opcional) Docker**, si deseas ejecutar el proyecto en un contenedor o utilizar el pipeline de Docker en GitHub Actions.
- 🔗 **Conexión a Internet** para descargar los datos.
- 🤖 **Una cuenta en GitHub**, si quieres aprovechar la automatización con GitHub Actions.

---

## 4. Clonar o Descargar el Proyecto 📂

### 🔹 Clonar con Git  
Ejecuta el siguiente comando en tu terminal:  

```bash
git clone https://github.com/Alexis-Machado/infra-arquitectura-bigdata_Alexis_Machado.git
```

---

> **Nota:**  
> Las carpetas `auditoria/`, `db/` y `xlsx/` se crean vacías en el repositorio, pero el código las poblará en tiempo de ejecución.  
> No te preocupes si las ves vacías inicialmente. 🗂️

---

## 5. Creación y Activación de un Entorno Virtual (Recomendado) 🛠️

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
Si el entorno se activó correctamente, deberías ver (venv) al inicio de tu línea de comandos.

---

## 6. Instalación de Dependencias y Uso de `setup.py` 📦

Para ejecutar el proyecto correctamente y facilitar su instalación, es necesario instalar las bibliotecas requeridas y utilizar `setup.py`.

### 🔹 Instalación de dependencias  

Ejecuta los siguientes comandos en la raíz del proyecto (asegúrate de tener el entorno virtual activo si lo estás usando):  

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

Esto instalará todas las bibliotecas necesarias para el proyecto (por ejemplo: requests, pandas, openpyxl, etc.). ✅

## 🔹 Recomendado Uso de setup.py (Empaquetado e Instalación)
El proyecto incluye un setup.py que permite instalarlo como un paquete Python local.

Asegúrate de estar en el directorio raíz del proyecto (donde está setup.py).
Para instalarlo, ejecuta:

```bash
pip install -e .
```

Esto instalará el paquete en tu entorno Python y permitirá modificar el código sin necesidad de reinstalarlo.

---

## 7. Ejecución del Proyecto (Local) 🚀  

Para ejecutar el proyecto, asegúrate de tener el entorno virtual activo (si lo estás utilizando) o haber instalado las dependencias globalmente. Luego, ejecuta el script principal:  

```bash
python src/bigdata/ingestion.py
```

🔹 Ejemplo de salida en consola
Al ejecutar el script, verás un proceso similar a este:

```bash
Comenzando la Ingesta de Datos de COVID-19...
¡Datos obtenidos! Se han obtenido 420 Registros Históricos del COVID-19 en EE.UU
Los Datos del COVID-19 se han Almacenado en la Base de Datos SQLite
Archivo de Excel Generado en: ...\src\bigdata\static\xlsx\ingestion.xlsx
Auditoría Generada en: ...\src\bigdata\static\auditoria\ingestion.txt
¡Proceso Finalizado con Éxito!
```

🔹 Archivos generados al finalizar

✔ Base de datos SQLite:
📂 Se creará (o actualizará) el archivo ingestion.db en src/bigdata/static/db/.

✔ Archivo Excel de muestra:
📊 Se generará un archivo ingestion.xlsx con 50 registros en src/bigdata/static/xlsx/.

✔ Informe de auditoría:
📝 Un archivo ingestion.txt estará disponible en src/bigdata/static/auditoria/.

¡Listo! El proceso de ingesta y almacenamiento de datos ha sido completado con éxito. 🎉

---
 
## 8. Ejecución del Proyecto con Docker 🐳 (Opcional)

Si prefieres ejecutar todo dentro de un contenedor Docker, sigue estos pasos:

Crear la imagen Docker (en la raíz del proyecto, donde está el Dockerfile):

```bash
docker build -t bigdata-ingestion .
```

Ejecutar el contenedor:

```bash
docker run --name bigdata_container bigdata-ingestion
```

Este comando creará un contenedor llamado `bigdata_container` que ejecutará el script `ingestion.py`.

Para ver los archivos generados (base de datos, Excel, auditoría) dentro del contenedor, puedes montar un volumen o copiar los archivos al host. Un ejemplo simple de montar el directorio actual al contenedor:

```bash
docker run -v ${PWD}/src/bigdata/static:/app/src/bigdata/static bigdata-ingestion
```

De esta manera, verás los archivos en tu máquina local en la carpeta `src/bigdata/static/`.

Si el contenedor ya se ejecutó y deseas copiar los archivos generados manualmente a tu sistema local, usa:

```bash
docker cp bigdata_container:/app/src/bigdata/static ./src/bigdata/static
```

Después de la ejecución, deberías ver los siguientes archivos en `src/bigdata/static/`:

- 🗃️ `db/ingestion.db` → Base de datos SQLite con los datos procesados.
- 📑 `xlsx/ingestion.xlsx` → Archivo Excel con los últimos 50 registros.
- 📝 `auditoria/ingestion.txt` → Informe de auditoría con el resumen de datos.

¡Listo! Ahora tienes tu proyecto ejecutándose en Docker con todos los archivos generados correctamente. 🚀

---

## 9. Automatización con GitHub Actions 🤖

Este proyecto incluye un flujo de trabajo en `.github/workflows/main.yml` que automatiza:

- 📥 **Ingesta de datos**: Ejecuta el script `ingestion.py`.
- 📤 **Commit automático**: Guarda los cambios en la base de datos, Excel y auditoría si hay modificaciones.
- 🐳 **Construcción y ejecución de Docker**: Crea y ejecuta la imagen del contenedor.

### 🔹 9.1 Estructura del Flujo de Trabajo  

El archivo de configuración `.github/workflows/main.yml` tiene el siguiente contenido:

```yaml
name: Data Ingestion Automation

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

      - name: 🚀 Ejecutar script de ingesta
        run: python src/bigdata/ingestion.py

      - name: 📂 Configurar Git
        run: |
          git config --global user.name "github-actions[bot]"
          git config --global user.email "github-actions[bot]@users.noreply.github.com"

      - name: 📤 Hacer commit de los cambios
        run: |
          git add .
          git commit -m "Actualización Automática de Datos ✅🎉" || echo "No hay cambios para commitear"
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

🔹 9.2 Explicación del Flujo
🎯 Evento de disparo:

Cada vez que se hace un push a la rama main, se ejecutan los siguientes jobs:

✅ ingestion
Descarga el repositorio (checkout).

Configura Python 3.9.

Instala las dependencias (requirements.txt).

Ejecuta el script de ingesta ingestion.py.

Configura Git para realizar commits automáticos desde GitHub Actions.

Realiza un commit de los cambios generados (nuevos datos, Excel, auditoría) si existen.

🐳 docker-build (depende de ingestion)

Descarga el repositorio (checkout).

Construye la imagen Docker (docker build).

Ejecuta el contenedor Docker (docker run).


🔹 9.3 Cómo Personalizarlo 🔧

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
Asegúrate de que el paso git push apunte a tu repositorio:

```yaml
git push https://${{ secrets.GITHUB_TOKEN }}@github.com/TU_USUARIO/TU_REPO.git main
```

📊 Ver logs y resultados:

Para revisar la ejecución, dirígete a la pestaña Actions en tu repositorio de GitHub.

🚀 ¡Listo! Con este flujo de trabajo, la ingesta de datos y la construcción de Docker se ejecutarán automáticamente cada vez que subas cambios al repositorio. 🎉

---

## 10. Conclusión 🎯  

Con este proyecto, has construido un **pipeline de extracción, transformación y carga (ETL)** para datos de COVID-19.  

🔹 **Flujo del Proyecto:**  
✅ **Extracción**: Obtención de datos desde la API del **COVID Tracking Project**.  
✅ **Transformación**: Limpieza y almacenamiento en una base de datos **SQLite**.  
✅ **Carga**: Generación de un reporte en **Excel** y un archivo de **auditoría**.  
✅ **Automatización**: Integración con **GitHub Actions** para ejecutar el flujo y construir un contenedor **Docker** automáticamente.  


🎉 ¡Felicidades! Has finalizado el desarrollo de este proyecto con éxito. 🚀

--- 

## Autores

<div align="center">
  <img src="https://www.iudigital.edu.co/images/11.-IU-DIGITAL.png" alt="IU Digital" width="350">

  ━━━━━━━━━━━━━━━━━━━━━━━

  <h1>📋 Evidencia de Aprendizaje 1<br>
  <sub>Ingestión de Datos desde un API</sub></h1>
  <h3>Parte 1 del Proyecto Integrador</h3>

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

  **🗓️ 2 de marzo del 2025**  
</div>
