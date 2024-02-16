from uuid import UUID

from fastapi import HTTPException, status, Depends
from fastapi.security import APIKeyHeader
from fastapi.security.utils import get_authorization_scheme_param

header_scheme = APIKeyHeader(name="Authorization")


def verify(key: str = Depends(header_scheme)):
    """Guard to verify request contain expected Authorization header and key is valid"""
    scheme, param = get_authorization_scheme_param(key)

    if scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header is missing or malformed.",
        )

    if _validate_key(param) is False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API KEY is not valid.",
        )

    return True


def _validate_key(key: str) -> bool:
    """
    Check that provided key is a valid UUID
    :param key: string with UUID format
    :return: true if valid false otherwise

    :note: using this approach to avoid overcomplexity,
    in a real scenario authentication should be based on something more robust like JWT or another kind of token
    """

    try:
        _ = UUID(key, version=4)
        return True
    except ValueError:
        return False
