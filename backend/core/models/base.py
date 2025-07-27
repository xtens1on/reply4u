import sqlalchemy as sa

from sqlalchemy.orm import declarative_base
from sqlalchemy.sql.functions import now

Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True

    id = sa.Column(sa.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    created_at = sa.Column(sa.TIMESTAMP, nullable=False, server_default=now(), default=now())
    updated_at = sa.Column(sa.TIMESTAMP, onupdate=now(), default=now())

    def __repr__(self):
        return f'<{self.__class__.__name__}: {self.id}>'
