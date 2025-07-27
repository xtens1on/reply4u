import pytest

from core.services.user.json import UserServiceJSON
from core.config import JSON_USER_STORE_PATH

TEST_USER_STORE_PATH = JSON_USER_STORE_PATH.parent / 'users_test.json'


@pytest.fixture(scope='module')
async def user_service_json():
    UserServiceJSON.STORE_PATH = TEST_USER_STORE_PATH
    yield UserServiceJSON
    UserServiceJSON.STORE_PATH = JSON_USER_STORE_PATH
    TEST_USER_STORE_PATH.unlink()
