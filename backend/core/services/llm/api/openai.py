from openai import AsyncClient

from core.config import OPENAI_BASE_URL, OPENAI_API_KEY

from .base import LLMApi


class OpenAIAPI(LLMApi):

    @classmethod
    async def get_completion(cls, model: str, messages: list[dict[str, str]]):
        client = AsyncClient(
            base_url=OPENAI_BASE_URL,
            api_key=OPENAI_API_KEY,
        )
        completion = await client.chat.completions.create(
            model=model,
            messages=messages,
        )
        return completion.choices[0].message.content

    @classmethod
    async def models_list(cls, query: str = '', limit: int = 10) -> list[str]:
        client = AsyncClient(
            base_url=OPENAI_BASE_URL,
            api_key=OPENAI_API_KEY,
        )
        models_iterator = client.models.list()
        filtered_models = []
        async for model in models_iterator:
            matches_query = await cls._model_matches_query(model.id, query)
            if query and not matches_query:
                continue
            filtered_models.append(model.id)
            if len(filtered_models) == limit:
                break
        return filtered_models

    @classmethod
    async def _model_matches_query(cls, model_name: str, query: str):
        return query.lower().strip() in model_name.lower().strip()
