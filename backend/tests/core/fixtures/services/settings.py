import pytest

from core.services.settings import SettingsService
from core.config import SETTINGS_PATH

TEST_SETTINGS_STORE_PATH = SETTINGS_PATH.parent / 'settings_test.json'


@pytest.fixture(scope='module')
async def settings_service():
    SettingsService.STORE_PATH = TEST_SETTINGS_STORE_PATH
    yield SettingsService
    SettingsService.STORE_PATH = SETTINGS_PATH
    TEST_SETTINGS_STORE_PATH.unlink()
