from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.exceptions import (
    BadRequestError,
    ForbiddenError,
    UnauthorizedError,
)
from app.core.security import (
    hash_password,
    verify_password,
)
from app.models.user import User
from app.schemas.user import UserCreate


def register_user(
    db: Session,
    user_data: UserCreate,
) -> User:
    normalized_email = str(
        user_data.email
    ).strip().lower()

    existing_user = (
        db.query(User)
        .filter(User.email == normalized_email)
        .first()
    )

    if existing_user is not None:
        raise BadRequestError(
            "Email đã được sử dụng."
        )

    new_user = User(
        email=normalized_email,
        full_name=user_data.full_name,
        password_hash=hash_password(
            user_data.password
        ),
    )

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

    except IntegrityError as error:
        db.rollback()

        raise BadRequestError(
            "Email đã được sử dụng."
        ) from error

    return new_user


def authenticate_user(
    db: Session,
    email: str,
    password: str,
) -> User:
    """
    Xác thực email và mật khẩu.
    """
    normalized_email = email.strip().lower()

    user = (
        db.query(User)
        .filter(User.email == normalized_email)
        .first()
    )

    # Không thông báo riêng email có tồn tại hay không.
    if user is None:
        raise UnauthorizedError()

    if not verify_password(
        password,
        user.password_hash,
    ):
        raise UnauthorizedError()

    if not user.is_active:
        raise ForbiddenError(
            "Tài khoản đã bị khóa hoặc không hoạt động."
        )

    return user