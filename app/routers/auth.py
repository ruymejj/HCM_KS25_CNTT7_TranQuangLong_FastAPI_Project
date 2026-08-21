from fastapi import (
    APIRouter,
    Depends,
    status,
)
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import create_access_token
from app.db.database import get_db
from app.schemas.auth import (
    LoginRequest,
    TokenResponse,
)
from app.schemas.user import (
    UserCreate,
    UserResponse,
)
from app.services.auth_service import (
    authenticate_user,
    register_user,
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Đăng ký tài khoản",
)
def register(
    user_data: UserCreate,
    db: Session = Depends(get_db),
):
    return register_user(
        db=db,
        user_data=user_data,
    )


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Đăng nhập và nhận JWT",
)
def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db),
):
    user = authenticate_user(
        db=db,
        email=str(login_data.email),
        password=login_data.password,
    )

    access_token = create_access_token(
        subject=user.id,
    )

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=(
            settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        ),
    )