import os
import json
import redis
import sys
import gridfs
from datetime import datetime
from pymongo import MongoClient
from dotenv import load_dotenv
from cryptography.fernet import Fernet
from iota_sdk import Wallet, MetadataFeature, hex_to_utf8, TagFeature

username = sys.argv[1]
r = redis.Redis(host='localhost', port=6379, db=0)

field = 'transaction_id'
#for hash_k in r.scan_iter('transaction:*'):
#    value = r.hget(hash_k, field)
#    if value:
#        decoded_value = value.decode('utf-8')
#        print(decoded_value)

# This example uses secrets in environment variables for simplicity which
# should not be done in production.
load_dotenv()

wallet = Wallet(os.environ['WALLET_DB_PATH'])

account = wallet.get_account('TestCR23')
account.sync({'syncIncomingTransactions': True})

# All transactions sent from the the account
transactions = account.transactions()
print('Sent transactions:')
for transaction in transactions:
        print(transaction.transactionId)

transaction_keys = list(r.scan_iter('transaction:*'))
transaction_keys_sorted = sorted(transaction_keys, key=lambda x: int(x.split(b':')[1]))

#for hash_k in r.scan_iter('transaction:*'):
for hash_k in transaction_keys_sorted:
    value = r.hget(hash_k, field)
    if value:
        decoded_value = value.decode('utf-8')
        specific_transaction_id = decoded_value                
        print("SE",specific_transaction_id)

        # Incoming transactions
        incoming_transactions = account.incoming_transactions()
        print('Received transactions:')
        for transaction in incoming_transactions:
            if transaction.transactionId == specific_transaction_id:
                #transaction_id = transaction.transactionId
                payload = transaction.payload
        #segment_hex = metadata_feature.data
        #segment = bytes.fromhex(segment_hex)
        #print(segment)

                try:
                    transaction_json = json.dumps(payload)
    #    print("JSON",transaction_json)  
                except TypeError as e:
                    print(f"Error al convertir la transacción a JSON: {e}")
                data = json.loads(transaction_json)
                #print("DATA", data)
                dicc = {}

                try:
                    features = data['essence']['outputs'][0]['features'][0]['data']
#    print(features)
                except:
                    print("Not exist features")

                encryp = hex_to_utf8(features)
                orig_by = bytes.fromhex(encryp)
                orig_str = orig_by.decode('utf-8')
                print("EN", orig_str)
                counter = r.incr('recepcion_counter')
                transaction_key = f'recepcion:{counter}'
                r.hset(transaction_key, 'orig_str', orig_str)

segmen_recep = list(r.scan_iter('recepcion:*'))
segmen_recep_sorted = sorted(segmen_recep, key=lambda x: int(x.split(b':')[1]))
segmentos_content = [''.join(map(lambda x: x.decode('utf-8'), r.hgetall(seg).values())) for seg in segmen_recep_sorted]
contenido_completo = ''.join(segmentos_content)
filename = r.get('filename').decode('utf-8')
filepath = f"enc/{filename}"
with open(filepath, "w", encoding="utf-8") as f:
        f.write(contenido_completo)
        print("Recepcion finalizada y archivo recuperado")

key = os.environ.get('SECRET_KEY').encode()
cipher = Fernet(key)

with open(filepath, "rb") as f:
        encrypted_data = f.read()

decrypted_data = cipher.decrypt(encrypted_data)

filepath = f"output/{filename}"
with open(filepath, "wb") as f:
        f.write(decrypted_data)

print("Archivo desencriptado y guardado exitosamente.")

client = MongoClient('mongodb://localhost:27017/')
db = client['transaction_his']  # Reemplaza con el nombre de tu base de datos

# Crear una instancia de GridFS
fs = gridfs.GridFS(db)

# Leer los datos del archivo
with open(filepath, 'rb') as f:
        contents = f.read()

        # Obtener la hora actual
        current_time = datetime.utcnow()

        # Metadatos para almacenar junto con el archivo
        metadata = {
                "username": username,          # Tu variable de nombre de usuario
                "transactionID": transaction.transactionId,  # Tu ID de transacción
                "upload_time": current_time     # Hora de carga
                   }
# Guardar los datos en GridFS con metadatos
file_id = fs.put(contents, filename=filename, metadata=metadata)


print(f"Archivo guardado con ID: {file_id}")
