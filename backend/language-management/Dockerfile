FROM python:3.11-slim

RUN apt-get update && apt-get install -y postgresql-client

# Copiar código común
WORKDIR /app/common
COPY common /app/common
RUN pip install -r requirements.txt

# Crear directorio y copiar /app
WORKDIR /app
COPY backend/user-management/app ./app
COPY backend/user-management/requirements.txt ./app/requirements.txt
COPY backend/user-management/scripts/create_default_language.sh /scripts/create_default_language.sh
RUN chmod +x /scripts/create_default_language.sh
RUN pip install -r ./app/requirements.txt

WORKDIR /app
CMD ["sh", "-c", "/scripts/create_default_language.sh && uvicorn app.api:app --host 0.0.0.0 --port 8003"]

