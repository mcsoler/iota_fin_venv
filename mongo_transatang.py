from pymongo import MongoClient
import gridfs
from datetime import datetime, timedelta

# Conectar a MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['transaction_his']  # Reemplaza con el nombre de tu base de datos
fs = gridfs.GridFS(db)

# Definir el rango de fechas
fecha_inicio = datetime(2023, 11, 20)  # Año, mes, día
fecha_fin = fecha_inicio + timedelta(days=1)

# Realizar la consulta en MongoDB
cursor = fs.find({"metadata.upload_time": {"$gte": fecha_inicio, "$lt": fecha_fin}})

# Iterar sobre los resultados y procesar cada archivo
for file in cursor:
    print(f"Archivo ID: {file._id}")
    print(f"Metadatos: {file.metadata}")
