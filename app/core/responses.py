from typing import Any

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse


def success_response(
    message: str,
    data: Any = None,
    status_code: int = 200,
) -> JSONResponse:
    """
    Format response thành công thống nhất.
    """
    content = {
        "success": True,
        "message": message,
        "data": data,
    }

    return JSONResponse(
        status_code=status_code,
        content=jsonable_encoder(content),
    )


def error_response(
    status_code: int,
    code: str,
    message: str,
) -> JSONResponse:
    """
    Format response lỗi thống nhất.
    """
    content = {
        "success": False,
        "error": {
            "code": code,
            "message": message,
        },
    }

    return JSONResponse(
        status_code=status_code,
        content=jsonable_encoder(content),
    )