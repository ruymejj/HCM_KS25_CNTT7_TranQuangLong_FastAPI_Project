from fastapi import (
    APIRouter,
    Depends,
)

from app.dependencies.permissions import require_admin
from app.models.user import User


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get(
    "/admin-check",
    summary="Kiểm tra quyền Admin",
)
def admin_check(
    current_admin: User = Depends(
        require_admin
    ),
):
    return {
        "message": "Bạn có quyền ADMIN.",
        "user": {
            "id": current_admin.id,
            "email": current_admin.email,
            "full_name": current_admin.full_name,
            "role": current_admin.role,
        },
    }