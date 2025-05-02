db = db.getSiblingDB('testing-sample-app');

db.createCollection('catalog');

print("Database 'testing-sample-app' and initial collection 'catalog' created.");