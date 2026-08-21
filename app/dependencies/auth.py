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


# auto_error=False để tự xử lý token thiếu thành lỗi 401.
bearer_scheme = HTTPBearer(
    auto_error=False,
)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(
        bearer_scheme
    ),
    db: Session = Depends(get_db),
) -> User:
    """
    Đọc Bearer token, giải mã JWT và lấy User từ database.
    """

    # Không gửi Authorization header.
    if credentials is None:
        raise UnauthorizedError(
            "Thiếu access token."
        )

    # Header không sử dụng Bearer scheme.
    if credentials.scheme.lower() != "bearer":
        raise UnauthorizedError(
            "Authorization scheme phải là Bearer."
        )

    token = credentials.credentials

    try:
        payload = decode_access_token(token)

    except jwt.ExpiredSignatureError as error:
        raise UnauthorizedError(
            "Access token đã hết hạn."
        ) from error

    except jwt.InvalidTokenError as error:
        raise UnauthorizedError(
            "Access token không hợp lệ."
        ) from error

    # Không chấp nhận refresh token hoặc token loại khác.
    if payload.get("type") != "access":
        raise UnauthorizedError(
            "Token không phải access token."
        )

    subject = payload.get("sub")

    if subject is None:
        raise UnauthorizedError(
            "Access token không hợp lệ."
        )

    try:
        user_id = int(subject)

    except (TypeError, ValueError) as error:
        raise UnauthorizedError(
            "Access token không hợp lệ."
        ) from error

    user = db.get(
        User,
        user_id,
    )

    # User có thể đã bị xóa sau khi token được tạo.
    if user is None:
        raise UnauthorizedError(
            "Không thể xác thực thông tin đăng nhập."
        )

    # Chặn tài khoản đã bị khóa.
    if not user.is_active:
        raise ForbiddenError(
            "Tài khoản đã bị khóa hoặc không hoạt động."
        )

    return user