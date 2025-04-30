docker build -f frontend/Dockerfile -t ui-service .
docker build -f backend/user-management/Dockerfile -t user-management-service .
docker build -f backend/catalog-management/Dockerfile -t catalog-management-service .
docker build -f backend/language-management/Dockerfile -t language-management-service .
docker build -f database/postgres/Dockerfile -t db-postgres .
