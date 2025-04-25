from fastapi import FastAPI, HTTPException, Header, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List

from common.jwt_utils import create_access_token, verify_permission
from common.permissions import Permissions
from .models import User
from .service import login_service, get_user_list_service, create_user_service, delete_user_service

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

@app.post("/login/")
def login(username: str, password: str):
    logger.info(f"[POST /login/] - Login attempt for username: {username}")
    response = login_service(username, password)

    if response == 'User not found' or response == 'Incorrect password':
        logger.error(f"[POST /login/ - Failed login for username: {username} - Reason: {response}")
        raise HTTPException(status_code=404, detail=response)
    
    user_data = {"username": response["username"], "permissions": response["permissions"]}

    access_token = create_access_token(data=user_data)
    logger.info(f"[POST /login/] - Login successful for username: {username} - Token: {access_token}")
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@app.get("/users/", response_model=List[User])
def get_user_list(authorization: str = Header(...)):
    token = authorization.split(" ")[1]    
    if verify_permission(Permissions.READ_USERS, token): 
        response = get_user_list_service()
        logger.info(f"[GET /users/] - User list retrieved: {response}")
        return response        
    else:
        logger.warning(f"[GET /users/] - Permission denied for retrieving user list. Token: {token}")
        raise HTTPException(status_code=401, detail="Missing permission.")
    

@app.post("/users/", response_model=User)
def create_user(body: User, authorization: str = Header(...)):
    token = authorization.split(" ")[1]    
    if verify_permission(Permissions.CREATE_USERS, token):
        response = create_user_service(body)

        if response == "Username can't be empty." or response == "Password can't be empty." or response == "At least 1 permission should be assigned.":
            logger.error(f"[POST /users/ - Failed create user: {response}")
            raise HTTPException(status_code=400, detail=response)
    
        logger.info(f"[POST /users/] - User created: {response}")
        return response
    else:
        logger.warning(f"[POST /users/] - Permission denied for creating user. Token: {token}")
        raise HTTPException(status_code=401, detail="Missing permission.")
    

@app.delete("/users/", response_model=dict)
def delete_user(username: str = Query(...), authorization: str = Header(...)):
    token = authorization.split(" ")[1]

    if verify_permission(Permissions.DELETE_USERS, token):
        response = delete_user_service(username)

        if response == "Username can't be empty.":
            logger.error(f"[DELETE /users/ - Failed delete user: {response}")
            raise HTTPException(status_code=400, detail=response)
    
        if response:
            logger.info(f"[DELETE /users/] - User deleted: {username}")
            return {"message": f"User '{username}' deleted successfully."}
        else:
            logger.warning(f"[DELETE /users/] - Failed to delete user: {username}")
            raise HTTPException(status_code=404, detail="User not found or deletion failed.")
    else:
        logger.warning(f"[DELETE /users/] - Permission denied. Token: {token}")
        raise HTTPException(status_code=401, detail="Missing permission.")
