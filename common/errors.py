# Enum for error codes
from enum import Enum
from pydantic import BaseModel


class ErrorCode(Enum):
    INVALID_INPUT = "INVALID_INPUT"
    NOT_FOUND = "NOT_FOUND"
    UNAUTHORIZED = "UNAUTHORIZED"
    INTERNAL_ERROR = "INTERNAL_ERROR"


# Custom error class
class APIError(BaseModel):
    code: ErrorCode
    message: str
    details: str = None


# Example error list, as a dictionary or list
class APIErrorList:
    INVALID_INPUT_ERROR = APIError(code=ErrorCode.INVALID_INPUT, message="The input provided is invalid")
    NOT_FOUND_ERROR = APIError(code=ErrorCode.NOT_FOUND, message="The resource could not be found")
    UNAUTHORIZED_ERROR = APIError(code=ErrorCode.UNAUTHORIZED, message="Unauthorized access")
    INTERNAL_ERROR = APIError(code=ErrorCode.INTERNAL_ERROR, message="An internal server error occurred")