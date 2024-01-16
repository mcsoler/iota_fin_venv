from iota import Iota, TryteString, Address, Tag
import os

# Convierte el archivo en Trytes
file_path = 'ruta/al/archivo/a/enviar.txt'
with open(file_path, 'rb') as file:
    file_data = TryteString.from_bytes(file.read())

# Dirección de destino en el servidor Ubuntu
server_address = 'DIRECCION_DEL_SERVIDOR'  # Reemplaza con la dirección del servidor

# Crea una instancia de Iota
api = Iota('https://nodes.iota.org:443')  # Utiliza un nodo IOTA de tu elección

# Crea una transacción con los Trytes del archivo
tx = api.prepare_transfer(
    transfers=[
        {
            'address': Address(server_address),
            'value': 0,
            'message': file_data,
            'tag': Tag('FILETRANSFER')
        }
    ]
)

# Realiza la transacción
api.send_trytes(tx['trytes'], depth=3, min_weight_magnitude=9)