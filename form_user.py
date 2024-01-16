import bcrypt
import redis

r = redis.Redis(host='localhost', port=6379, db=0)
# Generar un hash de una contraseña
user: 'Prueba2023'
password = b"Prueba2023"
salt = bcrypt.gensalt()
hashed_password = bcrypt.hashpw(password, salt)
email = "prueba203@gmail.com"

r.hset(f'users:{user}',mapping={'password': hashed_password, 'email': email})
