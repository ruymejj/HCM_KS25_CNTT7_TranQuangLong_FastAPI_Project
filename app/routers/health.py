from fastapi import APIRouter

from app.core.responses import success_response


router = APIRouter(
    tags=["System"],
)


@router.get(
    "/health",
    summary="Kiểm tra trạng thái API",
)
def health_check():
    return success_response(
        message="API đang hoạt động bình thường.",
        data={
            "status": "healthy",
        },
    )