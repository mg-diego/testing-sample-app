# Start from the official PostgreSQL image
FROM postgres:14

# Copy the initialization script into the image
COPY database/postgres/init-db.sh /docker-entrypoint-initdb.d/init-db.sh
RUN chmod +x /docker-entrypoint-initdb.d/init-db.sh