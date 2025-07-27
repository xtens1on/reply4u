from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncEngine,
    AsyncSession,
)


def get_engine(url: URL | str, echo: bool = True):
    return create_async_engine(url, echo=echo, pool_pre_ping=True)


def get_sessionmaker(engine: AsyncEngine):
    return async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
