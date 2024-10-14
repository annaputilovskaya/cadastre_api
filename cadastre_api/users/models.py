from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column

from config.base import Base


class User(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[Optional[str]]
    is_admin: Mapped[Optional[bool]] = mapped_column(default=False)
    hashed_password: Mapped[str]
