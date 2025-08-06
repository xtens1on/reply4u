from datetime import datetime

import pytest

from core.schemas.message import MessageSchema
from core.schemas.user import CreateUserSchema
from core.services.llm.llm import LLMService
from core.services.llm.api.base import LLMApi

from tests.core.fixtures.services import user_service

try:
    from tests.db import sessionmaker, async_engine
except ModuleNotFoundError:
    pass

MOCK_RESPONSE_CONTENT = 'hello, world!'
MOCK_MODELS_LIST = ['model1', 'model2']


class MockLLMApi(LLMApi):

    @classmethod
    async def get_completion(cls, model: str = '', messages: list[dict[str, str]] = None):
        return MOCK_RESPONSE_CONTENT

    @classmethod
    async def models_list(cls, query: str = '', limit: int = 10) -> list[str]:
        return MOCK_MODELS_LIST


@pytest.fixture(scope='module')
async def llm_service(user_service):
    LLMService.user_service = user_service
    LLMService.set_llm_api(MockLLMApi)
    return LLMService


@pytest.mark.anyio
async def test_generate_response(user_service, llm_service):
    telegram_id = 15
    payload = CreateUserSchema(telegram_id=telegram_id, active=True)
    user = await user_service.create_user(payload)
    messages = [
        MessageSchema(
            content='hello',
            role='user',
            date=datetime.now(),
        ),
        MessageSchema(
            content='world',
            role='user',
            date=datetime.now(),
        ),
    ]

    response = await llm_service.generate_response(user, messages)
    assert response == MOCK_RESPONSE_CONTENT


@pytest.mark.anyio
async def test_models_list(llm_service):
    models_list = await llm_service.models_list()
    assert models_list == MOCK_MODELS_LIST
