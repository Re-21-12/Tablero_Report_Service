# Imagen base de Python
FROM python:3.11-slim

# Configurar el directorio de trabajo
WORKDIR /app

# Copiar los archivos
COPY . /app

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto Flask
EXPOSE 5000

# Variable de entorno para Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Ejecutar la app
CMD ["flask", "run"]
