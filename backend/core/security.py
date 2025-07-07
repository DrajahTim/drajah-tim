from datetime import datetime, timedelta, timezone
from typing import Optional, Any, Union
from jose import JWTError, jwt
from passlib.context import CryptContext

from backend.core.config import settings

# Password Hashing using passlib
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plain password against a hashed password."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hashes a plain password."""
    return pwd_context.hash(password)


# JWT Token Handling using python-jose
def create_access_token(
    subject: Union[str, Any], expires_delta: Optional[timedelta] = None
) -> str:
    """
    Creates a new JWT access token.
    :param subject: The subject of the token (e.g., user ID or email).
    :param expires_delta: Optional timedelta for token expiry. If None, uses default from settings.
    :return: The encoded JWT access token.
    """
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt

# The verify_token function will be more useful when we have the OAuth2 password bearer flow.
# For now, a basic structure. It would typically be used in a dependency that extracts
# the token from the request and verifies it.

# Example structure for a token verification function (to be expanded later)
# from fastapi import HTTPException, status
# from backend.schemas.token import TokenData
#
# async def decode_access_token(token: str, credentials_exception: HTTPException) -> TokenData:
#     """
#     Decodes an access token.
#     :param token: The JWT token string.
#     :param credentials_exception: Exception to raise if token is invalid.
#     :return: TokenData schema containing the payload.
#     """
#     try:
#         payload = jwt.decode(
#             token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
#         )
#         user_id: Optional[str] = payload.get("sub")
#         if user_id is None:
#             raise credentials_exception
#         token_data = TokenData(user_id=user_id) # In Pydantic v2, use user_id=uuid.UUID(user_id) if sub is UUID
#     except JWTError:
#         raise credentials_exception
#     return token_data
