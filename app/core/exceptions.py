from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException

from app.core.responses import error_response


class AppException(Exception):
    """
    Exception chung của ứng dụng.
    """

    def __init__(
        self,
        status_code: int,
        code: str,
        message: str,
    ):
        self.status_code = status_code
        self.code = code
        self.message = message

        super().__init__(message)


class BadRequestError(AppException):
    """
    Lỗi 400: dữ liệu hoặc yêu cầu không hợp lệ.
    """

    def __init__(
        self,
        message: str = "Yêu cầu không hợp lệ.",
    ):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            code="BAD_REQUEST",
            message=message,
        )


class ForbiddenError(AppException):
    """
    Lỗi 403: người dùng không có quyền.
    """

    def __init__(
        self,
        message: str = "Bạn không có quyền thực hiện thao tác này.",
    ):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            code="FORBIDDEN",
            message=message,
        )


class NotFoundError(AppException):
    """
    Lỗi 404: không tìm thấy dữ liệu.
    """

    def __init__(
        self,
        resource: str = "dữ liệu",
    ):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            code="NOT_FOUND",
            message=f"Không tìm thấy {resource}.",
        )


async def app_exception_handler(
    request: Request,
    exc: AppException,
) -> JSONResponse:
    """
    Xử lý các AppException do chương trình chủ động raise.
    """
    return error_response(
        status_code=exc.status_code,
        code=exc.code,
        message=exc.message,
    )


async def http_exception_handler(
    request: Request,
    exc: HTTPException,
) -> JSONResponse:
    """
    Xử lý các HTTPException mặc định của FastAPI,
    bao gồm lỗi 404 khi endpoint không tồn tại.
    """
    error_codes = {
        400: "BAD_REQUEST",
        403: "FORBIDDEN",
        404: "NOT_FOUND",
    }

    code = error_codes.get(
        exc.status_code,
        f"HTTP_{exc.status_code}",
    )

    return error_response(
        status_code=exc.status_code,
        code=code,
        message=str(exc.detail),
    )


def register_exception_handlers(app: FastAPI) -> None:
    """
    Đăng ký exception handler vào ứng dụng FastAPI.
    """
    app.add_exception_handler(
        AppException,
        app_exception_handler,
    )

    app.add_exception_handler(
        HTTPException,
        http_exception_handler,
    )