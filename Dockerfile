# Usar una imagen base de Python 3.11 completa
FROM python:3.11

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar los archivos de requisitos
COPY requirements.txt .

# Instalar las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto de los archivos de la aplicación
COPY . .

# Exponer el puerto
EXPOSE 8080

# Comando para ejecutar la aplicación
CMD ["python", "main.py"]