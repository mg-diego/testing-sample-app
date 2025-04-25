# Imagen base oficial de Python
FROM python:3.11-slim

# Crear directorio y copiar /app
WORKDIR /app
COPY backend/catalog-management/app ./app
COPY backend/catalog-management/requirements.txt ./app/requirements.txt
RUN pip install -r ./app/requirements.txt

# Expone el puerto por defecto del microservicio
EXPOSE 8002

# Comando para arrancar la API
CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "8002"]
