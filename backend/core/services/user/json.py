import json

from anyio import open_file

from core.schemas.user import UserSchema, UserInDBSchema, PatchUserSchema, CreateUserSchema
from core.services.settings import SettingsService

from core.config import BASE_DIR

from .base import BaseUserService


class UserServiceJSON(BaseUserService):
    STORE_PATH = BASE_DIR / 'users.json'

    @classmethod
    async def _get_store(cls):
        if not cls.STORE_PATH.exists():
            store = {}
            await cls._save(store)
        async with await open_file(cls.STORE_PATH, 'r+', encoding='utf-8') as file:
            content = await file.read()
            try:
                store = json.loads(content)
            except json.JSONDecodeError:
                store = {}
                content = json.dumps(store)
                await file.write(content)
        return store

    @classmethod
    async def _save(cls, store):
        content = json.dumps(store)
        async with await open_file(cls.STORE_PATH, 'w', encoding='utf-8') as file:
            await file.write(content)

    @classmethod
    async def list_users(cls, limit: int = None, only_active: bool = False) -> list[UserSchema]:
        store = await cls._get_store()
        filtered_users = []
        for user in store.values():
            if only_active and not user['active']:
                continue
            serialized_user = await cls._serialize(user)
            filtered_users.append(serialized_user)
            if len(filtered_users) == limit:
                break
        return filtered_users

    @classmethod
    async def get_user(cls, telegram_id: int) -> UserSchema | None:
        store = await cls._get_store()
        user = store.get(str(telegram_id))
        if not user:
            return None
        return await cls._serialize(user)

    @classmethod
    async def _serialize(cls, user: dict) -> UserSchema:
        if not user['chat_history']:
            user['chat_history'] = None
        return UserSchema(
            telegram_id=user['telegram_id'],
            description=user['description'],
            chat_history=user['chat_history'],
            active=user['active'],
        )

    @classmethod
    async def get_or_create_user(cls, telegram_id: int) -> UserSchema:
        user = await cls.get_user(telegram_id)
        if not user:
            data = CreateUserSchema(telegram_id=telegram_id)
            user = await cls.create_user(data)
        return user

    @classmethod
    async def create_user(cls, data: CreateUserSchema) -> UserSchema:
        store = await cls._get_store()
        if not data.active:
            settings = await SettingsService.get_settings()
            data.active = settings.users_active_by_default
        db_data = UserInDBSchema(**data.model_dump())
        user_db = db_data.model_dump()
        store[str(data.telegram_id)] = user_db
        await cls._save(store)

        user = await cls.get_user(data.telegram_id)
        return user

    @classmethod
    async def update_or_create_user(cls, telegram_id: int, data: PatchUserSchema) -> UserInDBSchema:
        user = await cls.get_user(telegram_id)
        if user:
            user.update(**data.model_dump())
            await cls.save(user)
            return user
        full_data = CreateUserSchema(telegram_id=telegram_id, **data.model_dump())
        user = await cls.create_user(full_data)
        return user

    @classmethod
    async def save(cls, user: UserInDBSchema):
        store = await cls._get_store()
        user_data = user.db_dump(exclude_none=True)

        store[str(user.telegram_id)] = user_data
        await cls._save(store)

    @classmethod
    async def clear_user_chat_history(cls, telegram_id: int):
        user = await cls.get_user(telegram_id)
        user.chat_history = None
        await cls.save(user)
