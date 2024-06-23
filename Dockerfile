# Usa una imagen base de Python
FROM python:3.9-slim

# Establece el directorio de trabajo
WORKDIR /app

# Instala netcat-openbsd
RUN apt-get update && apt-get install -y netcat-openbsd

# Copia los archivos de requisitos, el script y el archivo wait-for-it.sh
COPY requirements.txt requirements.txt
COPY app.py app.py
COPY wait-for-it.sh wait-for-it.sh

# Haz que el script wait-for-it.sh sea ejecutable
RUN chmod +x wait-for-it.sh

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Ejecuta el script de espera y luego la aplicación
CMD ["./wait-for-it.sh", "postgres:5432", "mysql:3306", "--", "python", "app.py"]
