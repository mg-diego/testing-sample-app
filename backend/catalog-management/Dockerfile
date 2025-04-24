# Imagen base oficial de Python
FROM python:3.11-slim

# Establece directorio de trabajo
WORKDIR /app

# Copia los requirements
COPY requirements.txt .

# Instala dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el código fuente
COPY . .

# Expone el puerto por defecto del microservicio
EXPOSE 8002

# Comando para arrancar la API
CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "8002"]
