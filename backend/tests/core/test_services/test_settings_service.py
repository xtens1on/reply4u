import json
import pytest

from anyio import open_file

from core.config import SETTINGS_PATH

from core.schemas.settings import UpdateAppSettingsSchema

from tests.core.fixtures.services.settings import settings_service


TEST_SETTINGS_STORE_PATH = SETTINGS_PATH.parent / 'settings_test.json'


@pytest.mark.anyio
async def test_get_settings(settings_service):
    settings = await settings_service.get_settings()
    async with await open_file(TEST_SETTINGS_STORE_PATH) as file:
        content = await file.read()
        settings_store = json.loads(content)

    for field, value in settings_store.items():
        assert getattr(settings, field) == value


@pytest.mark.anyio
async def test_update_settings(settings_service):
    payload = UpdateAppSettingsSchema(
        model='qwen3:32b',
        users_active_by_default=True,
        system_message_template='test',
        message_template='some_content',
    )
    await settings_service.update(payload)

    settings = await settings_service.get_settings()
    payload_dict = payload.model_dump()
    for field, value in payload_dict.items():
        assert getattr(settings, field) == value
