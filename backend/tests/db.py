import pytest

from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from core.models.base import Base
from core.db.engine import get_engine

from core.config import DB


TEST_DB_NAME = DB['NAME'] + '_test'
TEST_DB_URL = URL.create(
    drivername=DB['DRIVER'],
    username=DB['USERNAME'],
    password=DB['PASSWORD'],
    host=DB['HOST'],
    port=DB['PORT'],
    database=TEST_DB_NAME,
)


@pytest.fixture(scope='module')
async def async_engine():
    engine = get_engine(TEST_DB_URL)

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope='module')
async def sessionmaker(async_engine):
    return async_sessionmaker(
        expire_on_commit=False,
        autoflush=False,
        bind=async_engine,
        class_=AsyncSession,
    )
