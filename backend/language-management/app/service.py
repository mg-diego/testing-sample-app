from http import HTTPStatus
import json
import logging
import os
from common.errors import ErrorCode
from .database import LanguageManagementDatabase

language_management_database = LanguageManagementDatabase()

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def get_translations_service():
    active_language = language_management_database.get_active_language()['detail']
    return read_json_file(f'translations', f"{active_language}.json")

def set_active_language_service(new_active_language):
    db_status = language_management_database.set_active_language(new_active_language)
    logger.debug(f"DB Status: {db_status}")

    if db_status.get('success'):
        logger.info(f"[POST /language/] [200] - Language set to: {new_active_language}")
        return {"status": HTTPStatus.OK, "detail": ""}
    else:
        logger.info(f"[POST /language/] [500] - Internal Server Error: {db_status.get('error', ErrorCode.UNKNOWN_ERROR.value)}")
        return {
            "status": HTTPStatus.INTERNAL_SERVER_ERROR,
            "detail": db_status.get("error", ErrorCode.UNKNOWN_ERROR.value)
        }

def get_active_language_service():
    db_status = language_management_database.get_active_language()
    logger.debug(f"DB Status: {db_status}")

    if db_status.get('success'):
        logger.info(f"[GET /language/] [200] - Language retrieved: {db_status.get('detail')}")
        return {"status": HTTPStatus.OK, "detail": db_status.get('detail')}
    else:
        if db_status.get('error') == "No language is configured.":
            return { "status": HTTPStatus.NOT_FOUND, "detail": ErrorCode.NO_LANGUAGE.value }
        else:
            logger.info(f"[GET /language/] [500] - Internal Server Error: {db_status.get('error', ErrorCode.UNKNOWN_ERROR.value)}")
            return {
                "status": HTTPStatus.INTERNAL_SERVER_ERROR,
                "detail": db_status.get("error", ErrorCode.UNKNOWN_ERROR.value)
            }

def read_json_file(folder, filename):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(base_dir, folder, filename)
    with open(path, 'r', encoding='utf-8') as file:
        return json.load(file)
