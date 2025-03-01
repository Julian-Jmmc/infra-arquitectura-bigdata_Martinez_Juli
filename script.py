import pandas as pd  # Importamos la librería Pandas para manejar datos en formato tabular
import json  # Importamos la librería JSON para manejar archivos JSON

def main():
    # Leemos el archivo JSON
    with open('data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)  # Cargamos el contenido del archivo JSON en la variable 'data'
    
    # Si el JSON es un diccionario único, convertirlo a una lista para procesarlo con Pandas
    if isinstance(data, dict):
        data = [data]  # Convertimos el diccionario en una lista de un solo elemento
    
    # Creamos un DataFrame de Pandas con los datos del JSON
    df = pd.DataFrame(data)
    
    # Guardamos el DataFrame en un archivo Excel
    df.to_excel('output.xlsx', index=False)  # Guardamos sin incluir los índices de Pandas
    
    # Mensaje de confirmación
    print("Archivo Excel 'output.xlsx' generado Exitosamente.")

if __name__ == '__main__':
    main() 
