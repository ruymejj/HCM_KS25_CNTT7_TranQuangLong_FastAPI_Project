from enum import Enum

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum as SQLEnum,
    Integer,
    String,
    func,
)
from sqlalchemy.orm import relationship

from app.db.database import Base


class UserRole(str, Enum):
    USER = "USER"
    ADMIN = "ADMIN"


class User(Base):
    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    email = Column(
        String(255),
        unique=True,
        index=True,
        nullable=False,
    )

    password_hash = Column(
        String(255),
        nullable=False,
    )

    full_name = Column(
        String(255),
        nullable=False,
    )

    role = Column(
        SQLEnum(
            UserRole,
            name="user_role_enum",
        ),
        default=UserRole.USER,
        server_default=UserRole.USER.value,
        nullable=False,
    )

    is_active = Column(
        Boolean,
        default=True,
        server_default="1",
        nullable=False,
    )

    created_at = Column(
        DateTime,
        server_default=func.now(),
        nullable=False,
    )

    # Một User có thể sở hữu nhiều công trình.
    owned_sites = relationship(
        "ConstructionSite",
        back_populates="owner",
        foreign_keys="ConstructionSite.owner_id",
    )

    # Một User có thể tham gia nhiều công trình.
    memberships = relationship(
        "SiteMember",
        back_populates="user",
        passive_deletes=True,
    )

    # Một User có thể được giao nhiều hạng mục.
    assigned_work_items = relationship(
        "WorkItem",
        back_populates="assignee",
        foreign_keys="WorkItem.assignee_id",
    )