from config.base import Base
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column


class Query(Base):
    """
    Модель запроса для отображения в базе данных.
    """
    id: Mapped[int] = mapped_column(primary_key=True)
    cadastre_number: Mapped[str]
    latitude: Mapped[str]
    longitude: Mapped[str]
    result: Mapped[Optional[bool]]
