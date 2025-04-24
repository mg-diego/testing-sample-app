#!/bin/bash

# Variables de conexión
DB_HOST=${DB_HOST:-postgres}  # Asegúrate de usar 'postgres' como nombre de host
DB_PORT=${DB_PORT:-5432}
DB_USER=${DB_USER:-user}
DB_NAME=${DB_NAME:-users}
DB_PASSWORD=${DB_PASSWORD:-password}

# Comando SQL para crear la tabla si no existe
CREATE_TABLE_QUERY="CREATE TABLE IF NOT EXISTS public.users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(100) NOT NULL,
    permissions TEXT[]
);"

# Comando SQL para verificar si el usuario ya existe
SQL_QUERY="SELECT 1 FROM public.users WHERE username='admin';"

# Comando SQL para insertar el usuario admin si no existe
INSERT_QUERY="INSERT INTO public.users (username, password, permissions) 
              VALUES ('admin', 'admin', ARRAY['ACCESS_USER_MANAGEMENT', 'ACCESS_CATALOG_MANAGEMENT', 'READ_USERS', 'CREATE_USERS', 'DELETE_USERS', 'CREATE_CATALOG']);"

# Crear la tabla si no existe
echo "Creando tabla users si no existe..."
PGPASSWORD=$DB_PASSWORD psql -U $DB_USER -d $DB_NAME -h $DB_HOST -p $DB_PORT -c "$CREATE_TABLE_QUERY"

# Ejecutar la consulta y verificar si el usuario admin existe
USER_EXISTS=$(PGPASSWORD=$DB_PASSWORD psql -U $DB_USER -d $DB_NAME -h $DB_HOST -p $DB_PORT -t -c "$SQL_QUERY")

# Si el usuario no existe, insertamos el nuevo usuario admin
if [ -z "$USER_EXISTS" ]; then
    echo "El usuario admin no existe. Creando usuario admin..."
    PGPASSWORD=$DB_PASSWORD psql -U $DB_USER -d $DB_NAME -h $DB_HOST -p $DB_PORT -c "$INSERT_QUERY"
    echo "Usuario admin creado exitosamente."
else
    echo "El usuario admin ya existe. No se realiza ninguna acción."
fi
