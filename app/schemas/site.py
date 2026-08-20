from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)

from app.models.site import SiteMemberRole


class ConstructionSiteBase(BaseModel):
    name: str = Field(
        min_length=2,
        max_length=255,
    )

    description: str | None = Field(
        default=None,
        max_length=5000,
    )


class ConstructionSiteCreate(ConstructionSiteBase):
    pass


class ConstructionSiteUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=2,
        max_length=255,
    )

    description: str | None = Field(
        default=None,
        max_length=5000,
    )


class ConstructionSiteResponse(ConstructionSiteBase):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int
    owner_id: int
    created_at: datetime



class SiteMemberBase(BaseModel):
    user_id: int = Field(gt=0)

    role: SiteMemberRole = SiteMemberRole.MEMBER


class SiteMemberCreate(SiteMemberBase):
    pass


class SiteMemberUpdate(BaseModel):
    role: SiteMemberRole | None = None


class SiteMemberResponse(SiteMemberBase):
    model_config = ConfigDict(
        from_attributes=True,
    )

    site_id: int
    joined_at: datetime