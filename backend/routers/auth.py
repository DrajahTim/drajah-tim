from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
import uuid

from backend.core.database import get_async_db
from backend.core.security import create_access_token, verify_password
from backend.crud import crud_user
from backend.schemas import user as user_schemas # Alias to avoid conflict with models.user
from backend.schemas import token as token_schemas
from backend.dependencies import get_current_active_user # Using active user for /me
from backend.models import user as user_models # Alias for model access

router = APIRouter(prefix="/api/v1/auth", tags=["Authentication"])

@router.post("/token", response_model=token_schemas.Token)
async def login_for_access_token(
    db: AsyncSession = Depends(get_async_db),
    form_data: OAuth2PasswordRequestForm = Depends()
):
    """
    OAuth2 compatible token login, get an access token for future requests.
    Username is the user's phone number.
    """
    user = await crud_user.get_user_by_phone(db, phone_number=form_data.username)
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect phone number or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(subject=user.id)
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register", response_model=user_schemas.User)
async def register_user(
    user_in: user_schemas.UserCreate,
    db: AsyncSession = Depends(get_async_db)
):
    """
    Create new user.
    """
    existing_user_phone = await crud_user.get_user_by_phone(db, phone_number=user_in.phone_number)
    if existing_user_phone:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this phone number already exists.",
        )
    if user_in.email: # Check email only if provided
        existing_user_email = await crud_user.get_user_by_email(db, email=user_in.email)
        if existing_user_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A user with this email address already exists.",
            )

    user = await crud_user.create_user(db=db, user_in=user_in)
    return user

@router.get("/users/me", response_model=user_schemas.User)
async def read_users_me(
    current_user: user_models.User = Depends(get_current_active_user) # Depends on our new dependency
):
    """
    Get current authenticated user.
    """
    return current_user

# Example of a protected route requiring authentication:
# @router.get("/users/me/items")
# async def read_own_items(
# current_user: user_models.User = Depends(get_current_active_user)
# ):
#     return [{"item_id": "Foo", "owner": current_user.phone_number}]
