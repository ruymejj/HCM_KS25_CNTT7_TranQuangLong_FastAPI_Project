from typing import Any

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.responses import error_response


class AppException(Exception):
    def __init__(
        self,
        status_code: int,
        code: str,
        message: str,
        details: Any = None,
    ):
        self.status_code = status_code
        self.code = code
        self.message = message
        self.details = details

        super().__init__(message)


class BadRequestError(AppException):
    def __init__(
        self,
        message: str = "Dữ liệu không hợp lệ.",
        details: Any = None,
    ):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            code="BAD_REQUEST",
            message=message,
            details=details,
        )


class ForbiddenError(AppException):
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
):
    return error_response(
        status_code=exc.status_code,
        code=exc.code,
        message=exc.message,
        details=exc.details,
    )


async def http_exception_handler(
    request: Request,
    exc: StarletteHTTPException,
):
    return error_response(
        status_code=exc.status_code,
        code=f"HTTP_{exc.status_code}",
        message=str(exc.detail),
    )


async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
):
    return error_response(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        code="VALIDATION_ERROR",
        message="Dữ liệu gửi lên không hợp lệ.",
        details=exc.errors(),
    )


def register_exception_handlers(app: FastAPI):
    app.add_exception_handler(
        AppException,
        app_exception_handler,
    )

    app.add_exception_handler(
        StarletteHTTPException,
        http_exception_handler,
    )

    app.add_exception_handler(
        RequestValidationError,
        validation_exception_handler,
    )