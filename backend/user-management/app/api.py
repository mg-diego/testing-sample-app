from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from typing import List

from common.jwt_utils import create_access_token, verify_permission
from common.permissions import Permissions
from .models import User
from .service import login_service, get_user_list_service

import logging

# Configurar el logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite solicitudes desde cualquier origen (en producción, es recomendable restringir esto)
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permite todos los encabezados
)

# Endpoint de login
@app.post("/login/")
def login(username: str, password: str):
    response = login_service(username, password)

    if response == 'User not found' or response == 'Incorrect password':
        raise HTTPException(status_code=404, detail=response)
    
    user_data = {"username": response["username"], "permissions": response["permissions"]}

    # Generar el token JWT
    access_token = create_access_token(data=user_data)
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@app.get("/users/", response_model=List[User])
def get_user_list(authorization: str = Header(...)):
    token = authorization.split(" ")[1]
    print(token)
    if verify_permission(Permissions.READ_USERS, token):      
        return get_user_list_service()
    else:
        raise HTTPException(status_code=401, detail="Missing permission.")
