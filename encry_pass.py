
from cryptography.fernet import Fernet

# Genera una clave secreta para Fernet
key = Fernet.generate_key()
cipher = Fernet(key)
print("KEY",key)
# Cifra tu clave
my_password = "TangleCR23"
encrypted_password = cipher.encrypt(my_password.encode())

# Imprime el valor cifrado en formato hexadecimal (opcional)
print("ECR",encrypted_password)

