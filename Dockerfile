# Utiliza la imagen base oficial de Ubuntu 22.04
FROM ubuntu:22.04

# Actualiza los paquetes e instala las dependencias necesarias
RUN apt-get update && apt-get install -y \
    python3-pip \
    python3 \
    nginx \
    curl && \
    rm -rf /var/lib/apt/lists/*

# Copia el archivo de configuración de Nginx en su lugar
COPY nginx.conf /etc/nginx/sites-available/default

# Instala las dependencias de Flask
COPY requirements.txt /tmp/
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt

# Copia el código de la aplicación al contenedor en el directorio /app
COPY . /app
WORKDIR /app

# Expone los puertos en los que se ejecutará la aplicación Flask y Nginx
EXPOSE 80
EXPOSE 8080

# Define el comando para ejecutar la aplicación Flask con Gunicorn y Nginx
CMD gunicorn -w 4 -b 0.0.0.0:8000 wsgi:app & nginx -g 'daemon off;'
