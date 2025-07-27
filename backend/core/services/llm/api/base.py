from abc import ABC, abstractmethod


class LLMApi(ABC):

    @classmethod
    @abstractmethod
    async def get_completion(cls, model: str, messages: list[dict[str, str]]):
        ...

    @classmethod
    @abstractmethod
    async def models_list(cls, query: str, limit: int) -> list[str]:
        ...
