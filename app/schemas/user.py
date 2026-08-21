from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    field_validator,
)

from app.models.user import UserRole


class UserBase(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
    )

    email: EmailStr

    full_name: str = Field(
        min_length=2,
        max_length=255,
    )


class UserCreate(UserBase):
    password: str = Field(
        min_length=8,
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


class UserUpdate(BaseModel):
    email: EmailStr | None = None

    full_name: str | None = Field(
        default=None,
        min_length=2,
        max_length=255,
    )

    is_active: bool | None = None


class UserResponse(UserBase):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int
    role: UserRole
    is_active: bool
    created_at: datetime