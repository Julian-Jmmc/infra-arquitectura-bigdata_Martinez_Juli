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

# Ejecutamos en secuencia el script de ingesta de EA1 y luego el de preprocesamiento y limpieza de EA2
CMD ["sh", "-c", "python src/bigdata/ingestion.py && python src/bigdata/cleaning.py"]