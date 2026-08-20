from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)

from app.models.work_item import (
    WorkItemPriority,
    WorkItemStatus,
)


class WorkItemBase(BaseModel):
    title: str = Field(
        min_length=2,
        max_length=255,
    )

    description: str | None = Field(
        default=None,
        max_length=5000,
    )

    assignee_id: int | None = Field(
        default=None,
        gt=0,
    )

    status: WorkItemStatus = WorkItemStatus.TODO

    priority: WorkItemPriority = WorkItemPriority.MEDIUM

    due_date: datetime | None = None


class WorkItemCreate(WorkItemBase):
    pass


class WorkItemUpdate(BaseModel):
    title: str | None = Field(
        default=None,
        min_length=2,
        max_length=255,
    )

    description: str | None = Field(
        default=None,
        max_length=5000,
    )

    assignee_id: int | None = Field(
        default=None,
        gt=0,
    )

    status: WorkItemStatus | None = None

    priority: WorkItemPriority | None = None

    due_date: datetime | None = None


class WorkItemResponse(WorkItemBase):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int
    site_id: int
    created_at: datetime