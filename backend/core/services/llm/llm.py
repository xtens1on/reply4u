from datetime import datetime

from core.schemas.user import UserSchema
from core.schemas.message import MessageSchema

from core.services.settings import SettingsService
from core.services.user import UserService
from core.services.llm.api.base import LLMApi as BaseLLMApi

from core.config import LLM_PROVIDER


if LLM_PROVIDER == 'ollama':
    from core.services.llm.api import OllamaAPI as LLMApi
elif LLM_PROVIDER == 'openai':
    from core.services.llm.api import OpenAIAPI as LLMApi


class LLMService:
    user_service = UserService
    llm_api = LLMApi

    @classmethod
    def set_llm_api(cls, api_class: type[BaseLLMApi]):
        cls.llm_api = api_class

    @classmethod
    async def generate_response(cls, user: UserSchema, messages: list[MessageSchema]) -> str:
        user.update_context(messages)
        context = await cls.user_service.get_context(user)
        settings = await SettingsService.get_settings()
        response = await cls.llm_api.get_completion(model=settings.model, messages=context)
        user.update_context([
            MessageSchema(
                content=response,
                role='assistant',
                date=datetime.now(),
            ),
        ])
        await cls.user_service.save(user)
        return response

    @classmethod
    async def models_list(cls, query: str = '', limit: int = 10):
        models = await cls.llm_api.models_list(query=query, limit=limit)
        return models
