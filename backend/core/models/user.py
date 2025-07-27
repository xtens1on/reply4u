import sqlalchemy as sa

from .base import BaseModel


class User(BaseModel):
    __tablename__ = 'users'

    telegram_id = sa.Column(sa.BigInteger(), unique=True, nullable=False)
    description = sa.Column(sa.VARCHAR(4096))
    chat_history = sa.Column(sa.Text)
    active = sa.Column(sa.Boolean, default=False, nullable=False)
