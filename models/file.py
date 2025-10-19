from database.session import Base
from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from datetime import datetime

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User


class File(Base):
    __tablename__ = "files"

    id: Mapped[int] = mapped_column(primary_key=True)
    filename: Mapped[str] = mapped_column(nullable=False)
    path: Mapped[str] = mapped_column(nullable=False)
    uploadet_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        # ondelete="CASCADE",
    )

    owner: Mapped["User"] = relationship(
        "User",
        back_populates="files",
    )
