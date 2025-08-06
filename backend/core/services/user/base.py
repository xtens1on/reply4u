from abc import ABC

from core.schemas.message import MessageSchema
from core.schemas.user import UserSchema, UserInDBSchema, CreateUserSchema, PatchUserSchema

from core.services.settings import SettingsService


class BaseUserService(ABC):

    @classmethod
    async def list_users(cls, limit: int = None, only_active: bool = False) -> list[UserSchema]:
        ...

    @classmethod
    async def get_user(cls, telegram_id: int) -> UserSchema | None:
        ...

    @classmethod
    async def _serialize(cls, user: dict) -> UserSchema:
        return UserSchema(
            telegram_id=user['telegram_id'],
            description=user['description'],
            chat_history=user['chat_history'],
            active=user['active'],
        )

    @classmethod
    async def get_or_create_user(cls, telegram_id: int) -> UserSchema:
        ...

    @classmethod
    async def create_user(cls, data: CreateUserSchema) -> UserSchema:
        ...

    @classmethod
    async def update_or_create_user(cls, telegram_id: int, data: PatchUserSchema) -> UserInDBSchema:
        ...

    @classmethod
    async def save(cls, user: UserInDBSchema):
        ...

    @classmethod
    async def get_context(cls, user: UserSchema) -> list[dict]:
        system_message = await cls.format_system_message(user)
        formatted_chat_history = [await cls.format_history_message(message) for message in user.chat_history]
        return formatted_chat_history + [system_message]

    @classmethod
    async def format_system_message(cls, user: UserSchema) -> dict:
        settings = await SettingsService.get_settings()
        template = settings.system_message_template
        content = template.format(**user.shortcuts)
        return {
            'role': 'system',
            'content': content
        }

    @classmethod
    async def format_history_message(cls, message: MessageSchema) -> dict:
        settings = await SettingsService.get_settings()
        template = settings.message_template
        content = template.format(**message.shortcuts)
        return {
            'role': message.role,
            'content': content or message.content
        }


    @classmethod
    async def clear_user_chat_history(cls, telegram_id: int):
        ...
