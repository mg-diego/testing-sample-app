from enum import Enum

class Permissions(Enum):
    ACCESS_USER_MANAGEMENT = 1
    ACCESS_CATALOG_MANAGEMENT = 2
    SET_LANGUAGE = 3

    READ_USERS = 4
    CREATE_USERS = 5
    DELETE_USERS = 6

    CREATE_CATALOG = 7
    UPDATE_CATALOG = 8
    DELETE_CATALOG = 9
    