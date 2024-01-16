from dotenv import load_dotenv
from flask import Flask, render_template, request, send_from_directory, redirect, url_for, flash
from cryptography.fernet import Fernet
from flask import session, jsonify
from pymongo import MongoClient
import gridfs
from datetime import datetime, timedelta
import os
import redis
import PyPDF2
import base64
import subprocess
import bcrypt
import time

load_dotenv()
app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY')

#UPLOAD_FOLDER = 'uploads/'

key = os.environ.get('SECRET_KEY').encode()
cipher = Fernet(key)
#print("CI", cipher)

r = redis.StrictRedis(host='localhost', port=6379, db=0)
#r.set('key', KEY)
def is_pdf(file):
    #if file.filename.endswith('.pdf'):
        #file.filename = file.filename.rsplit('.', 1)[0] + '.txt'
    return file.filename.endswith('.pdf')	

def change_namepdf(file):
    if file.filename.endswith('.pdf'):
            app.config['UPLOAD_FOLDER'] = 'uploads/' 
            file.filename = file.filename.rsplit('.', 1)[0] + '.enc'
    return print("FL", file.filename)




def pdf_to_txt(file_path):
    text = ""
    try:
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfFileReader(file)
            for page_num in range(reader.numPages):
                text += reader.getPage(page_num).extractText()
    except Exception as e:
        text = str(e)
    return text



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'].encode('utf-8')
        stored_password = r.hget('users', username)
        if stored_password is None:
            flash("El usuario no existe. Por favor, regístrese.", "warning")
            return render_template('login.html')
        if bcrypt.checkpw(password, stored_password):
        #if stored_password and stored_password.decode('utf-8') == password:
            #flash("Ingreso exitoso", "success")
            # Aquí puedes redirigir al usuario a otra vista o hacer alguna otra acción
            session['username'] = username  
            return redirect(url_for('index'))
        else:
            print(flash("Error en el ingreso. Por favor registrese en el sistema.", "Alert"))
    return render_template('login.html')

@app.route('/registro')
def registro():
        return render_template('registro.html') 


def profile():
    session['username'] = username
    if not username:
        return 'Usuario no está en sesión', 401
    user_data = r.hgetall(f'users:{username}')
    if not user_data:
        return 'No se encontraron datos para el usuario', 404
    return f'Datos del usuario {username}: {user_data}'


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user = request.form['user']
        password = request.form['password']
        name = request.form['name']
        surname = request.form['apell']
        email = request.form['email']
        prof = request.form['Prof']
        address2 = request.form['address2']
        pais = request.form['pais']
        ciudad = request.form['ciudad']
        if r.hexists('users', user):
            return "Usuario ya existe"
        else:
            password_bytes = password.encode('utf-8')
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(password_bytes, salt)
            r.hset('users', user, hashed_password)
            r.hset('users', f"{user}:name", name)
            r.hset('users', f"{user}:surname", surname)
            r.hset('users', f"{user}:email", email)
            r.hset('users', f"{user}:prof", prof)
            r.hset('users', f"{user}:address", f"{address2}")
            r.hset('users', f"{user}:pais", pais)
            r.hset('users', f"{user}:ciudad", ciudad)
            flash("El usuario fue registrado correctamente, por favor inicie sesion", "warning")
            return redirect(url_for('login'))
    return render_template('registro.html')

@app.route('/encrypsec', methods=['GET', 'POST'])
def index():
    username = session.get('username')
    if username:
        redis_key = f"users"
        user = f"{username}"
        attributes = ['name', 'surname', 'email', 'prof', 'address', 'pais', 'ciudad']
        keys = [f"{user}:{attribute}" for attribute in attributes]
        values = r.hmget(redis_key, keys)
        decoded_values = [val.decode('utf-8') if isinstance(val, bytes) else val for val in values]
        user_data = dict(zip(attributes, decoded_values))
        print("USRD", user_data)
    else:
        # Manejar el caso donde el username no está en la sesión
        print("Usuario no encontrado en la sesión.")
    message = None
    if request.method == 'POST':
        app.config['UPLOAD_FOLDER'] = 'uploads/'
        print("USER", username)
        file = request.files['file']
        #if file and is_pdf(file):
        filename = file.filename

        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        print("FP", filepath)
        if os.path.exists(filepath):
            #pdf_text = pdf_to_txt(filepath)
            #encrypted_data = cipher.encrypt(pdf_text.encode('utf-8'))
            with open(filepath, 'rb') as f:
                file_data = f.read()
            encrypted_data = cipher.encrypt(file_data)
            
            #filename_without_extension = os.path.splitext(filename)[0]
            #encrypted_filename = filename_without_extension + ".enc"
            #encrypted_filepath = os.path.join(app.config['UPLOAD_FOLDER'], encrypted_filename)
    
            with open(filepath, 'wb') as f:
                f.write(encrypted_data)
            scr = 'iota_advanc_trans.py'
            subprocess.run(['python3', scr, filepath])
            message = "El archivo se encriptó y envió por la red tangle a la billetera del nodo servidor correctamente"
           
        else:
            message = "Tipo de archivo invalido"

            #os.remove(filepath)

            #return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)
            #return "El archi)vo se encriptó correctamenteo"
        #return "Invalid file or file type."
    return render_template('crypsec_fin.html', username=username,message=message, user_data=user_data)

@app.route('/logout')
def logout():
    # Borrar 'username' de la sesión
    session.pop('username')
    # Redirigir al usuario a la página de inicio o de inicio de sesión
    return redirect(url_for('login'))


@app.route('/get_transactions', methods=['GET'])
def get_transactions():
    counter = int(r.get('transaction_counter') or 0)
    transactions = []
    for i in range(1, counter + 1):
        transaction_key = f'transaction:{i}'
        transaction_id = r.hget(transaction_key, 'transaction_id')
        if transaction_id:
            transactions.append(transaction_id.decode('utf-8'))
    return jsonify(transactions)

@app.route('/download_file')
def download_file():
    username = session.get('username')
    scr = 'list_transaction.py'
    subprocess.run(['python3', scr, username])
    filename = r.get('filename')
    directory = 'output/'
    if filename:
        if isinstance(filename, bytes):
            filename = filename.decode('utf-8')
        filepath = os.path.join('output', filename)
        print("FL", directory, filename)
        return send_from_directory(directory, filename, as_attachment=True)
    else:
        return "Archivo no encontrado", 404

@app.route('/documentacion')
def documentacion():
    username = session.get('username')
    return render_template('doc_fin.html', username=username)

@app.route('/table', methods=['GET', 'POST'])  
def table():
    username = session.get('username')
    if username:
        redis_key = f"users"
        user = f"{username}"
        attributes = ['name', 'surname', 'email', 'prof', 'address', 'pais', 'ciudad']
        keys = [f"{user}:{attribute}" for attribute in attributes]
        values = r.hmget(redis_key, keys)
        decoded_values = [val.decode('utf-8') if isinstance(val, bytes) else val for val in values]
        user_data = dict(zip(attributes, decoded_values))
        print("USRD", user_data)
    else:
        # Manejar el caso donde el username no está en la sesión
        print("Usuario no encontrado en la sesión.")
    client = MongoClient('mongodb://localhost:27017/')
    db = client['transaction_his']
    fs = gridfs.GridFS(db)
    archivos = []
    if request.method == 'POST':
        fecha_str = request.form.get('searchDate')
        if fecha_str:
            fecha_inicio = datetime.strptime(fecha_str, '%Y-%m-%d')
            fecha_fin = fecha_inicio + timedelta(days=1)
            cursor = fs.find({"metadata.upload_time": {"$gte": fecha_inicio, "$lt": fecha_fin}})
            for file in cursor:
                archivo_metadata = file.metadata
                archivo_metadata['upload_time'] = archivo_metadata['upload_time'].strftime('%Y-%m-%d %H:%M:%S')
                archivos.append({
                    "id": str(file._id),
                    "metadata": file.metadata,
                    "filename": file.filename
                })
    print("RES", archivos)
    return render_template('crypsec_fin.html', archivos=archivos, user_data=user_data)


if __name__ == '__main__':
    #if not os.path.exists(UPLOAD_FOLDER):
    #    os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True, host='0.0.0.0')

