from cryptography.fernet import Fernet

# Genera la clave Fernet
key = Fernet.generate_key()

# Almacena la clave en Stronghold
store_key_in_stronghold(key)

# ...

# Recupera la clave de Stronghold cuando la necesites
key = retrieve_key_from_stronghold()
print(key)
cipher = Fernet(key)
print(cipher)
