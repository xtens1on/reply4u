from datetime import datetime, timezone

import pytest

try:
    from sqlalchemy import select
except ModuleNotFoundError:
    print('skipping...')
    pytest.skip(allow_module_level=True)

from core.schemas.user import CreateUserSchema, PatchUserSchema
from core.schemas.message import MessageSchema
from core.models import User

from core.services.settings import SettingsService

from tests.core.fixtures.services.users_sql import user_service_sql as user_service
from tests.db import sessionmaker, async_engine


@pytest.mark.anyio
async def test_create_user(user_service, sessionmaker):
    telegram_id = 1
    payload = CreateUserSchema(telegram_id=telegram_id)
    await user_service.create_user(payload)

    query = select(User).where(User.telegram_id == telegram_id)
    async with sessionmaker.begin() as session:
        user = await session.scalar(query)
        assert user
        assert user.telegram_id == 1

        settings = await SettingsService.get_settings()
        assert user.active == settings.users_active_by_default


@pytest.mark.anyio
async def test_get_user(user_service):
    telegram_id = 1

    user = await user_service.get_user(telegram_id=telegram_id)
    assert user
    assert user.telegram_id == telegram_id


@pytest.mark.anyio
async def test_get_or_create_get_user(user_service):
    telegram_id = 1

    user = await user_service.get_or_create_user(telegram_id=telegram_id)
    assert user
    assert user.telegram_id == telegram_id


@pytest.mark.anyio
async def test_get_or_create_create_user(user_service, sessionmaker):
    telegram_id = 2
    user = await user_service.get_or_create_user(telegram_id=telegram_id)
    assert user
    assert user.telegram_id == telegram_id

    query = select(User).where(User.telegram_id == telegram_id)
    async with sessionmaker.begin() as session:
        user_db = await session.scalar(query)
        assert user_db
        assert user_db.telegram_id == user.telegram_id


@pytest.mark.anyio
async def test_list_users(user_service):
    users = await user_service.list_users()
    assert len(users) == 2

    user_ids = [user.telegram_id for user in users]
    assert 1 in user_ids
    assert 2 in user_ids


@pytest.mark.anyio
async def test_list_users_limit(user_service):
    users = await user_service.list_users(limit=1)
    assert len(users) == 1


@pytest.mark.anyio
async def test_save_user(user_service, sessionmaker):
    telegram_id = 1
    description = 'test_save_user'

    user = await user_service.get_user(telegram_id)
    user.description = description
    await user_service.save(user)

    query = select(User).where(User.telegram_id == telegram_id)
    async with sessionmaker.begin() as session:
        user_db = await session.scalar(query)
        assert user_db.description == description


@pytest.mark.anyio
async def test_list_users_only_active(user_service):
    telegram_id = 1
    user = await user_service.get_user(telegram_id=telegram_id)
    user.active = True
    await user_service.save(user)
    users = await user_service.list_users(only_active=True)
    assert len(users) == 1
    assert users[0].telegram_id == user.telegram_id


@pytest.mark.anyio
async def test_update_or_create_update_user(user_service, sessionmaker):

    telegram_id = 2
    payload = PatchUserSchema(active=True, description='test_update_or_create_update_user')

    user = await user_service.update_or_create_user(telegram_id, payload)

    assert user.active == payload.active
    assert user.description == payload.description

    query = select(User).where(User.telegram_id == telegram_id)
    async with sessionmaker.begin() as session:
        user_db = await session.scalar(query)
        assert user.active == user_db.active
        assert user.description == user_db.description


@pytest.mark.anyio
async def test_update_or_create_user_create_user(user_service, sessionmaker):
    telegram_id = 3
    payload = PatchUserSchema(active=True, description='test_update_or_create_user_create_user')

    user = await user_service.update_or_create_user(telegram_id, payload)

    assert user.active == payload.active
    assert user.description == payload.description

    query = select(User).where(User.telegram_id == telegram_id)
    async with sessionmaker.begin() as session:
        user_db = await session.scalar(query)
        assert user.active == user_db.active
        assert user.description == user_db.description


@pytest.mark.anyio
async def test_get_user_chat_history(user_service):
    telegram_id = 1
    message = MessageSchema(
        content='hello',
        role='user',
        date=datetime.now(tz=timezone.utc),
    )
    chat_history_payload = [message]

    user = await user_service.get_user(telegram_id=telegram_id)
    user.chat_history = chat_history_payload
    await user_service.save(user)

    settings = await SettingsService.get_settings()
    chat_history_response = [
        await user_service.format_history_message(message),
        {
            'role': 'system',
            'content': settings.system_message_template.format(**user.shortcuts),
        },
    ]
    user = await user_service.get_user(telegram_id)

    assert await user_service.get_context(user) == chat_history_response


@pytest.mark.anyio
async def test_clear_chat_history(user_service, sessionmaker):
    telegram_id = 4
    chat_history = [
        MessageSchema(
            content='hello',
            role='user',
            date=datetime.now(),
        )
    ]
    payload = CreateUserSchema(telegram_id=telegram_id)
    user = await user_service.create_user(payload)
    user.chat_history = chat_history
    await user_service.save(user)

    await user_service.clear_user_chat_history(telegram_id=telegram_id)

    query = select(User).where(User.telegram_id == telegram_id)
    async with sessionmaker.begin() as session:
        user_db = await session.scalar(query)
        assert not user_db.chat_history
