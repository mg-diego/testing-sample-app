FROM python:3.11-slim

# Copiar código común
WORKDIR /app/common
COPY common /app/common
RUN pip install -r requirements.txt

WORKDIR /app
COPY frontend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY frontend .

EXPOSE 8501

# Comando para lanzar Streamlit (sin navegador)
CMD ["streamlit", "run", "app.py", "--server.enableCORS=false", "--server.enableXsrfProtection=false", "--server.address=0.0.0.0"]
