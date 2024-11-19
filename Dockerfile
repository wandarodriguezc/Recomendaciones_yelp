# Usar una imagen base de Ubuntu completa y estable
FROM ubuntu:20.04

# Establecer el directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema y Python 3.10 desde un PPA
RUN apt-get update && apt-get install -y \
    software-properties-common \
    && add-apt-repository ppa:deadsnakes/ppa \
    && apt-get update && apt-get install -y \
    python3.10 \
    python3.10-venv \
    python3.10-dev \
    gcc \
    build-essential \
    libatlas-base-dev \
    gfortran \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Crear un enlace simbólico para python3 si no existe
RUN ln -sf /usr/bin/python3.10 /usr/bin/python3

# Instalar pip para Python 3.10
RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3.10

# Crear un enlace simbólico para pip si no existe
RUN ln -sf /usr/local/bin/pip3.10 /usr/local/bin/pip

# Copiar los archivos de requisitos
COPY requirements.txt .

# Instalar las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto de los archivos de la aplicación
COPY . .

# Exponer el puerto
EXPOSE 8080

# Comando para ejecutar la aplicación
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "main:server"]
