from datetime import datetime, timedelta, timezone
from typing import Any

import bcrypt
import jwt

from app.core.config import settings


def hash_password(password: str) -> str:
    """
    Hash mật khẩu bằng bcrypt.
    Không lưu mật khẩu dạng plaintext vào database.
    """
    password_bytes = password.encode("utf-8")
    hashed_password = bcrypt.hashpw(
        password_bytes,
        bcrypt.gensalt(),
    )

    return hashed_password.decode("utf-8")


def verify_password(
    plain_password: str,
    password_hash: str,
) -> bool:
    """
    Kiểm tra mật khẩu người dùng nhập với mật khẩu đã hash.
    """
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        password_hash.encode("utf-8"),
    )


def create_access_token(
    subject: str | int,
    extra_claims: dict[str, Any] | None = None,
) -> str:
    """
    Tạo JWT access token.
    """
    current_time = datetime.now(timezone.utc)

    payload: dict[str, Any] = {
        "sub": str(subject),
        "iat": current_time,
        "exp": current_time
        + timedelta(minutes=settings.access_token_expire_minutes),
        "type": "access",
    }

    if extra_claims:
        payload.update(extra_claims)

    return jwt.encode(
        payload,
        settings.secret_key,
        algorithm=settings.algorithm,
    )


def decode_token(token: str) -> dict[str, Any]:
    """
    Giải mã và kiểm tra JWT.
    """
    return jwt.decode(
        token,
        settings.secret_key,
        algorithms=[settings.algorithm],
    )