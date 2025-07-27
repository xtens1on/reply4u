from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import async_sessionmaker

from core.config import DB

# using alias to prevent import problems
from .engine import get_engine, get_sessionmaker as get_base_sessionmaker


def get_sessionmaker() -> async_sessionmaker:
    url = URL.create(
        drivername=DB['DRIVER'],
        username=DB['USERNAME'],
        password=DB['PASSWORD'],
        host=DB['HOST'],
        port=DB['PORT'],
        database=DB['NAME'],
    )
    engine = get_engine(url)
    return get_base_sessionmaker(engine)
