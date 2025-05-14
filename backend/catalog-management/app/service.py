from .database import CatalogManagementDatabase
from .models import CatalogItem
from common.errors import ErrorCode
from http import HTTPStatus
import logging

catalog_management_database = CatalogManagementDatabase()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_catalog_service(catalog: CatalogItem):
    if not catalog.name.strip():
        logger.info(f"[POST /catalog/] [400] - Name can't be empty: {catalog}")
        return {"status": HTTPStatus.BAD_REQUEST, "detail": ErrorCode.EMPTY_NAME.value}

    if not catalog.description.strip():
        logger.info(f"[POST /catalog/] [400] - Description can't be empty: {catalog}")
        return {"status": HTTPStatus.BAD_REQUEST, "detail": ErrorCode.EMPTY_DESCRIPTION.value}

    response = catalog_management_database.get_items(catalog.name)
    if not response.get("success"):
        logger.info(f"[POST /catalog/] [500] - Internal Server Error: {response.get('error', 'Unknown error')}")
        return {
            "status": HTTPStatus.INTERNAL_SERVER_ERROR,
            "detail": response.get("error", ErrorCode.UNKNOWN_ERROR.value)
        }

    if response.get("detail"):  # If catalog name already exists
        logger.info(f"[POST /catalog/] [409] - Catalog with name '{catalog.name}' already exists.")
        return {"status": HTTPStatus.CONFLICT, "detail": ErrorCode.ALREADY_EXIST.value}

    db_status = catalog_management_database.create_item(catalog)
    logger.debug(f"DB Status: {db_status}")

    if db_status.get("success"):
        logger.info(f"[POST /catalog/] [200] - Catalog created: {catalog}")
        return {"status": HTTPStatus.OK, "detail": catalog.model_dump(by_alias=True)}

    logger.info(f"[POST /catalog/] [500] - Internal Server Error: {db_status.get('error', 'Unknown error')}")
    return {
        "status": HTTPStatus.INTERNAL_SERVER_ERROR,
        "detail": db_status.get("error", ErrorCode.UNKNOWN_ERROR.value)
    }
  

def get_catalog_list_service(filter: str):
    db_status = catalog_management_database.get_items(filter)
    logger.debug(f"DB Status: {db_status}")

    if db_status.get("success"):
        logger.info(f"[GET /catalog/] - Catalog list retrieved: {db_status.get('detail')}")
        return {"status": HTTPStatus.OK, "detail": db_status.get("detail")}
    else:
        return {
            "status": HTTPStatus.INTERNAL_SERVER_ERROR,
            "detail": db_status.get("error", ErrorCode.UNKNOWN_ERROR.value)
        }
    

def delete_catalog_service(catalog_id: str):
    if catalog_id == "":
        logger.info(f"[DELETE /catalog/] [400] - ID can't be empty: {catalog_id}")
        return {"status": HTTPStatus.BAD_REQUEST, "detail": ErrorCode.EMPTY_ID.value}
    
    db_status = catalog_management_database.delete_item(catalog_id)
    logger.debug(f"DB Status: {db_status}")

    if db_status.get("success"):
        logger.info(f"[DELETE /catalog/] - Catalog deleted: {catalog_id}")
        return {"status": HTTPStatus.OK, "detail": catalog_id}
    else:
        if db_status.get("error") == 'No document matched the provided ID.':
            return {"status": HTTPStatus.NOT_FOUND, "detail": ErrorCode.NOT_FOUND.value}
        else:
            return {
                "status": HTTPStatus.INTERNAL_SERVER_ERROR,
                "detail": db_status.get("error", ErrorCode.UNKNOWN_ERROR.value)
            }

def update_catalog_service(catalog: CatalogItem):
    if not catalog.id.strip():
        return {"status": HTTPStatus.BAD_REQUEST, "detail": ErrorCode.EMPTY_ID.value}
    if not catalog.name.strip():
        return {"status": HTTPStatus.BAD_REQUEST, "detail": ErrorCode.EMPTY_NAME.value}
    if not catalog.description.strip():
        return {"status": HTTPStatus.BAD_REQUEST, "detail": ErrorCode.EMPTY_DESCRIPTION.value}

    response = catalog_management_database.get_items(catalog.name)
    if not response.get("success"):
        return {
            "status": HTTPStatus.INTERNAL_SERVER_ERROR,
            "detail": response.get("error", ErrorCode.UNKNOWN_ERROR.value)
        }

    if response.get("detail"):  # If catalog name already exists
        return {
            "status": HTTPStatus.CONFLICT,
            "detail": ErrorCode.ALREADY_EXIST.value
        }

    db_status = catalog_management_database.update_item(catalog)
    logger.debug(f"DB Status: {db_status}")

    if db_status.get("success"):
        logger.info(f"[PUT /catalog/] - Catalog updated: {catalog}")
        return {"status": HTTPStatus.OK, "detail": catalog.model_dump(by_alias=True)}

    if db_status.get("error") == "No document matched the provided ID.":
        return {"status": HTTPStatus.NOT_FOUND, "detail": ErrorCode.NOT_FOUND.value}

    return {
        "status": HTTPStatus.INTERNAL_SERVER_ERROR,
        "detail": db_status.get("error", ErrorCode.UNKNOWN_ERROR.value)
    }
    