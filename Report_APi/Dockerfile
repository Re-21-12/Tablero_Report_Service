FROM python:3.11

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos del proyecto al contenedor
COPY . /app

# Instala las dependencias
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expone el puerto 5000
EXPOSE 5000

# Variable de entorno para Flask
ENV FLASK_APP=app.py

# Comando para ejecutar la aplicación Flask
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
