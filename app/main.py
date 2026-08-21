from fastapi import (
    Depends,
    FastAPI,
    status,
)
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.exceptions import (
    AppException,
    register_exception_handlers,
)
from app.core.responses import success_response
from app.db.database import (
    Base,
    engine,
    get_db,
)

# Import các model để SQLAlchemy nhận diện bảng.
from app.models import (
    ConstructionSite,
    SiteMember,
    User,
    WorkItem,
)

from app.routers.auth import router as auth_router
from app.routers.users import router as users_router


# Tạo bảng nếu chưa tồn tại.
Base.metadata.create_all(bind=engine)


# Phải tạo đối tượng FastAPI trước khi include router.
app = FastAPI(
    title=settings.APP_NAME,
    description="API quản lý công trình xây dựng",
    version="1.0.0",
)


# Đăng ký exception handler.
register_exception_handlers(app)


# Include router sau khi đã có app = FastAPI().
app.include_router(auth_router)
app.include_router(users_router)


@app.get(
    "/",
    tags=["System"],
    summary="Trang chủ API",
)
def home():
    return success_response(
        message="Construction Site Management API",
        data={
            "version": "1.0.0",
        },
    )


@app.get(
    "/health",
    tags=["System"],
    summary="Kiểm tra trạng thái FastAPI",
)
def health_check():
    return success_response(
        message="FastAPI đang hoạt động.",
        data={
            "status": "healthy",
        },
    )


@app.get(
    "/health/database",
    tags=["System"],
    summary="Kiểm tra kết nối MySQL",
)
def database_health_check(
    db: Session = Depends(get_db),
):
    try:
        db.execute(text("SELECT 1"))

        return success_response(
            message="Kết nối MySQL thành công.",
            data={
                "status": "healthy",
                "database": "connected",
            },
        )

    except SQLAlchemyError as error:
        raise AppException(
            status_code=(
                status.HTTP_503_SERVICE_UNAVAILABLE
            ),
            code="DATABASE_UNAVAILABLE",
            message="Không thể kết nối đến MySQL.",
        ) from error