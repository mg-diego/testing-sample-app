from fastapi import FastAPI, HTTPException, Header, Query
from fastapi.middleware.cors import CORSMiddleware

from common.jwt_utils import verify_permission
from common.permissions import Permissions
from common.api_utils import handle_response
from .service import get_translations_service, set_active_language_service, get_active_language_service

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

@app.get("/language/translations")
def get_language_translations(): 
    response = get_translations_service()
    logger.info(f"[GET /language/translations/] - Translations retrieved: {response}")
    return response

@app.get("/language/")
def get_language(authorization: str = Header(...)):
    token = authorization.split(" ")[1]    
    if verify_permission(Permissions.SET_LANGUAGE, token):
        handle_response(get_active_language_service())
    else:
        logger.warning(f"[GET /language/] - Permission denied. Token: {token}")
        raise HTTPException(status_code=401, detail="Missing permission.")
    

@app.post("/language/")
def set_language(language: str, authorization: str = Header(...)):
    token = authorization.split(" ")[1]    
    if verify_permission(Permissions.SET_LANGUAGE, token):
        handle_response(set_active_language_service(language))
    else:
        logger.warning(f"[POST /language/] - Permission denied. Token: {token}")
        raise HTTPException(status_code=401, detail="Missing permission.")