from typing import Literal

from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    field_validator,
)


class LoginRequest(BaseModel):
    email: EmailStr

    password: str = Field(
        min_length=1,
        max_length=72,
    )

    @field_validator("password")
    @classmethod
    def validate_password(cls, password: str) -> str:
        if len(password.encode("utf-8")) > 72:
            raise ValueError(
                "Mật khẩu không được vượt quá 72 byte."
            )

        return password


class TokenResponse(BaseModel):
    access_token: str
    token_type: Literal["bearer"] = "bearer"
    expires_in: int