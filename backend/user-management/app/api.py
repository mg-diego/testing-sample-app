from fastapi import FastAPI, HTTPException, Header, Query
from fastapi.middleware.cors import CORSMiddleware

from common.jwt_utils import verify_permission, verify_token
from common.permissions import Permissions
from common.api_utils import handle_response
from common.errors import ErrorCode
from .models import User
from .service import login_service, get_user_list_service, create_user_service, delete_user_service

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("uvicorn.access")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],  
)

@app.post("/login/")
def login(username: str, password: str):
    return handle_response(login_service(username, password))

@app.get("/users/")
def get_user_list(authorization: str = Header(...)):
    token = authorization.split(" ")[1]    
    if verify_permission(Permissions.READ_USERS, token): 
        return handle_response(get_user_list_service())
    else:
        logger.warning(f"[GET /users/] - Permission denied for retrieving user list. Token: {token}")
        raise HTTPException(status_code=401, detail=ErrorCode.UNAUTHORIZED.value)
    

@app.post("/users/")
def create_user(body: User, authorization: str = Header(...)):
    token = authorization.split(" ")[1]    
    if verify_permission(Permissions.CREATE_USERS, token):
        return handle_response(create_user_service(body))
    else:
        logger.warning(f"[POST /users/] - Permission denied for creating user. Token: {token}")
        raise HTTPException(status_code=401, detail=ErrorCode.UNAUTHORIZED.value)
    

@app.delete("/users/")
def delete_user(username: str = Query(...), authorization: str = Header(...)):
    token = authorization.split(" ")[1]

    if verify_permission(Permissions.DELETE_USERS, token):
        if verify_token(token)['username'] == username:
            raise HTTPException(status_code=403, detail=ErrorCode.CANT_DELETE_OWN_USER.value)
        return handle_response(delete_user_service(username))
    else:
        logger.warning(f"[DELETE /users/] - Permission denied. Token: {token}")
        raise HTTPException(status_code=401, detail=ErrorCode.UNAUTHORIZED.value)
