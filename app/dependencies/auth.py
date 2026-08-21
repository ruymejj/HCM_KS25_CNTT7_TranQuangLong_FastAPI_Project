import jwt

from fastapi import Depends
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)
from sqlalchemy.orm import Session

from app.core.exceptions import (
    ForbiddenError,
    UnauthorizedError,
)
from app.core.security import decode_access_token
from app.db.database import get_db
from app.models.user import User


bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(
        bearer_scheme
    ),
    db: Session = Depends(get_db),
) -> User:
    if credentials is None:
        raise UnauthorizedError(
            message="Bạn chưa cung cấp access token.",
        )

    if credentials.scheme.lower() != "bearer":
        raise UnauthorizedError(
            message="Phương thức xác thực không hợp lệ.",
        )

    token = credentials.credentials

    try:
        payload = decode_access_token(token)

    except jwt.ExpiredSignatureError as error:
        raise UnauthorizedError(
            message="Access token đã hết hạn.",
        ) from error

    except jwt.InvalidTokenError as error:
        raise UnauthorizedError(
            message="Access token không hợp lệ.",
        ) from error

    if payload.get("type") != "access":
        raise UnauthorizedError(
            message="Access token không hợp lệ.",
        )

    user_id = payload.get("sub")

    if user_id is None:
        raise UnauthorizedError(
            message="Access token không hợp lệ.",
        )

    try:
        user_id = int(user_id)
    except (TypeError, ValueError) as error:
        raise UnauthorizedError(
            message="Access token không hợp lệ.",
        ) from error

    user = db.get(User, user_id)

    if user is None:
        raise UnauthorizedError(
            message="Không thể xác thực người dùng.",
        )

    if not user.is_active:
        raise ForbiddenError(
            message="Tài khoản đã bị khóa hoặc không hoạt động.",
        )

    return user