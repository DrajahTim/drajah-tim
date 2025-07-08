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

from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import uuid # For converting string UUID from token sub back to UUID object

from backend.schemas.token import TokenData # Make sure TokenData schema is defined

# Instance of OAuth2PasswordBearer, tokenUrl should point to your token endpoint
# Adjust the tokenUrl as per your router prefix. If your auth router is at /api/v1/auth and token endpoint is /token:
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")


async def decode_access_token(token: str, credentials_exception: HTTPException) -> TokenData:
    """
    Decodes an access token.
    :param token: The JWT token string.
    :param credentials_exception: Exception to raise if token is invalid.
    :return: TokenData schema containing the payload (user_id).
    """
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        subject: Optional[str] = payload.get("sub")
        if subject is None:
            raise credentials_exception

        # Attempt to convert subject to UUID. If it fails, it's not a valid ID.
        try:
            user_id_uuid = uuid.UUID(subject)
        except ValueError:
            raise credentials_exception

        token_data = TokenData(user_id=user_id_uuid)
    except JWTError: # Catches errors from jwt.decode like ExpiredSignatureError, InvalidTokenError
        raise credentials_exception
    return token_data
