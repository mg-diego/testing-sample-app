

from fastapi import HTTPException


def handle_response(response):
    if not (200 <= response.get('status') < 300):
        raise HTTPException(status_code=response.get('status'), detail=response.get('detail'))   
    else:
        return response