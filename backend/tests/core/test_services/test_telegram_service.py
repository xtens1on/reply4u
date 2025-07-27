import pytest

from core.schemas.user import CreateUserSchema, TelegramUserSchema

from tests.core.fixtures.services import user_service
from tests.core.fixtures.services.telegram import telegram_service

try:
    from tests.db import sessionmaker, async_engine
except ModuleNotFoundError:
    pass


@pytest.mark.anyio
async def test_users_list(telegram_service):
    users = await telegram_service.list_users()

    for user in users:
        assert isinstance(user, TelegramUserSchema)


@pytest.mark.anyio
async def test_users_list_with_limit(telegram_service):
    limit = 10
    users = await telegram_service.list_users(limit=limit)

    assert len(users) <= 10  # user may have less than 10 dialogs in telegram


@pytest.mark.anyio
async def test_users_list_only_active(user_service, telegram_service):
    telegram_id = 777000  # telegram service notifications id, every account has chat with it
    payload = CreateUserSchema(telegram_id=telegram_id, active=True)
    active_user = await user_service.create_user(payload)

    users = await telegram_service.list_users(only_active=True)
    user_ids = [user.telegram_id for user in users]
    assert active_user.telegram_id in user_ids
    for user in users:
        assert user.active


@pytest.mark.anyio
async def test_users_list_with_query(telegram_service):
    telegram_id = 777000
    query_id = '77700'
    query_name = 'telegr'

    users_query_id = await telegram_service.list_users(query=query_id)
    assert telegram_id in [user.telegram_id for user in users_query_id]

    users_query_name = await telegram_service.list_users(query=query_name)
    assert telegram_id in [user.telegram_id for user in users_query_name]


@pytest.mark.anyio
async def test_get_my_account(telegram_service):
    account = await telegram_service.get_my_account()
    assert isinstance(account, TelegramUserSchema)
