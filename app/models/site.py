from enum import Enum

from sqlalchemy import (
    Column,
    DateTime,
    Enum as SQLEnum,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.orm import relationship

from app.db.database import Base


class SiteMemberRole(str, Enum):
    OWNER = "OWNER"
    MEMBER = "MEMBER"


class ConstructionSite(Base):
    __tablename__ = "construction_sites"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    name = Column(
        String(255),
        nullable=False,
    )

    description = Column(
        Text,
        nullable=True,
    )

    owner_id = Column(
        Integer,
        ForeignKey(
            "users.id",
            ondelete="RESTRICT",
        ),
        nullable=False,
        index=True,
    )

    created_at = Column(
        DateTime,
        server_default=func.now(),
        nullable=False,
    )

    # Người sở hữu công trình.
    owner = relationship(
        "User",
        back_populates="owned_sites",
        foreign_keys=[owner_id],
    )

    # Danh sách thành viên của công trình.
    members = relationship(
        "SiteMember",
        back_populates="site",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    # Danh sách hạng mục của công trình.
    work_items = relationship(
        "WorkItem",
        back_populates="site",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class SiteMember(Base):
    __tablename__ = "site_members"

    # site_id và user_id tạo thành khóa chính kết hợp.
    site_id = Column(
        Integer,
        ForeignKey(
            "construction_sites.id",
            ondelete="CASCADE",
        ),
        primary_key=True,
    )

    user_id = Column(
        Integer,
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        primary_key=True,
    )

    role = Column(
        SQLEnum(
            SiteMemberRole,
            name="site_member_role_enum",
        ),
        nullable=False,
    )

    joined_at = Column(
        DateTime,
        server_default=func.now(),
        nullable=False,
    )

    site = relationship(
        "ConstructionSite",
        back_populates="members",
    )

    user = relationship(
        "User",
        back_populates="memberships",
    )