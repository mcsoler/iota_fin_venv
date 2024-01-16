import redis
import bcrypt

r = redis.Redis(host='localhost', port=6379, db=0)
print(r)

def register_user(username, password):
    if r.hexists('users', username):
        return "Usuario ya existe"
    else:
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password, salt)
        r.hset('users', username, hashed_password)
        return "Usuario registrado exitosamente"

response = register_user("Cripto2023", b"Cripto2023")
print(response)
