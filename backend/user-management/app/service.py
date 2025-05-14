from http import HTTPStatus

from common.errors import ErrorCode
from common.jwt_utils import create_access_token
from common.errors import ErrorCode
from .database import UserManagementDatabase
from .models import User
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

user_management_database = UserManagementDatabase()

def login_service(username, password):    
    db_status = user_management_database.get_user(username)
    logger.debug(f"DB Status: {db_status}")

    if db_status.get('success'):
        if db_status.get("detail")['password'] == password: 
            user_data = {"username": db_status.get("detail")["username"], "permissions": db_status.get("detail")["permissions"]}
            access_token = create_access_token(data=user_data)
            logger.info(f"[POST /login/] [200] - User login: {username} - {access_token}")

            return { "status": HTTPStatus.OK, "detail": { "access_token": access_token, "token_type": "bearer" } }
        else:
            logger.info(f"[POST /login/] [400] - User login (wrong password): {username}")
            return {"status": HTTPStatus.NOT_FOUND, "detail": ErrorCode.USER_WRONG_PASSWORD.value}
    else:
        if db_status.get('error') == "User not found.":
            logger.info(f"[POST /login/] [404] - User not found: {username}")
            return {"status": HTTPStatus.NOT_FOUND, "detail": ErrorCode.USER_NOT_FOUND.value}
        else:
            logger.info(f"[POST /login/] [500] - Internal Server Error: {db_status.get('error', ErrorCode.UNKNOWN_ERROR.value)}")
            return {
                "status": HTTPStatus.INTERNAL_SERVER_ERROR,
                "detail": db_status.get("error", ErrorCode.UNKNOWN_ERROR.value)
            }   

def get_user_list_service():
    db_status = user_management_database.get_user_list()
    logger.debug(f"DB Status: {db_status}")

    if db_status.get('success'):
        logger.info(f"[GET /users/] [200] - User list retrieved.")
        return {"status": HTTPStatus.OK, "detail": db_status.get("detail")}
    else:
        logger.info(f"[GET /users/] [500] - Internal Server Error: {db_status.get('error', ErrorCode.UNKNOWN_ERROR.value)}")
        return {
            "status": HTTPStatus.INTERNAL_SERVER_ERROR,
            "detail": db_status.get("error", ErrorCode.UNKNOWN_ERROR.value)
        }

def create_user_service(user: User):
    if not user.username.strip():
        logger.info(f"[POST /users/] [400] - Username can't be empty: {user}")
        return {"status": HTTPStatus.BAD_REQUEST, "detail": ErrorCode.EMPTY_USERNAME.value}

    if not user.password.strip():
        logger.info(f"[POST /users/] [400] - Password can't be empty: {user}")
        return {"status": HTTPStatus.BAD_REQUEST, "detail": ErrorCode.EMPTY_PASSWORD.value}

    if not user.permissions:
        logger.info(f"[POST /users/] [400] - At least 1 permission should be assigned: {user}")
        return {"status": HTTPStatus.BAD_REQUEST, "detail": ErrorCode.NO_PERMISSION_ASSIGNED.value}

    db_user_list = user_management_database.get_user_list()
    logger.info(f"DB User List: {db_user_list}")

    if not db_user_list.get("success"):
        error = db_user_list.get("error", ErrorCode.UNKNOWN_ERROR.value)
        logger.info(f"[POST /users/] [500] - Internal Server Error: {error}")
        return {"status": HTTPStatus.INTERNAL_SERVER_ERROR, "detail": error}

    # Proceed if we got a successful response and list is not empty
    if not any(db_user.get("username") == user.username for db_user in db_user_list.get("detail", [])):
        db_status = user_management_database.create_user(user.username, user.password, user.permissions)
        logger.debug(f"DB Status: {db_status}")

        if db_status.get("success"):
            logger.info(f"[POST /users/] [200] - User created: {user}")
            return {"status": HTTPStatus.OK, "detail": ""}

        error = db_status.get("error", ErrorCode.UNKNOWN_ERROR.value)
        logger.info(f"[POST /users/] [500] - Internal Server Error: {error}")
        return {"status": HTTPStatus.INTERNAL_SERVER_ERROR, "detail": error}

    logger.info(f"[POST /users/] [409] - No existing users found or duplicate prevention logic needed.")
    return {"status": HTTPStatus.CONFLICT, "detail": ErrorCode.ALREADY_EXIST.value}


def delete_user_service(username: str):
    if username == "":
        logger.info(f"[DELETE /users/] [400] - Username can't be empty: {username}")
        return {"status": HTTPStatus.BAD_REQUEST, "detail": ErrorCode.EMPTY_USERNAME.value}       
    
    if username.lower() == "admin":
        logger.info(f"[POST /users/] [401] - Admin user can't be deleted: {username}")
        return {"status": HTTPStatus.FORBIDDEN, "detail": ErrorCode.CANT_DELETE_ADMIN_USER.value}
  
    db_status = user_management_database.delete_user(username)
    logger.debug(f"DB Status: {db_status}")

    if db_status.get('success'):
        logger.info(f"[DELETE /user/] [200] - User deleted: {username}")
        return {"status": HTTPStatus.OK, "detail": ""}
    else:
        if db_status.get('error') == "User not found.":
            logger.info(f"[DELETE /users/] [404] - User not found: {username}")
            return {"status": HTTPStatus.NOT_FOUND, "detail": ErrorCode.NOT_FOUND.value}
        else:
            logger.info(f"[DELETE /users/] [500] - Internal Server Error: {db_status.get('error', ErrorCode.UNKNOWN_ERROR.value)}")
            return {
                "status": HTTPStatus.INTERNAL_SERVER_ERROR,
                "detail": db_status.get("error", ErrorCode.UNKNOWN_ERROR.value)
            }
    