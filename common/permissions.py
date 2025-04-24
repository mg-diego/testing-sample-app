from enum import Enum

class Permissions(Enum):
    ACCESS_USER_MANAGEMENT = 1
    ACCESS_CATALOG_MANAGEMENT = 2
    READ_USERS = 3
    CREATE_USERS = 4
    DELETE_USERS = 5
    CREATE_CATALOG = 6