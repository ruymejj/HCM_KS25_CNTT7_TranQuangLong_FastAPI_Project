from fastapi import Depends

from app.core.exceptions import ForbiddenError
from app.dependencies.auth import get_current_user
from app.models.user import User, UserRole


def require_roles(
    *allowed_roles: UserRole,
):
    """
    Tạo dependency kiểm tra role.
    """

    allowed_role_values = {
        role.value
        for role in allowed_roles
    }

    def role_checker(
        current_user: User = Depends(
            get_current_user
        ),
    ) -> User:
        if isinstance(
            current_user.role,
            UserRole,
        ):
            current_role = current_user.role.value
        else:
            current_role = str(current_user.role)

        if current_role not in allowed_role_values:
            raise ForbiddenError(
                "Bạn không có quyền thực hiện thao tác này."
            )

        return current_user

    return role_checker


# Dependency dành riêng cho ADMIN.
require_admin = require_roles(
    UserRole.ADMIN
)


# Dependency cho cả USER và ADMIN.
require_user_or_admin = require_roles(
    UserRole.USER,
    UserRole.ADMIN,
)