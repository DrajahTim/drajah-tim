from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
import uuid

from backend.core.database import get_async_db
from backend.core.security import oauth2_scheme, decode_access_token
from backend.crud import crud_user
from backend.models.user import User, UserRole # Import User model and UserRole
from backend.schemas.token import TokenData

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

async def get_current_user(
    db: AsyncSession = Depends(get_async_db), token: str = Depends(oauth2_scheme)
) -> User:
    """
    Dependency to get the current user from a token.
    Decodes the token, retrieves the user by ID from the database.
    Raises HTTPException if token is invalid or user not found.
    """
    token_data: TokenData = await decode_access_token(token, credentials_exception)
    if token_data.user_id is None: # Should be caught by decode_access_token, but as a safeguard
        raise credentials_exception

    user = await crud_user.get_user_by_id(db, user_id=token_data.user_id)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Dependency to get the current active user.
    Builds on get_current_user and checks if the user is active (e.g. not banned).
    For now, all users are considered active after creation, this can be expanded.
    If User model had an `is_active: bool` field, it would be checked here.
    """
    # if not current_user.is_active: # Example if User model had an is_active field
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return current_user

# Example of a role-based access dependency (can be added later)
# def require_role(required_role: UserRole):
#     async def role_checker(current_user: User = Depends(get_current_active_user)) -> User:
#         if current_user.role != required_role and current_user.role != UserRole.SUPER_ADMIN: # Super admin bypasses
#             raise HTTPException(
#                 status_code=status.HTTP_403_FORBIDDEN,
#                 detail=f"User does not have the required role: {required_role.value}"
#             )
#         return current_user
#     return role_checker
