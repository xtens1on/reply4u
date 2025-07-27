import pytest

from core.services.telegram import TelegramService
from core.client import get_pyrogram_client

from . import user_service  # noqa: F401


@pytest.fixture(scope='module')
async def telegram_service(user_service):  # noqa: F811
    client = get_pyrogram_client()
    await client.start()
    TelegramService.set_client(client)
    TelegramService.user_service = user_service
    yield TelegramService
    TelegramService.client = None
