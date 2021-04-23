"""API dependencies."""


import os
from typing import Union

from fastapi import HTTPException, Security
from fastapi.security.api_key import APIKeyHeader
from starlette import status

API_KEY = os.environ["API_KEY"]
API_KEY_NAME = "access_token"

api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)


async def get_api_key(
    api_key: str = Security(api_key_header),
) -> Union[str, HTTPException]:
    """Verify the API key of the request.

    Args:
        api_key (str, optional): The request API key. Defaults to Security(api_key_header).

    Raises:
        HTTPException: Exception is raised if keys do not match

    Returns:
        Union[str, HTTPException]: Returns the key if it matches, or an exception.
    """
    if api_key == API_KEY:
        return api_key

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, detail="Could not validate API key"
    )
