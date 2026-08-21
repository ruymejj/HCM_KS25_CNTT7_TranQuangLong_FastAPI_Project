from datetime import datetime, timedelta, timezone

import bcrypt
import jwt

from app.core.config import settings


def hash_password(password: str) -> str:
    """
    Hash mật khẩu bằng bcrypt.
    """
    password_bytes = password.encode("utf-8")

    if len(password_bytes) > 72:
        raise ValueError(
            "Mật khẩu không được vượt quá 72 byte."
        )

    hashed_password = bcrypt.hashpw(
        password_bytes,
        bcrypt.gensalt(),
    )

    return hashed_password.decode("utf-8")


def verify_password(
    plain_password: str,
    password_hash: str,
) -> bool:
    try:
        if not plain_password:
            return False

        if not password_hash:
            return False

        password_bytes = plain_password.encode("utf-8")
        password_hash_bytes = password_hash.encode("utf-8")

        if len(password_bytes) > 72:
            return False

        return bcrypt.checkpw(
            password_bytes,
            password_hash_bytes,
        )

    except (
        ValueError,
        TypeError,
        AttributeError,
    ):
        return False


def create_access_token(
    subject: str | int,
) -> str:
    """
    Tạo JWT access token hợp lệ.
    """
    secret_key = settings.SECRET_KEY.strip()
    algorithm = settings.ALGORITHM
    expire_minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES

    if not secret_key:
        raise RuntimeError(
            "SECRET_KEY chưa được cấu hình."
        )

    allowed_algorithms = {
        "HS256",
        "HS384",
        "HS512",
    }

    if algorithm not in allowed_algorithms:
        raise RuntimeError(
            "ALGORITHM không được hỗ trợ."
        )

    if expire_minutes <= 0:
        raise RuntimeError(
            "ACCESS_TOKEN_EXPIRE_MINUTES phải lớn hơn 0."
        )

    current_time = datetime.now(timezone.utc)

    payload = {
        "sub": str(subject),
        "type": "access",
        "iat": current_time,
        "exp": current_time + timedelta(
            minutes=expire_minutes
        ),
    }

    return jwt.encode(
        payload,
        secret_key,
        algorithm=algorithm,
    )
def decode_access_token(token: str) -> dict:
    return jwt.decode(
        token,
        settings.SECRET_KEY,
        algorithms=[settings.ALGORITHM],
        options={
            "require": [
                "sub",
                "type",
                "iat",
                "exp",
            ],
        },
    )