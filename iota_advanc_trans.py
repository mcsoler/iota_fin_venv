import datetime
import os
import sys
import time
import gzip
import shutil
import redis
import subprocess
from cryptography.fernet import Fernet
from dotenv import load_dotenv

from iota_sdk import (
        AddressUnlockCondition,
        Client,
        Ed25519Address,
        Wallet,
        Utils,
        TimelockUnlockCondition,
        types,
        MetadataFeature,
        utf8_to_hex,
        TagFeature,
        secret_manager,
)

load_dotenv()
r = redis.Redis(host='localhost', port=6379, db=0)

commands = [
    'redis-cli KEYS "*recepcion*" | xargs redis-cli DEL',
    'redis-cli KEYS "*transaction*" | xargs redis-cli DEL',
    'redis-cli KEYS "*segment*" | xargs redis-cli DEL',
    'redis-cli KEYS "*filename*" | xargs redis-cli DEL'
]

for cmd in commands:
    try:
        print(subprocess.run(cmd, shell=True, check=True))
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar el comando {cmd}: {e}")


def divide_file(file_path, segment_size):
    """
    Divide un archivo en segmentos.
    :param file_path: Ruta del archivo a dividir.
    :param segment_size: Tamaño de cada segmento en bytes.
    :return: Lista de segmentos.
    """
    segments = []
    with open(file_path, 'rb') as f:
        while True:
            # Leer segment_size bytes
            segment = f.read(segment_size)
            if not segment:
                #Final del archivo
                break
            segments.append(segment)
            counter = r.incr('segment_counter')
            segment_key = f'segment:{counter}'
            r.hset(segment_key, 'segment', segment)
    return segments

def file_to_hex(filename):
    # Leer el archivo en modo binario
    with open(filename, 'rb') as file:
        content = file.read()

        # Convertir el contenido a hexadecimal
        hex_representation = content.hex()

        return hex_representation


#with open(filename, 'rb') as file:
#with open('test.txt', 'rb') as file:
 #   file_data = file.read()

#with open(filename, 'rb') as f_in:
    #with gzip.open(compressed_filename, 'wb') as f_out:
        #shutil.copyfileobj(f_in, f_out)

# 2. Leer el archivo comprimido en modo binario
#with open(compressed_filename, 'rb') as file:
    #compressed_data = file.read()

#hex_data = ta.hex()
#encrypted_data = cipher.encrypt(file_data)
#encrypted_hex_data = encrypted_data.hex()
#hex_with_prefix = '0x' + encrypted_hex_data
#encrypted_hex_data = file_data.hex()

#hex_with_prefix = '0x' + encrypted_hex_data

# This example sends a transaction with a timelock.

wallet = Wallet(os.environ['WALLET_DB_PATH'])

#account = wallet.get_account('TestCR2023')  #NodoShimmer
account = wallet.get_account('nodorenzo')    
# Sync account with the node
response = account.sync()

if 'STRONGHOLD_PASSWORD' not in os.environ:
        raise Exception(".env STRONGHOLD_PASSWORD is undefined, see .env.example")

wallet.set_stronghold_password(os.environ["STRONGHOLD_PASSWORD"])


def send_segment_to_tangle(segment, account):
    # Create an ouput with amount 1_000_000 and a timelock of 1 hour
    hex_representation = segment.hex()
    print("HEX", hex_representation)
    #in_an_hour = int(
    #        time.mktime(
    #            (datetime.datetime.now() +
    #             datetime.timedelta(
    #                 hours=1)).timetuple()))
    basic_output = Client().build_basic_output(
    #basic_output = Client().build_and_post_block( 
     unlock_conditions=[
	     AddressUnlockCondition(
                    Ed25519Address(
                        #Utils.bech32_to_hex('rms1qry52gw8sq9xrx6jj833szff0kkaqfdlyx5kum52nwc6y47ezh7pylprqr3'))
                        Utils.bech32_to_hex('tst1qph6h7mt45at3986jnhf55z5wndw78z5s2tn4ys30qs2ulmn3pwrv6f9639'))
              	),
            	#TimelockUnlockCondition(in_an_hour),
            ],
            features=[
            #MetadataFeature(utf8_to_hex(encrypted_hex_data))
            #TagFeature(utf8_to_hex('Hello, World!'))
                MetadataFeature(utf8_to_hex(hex_representation))
            #data(utf8_to_hex(hex_data))
            ],
	)
#message_hex = "Hola Mundo".encode().hex()
#tagged_data_payload = types.payload.TaggedDataPayload(tag="YourTagInHex", data=message_hex)

#transaction_essence = types.payload.RegularTransactionEssence(
        #outputs=[basic_output],
        #payload=tagged_data_payload
#)
    #print("BO",basic_output)
    transaction = account.send_outputs([basic_output])
    #transaction = account.submit.payload([basic_output])
    #print(f'Transaction sent: {transaction.transactionId}')
    return transaction.transactionId

#filename = 'uploads/WEBAPI_PACAv4.docx'
filename = sys.argv[1]
filename1 = os.path.basename(sys.argv[1])
r.set('filename', filename1)
#filename = 'test.txt'
L = 4000
segments = divide_file(filename, L)

#Retry send transactions error
def try_send_segment(segment, account, max_retries=5):
    retries = 0
    while retries < max_retries:
        try:
            #account = wallet.get_account('TestCry23')
            #response = account.sync()
            #wallet.set_stronghold_password(os.environ["STRONGHOLD_PASSWORD"])
            transaction_id = send_segment_to_tangle(segment, account)
            return transaction_id
        except Exception as e:  # Captura todas las excepciones
            print(f"Error al enviar el segmento: {e}. Intento {retries + 1} de {max_retries}.")
            #wallet = Wallet(os.environ['WALLET_DB_PATH'])
            #account = wallet.get_account('TestCR2023') #Nodoshimer
            account = wallet.get_account('nodorenzo')
            response = account.sync()
            wallet.set_stronghold_password(os.environ["STRONGHOLD_PASSWORD"])
            transaction_id = send_segment_to_tangle(segment, account)
            retries += 1
            print("enviada")
            #time.sleep(40)  # Opcional: espera 5 segundos antes de reintentar
            return transaction_id
    raise Exception("No se pudo enviar el segmento después de todos los intentos.")

# Enviar cada segmento a Tangle
transaction_ids = []
for segment in segments:
    print("SEG",segment)
    #transaction_id = send_segment_to_tangle(segment, account)
    transaction_id = try_send_segment(segment, account)
    transaction_ids.append(transaction_id)
    counter = r.incr('transaction_counter')
    transaction_key = f'transaction:{counter}'
    r.hset(transaction_key, 'transaction_id', transaction_id)
    print(f'Segmento enviado con Transaction ID: {transaction_id}')


    block_id = account.retry_transaction_until_included(transaction_id)
    r.hset(transaction_key, 'block_id', block_id)
    print(f'Block sent: {os.environ["EXPLORER_URL"]}/block/{block_id}')

print("Transacción exitosa")
