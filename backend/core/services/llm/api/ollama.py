from ollama import AsyncClient, ChatResponse, list as models_list

from .base import LLMApi


class OllamaAPI(LLMApi):

    @classmethod
    async def get_completion(cls, model: str, messages: list[dict[str, str]]) -> str:
        client = AsyncClient()
        response: ChatResponse = await client.chat(
            model=model,
            messages=messages,
            think=True,
        )
        return response.message.content

    @classmethod
    async def models_list(cls, query: str = '', limit: int = 10) -> list[str]:
        models = models_list().models
        filtered_models = []
        for model in models:
            matches_query = await cls._model_matches_query(model.model, query)
            if query and not matches_query:
                continue
            filtered_models.append(model.model)
            if len(filtered_models) == limit:
                break
        return filtered_models

    @classmethod
    async def _model_matches_query(cls, model_name: str, query: str):
        return query.lower().strip() in model_name.lower().strip()
