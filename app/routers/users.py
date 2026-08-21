from typing import Literal

from fastapi import (
    APIRouter,
    Depends,
    Query,
)
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.dependencies.auth import get_current_user
from app.dependencies.permissions import require_admin
from app.models.user import User
from app.schemas.user import UserResponse
from app.services.user_service import get_users


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Xem thông tin người dùng hiện tại",
)
def get_my_profile(
    current_user: User = Depends(
        get_current_user
    ),
):
    return current_user


@router.get(
    "",
    response_model=list[UserResponse],
    summary="Danh sách người dùng",
    description=(
        "Chỉ ADMIN được truy cập. "
        "Hỗ trợ tìm kiếm theo họ tên/email "
        "và lọc trạng thái tài khoản."
    ),
)
def list_users(
    search: str | None = Query(
        default=None,
        min_length=1,
        max_length=255,
        description="Tìm kiếm theo họ tên hoặc email",
    ),
    status: Literal[
        "active",
        "inactive",
    ] | None = Query(
        default=None,
        description="Lọc trạng thái tài khoản",
    ),
    db: Session = Depends(get_db),
    current_admin: User = Depends(
        require_admin
    ),
):
    return get_users(
        db=db,
        search=search,
        status=status,
    )