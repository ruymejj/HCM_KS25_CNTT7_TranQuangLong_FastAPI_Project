from typing import Literal

from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from app.models.user import User


UserStatus = Literal[
    "active",
    "inactive",
]


def get_users(
    db: Session,
    search: str | None = None,
    status: UserStatus | None = None,
) -> list[User]:
    """
    Lấy danh sách người dùng.

    Hỗ trợ:
    - Tìm kiếm theo full_name hoặc email.
    - Lọc tài khoản active/inactive.
    """

    query = db.query(User)

    if search:
        normalized_search = search.strip().lower()

        if normalized_search:
            search_pattern = (
                f"%{normalized_search}%"
            )

            query = query.filter(
                or_(
                    func.lower(
                        User.full_name
                    ).like(search_pattern),
                    func.lower(
                        User.email
                    ).like(search_pattern),
                )
            )

    if status == "active":
        query = query.filter(
            User.is_active.is_(True)
        )

    elif status == "inactive":
        query = query.filter(
            User.is_active.is_(False)
        )

    return (
        query
        .order_by(User.created_at.desc())
        .all()
    )