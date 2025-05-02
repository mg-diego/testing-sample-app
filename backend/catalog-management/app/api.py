from fastapi import FastAPI, HTTPException, Header, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List

from common.jwt_utils import verify_permission
from common.permissions import Permissions
from .service import create_catalog_service, get_catalog_list_service, delete_catalog_service, update_catalog_service
from .models import CatalogItem

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],  
)

@app.post("/catalog/")
def create_catalog_item(item: CatalogItem, authorization: str = Header(...)):
    token = authorization.split(" ")[1]    
    if verify_permission(Permissions.CREATE_CATALOG, token):
        response = create_catalog_service(item)
        logger.info(f"[POST /catalog/] - Catalog created: {item}")
        return response
    else:
        logger.warning(f"[POST /catalog/] - Permission denied to create a catalog. Token: {token}")
        raise HTTPException(status_code=401, detail="Missing permission.")
    
@app.delete("/catalog/")
def delete_catalog_item(catalog_id: str, authorization: str = Header(...)):
    token = authorization.split(" ")[1]    
    if verify_permission(Permissions.DELETE_CATALOG, token):
        response = delete_catalog_service(catalog_id)
        logger.info(f"[DELETE /catalog/] - Catalog deleted: {catalog_id} - {response}")
        return response
    else:
        logger.warning(f"[DELETE /catalog/] - Permission denied to delete catalog. Token: {token}")
        raise HTTPException(status_code=401, detail="Missing permission.")
    
@app.put("/catalog/")
def update_catalog_item(item: CatalogItem, authorization: str = Header(...)):
    token = authorization.split(" ")[1]    
    if verify_permission(Permissions.UPDATE_CATALOG, token):
        response = update_catalog_service(item)
        logger.info(f"[PUT /catalog/] - Catalog updated: {item} - {response}")
        return response
    else:
        logger.warning(f"[PUT /catalog/] - Permission denied to update catalog. Token: {token}")
        raise HTTPException(status_code=401, detail="Missing permission.")

@app.get("/catalog/")
def get_catalog_list(filter: str, authorization: str = Header(...)):
    token = authorization.split(" ")[1]    
    if verify_permission(Permissions.ACCESS_CATALOG_MANAGEMENT, token):
        response = get_catalog_list_service(filter)
        json_response = {"catalog": response }
        logger.info(f"[GET /catalog/] - Catalog list retrieved: {json_response}")
        return json_response
    else:
        logger.warning(f"[GET /catalog/] - Permission denied to retrieve catalog list. Token: {token}")
        raise HTTPException(status_code=401, detail="Missing permission.")