FROM python:3.10-slim

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Crear directorio de trabajo
WORKDIR /app

# Copiar requirements
COPY requirements.txt .

# Instalar dependencias Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar TODO el proyecto
COPY . .

# Exponer puerto requerido por HuggingFace
EXPOSE 7860

# Comando de arranque
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]

FROM python:3.10-slim

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Crear directorio de trabajo
WORKDIR /app

# Copiar requirements
COPY requirements.txt .

# Instalar dependencias Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar TODO el proyecto
COPY . .

# Exponer puerto requerido por HuggingFace
EXPOSE 7860

# Comando de arranque
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]

FROM python:3.10-slim

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Crear directorio de trabajo
WORKDIR /app

# Copiar requirements
COPY requirements.txt .

# Instalar dependencias Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar TODO el proyecto
COPY . .

# Exponer puerto requerido por HuggingFace
EXPOSE 7860

# Comando de arranque
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]

FROM python:3.10-slim

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Crear directorio de trabajo
WORKDIR /app

# Copiar requirements
COPY requirements.txt .

# Instalar dependencias Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar TODO el proyecto
COPY . .

# Exponer puerto requerido por HuggingFace
EXPOSE 7860

# Comando de arranque
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]

FROM python:3.10-slim

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Crear directorio de trabajo
WORKDIR /app

# Copiar requirements
COPY requirements.txt .

# Instalar dependencias Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar TODO el proyecto
COPY . .

# Exponer puerto requerido por HuggingFace
EXPOSE 7860

# Comando de arranque
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]

FROM python:3.10-slim

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Crear directorio de trabajo
WORKDIR /app

# Copiar requirements
COPY requirements.txt .

# Instalar dependencias Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar TODO el proyecto
COPY . .

# Exponer puerto requerido por HuggingFace
EXPOSE 7860

# Comando de arranque
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]

