#!/bin/bash
set -e

echo "Running init-db.sh to create 'testing-sample-app' database..."

# Variables de conexión
DB_HOST=${DB_HOST:-postgres}
DB_PORT=${DB_PORT:-5432}
DB_USER=${DB_USER:-user}
DB_NAME="testing-sample-app"
DB_PASSWORD=${DB_PASSWORD:-password}

# Create the database only if it doesn't exist
psql -v ON_ERROR_STOP=1 --username "$DB_USER" --dbname "postgres" <<-EOSQL
    DO \$\$
    BEGIN
        IF NOT EXISTS (
            SELECT FROM pg_database WHERE datname = '${DB_NAME}'
        ) THEN
            CREATE DATABASE "${DB_NAME}";
            RAISE NOTICE 'Database "${DB_NAME}" created.';
        ELSE
            RAISE NOTICE 'Database "${DB_NAME}" already exists.';
        END IF;
    END
    \$\$;
EOSQL

echo "Database initialization complete."
