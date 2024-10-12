from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr

from config.services import convert_camelcase_to_snakecase


class Base(DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return convert_camelcase_to_snakecase(cls.__name__)

    id: Mapped[int] = mapped_column(primary_key=True)