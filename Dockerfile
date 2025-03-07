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

# Ejecutamos ambos scripts en secuencia
CMD ["sh", "-c", "python src/bigdata/ingestion.py && python src/bigdata/cleaning.py"]
