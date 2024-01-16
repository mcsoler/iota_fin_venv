import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv

# Carga las variables de entorno desde el archivo .env
load_dotenv()

# Obtiene la clave de la variable de entorno y crea un objeto Fernet
key = os.environ.get('SECRET_KEY').encode('utf-8')
cipher = Fernet(key)

# Leer el archivo .enc
with open('uploads/WEBAPI_PACAv4.docx', 'rb') as file:
        encrypted_data = file.read()

# Desencriptar los datos
decrypted_data = cipher.decrypt(encrypted_data)

# Guardar los datos desencriptados en un nuevo archivo
with open('output/WEBAPI_PACAv4.docx', 'wb') as file:
    file.write(decrypted_data)
    print("Archivo desencriptado con éxito!")
