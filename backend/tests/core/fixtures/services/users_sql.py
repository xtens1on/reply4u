import pytest

from core.services.user.sql import UserServiceSQL

from tests.db import sessionmaker, async_engine  # noqa: F401


@pytest.fixture(scope='module')
async def user_service_sql(sessionmaker):  # noqa: F811
    source_sessionmaker = UserServiceSQL.Session
    UserServiceSQL.Session = sessionmaker
    yield UserServiceSQL
    UserServiceSQL.Session = source_sessionmaker
