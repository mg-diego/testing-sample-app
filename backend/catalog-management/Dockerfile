# Imagen base oficial de Python
FROM python:3.11-slim

# Copiar código común
WORKDIR /app/common
COPY common /app/common
RUN pip install -r requirements.txt

# Crear directorio y copiar /app
WORKDIR /app
COPY backend/catalog-management/app ./app
COPY backend/catalog-management/requirements.txt ./app/requirements.txt
RUN pip install -r ./app/requirements.txt

# Expone el puerto por defecto del microservicio
EXPOSE 8002

# Comando para arrancar la API
WORKDIR /app
CMD ["sh", "-c", "uvicorn app.api:app --host 0.0.0.0 --port 8002"]


