import json

from anyio import open_file

from core.config import SETTINGS_PATH
from core.schemas.settings import AppSettingsSchema, UpdateAppSettingsSchema


class SettingsService:
    STORE_PATH = SETTINGS_PATH

    @classmethod
    async def get_settings(cls) -> AppSettingsSchema:
        store = await cls._get_store()
        return AppSettingsSchema(**store)

    @classmethod
    async def _get_store(cls):
        if not cls.STORE_PATH.exists():
            store = AppSettingsSchema().model_dump()
            await cls._save(store)
        async with await open_file(cls.STORE_PATH, 'r', encoding='utf-8') as file:
            content = await file.read()
            store = json.loads(content)
        return store

    @classmethod
    async def update(cls, settings: UpdateAppSettingsSchema):
        store = await cls._get_store()
        data = settings.model_dump(exclude_none=True)
        for key, value in data.items():
            store[key] = value
        await cls._save(store)

    @classmethod
    async def _save(cls, store):
        content = json.dumps(store)
        async with await open_file(cls.STORE_PATH, 'w', encoding='utf-8') as file:
            await file.write(content)
